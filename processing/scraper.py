import praw
import sys
import string
from nltk.stem import *
from prawcore import NotFound

reddit = praw.Reddit(user_agent='SimSubReds',
                     client_id='ZLLdCB1K0e4fLA',
                     client_secret='eVBMIHzTJ50CnuUsbjQcczxCBkA',
                     password='wedungoofed',
                     username='UIUCcs410')

def subExists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists

def getComments(subred, niters):
    num = 0
    commentList = []
    docCollection = [[] for i in range(niters)]
    for s in reddit.subreddit(subred).top('all'):
        if num >= niters:
            return (commentList, docCollection)
            break
        sub = reddit.submission(id=s)
        sub.comments.replace_more(limit=0)
        for comment in sub.comments.list():
            temp = (comment.body.rstrip()).split()
            commentList += temp
            docCollection[num] += temp
        num += 1
    return (commentList, docCollection)

def getStopWords(fileName):
    stopwords = []
    with open(fileName) as f:
        for line in f:
            stopwords.append(line.rstrip())
    return stopwords

def genVocab(comments, stopwords):
    stemmer = PorterStemmer()
    stop = getStopWords(stopwords)
    translator = str.maketrans('', '', string.punctuation)
    vocab = [com.translate(translator).lower() for com in comments]
    actualVocab = [stemmer.stem(v) for v in vocab if v not in stop]
    return (list(set(actualVocab)) , actualVocab)

def genDoc(docArg, stopwords):
    stemmer = PorterStemmer()
    stop = getStopWords(stopwords)
    translator = str.maketrans('', '', string.punctuation)
    doc = [word.translate(translator).lower() for word in docArg]
    return [stemmer.stem(word) for word in doc if word not in stop]

def getTopKWordsInVocab(vocabLst, vocabActual, k):
    wordCount = {word: 0 for word in vocabLst}
    for word in vocabLst:
        wordCount[word] = vocabActual.count(word)
    sortedWordCount = sorted(wordCount, key=wordCount.__getitem__, reverse=True)
    return sortedWordCount[:k]

def caller(searchTerm, stopwords, numIter):
    if not(subExists(searchTerm)):
        return None
    comments, docCollection = getComments(searchTerm, numIter)
    vocab, orgVocab = genVocab(comments, stopwords)
    for i in range(len(docCollection)):
        docCollection[i] = genDoc(docCollection[i], stopwords)
    top2words = getTopKWordsInVocab(vocab, orgVocab, 2)
    recommended =  reddit.subreddits.search_by_topic(top2words[0]+ " " +top2words[1])
    names = []
    for subr in recommended:
        names.append(subr.display_name)
    return names

def main():
    if len(sys.argv) != 4:
        print ("Wrong number of arguments, expected: 4, got: {}".format((len(sys.argv)-1)))
        print ("Usage: python3 scraper.py [subreddit name] [stopwords filename] [iterations]")
        sys.exit()
    if not(subExists(sys.argv[1])):
        print ("No subreddit called '{}' found".format(sys.argv[1]))
        sys.exit()
    comments, docCollection = getComments(sys.argv[1], int(sys.argv[3]))
    vocab, orgVocab = genVocab(comments, sys.argv[2])
    for i in range(len(docCollection)):
        docCollection[i] = genDoc(docCollection[i], sys.argv[2])
    top5words = getTopKWordsInVocab(vocab, orgVocab, 5)
    print (top5words)
    recommended =  reddit.subreddits.search_by_topic(top5words[0]+ " " +top5words[1])
    for subr in recommended:
        print (subr.display_name)

if __name__ == "__main__": main()
