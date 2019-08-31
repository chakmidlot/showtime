from collections import defaultdict

from pytest import fixture

from showtime.telegram.commands import Commands


class MockDb:

    def __init__(self):
        self.data = defaultdict(list)

    def add_movie(self, user, movie):
        self.data[user].append(movie)

    def list(self, user):
        return self.data[user]


@fixture()
def db():
    yield MockDb()


@fixture()
def commands(db):
    cmd = Commands()
    cmd.db = db
    yield cmd


def test_help(commands):
    help_message = commands.help(user_id=0, data=None)
    assert len(help_message) > 0


def test_empty_list(commands):
    items = commands.list(user_id=0, data=None)
    assert items == "No movies tracking"


def test_single_list(commands, db):
    db.add_movie(12, "movie_a")
    items = commands.list(user_id=12, data=None)
    assert items == "Movie dates tracking:\nmovie_a"


def test_multiple_list(commands, db):
    db.add_movie(12, "movie_a")
    db.add_movie(12, "movie_b")
    db.add_movie(13, "movie_c")
    items = commands.list(user_id=12, data=None)
    assert items == "Movie dates tracking:\nmovie_a\nmovie_b"
