from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/shower')
def shower():
    return render_template('shower.html') 

@app.route('/environmental')
def environmental():
    return render_template('environmental.html') 

@app.route('/office')
def office():
    return render_template('office.html') 

if __name__ == '__main__':
    app.run(debug=True)