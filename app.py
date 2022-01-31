from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>" #This would be afterwards  replaced by an HTML file.
