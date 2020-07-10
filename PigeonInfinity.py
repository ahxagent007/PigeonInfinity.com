
from flask import Flask, render_template, request, flash, url_for, jsonify, session, redirect

app = Flask(__name__)
app.secret_key = 'SECRETKEYXIAN'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Login')
def login():
    return render_template('login.html')

@app.route('/Registration')
def registration():
    return render_template('register.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
