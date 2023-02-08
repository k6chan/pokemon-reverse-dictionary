from flask import Flask, request, render_template


app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def query():
    if request.method == "POST":
        user_query = request.form.get("query")
        return render_template("output.html",user_query=user_query)
    return render_template("input.html")