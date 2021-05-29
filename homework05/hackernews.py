from bottle import (
    route, run, template, request, redirect)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():

    s = session()
    label, _id = request.query["label"], request.query["id"]
    row = s.query(News).filter(News.id == _id).all()[0]
    row.label = label
    s.add(row)
    s.commit()
    redirect("/news")


@route("/update")
def update_news():

    s = session()

    number_of_pages = 5
    url = "https://news.ycombinator.com/newest"
    news = get_news(url, number_of_pages)

    for article in news:
        title = article['title']
        author = article['author']
        row = s.query(News).filter(
            News.title == title and News.author == author).all()
        if not row:

            new_entry = News(title=article.get('title'), author=article.get('author'), url=article.get(
                'url'), comments=article.get('comments'), points=article.get('points'))
            s.add(new_entry)
            s.commit()

    redirect("/news")


@route('/recommendations')
def recommendations():

    s = session()

    classified_news = []

    unmarked_rows = s.query(News).filter(News.label == None).all()
    marked_rows = s.query(News).filter(News.label != None).all()

    X = []
    y = []

    for row in marked_rows:
        title = row.title
        label = row.label
        X.append(title)
        y.append(label)

    model = NaiveBayesClassifier()
    model.fit(X, y)

    for row in unmarked_rows:

        title = row.title
        score = model.predict(title)
        classified_news.append([score, row])

    # g, m, n are already sorted
    classified_news.sort(key=lambda x: x[0])

    final = []
    for data in classified_news:
        final.append(data[1])
    print(final)

    return template('recommendations_template', rows=final)


if __name__ == "__main__":
    run(host="localhost", port=8080)
