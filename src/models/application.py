from flask import Flask
import markdown


app = Flask(__name__)

@app.route("/")
def hello_world():
    return markdown.markdown("Hello world!")
