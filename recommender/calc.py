import sqlite3

TEAM_LIKES_SQL = """
    SELECT restaurantId
    FROM ratings
    WHERE rating='LIKE' AND teammateId=?
"""
TEAM_DISLIKES_SQL = """
    SELECT restaurantId
    FROM ratings
    WHERE rating='DISLIKE' AND teammateId=?
"""
TOTAL_SQL = """
    SELECT COUNT(DISTINCT restaurantId)
    FROM ratings
    WHERE teammateId=? OR teammateId=?
"""


def similarity(db_conn: sqlite3.Connection, t1_id: str, t2_id: str) -> float:
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
    total = db_conn.execute(TOTAL_SQL, (t1_id, t2_id)).fetchone()[0]
    return (both_like + both_dislike - like_dislike - dislike_like) / total


def prediction(t_id: str, r_id: str) -> float:
    pass
