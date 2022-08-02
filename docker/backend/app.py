from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

@app.route("/api/")
def hello_world():
    return jsonify({
        "data": "Hello World"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)