from pymongo import MongoClient
from pymongo.collection import Collection

from showtime import settings


class DB:

    def __init__(self):
        self.connection = MongoClient(settings.MONGO_URI)
        self.users_collection: Collection = self.connection.showtime_db.users
        self.dates_collection: Collection = self.connection.showtime_db.dates
        self.checkpoints_collection: Collection = self.connection.showtime_db.telegram_checkpoints

    def list(self, user):
        user_data = self.users_collection.find_one({"_id": user})
        if user_data:
            return user_data["movies_set"]
        else:
            return []

    def add_movie(self, user, movie):
        self.users_collection.update_one({"_id": user}, {
            "$addToSet": {
                "movies_set": movie
            }
        }, True)

    def add_dates(self, movie, name, dates):
        self.dates_collection.update_one(
            {"_id": movie},
            {"$set": {
                "dates": dates,
                "name": name,
            }},
            True
        )

    def get_all_dates(self, movies):
        dates = self.dates_collection.find({"_id": {"$in": movies}})
        return list(dates)

    def remove(self, user, movie):
        self.users_collection.update_one(
            {"_id": user},
            {
                "$pull": {
                    "movies_set": movie
                }
            }
        )

    def set_telegram_checkpoint(self, name, value):
        self.checkpoints_collection.update_one(
            {"_id": name},
            {"$set": {"value": value}},
            True
        )

    def get_telegram_checkpoint(self, name):
        value_row = self.checkpoints_collection.find_one({"_id": name})
        if value_row:
            return value_row['value']
        else:
            return None

    def remove_all(self, user):
        self.users_collection.delete_one({"_id": user})

    def get_movie_subscribers(self, movie):
        return (x['_id'] for x in self.users_collection.find({"movies_set": movie}))


if __name__ == '__main__':
    db = DB()

    db.add_movie(1234, "test")
    db.add_dates("test", "name", [1, 2, 3])
    db.get_all_dates(["test"])
    db.add_dates("test", "name", [2, 5])
    print(db.get_all_dates(["test"]))

    db.add_dates("test2", "empty", [])
    print(db.get_all_dates(["test2"]))

    print("all dates ", db.get_all_dates(["test", "test2"]))