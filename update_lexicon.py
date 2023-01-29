import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def update_lexicon(timeframe, risk):
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()

    if int(timeframe) > 4:
        long_term = 2.5
        short_term = -2.5
    else:
        long_term = -2.5
        short_term = 2.5

    if risk == 'lowRisk':
        risk = -2.5
    else:
        risk = 2.5

    # add finance words
    new_words = {
        'rose': 1.8,
        'rising': 1.8,
        'outperformed': 1.7,
        'outperforms': 1.7,
        'favorable': 0.9,
        'gain': 1.2,
        'gains': 1.2,
        'gained': 1.2,
        'positive': 2.0,
        "hope": 1.8,
        "optimism": 1.7,

        'fell': -1.2,
        'falling': -1.2,
        'dropped': -0.9,
        'dropping': -0.9,
        'underperformed': -1.8,
        'decreased': -1.7,
        'decreasing': -1.7,
        'lost': -0.8,
        'losing': -0.8,
        'slump': -2.0,
        'slumped': -2.5,
        'slumping': -2.5,
        'negative': -2.3,
        'doubt': -1.9,
        'fear': -1.5,

        'long-term': long_term,
        'short-term': short_term,
        'risk': risk,
        'volatile': risk,
        'dangerous': risk
    }
    sia.lexicon.update(new_words)
