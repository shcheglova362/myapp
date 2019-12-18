from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def instruction():
    return render_template('index.html')


@app.route("/questionnaire")
def quest():
    return render_template('questions.html')


if __name__ == "__main__":
    app.run()
