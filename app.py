from flask import Flask, render_template_string, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Load configuration from Docker Environment Variables
DB_PATH = os.environ.get("DB_PATH", "/app/data/notes.db")
APP_ENV = os.environ.get("APP_ENV", "Docker-Container")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
    conn.commit()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dockerized Notes App</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        input[type="text"] { width: 70%; padding: 10px; }
        button { padding: 10px 15px; background: #0db7ed; color: white; border: none; cursor: pointer; }
        ul { list-style: none; padding: 0; }
        li { background: #f4f4f4; margin: 5px 0; padding: 10px; border-radius: 4px; }
    </style>
</head>
<body>
    <h2>Dockerized Web App ({{ env }})</h2>
    <form method="POST" action="/add">
        <input type="text" name="content" placeholder="Enter a note..." required>
        <button type="submit">Save Note</button>
    </form>
    <ul>
        {% for note in notes %}
            <li>{{ note[1] }}</li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, notes=notes, env=APP_ENV)

@app.route('/add', methods=['POST'])
def add_note():
    content = request.form.get('content')
    if content:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        conn.commit()
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
