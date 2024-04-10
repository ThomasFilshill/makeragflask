import pdfminer.high_level
import markdown
from config import Config
import os

class PdfToMD():

    pdf_path = Config.PDF_ROOT
    markdown_path = Config.MARKDOWN_ROOT

    def convertPDFtoMD(self, fileName):
        mdname = fileName.replace("pdf", "md")

        with open(f"{self.pdf_path}/{fileName}", "rb") as f:
            text = pdfminer.high_level.extract_text(f)
        markdown_text = markdown.markdown(text)

        with open(f"{self.markdown_path}/{mdname}", 'w') as f:
            f.write(markdown_text)
        
    def convertAllPDFtoMD(self):
        '''Converts all pdfs into markdown'''
        dir_list = os.listdir(self.pdf_path)
        for file in dir_list:
            self.convertPDFtoMD(file)
