'''
Created on Mar 24, 2020

@author: Haniel Wang
'''
from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')   
def index():
    return '<h1>Hi !</h1>'

@app.route('/hello')   
def hello():
    return render_template('hello.html')

if __name__ == "__main__":
    app.run(debug = True)

