import pdfminer.high_level
from qdrant.config import Config
import os
import json

class PDFMethods():

    pdf_path = Config.PDF_ROOT
    markdown_path = Config.MARKDOWN_ROOT
    json_path = Config.JSON_ROOT

    def convertPDFtoText(self, fileName):
        with open(f"{self.pdf_path}/{fileName}", "rb") as f:
            text = pdfminer.high_level.extract_text(f)
            text = text.replace('\n', ' ')

            return text
        
    def convertAllPDFtoText(self):
        result = ''

        dir_list = os.listdir(self.pdf_path)
        for file in dir_list:
            text = self.convertPDFtoText(file)
            result += text

        return result

    def convertPDFtoJSON(self):
        '''Converts all pdfs into a single json containing them all'''
        files = []
        dir_list = os.listdir(self.pdf_path)
        for file in dir_list:
            text = self.convertPDFtoText(file)
            result = {
                "filename":file,
                "contents":text
            }
            files.append(result)
  
        with open(f"{self.json_path}/documentCollection.json", "w") as f:
            f.write(json.dumps(result))

