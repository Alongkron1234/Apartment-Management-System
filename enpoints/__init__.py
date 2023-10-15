from fastapi import APIRouter

from . import room, invoice

router = APIRouter()


router.include_router(router=room.router, prefix="/room", tags=["Room"])
router.include_router(router=invoice.router, prefix="/invoice", tags=["Invoice"])
