"""

"""

from argparse import ArgumentParser, FileType


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


