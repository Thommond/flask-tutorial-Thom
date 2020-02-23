from flask import Flask  # test file for server

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, does this work?'
