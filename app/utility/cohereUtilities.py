import os
import cohere


def analyze_review_sentiment(reviewsList):
    # Initializing cohere client with api key saved as env variable
    co = cohere.Client(os.environ.get('COHERE_API_KEY'))

    inputs = reviewsList

    response = co.classify(
        model=os.environ.get("CLASSIFY_MODEL_ID","large"), # Fine tuned trained model in cohere platform using open source data from kaggle
        inputs=inputs
    )

    returnData = [
        {
            "review": classification.input,
            "reviewSentiment": classification.prediction,
            "reviewSentimentScore": round(classification.confidence * 100, 2)
        }
        for classification in response.classifications
    ]
    
    return returnData
