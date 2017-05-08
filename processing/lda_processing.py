import lda_scraper
import gensim
from gensim import corpora


def run_lda(doc_term_matrix, dictionary):
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    
    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)
    
    print(ldamodel.print_topics(num_topics=10, num_words=4))
    #print("Finished \n")
    
    for i in range(10):
        print(ldamodel.show_topic(i, 3), "\n")
        
        
    #print(ldamodel.show_topics(num_topics=10, num_words=4))


def create_matrix(doc_clean):
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    run_lda(doc_term_matrix, dictionary)


def main():
    complete_docs = lda_scraper.get_docs()
    create_matrix(complete_docs)


if __name__ == "__main__":
    main()
