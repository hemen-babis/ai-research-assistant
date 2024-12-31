from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF for PDF parsing
import pdfkit  # For exporting chat history
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['HISTORY_FOLDER'] = 'history'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['HISTORY_FOLDER'], exist_ok=True)

# Initialize OpenAI API
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    model="gpt-4-turbo",  # Larger context size
    temperature=0.3,
    api_key=api_key
)

# Prompts
summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following text into key points:\n\n{text}"
)

chat_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="Based on the following text:\n\n{context}\n\nAnswer the question:\n{question}"
)


@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    chat_history = []
    pdf_name = None

    # Load existing data if available
    if os.path.exists("current_session.json"):
        with open("current_session.json", "r") as f:
            session_data = json.load(f)
            pdf_name = session_data.get("pdf_name")
            summary = session_data.get("summary", "")
            chat_history = session_data.get("chat_history", [])

    if request.method == "POST":
        # Handle File Upload
        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            pdf_name = file.filename

            # Process PDF
            text = extract_text_from_pdf(filepath)
            summary = summarize_text(text)

            # Save summary and chat history
            save_to_history(pdf_name, summary, [])

            # Save to current session
            with open("current_session.json", "w") as f:
                json.dump({"pdf_name": pdf_name, "summary": summary, "chat_history": []}, f)

    return render_template("index.html", summary=summary, chat_history=chat_history, pdf_name=pdf_name)


def extract_text_from_pdf(filepath):
    """Extract text from PDF page-by-page."""
    text_chunks = []
    with fitz.open(filepath) as doc:
        for page in doc:
            text = page.get_text()
            text_chunks.append(text)
    return "\n\n".join(text_chunks)


def summarize_text(text):
    """Summarize the extracted text."""
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    summaries = []
    for chunk in chunks:
        chain = summary_prompt | llm
        response = chain.invoke({"text": chunk})
        summaries.append(response.content if hasattr(response, "content") else str(response))

    return "\n\n".join(summaries)

@app.route("/download-summary", methods=["POST"])
def download_summary():
    """Download the summary as a PDF."""
    data = request.json
    summary = data.get("summary", "")

    if not summary:
        return "No summary available!", 400

    # Save summary as HTML first
    summary_html = f"<h1>Summary</h1><pre>{summary}</pre>"
    temp_html = "summary.html"

    with open(temp_html, "w") as file:
        file.write(summary_html)

    # Convert HTML to PDF
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], "summary.pdf")
    pdfkit.from_file(temp_html, pdf_path)

    return send_file(pdf_path, as_attachment=True)

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat questions."""
    data = request.json
    question = data.get("question")

    # Load current session
    with open("current_session.json", "r") as f:
        session_data = json.load(f)
        summary = session_data.get("summary", "")
        pdf_name = session_data.get("pdf_name")
        chat_history = session_data.get("chat_history", [])

    # Process query
    chain = chat_prompt | llm
    response = chain.invoke({"context": summary, "question": question})
    answer = response.content if hasattr(response, "content") else str(response)

    # Save question-answer pair
    chat_history.append({"question": question, "answer": answer})

    # Update session
    session_data["chat_history"] = chat_history
    with open("current_session.json", "w") as f:
        json.dump(session_data, f)

    # Save to history folder
    save_to_history(pdf_name, summary, chat_history)

    return jsonify({"response": answer, "history": chat_history})


@app.route("/history")
def history():
    """Display history of uploaded PDFs."""
    files = os.listdir(app.config['HISTORY_FOLDER'])
    pdfs = [f.replace(".json", "") for f in files]
    return render_template("history.html", pdfs=pdfs)


@app.route("/history/<pdf_name>")
def view_history(pdf_name):
    """View history for a specific PDF."""
    filepath = os.path.join(app.config['HISTORY_FOLDER'], f"{pdf_name}.json")
    with open(filepath, "r") as f:
        data = json.load(f)
    return render_template("view_history.html", pdf_name=pdf_name, summary=data["summary"], chat_history=data["chat_history"])


def save_to_history(pdf_name, summary, chat_history):
    """Save summary and chat history to history folder."""
    filepath = os.path.join(app.config['HISTORY_FOLDER'], f"{pdf_name}.json")
    with open(filepath, "w") as f:
        json.dump({"summary": summary, "chat_history": chat_history}, f)


if __name__ == "__main__":
    app.run(debug=True)
