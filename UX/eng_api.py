import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re
# csv datasets
print("   reading csv files...")
comments_df = pd.read_csv("UX/antique_docs.csv") 
documents_df = pd.read_csv("UX/mr_tydi_docs.csv")

# preprcessing
print("   creating preprocessing image")
acronyms = {
    "u.s": "united states",
    "u.s.a": "united states",
    "u.n": "united nations",
    "i.e": "example",
    "e.g.": "for example",
    "m.p": "member of the house of lords",
    "ibm": "International Business Machines Corporation",
    "tss": "Time Sharing System",
}

# or using nltk
"""
print(dataset.queries_cls()._fields)
"""
punc_list = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']
def remove_puctuation(text):
  return re.sub("["+"".join(punc_list)+"]","",text)

def lower(text):
  return text.lower()

def replace_acronyms(text, acronyms_dict=acronyms):
  tmp = text
  for word in text.split(' '):
    if word in acronyms_dict.keys():
      tmp = tmp.replace(word, acronyms_dict[word])
  return tmp

en_sw = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

def remove_stop_words(text, sw = en_sw):
  ls = []
  for word in text.split(' '):
    if(word != '' and word.lower() not in en_sw):
       ls.append(word)
  return ' '.join(ls)

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')

def lemmatize(text):
  return ' '.join([lemmatizer.lemmatize(i) for i in text.split(' ')])

from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
def stem(text):
  return ' '.join([stemmer.stem(i) for i in text.split(' ')])

def preprocess(text_df, remove_puctuation_=True, lower_=True, replace_acronyms_=True, acronyms_dict=acronyms, remove_stop_words_=True, lemmatize_=True, stem_=True):
  # df is the text column to be preprocessed
  if(type(text_df)==type(pd.DataFrame())):
    if remove_puctuation_: text_df = text_df.apply(lambda x: remove_puctuation(x))
    if lower_: text_df = text_df.apply(lambda x: lower(x))
    if replace_acronyms_: text_df = text_df.apply(lambda x: replace_acronyms(x, acronyms_dict))
    if remove_stop_words_: text_df = text_df.apply(lambda x: remove_stop_words(x))
    if lemmatize_: text_df = text_df.apply(lambda x: lemmatize(x))
    if stem_: text_df = text_df.apply(lambda x: stem(x))
  if(type(text_df)==type(str())):
    if remove_puctuation_: text_df = remove_puctuation(text_df)
    if lower_: text_df = lower(text_df)
    if replace_acronyms_: text_df = replace_acronyms(text_df, acronyms_dict)
    if remove_stop_words_: text_df = remove_stop_words(text_df)
    if lemmatize_: text_df = lemmatize(text_df)
    if stem_: text_df = stem(text_df)
  return text_df

print("   creating recommendation system...")
def get_recommendations(docs_df, scores_array, start=0, n=10, TextColName="text"):
  # for the API send doc_df as all the dataset
  # for the test make doc_df only the text
  sorted_indices = scores_array.argsort()[::-1]
  start = min(start, len(sorted_indices))
  n = min(start+n, len(sorted_indices))
  docs_id = list()
  for position, idx in enumerate(sorted_indices[start:start+n]):
    """
    row = docs_df.iloc[idx]
    text = row[TextColName]
    score = scores_array[idx]
    print(docs_df.iloc[idx].doc_id)
    print(f"{position + 1} {idx} [score = {score}]: {text}")
    """
    docs_id.append(docs_df.iloc[idx].doc_id)
  return docs_id

# create the vectorize model on the whole dataset
print("   creating tfidf vertorizers...")
# you can generate corpuses or load them using joblib
# to generated corpuses

from sklearn.feature_extraction.text import TfidfVectorizer
documents_Vectorizer = TfidfVectorizer()
corpus = list(preprocess(documents_df.text))
documents_corpus_vectorized = documents_Vectorizer.fit_transform(corpus)

comments_Vectorizer = TfidfVectorizer()
corpus = list(preprocess(comments_df.text.astype('U')))
comments_corpus_vectorized = comments_Vectorizer.fit_transform(corpus)

"""
import joblib
comments_corpus_vectorized = joblib.load('UX/antique_docs_vectorizer.tfidf')
documents_corpus_vectorized = joblib.load('UX/mr_tydi_docs_vectorizer.tfidf')
"""
def get_docs(q, docs_df, start=0, n=10, TextColName="text"):
  query = preprocess(text_df=q)
  query_vectorized = documents_Vectorizer.transform([query])
  scores = query_vectorized.dot(documents_corpus_vectorized.transpose())
  scores_array = scores.toarray()[0]
  docs_id = get_recommendations(docs_df, scores_array, start, n)
  docs_df =  docs_df.set_index('doc_id')
  docs_df = docs_df.loc[docs_id]
  print(docs_df.text.head())
  print(docs_df.columns)
  print(docs_df)
  docs_list = []
  for doc in docs_df:
    print("doc: " + str(doc))
    docs_list.append({"doc_id":str(doc.doc_id), "title":str(doc.title), "text":str(doc.text)})
  
  return docs_list

def get_comments(q, docs_df, start=0, n=10, TextColName="text"):
  query = preprocess(text_df=q)
  query_vectorized = comments_Vectorizer.transform([query])
  scores = query_vectorized.dot(comment_corpus_vectorized.transpose())
  scores_array = scores.toarray()[0]
  docs_id = get_recommendations(docs_df, scores_array, start, n)
  docs_df =  docs_df.set_index('doc_id')
  docs_df = docs_df.loc[docs_id]
  docs_df = list(docs_df.to_dict().values())
  return docs_df

print("Done.")
# __docs = get_docs(q = "war on iraq", docs_df=documents_df, start=0, n=10, TextColName="text")

# __comments = get_docs(q = "war on iraq", docs_df=comments_df, start=0, n=10, TextColName="text")