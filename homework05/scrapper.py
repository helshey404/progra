import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """

    news_list = []
    titles = parser.find_all("tr", {"id": True, "class": "athing"})

    for title in titles:
        article_id = title.get("id")
        article_url = title.find("a", {"class": "storylink"})
        article_title = article_url.text

        if not "https" in article_url:
            article_url = "https://news.ycombinator.com/" + \
                article_url.get("href")

        score = parser.find("span", {"id": f"score_{article_id}"})
        score_parent_tag = score.parent

        score = score.text.split(" ")[0]

        author = score_parent_tag.find("a").text
        comments = score_parent_tag.find(
            "a", {"href": f"item?id={article_id}"}).text.split(" ")[0]

        article = {

            'author': author,
            'comments': comments,
            'points': score,
            'title': article_title,
            'url': article_url,
        }
        news_list.append(article)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """

    next_url = parser.find("a", {"class": "morelink"})

    return "https://news.ycombinator.com/" + next_url.get("href")


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        news_list = extract_news(soup)
        url = extract_next_page(soup)
        news.extend(news_list)
        n_pages -= 1
    return news
