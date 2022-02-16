from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html') #now, when entering 127.0.0.0:5000/, the file index.html will pop up in the browser.

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@app.route("/team")
def team():
    return render_template('team.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

#These URLs above will be later on substituted by the sections specified
#in the document.







            #This is a test comment.