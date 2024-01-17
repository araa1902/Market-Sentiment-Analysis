import requests
import math
from datetime import datetime
import os

def Get_market_news(ticker):
    market_news = []
    try:
        # Fetch market news data for the specified ticker from the API
        response = requests.get(f"https://api.marketaux.com/v1/news/all?symbols={ticker}&must_have_entities=true&published_after=2023-01-01&language=en&api_token=PCCHjrMwiZzPK2iuujAjsi63DCVfJzyGujYyk7I7")
        data = response.json()['data']

        for article in data:
            entities = article.get('entities', [])
            
            # Check if any entity in the article matches the specified ticker
            if any(entity.get('symbol') == ticker for entity in entities):
                title = article.get('title')
                description = article.get('description')
                if title and description:
                    # Store title and description in a tuple within the list
                    market_news.append((title, description))

        return market_news
    except Exception as e:
        return f"Failed to retrieve market news data for ticker {ticker}. Error: {e}"

def preprocessing(news):
    with open(os.path.join(os.path.dirname(__file__), "stopwords.txt"), 'r') as f:
        words_to_remove = set(word.strip() for word in f.readlines())

    # Iterate through each tuple (title, description) in the list
    processed_news = []
    for title, description in news:
        # Remove stopwords from title and description, and convert to lowercase
        title_filtered = [word.lower() for word in title.split() if word.lower() not in words_to_remove]
        description_filtered = [word.lower() for word in description.split() if word.lower() not in words_to_remove]
        processed_news.append((title_filtered, description_filtered))

    return processed_news

def lexicon_sentiments(): # Creates dictionary holding the words and their corresponding sentiment
    sentiment_dict = {}
    with open(os.path.join(os.path.dirname(__file__), "lexicon_sentiments.txt"), 'r') as f:
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
                # Count positive and negative lexicons based on sentiment values
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
    
    # Check if both positive and negative lexicons are zero, indicating a neutral sentiment
    if p_lexicons == 0 and n_lexicons == 0:
        return "This stock has a neutral sentiment"
    
    # Calculate positive and negative probabilities using Naive Bayes formula
    try:
        positive_prob, negative_prob = math.log(p_lexicons / (p_lexicons + n_lexicons)), math.log(n_lexicons / (p_lexicons + n_lexicons))
    except:
        return "Unable to calculate sentiment for ticker."
    
    # Compare probabilities to determine sentiment
    if positive_prob > negative_prob:
        print(positive_prob)
        return "This stock is following a positive sentiment"
    else:
        print(negative_prob)
        return "This stock is following a negative sentiment"

def get_sentiment():
    ticker = input("Please enter a valid ticker: ")
    try:
        print(get_sentiment_result(get_lexicon_sentiments(preprocessing(Get_market_news(ticker)))))
    except OSError as e:
        print(e)

get_sentiment()
