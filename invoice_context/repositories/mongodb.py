from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId
from typing import List
from invoice_context.domain.invoice import Invoice, InvoiceItem
from invoice_context.domain.repository import InvoiceRepository
from datetime import date


class MongoInvoiceRepository(InvoiceRepository):
    def __init__(self, connection_string: str, db_name: str, collection_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def next_identity(self) -> str:
        return str(ObjectId())

    def from_reference(self, ref) -> Invoice:
        try:
            invoice_data = self.collection.find_one({"reference": ref})
            if invoice_data:
                return self._deserialize_invoice(invoice_data)

            return None

        except Exception as err:
            raise err

    def all(self, limit) -> List[Invoice]:
        try:
            cursor = self.collection.find().limit(limit)
            invoices = [self._deserialize_invoice(data) for data in cursor]
            return invoices

        except Exception as err:
            raise err

    def save(self, invoice: Invoice):
        try:
            invoice_data = self._serialize_invoice(invoice)
            print(invoice_data)
            self.collection.replace_one(
                {"reference": invoice.reference}, invoice_data, upsert=True
            )

        except Exception as err:
            raise err

    def delete(self, ref: str):
        try:
            self.collection.delete_one({"reference": ref})

        except Exception as err:
            raise err

    def _serialize_invoice(self, invoice: Invoice):
        return {
            "reference": invoice.reference,
            "customer": invoice.customer,
            "room_id": invoice.room_id,
            "items": [
                {
                    "description": item.description,
                    "amount": item.amount,
                    "rate_price": item.rate_price,
                }
                for item in invoice.items
            ],
            "invoice_date": invoice.invoice_date.isoformat(),  # Convert to ISO string
            "paid_time": invoice.paid_time.isoformat() if invoice.paid_time else None,
            "submitted": invoice.submitted,
        }

    def _deserialize_invoice(self, data):
        invoice = Invoice(
            ref=data["reference"],
            customer=data["customer"],
            room_id=data["room_id"],
            items=[
                InvoiceItem(
                    description=item["description"],
                    amount=item["amount"],
                    rate_price=item["rate_price"],
                )
                for item in data["items"]
            ],
            invoice_date=date.fromisoformat(data["invoice_date"]),
            paid_time=data["paid_time"],
            submitted=data["submitted"],
        )
        invoice.price = invoice.total_price
        return invoice
