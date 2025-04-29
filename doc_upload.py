import sqlite3
import os
import openai
from flask import Flask, request, render_template_string

#setup
app = Flask(__name__)
DATABASE = 'documents.db'
openai.api_key = os.getenv() # add your key

# create table in the DB if it doesnt already exist
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                     filename TEXT NOT NULL,
                     content BLOB NOT NULL,
                     grade TEXT
                     );
                ''')
        
init_db()

# HTML form + table template
UPLOAD_FORM = '''
<!doctype html>
<title>Upload & Grade Documents</title>
<h1>Upload a Document</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=document required>
  <input type=submit value=Upload>
</form>

{% if documents %}
<h2>Uploaded Documents</h2>
<table border=1 cellpadding=5>
    <tr><th>ID</th><th>Filename</th><th>Grade</th></tr>
    {% for doc in documents %}
        <tr>
          <td>{{ doc[0] }}</td>
          <td>{{ doc[1] }}</td>
          <td>{{ doc[2] or '—' }}</td>
        </tr>
    {% endfor %}
</table>
{% endif %}
'''


# ChatGPT Grading
def grade_text(text: str) -> str:
    """
    Sends `text` to ChatGPT and returns one of: A, B, C, D, F.
    """
    prompt = (
        "You are an expert grader. "
        "Read the student document below and assign a single letter grade (A, B, C, D, or F) "
        "based on clarity, completeness, and correctness. "
        "Respond with JUST the letter grade.\n\n"
        f"--- DOCUMENT START ---\n{text}\n--- DOCUMENT END ---"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=5,
    )
    grade = resp.choices[0].message.content.strip().upper()
    if grade and grade[0] in {"A","B","C","D","F"}:
        return grade[0]
    return "F"

@app.route('/', methods=['GET', 'POST'])
def upload_and_grade():
    if request.method == 'POST':
        file = request.files['document']
        if file:
            content = file.read()
            filename = file.filename

            # Grade via ChatGPT
            text = content.decode('utf-8', errors='ignore')
            grade = grade_text(text)

            with sqlite3.connect(DATABASE) as conn:
                conn.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (filename, content, grade))
                conn.commit()

     # Retrieve list of documents
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute("SELECT id, filename, grade FROM documents")
        documents = cursor.fetchall()

    return render_template_string(UPLOAD_FORM, documents=documents)

if __name__ == '__main__':
    app.run(debug=True)
