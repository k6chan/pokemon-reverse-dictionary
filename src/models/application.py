from flask import Flask, request, render_template
import pandas as pd
import sklearn.feature_extraction as fe
from sklearn.metrics.pairwise import cosine_similarity

import spacy

import gensim.downloader
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from scipy import spatial


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def query():
    if request.method == "POST":
        functions = {
            "ir_tf_idf": ir_tf_idf,
            "ir_tf_idf_word2vec": ir_tf_idf_word2vec
        }
        
        user_query = request.form.get("query")
        model_type = functions[request.form.get("model_type")]
        results = model_type(clean_query(user_query))
        return render_template("output.html",pokemon_1=results[0],pokemon_2=results[1],
        pokemon_3=results[2],pokemon_4=results[3],pokemon_5=results[4])
    return render_template("input.html")


df = pd.read_csv("data/bulbapedia_smogon_data.csv")


nlp = spacy.load("data/vocabulary/en_core_web_sm-3.5.0")
def clean_query(raw_query):
    #lowercase, stem, remove stopwords
    lowercase = raw_query.lower()
    document = nlp(lowercase)
    tokens = []
    for token in document:
        if token.text not in spacy.lang.en.stop_words.STOP_WORDS:
            tokens.append(token.lemma_)
    cleaned_query = " ".join(tokens)
    return cleaned_query


model = fe.text.TfidfVectorizer(input="content")
vector = model.fit_transform(df["description"])
def ir_tf_idf(query):
    res = model.transform([query])
    similarities = cosine_similarity(vector,res)
    df_sims = df.assign(sim=similarities.reshape(-1)).sort_values(by="sim",ascending=False)
    top_5 = []
    for i in range(5):
        top_5.append((df_sims.iloc[i]["name"],df_sims.iloc[i]["thumbnail"]))
    return top_5


w2v_model =  KeyedVectors.load('data/vocabulary/glove-wiki-gigaword-50_vectors.bin')
def ir_tf_idf_word2vec(query):
    sims = []
    large_query = query
    for token in query.split():
        additional_words = list(map(lambda item: item[0], w2v_model.most_similar(token)))
        large_query = large_query + " " + " ".join(additional_words)
    return ir_tf_idf(large_query)