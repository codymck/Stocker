import score_sentiment
import update_lexicon
import forecaster
import requests
from bs4 import BeautifulSoup

def main(data):
    # input market sector: energy, healthcare, financial, tech
    market_sector = data.get('market')
    timeframe = data.get('timeframe')
    risk = data.get('risk')

    update_lexicon.update_lexicon(timeframe, risk)

    URL = f'https://www.forbes.com/advisor/investing/best-{market_sector}-stocks/'
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html5lib')

    stocks = []  # a list to store stocks
    stock_names = {}  # a dictionary to store stock names
    table = soup.find('div', attrs={'class': 'bottom-section'})

    for row in table.find_all('div', attrs={'class': 'article-section hide-section-title'}):
        card_element = row.find('h3', attrs={'class': 'card-title'})

        # make sure the element is not none
        if card_element is None:
            continue
        card_title = card_element.text

        # check if the ticker parenthesis exists (not an ad)
        if "(" not in card_title:
            continue
        split = card_title.split('(')
        stock_names[split[1][:-1]] = split[0][:-1]
        stocks.append(split[1][:-1])

    print(f'Tickers to look through {stocks}')

    sentiment_results = []

    for stock in stocks:
        sentiment_results.append(score_sentiment.get_ticker_info(stock, stock_names[stock]))
        forecaster.formatData(stock)

    sorted_results = sorted(sentiment_results, reverse=True, key=score_sentiment.return_score)

    top_three = []
    for i in range(3):
        del sorted_results[i]['article_score']
        del sorted_results[i]['overall_score']
        top_three.append(sorted_results[i])

    return top_three
