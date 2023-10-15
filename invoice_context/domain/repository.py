from abc import abstractmethod, ABC
from .invoice import Invoice
from typing import List


class InvoiceRepository(ABC):
    @abstractmethod
    def next_identity(self):
        raise NotImplementedError

    @abstractmethod
    def from_reference(self, ref) -> Invoice:
        raise NotImplementedError

    @abstractmethod
    def all(self, limit) -> List[Invoice]:
        raise NotImplementedError

    @abstractmethod
    def save(self, invoice: Invoice):
        raise NotImplementedError

    @abstractmethod
    def delete(self, ref: str):
        raise NotImplementedError
