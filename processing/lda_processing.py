#import scraper
#import lda_scraper

from . import scraper
from . import lda_scraper
import gensim
from gensim import corpora


num_of_topics = 3


def make_query_get_topics(topic):
    words = [w[0] for w in topic]
    print(" ".join(words))
    search_query = " ".join(words)
    return search_query


def run_lda(doc_term_matrix, dictionary):
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    
    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics = num_of_topics, id2word = dictionary, passes=50)
    print(ldamodel.print_topics(num_topics=3, num_words=4))
    return ldamodel
       
        
def create_matrix(doc_clean):
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    return (doc_term_matrix, dictionary)



def get_lda_recommendations(subred):
    complete_docs = lda_scraper.get_docs(subred)
    doc_term_matrix, dictionary = create_matrix(complete_docs)
    ldamodel = run_lda(doc_term_matrix, dictionary)
    
    names = []
    for i in range(num_of_topics):
        topic = ldamodel.show_topic(i, 4)
        search_query = make_query_get_topics(topic)
        names = scraper.get_names_of_subreddits(search_query)
        if len(names) != 0:
            return names
        
    return names
    
    #topic = ldamodel.show_topic(0, 4)
    #search_query = make_query_get_topics(topic)
    #names = scraper.get_names_of_subreddits(search_query)
    #return names

def main():
    names = get_lda_recommendations("all")
    print(names)

if __name__ == "__main__":
    main()
