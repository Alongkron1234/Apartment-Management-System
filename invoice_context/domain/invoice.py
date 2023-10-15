from datetime import date, datetime
from dataclasses import dataclass
from typing import List

from .exceptions import InvalidInfomation, InvoicePaidError, InvoiceSubmittedError

_ERR_INVOICE_INFOMATION_ARE_INVALID = "invoice infomation are invalid"
_ERR_INVOICE_SUBMITTED_ERROR = "The invoice has been submitted."
_ERR_INVOICE_PAID_ERROR = "The invioce has been paid."
_ERR_INVOICE_UNSUBMITTED_ERROR = "The invoice is unsubmitted."


@dataclass
class InvoiceItem:
    description: str
    amount: int = 1
    rate_price: float = 0


class Invoice:
    def __init__(
        self,
        ref: str,
        customer: str,
        room_id: str,
        items: List[InvoiceItem],
        invoice_date: date,
        paid_time: datetime | None = None,
        submitted: bool = False,
    ) -> None:
        self.reference = ref
        self.room_id = room_id
        self.customer = customer
        self.items = items
        self.invoice_date = invoice_date
        self.paid_time: datetime = paid_time
        self.submitted = submitted

    @classmethod
    def create_new_invoice(
        cls,
        *,
        ref: str,
        customer: str,
        room_id: str,
        items: List[InvoiceItem],
        invoice_date: date,
    ):
        if cls.is_invalid_infomation(customer, room_id):
            raise InvalidInfomation(_ERR_INVOICE_INFOMATION_ARE_INVALID)

        invoice = cls(
            ref=ref,
            customer=customer,
            room_id=room_id,
            items=items,
            invoice_date=invoice_date,
        )
        return invoice

    @classmethod
    def is_invalid_infomation(cls, customer, room_id):
        if (
            customer is None
            or room_id is None
            or len(customer) == 0
            or len(room_id) == 0
        ):
            return True

        return False

    def is_paid(self):
        return self.paid_time is not None

    def is_submitted(self):
        return self.submitted

    def update_customer_and_room_id(self, customer: str, room_id: str):
        if self.is_submitted():
            raise InvoiceSubmittedError(_ERR_INVOICE_SUBMITTED_ERROR)

        self.customer = customer
        self.room_id = room_id

    def update_items(self, new_items: List[InvoiceItem]):
        if self.is_submitted():
            raise InvoiceSubmittedError(_ERR_INVOICE_SUBMITTED_ERROR)

        self.items = new_items

    @property
    def total_price(self):
        return sum((item.rate_price * item.amount) for item in self.items)

    def submit(self):
        if self.is_submitted():
            raise InvoiceSubmittedError(_ERR_INVOICE_SUBMITTED_ERROR)

        self.submitted = True

    def settle(self):
        if not self.is_submitted():
            raise InvoiceSubmittedError(_ERR_INVOICE_UNSUBMITTED_ERROR)

        if self.is_paid():
            raise InvoicePaidError(_ERR_INVOICE_PAID_ERROR)

        self.paid_time = datetime.today()
