"""

"""

from argparse import ArgumentParser, FileType
from contextlib import closing

import recommender.database as db


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    "ratings_file",
    type=FileType('r'),
    help="JSON formatted file containing teammates' restaurant ratings"
)
parser.add_argument(
    "teammates_file",
    type=FileType('r'),
    help="JSON formatted file containing the teammates"
)
parser.add_argument(
    "restaurants_file",
    type=FileType('r'),
    help="JSON formatted file containing restaurant information"
)
parser.add_argument(
    "-c", "--cache",
    action='store_true',
    help="Cache internal database"
)
args = parser.parse_args()

with closing(db.db_connection()) as db_conn:
    db.init(db_conn)
    db.add_ratings(db_conn, args.ratings_file)
    db.add_restaurants(db_conn, args.restaurants_file)
    db.add_teammates(db_conn, args.teammates_file)
