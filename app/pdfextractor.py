from pypdf import PdfReader

def text_extractor(filepath):
    pdf_file = PdfReader(filepath)
    content = ''
    for page in pdf_file.pages:
        content += (page.extract_text() or "")+'\n'
    return content