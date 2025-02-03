from fastapi import FastAPI, Query
from typing import Union, Optional
from pydantic import BaseModel, conlist
from .utility import cohereUtilities
from .db import create_table, fetch_review_sentiment, insert_review_sentiment, fetch_reviews
import traceback
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()


try:
    # Initialize DB Table
    create_table()
except:
    traceback.print_exc()

class ProductReviews(BaseModel):
    reviews: conlist(str, min_length=1) # type: ignore


@app.get('/')
def index():
    return {'message': "Success!"}


@app.post("/sentiment-analysis")
def post_sentiment_analysis(reviews: ProductReviews):
    responses = []

    for review in reviews.reviews:
        existing_record = fetch_review_sentiment(review)

        if existing_record:
            print(existing_record)
            responses.append({
                "review": existing_record["review"],
                "reviewSentiment": existing_record["review_sentiment"],
                "reviewSentimentScore": existing_record["review_sentiment_score"]
            })
        else:
            new_sentiment = cohereUtilities.analyze_review_sentiment([review])[0]
            insert_review_sentiment(new_sentiment["review"], new_sentiment["reviewSentiment"], new_sentiment["reviewSentimentScore"])
            responses.append(new_sentiment)

    return {"responses": responses}


# For search result page
@app.get("/sentiment-analysis")
def get_sentiment_analysis(
    searchQuery: Optional[str] = Query(None, description="Search query for filtering reviews"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Limit for pagination (max 100)")
):
    results = fetch_reviews(search_query=searchQuery, offset=offset, limit=limit)
    return {"reviews": results}
