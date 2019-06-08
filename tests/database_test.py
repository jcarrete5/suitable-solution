from contextlib import closing
from io import StringIO

import pytest

import recommender.database as db


@pytest.fixture
def closing_db_conn() -> closing:
    db_conn = db.db_connection(':memory:')
    db.init(db_conn)
    return closing(db_conn)


@pytest.fixture
def ratings() -> StringIO:
    return StringIO('''
    [
        {
            "teammateId": "e17b91cb-5a2c-4055-befb-1d1ea9f7daca",
            "restaurantId": "Uky0DD3LU4C7eyNDhpmOXg",
            "rating": "DISLIKE"
        },
        {
            "teammateId": "e17b91cb-5a2c-4055-befb-1d1ea9f7daca",
            "restaurantId": "w55VlTgAoRXPnqFte3j9ew",
            "rating": "LIKE"
        },
        {
            "teammateId": "e17b91cb-5a2c-4055-befb-1d1ea9f7daca",
            "restaurantId": "aL53puqxtcR1KZrrj4U7Jw",
            "rating": "LIKE"
        },
        {
            "teammateId": "e17b91cb-5a2c-4055-befb-1d1ea9f7daca",
            "restaurantId": "vuE1iseFrgNPumUEfHIZZQ",
            "rating": "LIKE"
        }
    ]
    ''')


@pytest.fixture
def teammates() -> StringIO:
    return StringIO('''
    [
        {
            "id": "20ff670d-1ac9-4ddf-809b-a40d48519398",
            "name": "Macy Pacocha"
        },
        {
            "id": "03af83cb-ca91-4794-8970-fb538b653e1b",
            "name": "Austin Witting"
        },
        {
            "id": "a8b735f7-45f2-4cc4-815b-7b680e89badc",
            "name": "Miracle Williamson"
        },
        {
            "id": "2bb0d80c-b2ba-47f9-a6b2-c9faa15f030e",
            "name": "Ottis Hickle"
        }
    ]
    ''')


@pytest.fixture
def restaurants() -> StringIO:
    return StringIO('''
    [
        {
            "name": "Barbuzzo",
            "id": "6ajnOk0GcY9xbb5Ocaw8Gw",
            "image_url": "https://example.com",
            "categories": [
                {
                    "alias": "mediterranean",
                    "title": "Mediterranean"
                },
                {
                    "alias": "pizza",
                    "title": "Pizza"
                }
            ],
            "price": "$$",
            "rating": 4.5
        },
        {
            "name": "Butcher Bar",
            "id": "jS3affmkXWrBnidXA-DIfQ",
            "image_url": "https://example.com",
            "categories": [
                {
                    "alias": "steak",
                    "title": "Steakhouses"
                },
                {
                    "alias": "bars",
                    "title": "Bars"
                },
                {
                    "alias": "comfortfood",
                    "title": "Comfort Food"
                }
            ],
            "price": "$$",
            "rating": 4
        }
    ]
    ''')


def test_add_ratings(closing_db_conn: closing, ratings: StringIO):
    with closing_db_conn as db_conn:
        db.add_ratings(db_conn, ratings)
        with closing(db_conn.cursor()) as cur:
            cur.execute("SELECT * FROM ratings;")
            assert len(cur.fetchall()) == 4


def test_add_teammates(closing_db_conn: closing, teammates: StringIO):
    with closing_db_conn as db_conn:
        db.add_teammates(db_conn, teammates)
        with closing(db_conn.cursor()) as cur:
            cur.execute("SELECT * FROM teammates;")
            assert len(cur.fetchall()) == 4


def test_add_restaurants(closing_db_conn: closing, restaurants: StringIO):
    with closing_db_conn as db_conn:
        db.add_restaurants(db_conn, restaurants)
        with closing(db_conn.cursor()) as cur:
            cur.execute("SELECT * FROM restaurants;")
            assert len(cur.fetchall()) == 2
