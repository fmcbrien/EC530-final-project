# EC530-final-project Document Organizer for Teachers

This is a simple Flask web application that allows users to:

- Upload documents through a web interface.
- Store them in a SQLite database.
- Automatically grade them using OpenAI's ChatGPT (A, B, C, D, or F).
- View the list of uploaded documents with their assigned grades.

---

## 🚀 Features

- 📁 Upload any text-based file (e.g., `.txt`, `.md`, `.pdf` with UTF-8 content).
- 🤖 Automatic grading via ChatGPT using OpenAI's API.
- 💾 Persistent storage with SQLite.
- 📊 Live table showing filenames and grades.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/document-grader.git
cd document-grader
```

### 2. Install Dependencies

```bash
pip install flask openai
```

### 3. Set OpenAI API Key

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

On Windows (CMD):

```cmd
set OPENAI_API_KEY=your-api-key-here
```

### 4. Run the App

```bash
python upload_store.py
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

## 🧠 How Grading Works

Upon upload, the app sends your document text to OpenAI's ChatGPT with a prompt asking it to assign a single letter grade (A–F) based on:

- Clarity
- Completeness
- Correctness

The grade is stored alongside the document in the database and displayed in the UI.

---

## 🛠 Customization Ideas

- 🔍 Add document previews or download links.
- ⏳ Queue longer grading tasks for background processing.
- 🧾 Store grading feedback, not just the grade.
- 🔐 Add user authentication or file size limits.

---
