from room_context.domain.repository import RoomRepository
from room_context.domain.room import Room, RoomType
from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId


class MongoDBRoomRepository(RoomRepository):
    def __init__(self, connection_string: str, db_name: str, collection_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def next_identity(self):
        return str(ObjectId)

    def get_all(self):
        rooms_data = self.collection.find({})
        rooms = [self._deserialize_room(room_data) for room_data in rooms_data]
        return rooms

    def from_room_id(self, room_id: str):
        room_data = self.collection.find_one({"room_id": room_id})
        if room_data:
            return self._deserialize_room(room_data)
        return None

    def save(self, room: Room):
        room_data = self._serialize_room(room)
        self.collection.replace_one({"room_id": room.room_id}, room_data, upsert=True)

    def _serialize_room(self, room: Room) -> dict:
        return {
            "room_id": room.room_id,
            "model": {
                "name": room.model.name,
                "description": room.model.description,
                "price": room.model.price,
                "deposit": room.model.deposit,
            },
            "is_available": room.is_available,
        }

    def _deserialize_room(self, room_data) -> Room:
        return Room(
            room_id=room_data["room_id"],
            model=RoomType(
                name=room_data["model"]["name"],
                description=room_data["model"]["description"],
                price=room_data["model"]["price"],
                deposit=room_data["model"]["deposit"],
            ),
            is_available=room_data["is_available"],
        )
