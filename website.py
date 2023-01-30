from flask import Flask, render_template, request
from webScraper import webScraper
import pandas as pd

# from flask_frozen import Freezer

app = Flask(__name__)

# Not sure what most of this (or any of the associated HTML) does, ChatGPT wrote most of it.


@app.route("/")
def input_page():
    return render_template("input_page.html")


@app.route("/display_list", methods=["POST"])
def display_list():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    output = webScraper(first_name, last_name)
    return render_template(
        "display_list.html",
        output=output,
        isinstance=isinstance,
        str=str,
        df=pd.DataFrame,
    )


# freezer = Freezer(app)

if __name__ == "__main__":
    app.run(debug=True)
    # freezer.freeze()
