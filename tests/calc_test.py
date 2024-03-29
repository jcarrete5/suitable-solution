import sqlite3
from importlib.resources import open_text
from math import isclose

import pytest

import recommender.calc as calc
import recommender.database as db


@pytest.fixture
def db_conn():
    db_conn = db.db_connection(':memory:')
    db_conn.row_factory = sqlite3.Row
    db.init(db_conn)
    with open_text('tests', 'test_ratings.json') as ratings:
        db.add_ratings(db_conn, ratings)
    with open_text('tests', 'test_restaurants.json') as restaurants:
        db.add_restaurants(db_conn, restaurants)
    with open_text('tests', 'test_teammates.json') as teammates:
        db.add_teammates(db_conn, teammates)
    return db_conn


def test_like_sql(db_conn: sqlite3.Connection):
    test = set(
        t[0] for t in db_conn.execute(
            calc.TEAM_LIKES_SQL, ('e17b91cb-5a2c-4055-befb-1d1ea9f7daca',)
        )
    )
    actual = {
        'jS3affmkXWrBnidXA-DIfQ',
        '8pqdJjefYq-a9IBSJJmKwA',
        'mtvT7uRey3F395STFRM1Tg'
    }
    assert test == actual
    test = set(
        t[0] for t in db_conn.execute(
            calc.TEAM_LIKES_SQL, ('3714b577-b693-4cb0-a77c-a6616c692225',)
        )
    )
    actual = set()
    assert test == actual
    test = set(
        t[0] for t in db_conn.execute(
            calc.TEAM_LIKES_SQL, ('67004926-1b19-427e-a764-de8c917f3d15',)
        )
    )
    actual = {
        'jS3affmkXWrBnidXA-DIfQ',
        'mtvT7uRey3F395STFRM1Tg'
    }
    assert test == actual


def test_dislike_sql(db_conn: sqlite3.Connection):
    test = set(
        t[0] for t in db_conn.execute(
            calc.TEAM_DISLIKES_SQL, ('e17b91cb-5a2c-4055-befb-1d1ea9f7daca',)
        )
    )
    actual = {
        '6ajnOk0GcY9xbb5Ocaw8Gw'
    }
    assert test == actual
    test = set(
        t[0] for t in db_conn.execute(
            calc.TEAM_DISLIKES_SQL, ('3714b577-b693-4cb0-a77c-a6616c692225',)
        )
    )
    actual = {
        '6ajnOk0GcY9xbb5Ocaw8Gw',
        'jS3affmkXWrBnidXA-DIfQ',
        '8pqdJjefYq-a9IBSJJmKwA'
    }
    assert test == actual
    test = set(
        t[0] for t in db_conn.execute(
            calc.TEAM_DISLIKES_SQL, ('67004926-1b19-427e-a764-de8c917f3d15',)
        )
    )
    actual = {
        '6ajnOk0GcY9xbb5Ocaw8Gw',
        '8pqdJjefYq-a9IBSJJmKwA'
    }
    assert test == actual


def test_team_total_sql(db_conn: sqlite3.Connection):
    cur = db_conn.execute(
        calc.TEAM_TOTAL_SQL,
        ("e17b91cb-5a2c-4055-befb-1d1ea9f7daca",
         "3714b577-b693-4cb0-a77c-a6616c692225"))
    assert cur.fetchone()[0] == 4
    cur = db_conn.execute(
        calc.TEAM_TOTAL_SQL,
        ("3714b577-b693-4cb0-a77c-a6616c692225",
         "67004926-1b19-427e-a764-de8c917f3d15"))
    assert cur.fetchone()[0] == 4


def test_similarity_index(db_conn: sqlite3.Connection):
    test = calc.similarity(db_conn,
                           "e17b91cb-5a2c-4055-befb-1d1ea9f7daca",
                           "3714b577-b693-4cb0-a77c-a6616c692225")
    assert test == -0.25
    test = calc.similarity(db_conn,
                           "e17b91cb-5a2c-4055-befb-1d1ea9f7daca",
                           "e17b91cb-5a2c-4055-befb-1d1ea9f7daca")
    assert test == 1.0


def test_res_likes_sql(db_conn: sqlite3.Connection):
    args = {
        'r': "jS3affmkXWrBnidXA-DIfQ",
        't': "e17b91cb-5a2c-4055-befb-1d1ea9f7daca"
    }
    test = set(t[0] for t in db_conn.execute(calc.RES_LIKES_SQL, args))
    actual = {
        "67004926-1b19-427e-a764-de8c917f3d15"
    }
    assert test == actual
    args = {
        'r': "jS3affmkXWrBnidXA-DIfQ",
        't': "3714b577-b693-4cb0-a77c-a6616c692225"
    }
    test = set(t[0] for t in db_conn.execute(calc.RES_LIKES_SQL, args))
    actual = {
        "67004926-1b19-427e-a764-de8c917f3d15",
        "e17b91cb-5a2c-4055-befb-1d1ea9f7daca"
    }
    assert test == actual


def test_res_dislikes_sql(db_conn: sqlite3.Connection):
    args = {
        'r': "jS3affmkXWrBnidXA-DIfQ",
        't': "e17b91cb-5a2c-4055-befb-1d1ea9f7daca"
    }
    test = set(t[0] for t in db_conn.execute(calc.RES_DISLIKES_SQL, args))
    actual = {
        "3714b577-b693-4cb0-a77c-a6616c692225"
    }
    assert test == actual
    args = {
        'r': "6ajnOk0GcY9xbb5Ocaw8Gw",
        't': "e17b91cb-5a2c-4055-befb-1d1ea9f7daca"
    }
    test = set(t[0] for t in db_conn.execute(calc.RES_DISLIKES_SQL, args))
    actual = {
        "67004926-1b19-427e-a764-de8c917f3d15",
        "3714b577-b693-4cb0-a77c-a6616c692225"
    }
    assert test == actual


def test_res_total_sql(db_conn: sqlite3.Connection):
    args = {'r': "6ajnOk0GcY9xbb5Ocaw8Gw"}
    test = db_conn.execute(calc.RES_TOTAL_SQL, args).fetchone()[0]
    assert test == 3
    args = {'r': "jS3affmkXWrBnidXA-DIfQ"}
    test = db_conn.execute(calc.RES_TOTAL_SQL, args).fetchone()[0]
    assert test == 3
    args = {'r': "mtvT7uRey3F395STFRM1Tg"}
    test = db_conn.execute(calc.RES_TOTAL_SQL, args).fetchone()[0]
    assert test == 2


def test_prediction(db_conn: sqlite3.Connection):
    args = {
        'r_id': "6ajnOk0GcY9xbb5Ocaw8Gw",
        't_id': "e17b91cb-5a2c-4055-befb-1d1ea9f7daca"
    }
    test = calc.prediction(db_conn, **args)
    assert isclose(test, -0.0833, rel_tol=1e-3)


def test_recommendation(db_conn: sqlite3.Connection):
    answer = ["Vernick Food & Drink", "Butcher Bar", "Barbuzzo"]
    t_id = 'e17b91cb-5a2c-4055-befb-1d1ea9f7daca'
    assert list(calc.recommendations(db_conn, t_id)) == answer
