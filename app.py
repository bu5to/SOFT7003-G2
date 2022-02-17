from flask import Flask, render_template, make_response, send_from_directory

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

@app.route('/sw.js')
def sw():
    response=make_response(
                     send_from_directory('static',path='sw.js'))
    #change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response
#These URLs above will be later on substituted by the sections specified
#in the document.







            #This is a test comment.