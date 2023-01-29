from GoogleNews import GoogleNews
import newspaper
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_ticker_info(ticker, stock_name):
    gn = GoogleNews()
    gn.search(f'{ticker} Stock Investment Opinion')

    print(f'{ticker}: Searching for articles related to {ticker}...')
    articles = []
    article_names = gn.get_texts()  # list to hold the name of each article
    article_links = gn.get_links()  # get list of links from google news

    for i, name in enumerate(article_names):
        articles.append({'name': name, 'link': article_links[i], 'text': [], 'score': 0})

    for article in articles:
        url = newspaper.Article(url="%s" % article.get('link'), language='en')
        print(f'{ticker}: Rating sentiment of "{article.get("name")}"')
        try:
            url.download()
            url.parse()
        except:
            articles.remove(article)
            # print("A download error occurred")
            continue
        whole_article = url.text
        split = whole_article.split('.')
        article['text'] = split

    print(f'{ticker}: Scoring sentiment of all articles combined...')
    sia = SentimentIntensityAnalyzer()
    for article in articles:
        compound_list = []
        for sentence in article.get('text'):
            scores = sia.polarity_scores(sentence)
            score = scores['compound']
            if score != 0.0:
                compound_list.append(score)
        if len(compound_list) != 0:
            compound_avg = sum(compound_list) / len(compound_list)
            article['score'] = compound_avg

    return_dict = {
        'ticker': ticker,
        'name': stock_name,
        'overall_score': 0,
        'article_score': 0,
        'article_name': '',
        'article_link': ''
    }

    sum_of_scores = 0
    for article in articles:
        if article.get('score') > return_dict.get('article_score'):
            return_dict['article_score'] = article.get('score')
            return_dict['article_name'] = article.get('name')
            return_dict['article_link'] = article.get('link')

        sum_of_scores += article.get('score')

    return_dict['overall_score'] = sum_of_scores / len(articles)
    print(f'{ticker}: Overall score: {sum_of_scores / len(articles)}')

    return return_dict


def return_score(d) -> float:
    return float(d.get('overall_score'))
