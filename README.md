# Market Sentiment Analysis
This program harvests news article data via API requests relative to given stock within the market. It then calculates the market sentiment based on lexical analysis and uses probabilistic models to evaluate a result.

The two text files, 'lexicon_sentiments' and 'stopwords,' are used in conjunction for both the filtering stage and to aid in the probabilistic section of calculating the given sentiment.

To supply the market news data, I utilised the **marketaux** API.

![Screenshot 2023-12-02 144329](https://github.com/araa1902/Market-Sentiment-Analysis/assets/92942390/0954d1d7-68d2-4197-97c2-b1ed9c85c566)

Above is an example of the program running using the META as the company of choice.

To run the analysis:
  1. Download the python file and two corresponding text files to a folder. 
  1. Retrieve an API token via the marketaux API client and place the token in the request URL at the position "APIKEY".

**NOTE:** Due to the constraints of the free API plan, a limited amount of data is received, and consequently, some sentiment results may not be entirely accurate.
