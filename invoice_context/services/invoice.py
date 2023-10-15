from typing import List
from datetime import date, datetime

from invoice_context.domain.invoice import (
    Invoice,
    InvoiceItem,
    InvoicePaidError,
    InvoiceSubmittedError,
)
from invoice_context.domain.repository import InvoiceRepository
from .exceptions import InvoiceDoesNotExist

_ERR_INVOICE_DOES_NOT_EXIST = "invoice does not exist"


class InvoiceService:
    def __init__(self, repo: InvoiceRepository) -> None:
        self.repo = repo

    def create_new_invoice(self, customer: str, room_id: str, items: List[InvoiceItem]):
        try:
            _id = f"IN-{self.repo.next_identity()}"
            invoice = Invoice.create_new_invoice(
                ref=_id,
                customer=customer,
                room_id=room_id,
                items=items,
                invoice_date=date.today(),
            )

            self.repo.save(invoice)

            return invoice

        except Exception as err:
            raise err

    def get_all_invoices(self, limit: int = 10):
        try:
            invoices = self.repo.all(limit=limit)
            return invoices

        except Exception as err:
            raise err

    def get_invoice_by_reference(self, ref: str) -> Invoice:
        try:
            invoice = self.repo.from_reference(ref=ref)
            if not invoice:
                raise InvoiceDoesNotExist(_ERR_INVOICE_DOES_NOT_EXIST)

            return invoice.serialize()

        except Exception as err:
            raise err

    def updating_customer_and_room_id(self, ref: str, customer: str, room_id: str):
        try:
            invoice = self.repo.from_reference(ref=ref)
            invoice.update_customer_and_room_id(customer=customer, room_id=room_id)

            self.repo.save(invoice)
            return invoice

        except Exception as err:
            raise err

    def update_invoice_item(self, ref: str, new_items: List[InvoiceItem]):
        try:
            invoice = self.repo.from_reference(ref=ref)
            invoice.update_items(new_items=new_items)

            self.repo.save(invoice)
            return invoice

        except Exception as err:
            raise err

    def settle_invoice(self, ref: str):
        try:
            invoice = self.repo.from_reference(ref=ref)
            if not invoice:
                raise InvoiceDoesNotExist(_ERR_INVOICE_DOES_NOT_EXIST)

            print(invoice.paid_time)
            invoice.settle()
            print(invoice.paid_time)
            self.repo.save(invoice)

        except Exception as err:
            raise err

    def submit_invoice(self, ref: str):
        try:
            invoice = self.repo.from_reference(ref=ref)
            if not invoice:
                raise InvoiceDoesNotExist(_ERR_INVOICE_DOES_NOT_EXIST)

            invoice.submit()
            self.repo.save(invoice)

        except Exception as err:
            raise err
