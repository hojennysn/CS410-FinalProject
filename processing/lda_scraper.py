import string
import praw
import win_unicode_console
from nltk.stem import *


win_unicode_console.enable()

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
    for post in reddit.subreddit(subred).top('all', limit=3):
        comment = get_comment_from_post(post)
        comment_clean = genVocab(comment)
        # print(comment_clean)
        commentsList.append(comment)

    print(commentsList)
    print(len(commentsList))
    return commentsList


def main():
    doc_complete = get_comments("all")
    # doc_clean = ["".join(genVocab(post)) for post in doc_complete]
    # print(doc_clean)


if __name__ == "__main__":
    main()


