import os
import webbrowser
import time
from threading import Timer
from flask import Flask, render_template, request
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import threading

app = Flask(__name__)

# Initialize the summarization pipeline with an instruct model
model_name = "sshleifer/distilbart-cnn-6-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

@app.route("/", methods=['GET', 'POST'])
def medicalnotes():
    internal_medicine = ""
    primary_care = ""
    internal_medicine_comments = ""
    primary_care_comments = ""
    summarized_info = ""

    if request.method == 'POST':
        internal_medicine = request.form['internal_medicine']
        primary_care = request.form['primary_care']
        internal_medicine_comments = request.form.get('internal_medicine_comments', '')
        primary_care_comments = request.form.get('primary_care_comments', '')

        combined_text = " ".join([internal_medicine, primary_care, internal_medicine_comments, primary_care_comments])

        # Summarize the text
        summarized_info = summarizer(combined_text,
                                     max_length=100,
                                     min_length=30,
                                     do_sample=False)[0]['summary_text']

    return render_template("MediSumHome_1.html",
                           internal_medicine=internal_medicine,
                           primary_care=primary_care,
                           internal_medicine_comments=internal_medicine_comments,
                           primary_care_comments=primary_care_comments,
                           summarized_info=summarized_info)

def open_browser():
    time.sleep(2)  # Delay to ensure the server starts
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    port = 5000
    url = f"http://127.0.0.1:{port}"
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port=port, debug=False)
