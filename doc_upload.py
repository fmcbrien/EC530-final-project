import sqlite3
from flask import Flask, request, redirect, url_for, render_template_string

#setup
app = Flask(__name__)
DATABASE = 'documents.db'

# create table in the DB if it doesnt already exist
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                     filename TEXT NOT NULL,
                     content BLOB NOT NULL
                     );
                ''')
        
init_db()

# HTML form + table template
UPLOAD_FORM = '''
<!doctype html>
<title>Upload Document</title>
<h1>Upload a Document</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=document required>
  <input type=submit value=Upload>
</form>

{% if documents %}
<h2>Uploaded Documents</h2>
<table border=1 cellpadding=5>
    <tr><th>ID</th><th>Filename</th></tr>
    {% for doc in documents %}
        <tr><td>{{ doc[0] }}</td><td>{{ doc[1] }}</td></tr>
    {% endfor %}
</table>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['document']
        if file:
            content = file.read()
            filename = file.filename

            with sqlite3.connect(DATABASE) as conn:
                conn.execute("INSERT INTO documents (filename, content) VALUES (?, ?)", (filename, content))
                conn.commit()

     # Retrieve list of documents
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute("SELECT id, filename FROM documents")
        documents = cursor.fetchall()

    return render_template_string(UPLOAD_FORM, documents=documents)

if __name__ == '__main__':
    app.run(debug=True)