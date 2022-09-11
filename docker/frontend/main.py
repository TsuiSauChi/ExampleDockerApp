import requests
from flask import Flask, render_template

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def home():
    x = requests.get('http://backend:5000/api/')
    return render_template('example.html', data = x.json()['data'])