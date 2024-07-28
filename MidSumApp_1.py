import webbrowser
import time
from threading import Timer
from flask import Flask, render_template_string, request
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)

# Initialize the summarization pipeline with a lighter instruct model
model_name = "sshleifer/distilbart-cnn-6-6"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Plastic Surgery Information Summarization</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #007BFF;
        }
        textarea {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            font-size: 18px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        h2 {
            margin-top: 30px;
        }
        p {
            padding: 10px;
            background-color: #f1f1f1;
            border-radius: 4px;
        }
        .two-column {
            display: flex;
            flex-wrap: wrap;
        }
        .two-column .form-group {
            flex: 1 1 calc(50% - 10px);
            margin: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Plastic Surgery Information Summarization</h1>
        <form method="post">
            <div class="two-column">
                <div class="form-group">
                    <label for="internal_medicine">Enter Internal Medicine report:</label>
                    <textarea id="internal_medicine" name="internal_medicine" rows="3">{{ internal_medicine }}</textarea>
                </div>
                <div class="form-group">
                    <label for="primary_care">Enter Primary Care report:</label>
                    <textarea id="primary_care" name="primary_care" rows="3">{{ primary_care }}</textarea>
                </div>
                <div class="form-group">
                    <label for="gi">Enter Gastroenterology (GI) report:</label>
                    <textarea id="gi" name="gi" rows="3">{{ gi }}</textarea>
                </div>
            </div>
            <button type="submit">Summarize Plastic Surgery Information</button>
        </form>
        {% if summarized_info %}
            <h2>Summarized Plastic Surgery Information:</h2>
            <p>{{ summarized_info }}</p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize the variables to hold the form data
    internal_medicine = ""
    primary_care = ""
    gi = ""

    summarized_info = ""
    if request.method == 'POST':
        internal_medicine = request.form['internal_medicine']
        primary_care = request.form['primary_care']
        gi = request.form['gi']

        combined_text = " ".join([internal_medicine, primary_care, gi])

        prompt = f"Summarize the plastic surgery information from the following text: {combined_text}"

        # Run the summarization
        summarized_info = summarizer(prompt,
                                     max_length=100,
                                     min_length=30,
                                     do_sample=False)[0]['summary_text']

    return render_template_string(html_template,
                                  internal_medicine=internal_medicine,
                                  primary_care=primary_care,
                                  gi=gi,
                                  summarized_info=summarized_info)


def open_browser():
    time.sleep(2)  # Delay to ensure the server starts
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == '__main__':
    Timer(1, open_browser).start()  # Open the browser after 1 second
    app.run(debug=True)
