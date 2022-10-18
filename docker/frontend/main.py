import requests
from flask import Flask, render_template
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

host = os.getenv('BACKEND_ADDRESS')
port = os.getenv('BACKEND_PORT')

@app.route("/")
def home():
    print("Frontend Execute")
    x = requests.get(host + ":" + port)
    return render_template('example.html', data = x.text)