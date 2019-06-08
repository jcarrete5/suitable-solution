import sqlite3
import json
from io import TextIOBase
from contextlib import closing

RECOMMENDER_SQL_LOCATION = 'data/recommender.sql'


def db_connection(db_location='data/recommender.sqlite3'):
    return sqlite3.connect(db_location)


def init(db_conn: sqlite3.Connection):
    with open(RECOMMENDER_SQL_LOCATION) as sql:
        db_conn.executescript(''.join(sql.readlines()))
        db_conn.commit()


def add_ratings(db_conn: sqlite3.Connection, ratings_file: TextIOBase):
    ratings = json.load(ratings_file)
    with closing(db_conn.cursor()) as cur:
        cur.executemany("INSERT INTO ratings VALUES "
                        "(:teammateId, :restaurantId, :rating);",
                        ratings)
        db_conn.commit()


def add_restaurants(db_conn: sqlite3.Connection,
                    restaurants_file: TextIOBase):
    restaurants = json.load(restaurants_file)
    with closing(db_conn.cursor()) as cur:
        for entry in restaurants:
            id_ = entry['id']
            name = entry['name']
            image_url = entry['image_url']
            categories = entry['categories']
            price = entry.get('price', '#')
            rating = entry['rating']
            cur.execute("INSERT INTO restaurants VALUES (?, ?, ?, ?, ?);",
                        (id_, name, image_url, price, rating))
            for cat_entry in categories:
                alias = cat_entry['alias']
                title = cat_entry['title']
                cur.execute("INSERT INTO categories VALUES (?, ?, ?);",
                            (id_, alias, title))
        db_conn.commit()


def add_teammates(db_conn: sqlite3.Connection, teammates_file: TextIOBase):
    teammates = json.load(teammates_file)
    with closing(db_conn.cursor()) as cur:
        cur.executemany("INSERT INTO teammates VALUES "
                        "(:id, :name);",
                        teammates)
        db_conn.commit()
