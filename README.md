\
# 📝 Document Summary Assistant (Minimal)

A super simple Streamlit app that:
- Uploads **PDF or Image** files
- Extracts text (PDF text via **PyPDF2**, image OCR via **pytesseract**)
- Generates a **summary** (short/medium/long)
- Shows **key points**

> This is intentionally minimal so it’s easy to read and extend. Plenty of comments included.

---

## 🚀 Quick Start (Local)

1. **Create and activate a virtual environment (recommended)**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

> For OCR: Install Tesseract on your OS:
> - Windows: https://github.com/UB-Mannheim/tesseract/wiki
> - macOS: `brew install tesseract`
> - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`

3. **Run the app**

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal.

---

## 🧠 Notes & Limitations

- **Scanned PDFs** are **not OCR'd** in this minimal build. Only image files are OCR’d.  
  - To OCR scanned PDFs, add `pdf2image` + Poppler and convert pages to images before OCR,
    or use a cloud OCR API.
- The app tries **Transformers** (abstractive) first. If unavailable, it uses a **simple extractive** fallback.
- This is a demo: simple error handling and loading states are included.

---

## 🏗️ Project Structure

```
.
├── app.py              # Streamlit UI + app logic
├── extract.py          # PDF & image text extraction helpers
├── summarizer.py       # Summarization (transformers + fallback)
├── requirements.txt
└── README.md
```

---

## 📦 Deploy (Free-tier friendly)
- **Streamlit Community Cloud**: Quick and easy for demos.
- **Render / Railway / Fly.io**: Works with a simple `pip install` + `streamlit run` command.
- **Vercel/Netlify/Heroku**: Prefer a static/frontend; for Python backend, use Render/Railway/Fly.

> Ensure the host has access to **Tesseract** binary if you need OCR.

---

## 📝 200-word Approach (Interview-ready)

I built a minimal **Document Summary Assistant** with a clean, commented codebase. The UI uses **Streamlit** for rapid, readable development. For PDFs, I extract text using **PyPDF2**; for images, I run OCR via **pytesseract** + **Pillow**. Summarization attempts an **abstractive** model with Hugging Face **Transformers** (`distilbart-cnn`), and gracefully falls back to a lightweight **extractive** summarizer based on word-frequency sentence scoring. This keeps the app functional even without GPU or heavy models. The UX is kept simple: upload → preview extracted text → choose summary length (short/medium/long) → summary + key points. I added basic error handling (unsupported formats, empty text) and a spinner for loading states. The design is deliberately minimal and mobile-friendly out of the box. For production, I’d add scanned PDF OCR via `pdf2image` + Poppler, background jobs for large docs, caching, and better testing. The code is organized into small modules (`extract.py`, `summarizer.py`) for clarity and testability.
