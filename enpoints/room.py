from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from enum import Enum

from room_context.domain.room import Room, RoomType
from room_context.services.room_service import (
    RoomServices,
    RoomAlreadyExist,
    RoomDoesNotExist,
)
from room_context.repositories.mongodb import MongoDBRoomRepository
from config import database_config

router = APIRouter()

__connection_string = f"mongodb://{database_config.database_username}:{database_config.database_password}@{database_config.database_host}:{database_config.database_port}"
room_repo = MongoDBRoomRepository(
    connection_string=__connection_string,
    db_name=database_config.database_name,
    collection_name="rooms",
)
room_service = RoomServices(repo=room_repo)


class RoomCraete(BaseModel):
    room_id: str
    room_model: RoomType


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_room(room: RoomCraete):
    try:
        room = room_service.create_new_room(room_id=room.room_id, model=room.room_model)
        return room
    except RoomAlreadyExist as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


@router.get("/{room_id}", status_code=status.HTTP_200_OK)
async def get_room_by_id(room_id: str):
    try:
        room = room_service.get_room_from_room_id(room_id=room_id)
        return room

    except RoomDoesNotExist as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


@router.put("/{room_id}/occupy", status_code=status.HTTP_204_NO_CONTENT)
async def occupy_a_room(room_id: str):
    try:
        room_service.customer_occupy_a_room(room_id=room_id)

    except RoomDoesNotExist as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


@router.put("/{room_id}/checkout", status_code=status.HTTP_204_NO_CONTENT)
async def check_out_a_room(room_id: str):
    try:
        room_service.check_out_room(room_id=room_id)

    except RoomDoesNotExist as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )


@router.put("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_room_model(room_id: str, room_model: RoomType):
    try:
        room_service.update_model_room(room_id=room_id, model=room_model)

    except RoomDoesNotExist as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
