from room_context.domain.repository import RoomRepository
from room_context.domain.room import Room, RoomType
from .exceptions import RoomDoesNotExist, RoomAlreadyExist

_ERR_ROOM_DOES_NOT_EXIST = "the room does not exist"
_ERR_ROOM_EXIST = "room already exist"


class RoomServices:
    def __init__(self, repo: RoomRepository) -> None:
        self.repo = repo

    def create_new_room(self, room_id: str, model: RoomType):
        try:
            exits_room = self.repo.from_room_id(room_id=room_id)
            if exits_room:
                raise RoomAlreadyExist(_ERR_ROOM_EXIST)

            room = Room.create_new_room(room_id=room_id, model=model)
            self.repo.save(room)

            return room

        except Exception as err:
            raise err

    def get_room_from_room_id(self, room_id: str):
        try:
            room = self.repo.from_room_id(room_id=room_id)
            if not room:
                raise RoomDoesNotExist(_ERR_ROOM_DOES_NOT_EXIST)

            return room

        except Exception as err:
            raise err

    def customer_occupy_a_room(self, room_id: str):
        try:
            room = self.repo.from_room_id(room_id=room_id)
            if not room:
                raise RoomDoesNotExist(_ERR_ROOM_DOES_NOT_EXIST)

            room.occupy()
            self.repo.save(room)

        except Exception as err:
            raise err

    def check_out_room(self, room_id: str):
        try:
            room = self.repo.from_room_id(room_id=room_id)
            if not room:
                raise RoomDoesNotExist(_ERR_ROOM_DOES_NOT_EXIST)

            room.check_out()
            self.repo.save(room)

        except Exception as err:
            raise err

    def update_model_room(self, room_id: str, model: RoomType):
        try:
            room = self.repo.from_room_id(room_id=room_id)
            if not room:
                raise RoomDoesNotExist(_ERR_ROOM_DOES_NOT_EXIST)

            room.update_model(model=model)
            self.repo.save(room)

        except Exception as err:
            raise err
