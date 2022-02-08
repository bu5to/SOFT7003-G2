from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html') #now, when entering 127.0.0.0:5000/, the file index.html will pop up in the browser.


#This is a test comment.