from flask import Flask, render_template, jsonify, request
import json
import random
from processing import scraper

app = Flask(__name__)


def random_topics(searchTerm, stopwords, numIter):
    temp = scraper.caller(searchTerm, stopwords, numIter)
    return temp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/topics', methods=['GET', 'POST'])
def get_topics():
    if request.method == 'GET':
        if 'subreddit' in request.args:
            sub = request.args.get('subreddit')
            topics = random_topics(sub, "processing/lemur-stopwords-edit.txt", 5)
            if topics is None:
                print ("No such sub")
                return json.dumps([])
            return json.dumps(topics)
    return jsonify(result="nope")

if __name__ == '__main__':
    app.run()
