from datetime import date, timedelta, datetime
import requests_cache
import requests
from typing import Protocol, TypedDict, Optional


class CacheOptions(TypedDict, total=False):
    cache_name: requests_cache.StrOrPath
    backend: Optional[requests_cache.BackendSpecifier]
    expire_after: requests_cache.ExpirationTime
    old_data_on_error: bool


class HttpServiceException(Exception):
    """Exception raised for HTTP service errors."""

    def __init__(self, error, response_text=None):
        self.error = error
        self.response_text = response_text
        super().__init__(f"{error}: {response_text}")


class BaseService:
    """Base class for HTTP services handling authentication and requests."""

    BASE_URL = "https://bankaccountdata.gocardless.com/api/v2"

    DEFAULT_CACHE_OPTIONS: CacheOptions = {
        "cache_name": "nordigen",
        "backend": "sqlite",
        "expire_after": 3600 * 24,
        "old_data_on_error": False,
    }

    def __init__(
        self,
        secret_id: str,
        secret_key: str,
        cache_options: Optional[CacheOptions],
    ):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = None
        merged_options = {**self.DEFAULT_CACHE_OPTIONS, **(cache_options or {})}
        self.session = requests_cache.CachedSession(**merged_options)

    def _ensure_token_valid(self):
        """Ensure a valid token exists (no-op here as Nordigen doesn't provide refresh tokens)."""
        if not self.token:
            self.get_token()

    def get_token(self):
        """Fetch a new API token using credentials."""
        response = requests.post(
            f"{self.BASE_URL}/token/new/",
            data={"secret_id": self.secret_id, "secret_key": self.secret_key},
        )
        self._handle_response(response)
        self.token = response.json()["access"]

    def _handle_response(self, response):
        """Check response status and handle errors."""
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HttpServiceException(str(e), response.text)

    def _request(self, method, endpoint, params=None, data=None):
        """Execute an HTTP request with token handling."""
        url = f"{self.BASE_URL}{endpoint}"
        self._ensure_token_valid()
        headers = {"Authorization": f"Bearer {self.token}"}

        response = self.session.request(
            method, url, headers=headers, params=params, data=data
        )

        # Retry once if token expired
        if response.status_code == 401:
            self.get_token()
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.request(
                method, url, headers=headers, params=params, data=data
            )

        self._handle_response(response)
        return response

    def _get(self, endpoint, params=None):
        return self._request("GET", endpoint, params=params).json()

    def _post(self, endpoint, data=None):
        return self._request("POST", endpoint, data=data).json()

    def _delete(self, endpoint):
        return self._request("DELETE", endpoint).json()


class NordigenClient(BaseService):
    """Client for interacting with the Nordigen API."""

    def list_banks(self, country="GB"):
        """List available institutions for a country."""
        return [
            {"name": bank["name"], "id": bank["id"]}
            for bank in self._get("/institutions/", params={"country": country})
        ]

    def find_requisition_id(self, reference):
        """Find requisition ID by reference."""
        requisitions = self._get("/requisitions/")["results"]
        return next(
            (req["id"] for req in requisitions if req["reference"] == reference), None
        )

    def create_link(self, reference, bank_id, redirect_url="http://localhost"):
        """Create a new bank link requisition."""
        if self.find_requisition_id(reference):
            return {"status": "exists", "message": f"Link {reference} exists"}

        response = self._post(
            "/requisitions/",
            data={
                "redirect": redirect_url,
                "institution_id": bank_id,
                "reference": reference,
            },
        )
        return {
            "status": "created",
            "link": response["link"],
            "message": f"Complete linking at: {response['link']}",
        }

    def list_accounts(self):
        """List all connected accounts with details."""
        accounts = []
        for req in self._get("/requisitions/")["results"]:
            for account_id in req["accounts"]:
                account = self._get(f"/accounts/{account_id}")
                details = self._get(f"/accounts/{account_id}/details")["account"]

                accounts.append(
                    {
                        "id": account_id,
                        "institution_id": req.get("institution_id", ""),
                        "reference": req["reference"],
                        "iban": account.get("iban", ""),
                        "currency": details.get("currency", ""),
                        "name": details.get("name", "Unknown"),
                    }
                )
        return accounts

    def delete_link(self, reference):
        """Delete a bank link by reference."""
        req_id = self.find_requisition_id(reference)
        if not req_id:
            return {"status": "not_found", "message": f"Link {reference} not found"}

        self._delete(f"/requisitions/{req_id}")
        return {"status": "deleted", "message": f"Link {reference} removed"}

    def get_transactions(self, account_id, days_back=180):
        """Retrieve transactions for an account."""
        date_from = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        return self._get(
            f"/accounts/{account_id}/transactions/",
            params={
                "date_from": date_from,
                "date_to": datetime.now().strftime("%Y-%m-%d"),
            },
        ).get("transactions", [])
