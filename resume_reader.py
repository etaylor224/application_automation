from docx import Document

def resume_parser(resume):
    if resume.endswith(".docx"):
        doc_paragraphs = list()

        with open(resume, 'rb') as file:
            doc = Document(file)
            for para in doc.paragraphs:
                if para.text != "":
                    doc_paragraphs.append(para.text)
        return doc_paragraphs
    elif resume.endswith(".txt"):
        with open(resume, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported resume format. Use .docx or .txt")
