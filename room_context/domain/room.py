from .room_type import RoomType
from .exceptions import InvalidRoomModel, RoomIsUnavailable, RoomIsAvailable

_ERR_ROOM_MODEL_IS_INVALID = "the room model is invalid"
_ERR_ROOM_IS_UNAVAILABLE = "can not occupy the unavailable room "
_ERR_ROOM_IS_AVAILABLE = "can not check out the available room"


class Room:
    def __init__(
        self, room_id: str, model: RoomType, is_available: bool = True
    ) -> None:
        self.room_id = room_id
        self.model = model
        self.is_available = is_available

    def is_valid_model(self, model) -> bool:
        return model is not None and model.price >= 0 and len(model.name) >= 1

    @classmethod
    def create_new_room(cls, *, room_id: str, model: RoomType):
        if not cls.is_valid_model(cls, model):
            raise InvalidRoomModel(_ERR_ROOM_MODEL_IS_INVALID)

        return cls(room_id=room_id, model=model)

    def occupy(self):
        if not self.is_available:
            raise RoomIsUnavailable(_ERR_ROOM_IS_UNAVAILABLE)
        self.is_available = False

    def check_out(self):
        if self.is_available:
            raise RoomIsAvailable(_ERR_ROOM_IS_AVAILABLE)
        self.is_available = True

    def update_model(self, model: RoomType):
        if not self.is_valid_model(model):
            raise InvalidRoomModel(_ERR_ROOM_MODEL_IS_INVALID)
        self.model = model
