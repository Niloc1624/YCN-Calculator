from flask import Flask, render_template, request
from webScraper import webScraper
import pandas as pd


app = Flask(__name__)


# Not sure what most of this (or any of the associated HTML) does, ChatGPT wrote most of it.
@app.route("/")
def input_page():
    return render_template("input_page.html")


@app.route("/display_list", methods=["POST"])
def display_list():
    first_names = request.form["first_name"]
    last_names = request.form["last_name"]
    webScraper_output = webScraper(first_names, last_names)
    output = webScraper_output[0]
    return render_template(
        "display_list.html",
        output=output,
        isinstance=isinstance,
        str=str,
        df=pd.DataFrame,
    )


if __name__ == "__main__":
    app.run(debug=True)
