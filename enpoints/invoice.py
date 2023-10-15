from fastapi import APIRouter, HTTPException, status
from datetime import date
from pydantic import BaseModel
from typing import List

from invoice_context.domain.invoice import (
    Invoice,
    InvoiceItem,
    InvoicePaidError,
    InvalidInfomation,
    InvoiceSubmittedError,
)
from invoice_context.repositories.mongodb import MongoInvoiceRepository
from invoice_context.services.invoice import InvoiceService, InvoiceDoesNotExist
from config import database_config

router = APIRouter()

__connection_string = f"mongodb://{database_config.database_username}:{database_config.database_password}@{database_config.database_host}:{database_config.database_port}"
repo = MongoInvoiceRepository(
    connection_string=__connection_string,
    db_name=database_config.database_name,
    collection_name="invoices",
)
service = InvoiceService(repo=repo)


class InvoiceCreate(BaseModel):
    room_id: str
    customer: str
    items: List[InvoiceItem]


class InvoiceEdit(BaseModel):
    customer: str
    room_id: str


@router.get("/")
async def get_all_invoice_infomations(limit: int = 10):
    try:
        invoices = service.get_all_invoices(limit)
        return invoices
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


@router.get("/{ref}")
async def get_invoice_infomation_by_reference(ref: str):
    try:
        invoice = service.get_invoice_by_reference(ref)
        return invoice

    except InvoiceDoesNotExist as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


@router.post("/")
async def creating_new_invoice(entity: InvoiceCreate):
    try:
        invoice = service.create_new_invoice(
            entity.customer, entity.room_id, items=entity.items
        )
        return invoice

    except InvoiceDoesNotExist as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    except (InvoicePaidError, InvalidInfomation, InvoiceSubmittedError) as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


@router.put("/update_items/{ref}")
async def update_items(ref: str, items: List[InvoiceItem]):
    try:
        updated_invoice = service.update_invoice_item(ref=ref, new_items=items)
        return updated_invoice

    except InvoiceDoesNotExist as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


@router.put("/edit/{ref}")
async def edit_customer_and_room_id(ref: str, entity: InvoiceEdit):
    try:
        updated_invoice = service.updating_customer_and_room_id(
            ref=ref, customer=entity.customer, room_id=entity.room_id
        )
        return updated_invoice

    except InvoiceDoesNotExist as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    except InvalidInfomation as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


@router.put("/settle/{ref}")
async def settle_invoice(ref: str):
    try:
        service.settle_invoice(ref)

    except InvoiceDoesNotExist as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    except InvoiceSubmittedError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    except InvoicePaidError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


@router.put("/submit/{ref}")
async def submit_invoice(ref: str):
    try:
        service.submit_invoice(ref)

    except InvoiceDoesNotExist as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    except InvoiceSubmittedError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )


# @router.delete("/destroy/{ref}")
# async def destroy_invoice_by_ref(ref: str):
#     try:
#         service.destroy_invoice(ref)
#     except Exception as error:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
