"""
Handles functionality for calculating predicted restaurants for any
teammate.
"""

import sqlite3

# All restaurants that a teammate likes
TEAM_LIKES_SQL = """
    SELECT restaurantId
    FROM ratings
    WHERE rating='LIKE' AND teammateId=?
"""
# All restaurants that a teammate dislikes
TEAM_DISLIKES_SQL = """
    SELECT restaurantId
    FROM ratings
    WHERE rating='DISLIKE' AND teammateId=?
"""
# Count of restaurants that either of two teammates have rated
TEAM_TOTAL_SQL = """
    SELECT COUNT(DISTINCT restaurantId)
    FROM ratings
    WHERE teammateId=? OR teammateId=?
"""
# All teammates that like a restaurant
RES_LIKES_SQL = """
    SELECT teammateId
    FROM ratings
    WHERE rating='LIKE' AND restaurantId=:r AND teammateId!=:t
"""
# All teammates that dislike a restaurant
RES_DISLIKES_SQL = """
    SELECT teammateId
    FROM ratings
    WHERE rating='DISLIKE' AND restaurantId=:r AND teammateId!=:t
"""
# Count of teammates that have rated a restaurant
RES_TOTAL_SQL = """
    SELECT COUNT(DISTINCT teammateId)
    FROM ratings
    WHERE restaurantId=:r
"""


def similarity(db_conn: sqlite3.Connection, t1_id: str, t2_id: str) -> float:
    """ Compute the similarity between two teammates, `t1_id` & `t2_id`. """
    t1_like = \
        set(t[0] for t in db_conn.execute(TEAM_LIKES_SQL, (t1_id,)))
    t1_dislike = \
        set(t[0] for t in db_conn.execute(TEAM_DISLIKES_SQL, (t1_id,)))
    t2_like = \
        set(t[0] for t in db_conn.execute(TEAM_LIKES_SQL, (t2_id,)))
    t2_dislike = \
        set(t[0] for t in db_conn.execute(TEAM_DISLIKES_SQL, (t2_id,)))
    both_like = len(t1_like & t2_like)
    both_dislike = len(t1_dislike & t2_dislike)
    like_dislike = len(t1_like & t2_dislike)
    dislike_like = len(t1_dislike & t2_like)
    total = db_conn.execute(TEAM_TOTAL_SQL, (t1_id, t2_id)).fetchone()[0]
    return (both_like + both_dislike - like_dislike - dislike_like) / total


def prediction(db_conn: sqlite3.Connection, t_id: str, r_id: str) -> float:
    """ Predict how likely `t_id` will enjoy `r_id`. """
    args = {'t': t_id, 'r': r_id}
    other_liked = set(t[0] for t in db_conn.execute(RES_LIKES_SQL, args))
    like_sum = sum(similarity(db_conn, t_id, other) for other in other_liked)
    other_disliked = set(t[0] for t in db_conn.execute(RES_DISLIKES_SQL, args))
    dislike_sum = sum(similarity(db_conn, t_id, other) for other in other_disliked)
    total = db_conn.execute(RES_TOTAL_SQL, args).fetchone()[0]
    return (like_sum - dislike_sum) / total


def recommendations(db_conn: sqlite3.Connection, t_id: str):
    """ Yield the top 3 recommended restaurants for `t_id`. """
    recommendation_sql = """
        SELECT DISTINCT restaurants.name
        FROM restaurants JOIN ratings ON restaurants.id=ratings.restaurantId
        WHERE ratings.teammateId!=:t
        ORDER BY PRED(:t, restaurants.id) DESC, restaurants.rating DESC
        LIMIT 3
    """
    for row in db_conn.execute(recommendation_sql, {'t': t_id}):
        yield row[0]
