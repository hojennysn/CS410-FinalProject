import praw
import sys
import string
from nltk.stem import *

reddit = praw.Reddit(user_agent='SimSubReds',
				     client_id='ZLLdCB1K0e4fLA',
				     client_secret='eVBMIHzTJ50CnuUsbjQcczxCBkA',
                     password='wedungoofed',
                     username='UIUCcs410')

def getComments(subred):
	num = 0
	f = open('comments.txt', 'a+')
	commentList = []
	for s in reddit.subreddit(subred).top('all'):
	    if num > 10:
	    	f.close()
	    	return commentList
	    	break
	    num +=1
	    sub = reddit.submission(id=s)
	    sub.comments.replace_more(limit=0)
	    for comment in sub.comments.list():
    		commentList += (comment.body.rstrip()).split()
	f.close()
	return commentList

def getStopWords(fileName):
	stopwords = []
	with open(fileName) as f:
		for line in f:
			stopwords.append(line.rstrip())
	return stopwords

def genVocab(comments):
	stemmer = PorterStemmer()
	stop = getStopWords(sys.argv[2])
	translator = str.maketrans('', '', string.punctuation)
	vocab = [com.translate(translator).lower() for com in comments]
	return [stemmer.stem(v) for v in vocab if v not in stop]

def main():
    if len(sys.argv) != 3:
    	print ("Wrong number of arguments, expected: 3, got: {}".format((len(sys.argv)-1)))
    	print ("Usage: python3 scraper.py [subreddit name] [stopwords filename]")
    	sys.exit()
    comments = (getComments(sys.argv[1]))
    vocab = genVocab(comments)
    print (vocab)

if __name__ == "__main__": main()