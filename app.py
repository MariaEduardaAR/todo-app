from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )


@app.route("/")
def home():
    return "Minha lista de tarefas"


@app.route("/tasks")
def tasks():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, name TEXT)"
    )

    cur.execute(
        "SELECT id,name FROM tasks"
    )

    data = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(data)


@app.route("/tasks", methods=["POST"])
def add_task():

    task = request.json["name"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks(name) VALUES(%s)",
        (task,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)