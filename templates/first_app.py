from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def main_page():
    return f"<p>Hello, world</p>"


if __name__ == '__main__':
    app.run(debug=True)
