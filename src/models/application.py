from flask import Flask, request, render_template
import pandas as pd
import sklearn.feature_extraction as fe
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def query():
    if request.method == "POST":
        user_query = request.form.get("query")
        results_ir_tf_idf = ir_tf_idf(user_query)
        return render_template("output.html",pokemon_1=results_ir_tf_idf[0],pokemon_2=results_ir_tf_idf[1],
        pokemon_3=results_ir_tf_idf[2],pokemon_4=results_ir_tf_idf[3],pokemon_5=results_ir_tf_idf[4])
    return render_template("input.html")


df = pd.read_csv("data/bulbapedia_smogon_data.csv")

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
