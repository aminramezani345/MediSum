import os
import webbrowser
import time
from threading import Timer
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def medicalnotes():
    internal_medicine = ""
    primary_care = ""
    internal_medicine_comments = ""
    primary_care_comments = ""
    search_results = ""

    if request.method == 'POST':
        internal_medicine = request.form['internal_medicine']
        primary_care = request.form['primary_care']
        internal_medicine_comments = request.form.get('internal_medicine_comments', '')
        primary_care_comments = request.form.get('primary_care_comments', '')

        combined_text = " ".join([internal_medicine, primary_care, internal_medicine_comments, primary_care_comments])

        # Search for the term "cardio" in the combined text
        if "cardio" in combined_text:
            search_results = "The term 'cardio' was found in the text."
        else:
            search_results = "The term 'cardio' was not found in the text."

    return render_template("MediSumHome_1.html",
                           internal_medicine=internal_medicine,
                           primary_care=primary_care,
                           internal_medicine_comments=internal_medicine_comments,
                           primary_care_comments=primary_care_comments,
                           search_results=search_results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
