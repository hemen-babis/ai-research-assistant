# AI Research Assistant

## About
The **AI Research Assistant** is a powerful and intelligent tool designed to help researchers, students, and professionals streamline their workflow by summarizing PDFs, answering questions based on uploaded documents, and storing histories for future reference. This tool integrates AI capabilities to enhance productivity and provide insights from academic papers, reports, and articles.

---

## Features
### 1. PDF Upload and Analysis
- Upload research papers, reports, or articles in PDF format.
- AI reads and extracts relevant content from the document.

### 2. AI-Powered Summarization
- Generate concise and structured summaries of lengthy documents.
- Summaries update dynamically and save automatically.

### 3. Question Answering System
- Ask questions related to the uploaded PDF.
- AI responds contextually based on document content.

### 4. Downloadable Summaries
- Export summaries as PDF files for offline access.

### 5. Session History Management
- Saves uploaded files and interactions in session history.
- View and access previous uploads via a dedicated history page.

### 6. User-Friendly Interface
- Clean, responsive design for easy navigation.
- Real-time progress loading indicators.

---

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript (Bootstrap for styling)
- **Backend:** Python (Flask Framework)
- **AI/ML Libraries:** LangChain, OpenAI API
- **PDF Processing:** PyMuPDF (fitz)
- **Data Management:** JSON-based session storage
- **Export Tools:** PDFKit for summary downloads

---

## Installation
### Prerequisites
1. **Python 3.10+** installed on your machine.
2. **Pip** and **virtualenv** installed.

### Steps
1. Clone the Repository:
   ```bash
   git clone https://github.com/hemen-babis/ai-research-assistant.git
   cd ai-research-assistant
   ```

2. Create and Activate Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/MacOS
   .\venv\Scripts\activate   # Windows
   ```

3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install **wkhtmltopdf** for PDF export:
   - Windows: [Download Here](https://wkhtmltopdf.org/downloads.html)
   - MacOS: `brew install wkhtmltopdf`

5. Set Environment Variables:
   ```bash
   cp .env.example .env
   ```
   Update `.env` with your **OpenAI API Key**.

6. Run the Application:
   ```bash
   python app.py
   ```

7. Open the app in your browser:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage
1. Upload a PDF document using the file upload button.
2. The AI generates a summary and displays it in real-time.
3. Use the question box to ask document-specific questions.
4. Download summaries as PDFs for offline access.
5. Access your previous uploads and history through the **History Page**.

---

## File Structure
```
.
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore file
├── static/                 # CSS, JS, and images
├── templates/              # HTML templates
├── history.html            # Saved session data page
├── summary.html            # Summary display page
├── document_context.txt    # Temporary text storage
├── current_session.json    # Stores session data
└── README.md               # Documentation
```

---

## Screenshots
**Home Page**
![Home Page](screenshots/home.png)

**Summary Display**
![Summary Display](screenshots/summary.png)

**History Page**
![History Page](screenshots/history.png)

---

## Future Improvements
- Multi-document uploads for comparison.
- Integration with Google Scholar for citation management.
- Collaboration tools for research teams.
- Voice-enabled search and commands.

---

## Contributing
Contributions are welcome! If you have suggestions for improvements or encounter any issues, feel free to **open an issue** or submit a **pull request**.

---

## License
This project is licensed under the **MIT License**.

---

## Contact
- **Author:** Hemen Babis  
- **Email:** hemenbabis@gmail.com  
- **GitHub:** [Hemen Babis](https://github.com/hemen-babis)

