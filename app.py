from flask import Flask, render_template, jsonify, request
import json
import random

app = Flask(__name__)


def random_topics(sub):
    temp = random.sample(range(100), 10)
    temp.append(sub)
    return temp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/topics', methods=['GET', 'POST'])
def get_topics():
    if request.method == 'GET':
        if 'subreddit' in request.args:
            sub = request.args.get('subreddit')
            topics = random_topics(sub)
            return json.dumps(topics)

    return jsonify(result="nope")

if __name__ == '__main__':
    app.run()
