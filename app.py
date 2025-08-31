\
import streamlit as st
from extract import extract_text_from_pdf, extract_text_from_image
from summarizer import summarize_text, get_key_points

# ============ Basic Page Config ============
st.set_page_config(page_title="Document Summary Assistant", page_icon="📝", layout="centered")

# ============ Header ============
st.title("📝 Document Summary Assistant")
st.caption("Upload a PDF or Image to get a smart summary. (Simple demo app)")

# ============ Sidebar Options ============
st.sidebar.header("Summary Options")
length_choice = st.sidebar.selectbox(
    "Summary length",
    options=["Short", "Medium", "Long"],
    help="Choose how detailed you want the summary to be."
)

length_map = {
    "Short": (60, 120),
    "Medium": (120, 200),
    "Long": (200, 280)
}

max_summary_tokens = length_map[length_choice]

# ============ File Uploader ============
uploaded_file = st.file_uploader(
    "Drag and drop or choose a PDF/Image file",
    type=["pdf", "png", "jpg", "jpeg", "webp"],
    help="For images, OCR (pytesseract) is used. For PDFs, text is extracted via PyPDF2."
)

process = st.button("Generate Summary")

def _extract_text(file):
    if file is None:
        return None, "Please upload a file."
    name = (file.name or "").lower()
    try:
        if name.endswith(".pdf"):
            return extract_text_from_pdf(file), None
        elif name.endswith((".png", ".jpg", ".jpeg", ".webp")):
            return extract_text_from_image(file), None
        else:
            return None, "Unsupported file format."
    except Exception as e:
        return None, f"Error while extracting text: {e}"

# ============ Main Logic ============
if process:
    with st.spinner("Processing your document..."):
        text, err = _extract_text(uploaded_file)
        if err:
            st.error(err)
        elif not text or len(text.strip()) == 0:
            st.warning("No text found. If this is a scanned PDF, this simple demo only OCRs image files.")
        else:
            # Show a preview of the extracted text
            with st.expander("Preview Extracted Text"):
                st.write(text[:2000] + ("..." if len(text) > 2000 else ""))

            # Summarize
            summary = summarize_text(text, max_tokens=max_summary_tokens[1])
            st.subheader("Summary")
            st.write(summary)

            # Key points
            st.subheader("Key Points")
            bullets = get_key_points(summary, max_points=6)
            for b in bullets:
                st.markdown(f"- {b}")

# ============ Footer ============
with st.expander("About this demo"):
    st.markdown(
        """
        **Tech:** Streamlit, PyPDF2 (PDF text), pytesseract+Pillow (image OCR), optional Transformers for abstractive summary.
        
        **Notes:** This is intentionally simple. Scanned PDFs are not OCR'd in this minimal build. 
        For OCR on scanned PDFs, you can add `pdf2image` + `poppler` or use an API.
        """
    )
