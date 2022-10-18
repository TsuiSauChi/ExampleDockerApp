import json
from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="example",
        host=os.getenv('DATABASE_ADDRESS')
    )
    return conn

@app.route('/')
def hello_geek():
    print("Backend Execute")
    conn = connection()
    cur = conn.cursor()

    cur.execute("select name from users")
    result = cur.fetchall()

    return json.dumps(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)