from textblob import TextBlob

def analyze(text):
    try:
        score = TextBlob(text).sentiment.polarity

        if score > 0:
            return "Positif"

        elif score < 0:
            return "Negatif"

        return "Netral"
    except Exception:
        return "Netral"