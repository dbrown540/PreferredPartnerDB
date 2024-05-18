import os
import spacy
from PyPDF2 import PdfReader  #pylint disable=import-error

class DocumentParser:
    def __init__(self) -> None:
        self.filepath = None
    
    def parse_document(self, filepath):
        self.filepath = filepath
        ext = os.path.splitext(filepath)[1]
        if ext == '.pdf':
            self._parse_pdf()
        elif ext == '.docx':
            self._parse_word()
        else:
            raise ValueError("Invalid filetype")

    def _parse_pdf(self):
        pdf_parser = PDFParser(filepath=self.filepath)
        text = pdf_parser.extract_text()
        pdf_parser.extract_desired_skills(text)

    def _parse_word(self):
        pass

class PDFParser:
    def __init__(self, filepath) -> None:
        self.filepath = filepath

    def _parse_pdf(self):
        pass

    def extract_text(self):
        text = ""
        with open(self.filepath, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    
    def extract_desired_skills(self, job_description):
        # Load the English language model
        nlp = spacy.load("en_core_web_sm")

        # Process the job description text
        doc = nlp(job_description)

        for token in doc:
            print(token.text, token.pos_, token.dep_, token.head.text)