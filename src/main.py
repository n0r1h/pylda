import pandas as pd
import os
import re
from wordcloud import WordCloud
import gensim 
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from pprint import pprint
import pyLDAvis.gensim
import pickle
import pyLDAvis


pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)

if __name__ == '__main__':
    os.chdir('..')
    papers = pd.read_csv('src/data/papers.csv')

    papers = papers.drop(columns=['id', 'event_type', 'pdf_name'], axis=1).sample(100)


    papers['paper_text_processed'] = papers['paper_text'].map(lambda x: re.sub('[,\.!?]', '', x))
    papers['paper_text_processed'] = papers['paper_text_processed'].map(lambda x: x.lower())

    long_string = ','.join(list(papers['paper_text_processed'].values))

    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
    wordcloud.generate(long_string)
    wordcloud.to_file('img.png')

    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

    def sent_to_words(sentences):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    def remove_stopwords(texts):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

    data = papers.paper_text_processed.values.tolist()
    data_words = list(sent_to_words(data))

    data_words = remove_stopwords(data_words)

    print(data_words[:1][0][:30])

    id2word = corpora.Dictionary(data_words)

    texts = data_words

    corpus = [id2word.doc2bow(text) for text in texts]

    print(corpus[:1][0][:30])

    num_topics = 10

    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=id2word, num_topics=num_topics)

    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    # pyLDAvis.enable_notebook()
    LDAvis_data_filepath = os.path.join('./ldavis_prepared_'+str(num_topics))
    # # this is a bit time consuming - make the if statement True
    # # if you want to execute visualization prep yourself
    if 1 == 1:
        LDAvis_prepared = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)
    # load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)
    pyLDAvis.save_html(LDAvis_prepared, './ldavis_prepared_'+ str(num_topics) +'.html')
    LDAvis_prepared
