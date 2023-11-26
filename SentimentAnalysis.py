import requests
import math
from datetime import datetime

def Get_market_news(ticker):
    market_news = []

    try:
        response = requests.get(f"https://api.marketaux.com/v1/news/all?symbols={ticker}&must_have_entities=true&published_after=2023-01-01&language=en&api_token=API_KEY")
        data = response.json()['data']

        for article in data:
            entities = article.get('entities', [])
            
            # Check if any entity in the article matches the specified ticker
            if any(entity.get('symbol') == ticker for entity in entities):
                title = article.get('title')
                description = article.get('description')
                if title and description:
                    market_news.append((title, description)) #Title and description held in tuple within the list.

        return market_news
    except Exception as e:
        return f"Failed to retrieve market news data for ticker {ticker}. Error: {e}"

def preprocessing(news):
    with open("C:\\Users\\kumar\\OneDrive\\semantics\\stopwords.txt", 'r') as f:
        words_to_remove = set(word.strip() for word in f.readlines())

    # Iterate through each tuple (title, description) in the list
    processed_news = []
    for title, description in news:
        # Remove stopwords from title and description
        title_filtered = [word.lower() for word in title.split() if word.lower() not in words_to_remove]
        description_filtered = [word.lower() for word in description.split() if word.lower() not in words_to_remove]
        processed_news.append((title_filtered, description_filtered))

    return processed_news

def lexicon_sentiments():
    sentiment_dict = {}
    with open("C:\\Users\\kumar\\OneDrive\\semantics\\lexicon_sentiments.txt", "r") as f:
        for line in f:
            results = line.strip().split('\t')
            word, sentiment_value = results[0], float(results[1])
            sentiment_dict[word] = sentiment_value
    return sentiment_dict

def get_lexicon_sentiments(processed_news):

    word_sentiments = lexicon_sentiments()
    positive_lexicons = 0
    negative_lexicons = 0

    for (title, description) in processed_news:
        for word in title:
            if word in word_sentiments:
                if word_sentiments[word] > 0:
                    positive_lexicons += 1
                else:
                    negative_lexicons += 1
            else:
                continue
        for word in description:
            if word in word_sentiments:
                if word_sentiments[word] > 0:
                    positive_lexicons += 1
                else:
                    negative_lexicons += 1
            else:
                continue

    return (positive_lexicons, negative_lexicons)

def get_sentiment_result(lexicon_polarities):
    p_lexicons, n_lexicons = lexicon_polarities[0], lexicon_polarities[1]
    if p_lexicons == 0 and n_lexicons == 0:
        return "This stock has a neutral sentiment"
    positive_prob, negative_prob = math.log(p_lexicons / (p_lexicons + n_lexicons)), math.log(n_lexicons / (p_lexicons + n_lexicons))
    if positive_prob > negative_prob:
        return "This stock is following a positive sentiment"
    else:
        return "This stock is following a negative sentiment"
    







