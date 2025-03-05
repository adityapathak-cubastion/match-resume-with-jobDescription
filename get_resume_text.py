"""
this script defines a function that:
- extracts text from all 'resumes' in a given directory,
- returns a list of all texts and their names.
"""

import fitz, os, re

def get_text_from_pdf(pdf_path): 
    doc = fitz.open(pdf_path)
    text = ""
    
    for page in doc: text += page.get_text()

    text = re.sub(r"Confidential", "", text) # removing the word 'Confidential' from the text
    return text

def get_all_texts(dir_path, all_texts, all_docs_name):
    print(f"message : extracting text from all resumes...\n")

    for document in os.listdir(dir_path):
        pdf_path = os.path.join(dir_path, document)
        pdf_text = ""
        pdf_text += get_text_from_pdf(pdf_path)
        all_texts.append(pdf_text)
        all_docs_name.append(str(os.path.basename(pdf_path)))

    print("message : text from all resumes extracted successfully!\n")

    return all_texts, all_docs_name