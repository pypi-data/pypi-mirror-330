from datetime import date, timedelta, datetime
from os import path
import beangulp
import yaml
from beancount.core import amount, data, flags
from beancount.core.number import D
from .client import NordigenClient


class NordigenImporter(beangulp.Importer):
    """An importer for Nordigen API with improved structure and extensibility."""

    def __init__(self):
        self.config = None
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = NordigenClient(
                self.config["secret_id"],
                self.config["secret_key"],
                cache_options={"expire_after": 3600 * 24, "old_data_on_error": True},
            )

        return self._client

    def identify(self, filepath: str) -> bool:
        return path.basename(filepath).endswith("nordigen.yaml")

    def account(self, filepath: str) -> str:
        return ""

    def load_config(self, filepath: str):
        """Load configuration from YAML file."""
        with open(filepath, "r") as f:
            raw_config = f.read()
            expanded_config = path.expandvars(raw_config)
            self.config = yaml.safe_load(expanded_config)

        return self.config

    def get_transactions_data(self, account_id):
        """Get transactions data either from API or debug files."""
        transactions_data = self.client.get_transactions(account_id)

        return transactions_data

    def get_all_transactions(self, transactions_data):
        """Combine and sort booked and pending transactions."""
        all_transactions = [
            (tx, "booked") for tx in transactions_data.get("booked", [])
        ] + [(tx, "pending") for tx in transactions_data.get("pending", [])]
        return sorted(
            all_transactions,
            key=lambda x: x[0].get("valueDate") or x[0].get("bookingDate"),
        )

    def add_metadata(self, transaction, filing_account: str):
        """Extract metadata from transaction - overridable method."""
        metakv = {}

        # Transaction ID
        if "transactionId" in transaction:
            metakv["nordref"] = transaction["transactionId"]

        # Names
        if "creditorName" in transaction:
            metakv["creditorName"] = transaction["creditorName"]
        if "debtorName" in transaction:
            metakv["debtorName"] = transaction["debtorName"]

        # Currency exchange
        if "currencyExchange" in transaction:
            instructedAmount = transaction["currencyExchange"]["instructedAmount"]
            metakv["original"] = (
                f"{instructedAmount['currency']} {instructedAmount['amount']}"
            )

        # Booking date if different from value date
        if (
            transaction.get("bookingDate")
            and transaction.get("valueDate")
            and transaction["bookingDate"] != transaction["valueDate"]
        ):
            metakv["bookingDate"] = transaction["bookingDate"]

        if filing_account:
            metakv["filing_account"] = filing_account

        return metakv

    def get_narration(self, transaction):
        """Extract narration from transaction - overridable method."""
        narration = ""

        if "remittanceInformationUnstructured" in transaction:
            narration += transaction["remittanceInformationUnstructured"]

        if "remittanceInformationUnstructuredArray" in transaction:
            narration += " ".join(transaction["remittanceInformationUnstructuredArray"])

        return narration

    def get_payee(self, transaction):
        """Extract payee from transaction - overridable method."""
        return ""

    def get_transaction_date(self, transaction):
        """Extract transaction date - overridable method."""
        date_str = transaction.get("valueDate") or transaction.get("bookingDate")
        return date.fromisoformat(date_str) if date_str else None

    def get_transaction_status(self, status):
        """Determine transaction status flag - overridable method."""
        # Could be configured to use "!" for pending transactions status == 'pending'
        return flags.FLAG_OKAY

    def create_transaction_entry(
        self, transaction, status, asset_account, filing_account
    ):
        """Create a Beancount transaction entry - overridable method."""
        metakv = self.add_metadata(transaction, filing_account)
        meta = data.new_metadata("", 0, metakv)

        trx_date = self.get_transaction_date(transaction)
        narration = self.get_narration(transaction)
        payee = self.get_payee(transaction)
        flag = self.get_transaction_status(status)

        # Get transaction amount
        tx_amount = amount.Amount(
            D(str(transaction["transactionAmount"]["amount"])),
            transaction["transactionAmount"]["currency"],
        )

        return data.Transaction(
            meta,
            trx_date,
            flag,
            payee,
            narration,
            data.EMPTY_SET,
            data.EMPTY_SET,
            [
                data.Posting(
                    asset_account,
                    tx_amount,
                    None,
                    None,
                    None,
                    None,
                ),
            ],
        )

    def extract(self, filepath: str, existing: data.Entries) -> data.Entries:
        """Extract entries from Nordigen transactions."""
        self.load_config(filepath)

        entries = []
        for account in self.config["accounts"]:
            account_id = account["id"]
            asset_account = account["asset_account"]
            filing_account = account.get("filing_account", None)

            transactions_data = self.get_transactions_data(account_id)
            all_transactions = self.get_all_transactions(transactions_data)

            for transaction, status in all_transactions:
                entry = self.create_transaction_entry(
                    transaction, status, asset_account, filing_account
                )
                entries.append(entry)

        return entries

    def cmp(self, entry1: data.Transaction, entry2: data.Transaction):
        return (
            "nordref" in entry1.meta
            and "nordref" in entry2.meta
            and entry1.meta["nordref"] == entry2.meta["nordref"]
        )
