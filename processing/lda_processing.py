#import scraper
#import lda_scraper

from . import scraper
from . import lda_scraper
import gensim
from gensim import corpora


num_of_topics = 4


def make_query(topic):
    words = [w[0] for w in topic]
    print(" ".join(words))
    search_query = " ".join(words)
    return search_query


def run_lda(doc_term_matrix, dictionary):
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    
    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics = num_of_topics, id2word = dictionary, passes=50)
    print(ldamodel.print_topics(num_topics=num_of_topics, num_words=4))
    return ldamodel
       
        
def create_matrix(doc_clean):
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    return (doc_term_matrix, dictionary)


def intersect(lists):
    return list(set.intersection(*map(set, lists)))


def get_subred_intersection(ldamodel):
    print("\n____Getting intersection____ ")   
    list_of_subs = [] 
    subreddits = []
    for i in range(num_of_topics):
        print(ldamodel.show_topic(i, 10))
        topic = ldamodel.show_topic(i, 3)
        search_query = make_query(topic)
        subreddits = scraper.get_names_of_subreddits(search_query)
        if len(subreddits) != 0:
            list_of_subs.append(subreddits)
            
    names = intersect(list_of_subs)
    print(names, "\n____Finished____\n")
    return names
    

def get_lda_recommendations(subred):
    complete_docs = lda_scraper.get_docs(subred)
    doc_term_matrix, dictionary = create_matrix(complete_docs)
    ldamodel = run_lda(doc_term_matrix, dictionary)
    
    #get intersection instead
    get_subred_intersection(ldamodel)
    
    names = []
    for i in range(num_of_topics):
        topic = ldamodel.show_topic(i, 3)
        search_query = make_query(topic)
        names = scraper.get_names_of_subreddits(search_query)
        if len(names) != 0:
            return names
        
    return names
    

def main():
    names = get_lda_recommendations("all")
    print(names)

if __name__ == "__main__":
    main()
