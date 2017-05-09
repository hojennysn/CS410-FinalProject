import string
import praw
from nltk.stem import *


# stop = set(stopwords.words('englsh'))
exclude = set(string.punctuation)
lemma = wordnet.WordNetLemmatizer()


reddit = praw.Reddit(user_agent='SimSubReds',
                     client_id='ZLLdCB1K0e4fLA',
                     client_secret='eVBMIHzTJ50CnuUsbjQcczxCBkA',
                     password='wedungoofed',
                     username='UIUCcs410')


def get_stop_words(fileName):
    stopwords = []
    with open(fileName) as f:
        for line in f:
            stopwords.append(line.rstrip())
    return stopwords


def genVocab(comments):
    stemmer = PorterStemmer()
    stop = get_stop_words(fileName="processing/lemur-stopwords-edit.txt")
    translator = str.maketrans('', '', string.punctuation)
    vocab = [com.translate(translator).lower() for com in comments]
    return [stemmer.stem(v) for v in vocab if v not in stop]


def get_comment_from_post(post):
    wordList = []
    sub = reddit.submission(id=post)
    sub.comments.replace_more(limit=0)
    for comment in sub.comments.list():
        wordList += (comment.body.rstrip()).split()

    return wordList


def get_comments(subred):
    commentsList = []
    for post in reddit.subreddit(subred).top('all', limit=10):
        comment = get_comment_from_post(post)
        comment_clean = genVocab(comment)
        # print(comment_clean)
        commentsList.append(comment_clean)

    return commentsList

def get_docs(subred):
    docs_complete = get_comments(subred)
    return docs_complete

def main():
    docs_complete = get_docs()
    print(docs_complete)
    print(len(docs_complete))


if __name__ == "__main__":
    main()


