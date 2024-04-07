import pdfminer.high_level
import markdown
# from config import Config
import os

class PdfToMD():

    pdf_path = 'data/pdf'
    markdown_path = 'data/markdown'

    def convertPDFtoMD(self, fileName):

        with open(f"{self.pdf_path}/{fileName}", "rb") as f:
            text = pdfminer.high_level.extract_text(f)
        markdown_text = markdown.markdown(text)

        with open(f"{self.markdown_path}/{fileName}", 'w') as f:
            f.write(markdown_text)
        
    def convertAllPDFtoMD(self):
        '''Converts all pdfs into markdown'''
        dir_list = os.listdir(self.pdf_path)
        for file in dir_list:
            self.convertPDFtoMD(file)
