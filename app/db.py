import os
import psycopg2
from psycopg2.extras import DictCursor


DATABASE_URL = os.getenv("DATABASE_URL", "dbname=postgres user=postgres host=localhost port=5432")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movie_review_sentiments (
            id SERIAL PRIMARY KEY, 
            review TEXT,
            review_sentiment TEXT,
            review_sentiment_score Decimal(5,2)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def fetch_review_sentiment(review):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movie_review_sentiments WHERE review = %s", (review.lower(),))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def insert_review_sentiment(review, sentiment, score):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO movie_review_sentiments (review, review_sentiment, review_sentiment_score) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (review.lower(), sentiment, score))
    conn.commit()
    cur.close()
    conn.close()


def fetch_reviews(search_query=None, offset=0, limit=10):
    conn = get_db_connection()
    cur = conn.cursor()

    if search_query:
        cur.execute("""
            SELECT review, review_sentiment, review_sentiment_score 
            FROM movie_review_sentiments 
            WHERE review ILIKE %s 
            ORDER BY id desc 
            LIMIT %s OFFSET %s
        """, (f"%{search_query}%", limit, offset))
    else:
        cur.execute("""
            SELECT review, review_sentiment, review_sentiment_score 
            FROM movie_review_sentiments 
            ORDER BY id desc 
            LIMIT %s OFFSET %s
        """, (limit, offset))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return [{"review": row["review"], "reviewSentiment": row["review_sentiment"], "reviewSentimentScore": row["review_sentiment_score"]} for row in results]

