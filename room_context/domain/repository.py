from room_context.domain.room import Room
from typing import List
from abc import ABC, abstractmethod


class RoomRepository(ABC):
    @abstractmethod
    def next_identity(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Room]:
        raise NotImplementedError

    @abstractmethod
    def from_room_id(self, room_id: str) -> Room:
        raise NotImplementedError

    @abstractmethod
    def save(self, entity: Room):
        raise NotImplementedError
