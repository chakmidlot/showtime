import logging
import time
import traceback

from showtime.db import DB
from showtime.silverscreen import query_dates
from showtime.telegram.sender import send

logger = logging.getLogger(__name__)


class Checker:

    def __init__(self):
        self.db = DB()

    def check(self):
        while True:
            try:
                update = list(query_dates())
                db_dates = self.db.get_all_dates([x[0] for x in update])
                db_dates_dict = {x['_id']: x['dates'] for x in db_dates}

                for movie_code, movie_name, dates in update:
                    last_date_in_db = db_dates_dict.get(movie_code, [""])[-1]
                    new_dates = [x for x in dates if x > last_date_in_db]
                    if new_dates:
                        self.alert(movie_code, movie_name, new_dates)
                        self.db.add_dates(movie_code, movie_name, dates)

            except Exception:
                logger.error(traceback.format_exc())

            time.sleep(2 * 3600)

    def alert(self, movie_id, movie_name, new_dates):
        for user in self.db.get_movie_subscribers(movie_id):
            send(user, 'New showtime for "{}":\n {}'.format(movie_name, ", ".join(new_dates)))
