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
    "teammate_id",
    help="Recommend restaurants for this teammate"
)
parser.add_argument(
    "-c", "--cache",
    action='store_true',
    help="Cache internal database"
)
args = parser.parse_args()

with closing(db.db_connection()) as db_conn:
    db.init(db_conn)
    with closing(args.ratings_file) as ratings_file:
        db.add_ratings(db_conn, ratings_file)
    with closing(args.restaurants_file) as restaurants_file:
        db.add_restaurants(db_conn, restaurants_file)
    with closing(args.teammates_file) as teammates_file:
        db.add_teammates(db_conn, teammates_file)
