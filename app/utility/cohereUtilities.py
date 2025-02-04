import os
import cohere


def analyze_review_sentiment(reviewsList):
    # Initializing cohere client with api key saved as env variable
    co = cohere.Client(os.environ.get('COHERE_API_KEY'))

    inputs = reviewsList

    response = co.classify(
        model=os.environ.get("CLASSIFY_MODEL_ID","large"), # Fine tuned trained model in cohere platform using open source data from kaggle
        inputs=inputs,
        examples=[
              cohere.ClassifyExample("I absolutely loved this movie, it was fantastic!", "Positive"),
              cohere.ClassifyExample("The plot was dull and boring, I didn't enjoy it at all.", "Negative"),
              cohere.ClassifyExample("The movie was okay, but nothing special.", "Neutral"),
              cohere.ClassifyExample("Great acting and direction, but the pacing was off.", "Positive"),
              cohere.ClassifyExample("I hated the ending, it ruined the whole experience.", "Negative"),
              cohere.ClassifyExample("It was just average, nothing memorable.", "Neutral")
          ]
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
