from showtime.db import DB


class Commands:

    def __init__(self):
        self.db = DB()

    def list(self, user_id, data):
        movies = self.db.list(user_id)

        if movies:
            return "Movie dates tracking:\n" + "\n".join(movies)
        else:
            return "No movies tracking"

    def add(self, user_id, data):
        clear_name = data.strip()
        if clear_name:
            self.db.add_movie(user_id, data)

    def remove(self, user_id, data):
        clear_name = data.strip()
        if clear_name:
            self.db.remove(user_id, data)

    def help(self, user_id, data):
        return "Helps to track movie tickets are available in Silverscreen cinema"
