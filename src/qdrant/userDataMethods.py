import pdfminer.high_level
from qdrant.config import Config
import os
import json
from dotenv import load_dotenv
from io import BytesIO
import boto3
from PyPDF2 import PdfReader

load_dotenv()

class PDFMethods():

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')

    pdf_path = Config.PDF_ROOT
    markdown_path = Config.MARKDOWN_ROOT
    json_path = Config.JSON_ROOT

    def convertPDFtoText(self, fileName):
        with open(f"{self.pdf_path}/{fileName}", "rb") as f:
            text = pdfminer.high_level.extract_text(f)
            text = text.replace('\n', ' ')

            return text
        
    def convertAllPDFtoText(self):
        '''Converts all fo that user's pdf files into one big text'''
        
        result = ''

        dir_list = os.listdir(self.pdf_path)
        for file in dir_list:
            text = self.convertPDFtoText(file)
            result += text

        return result
    
    def convertAllBucketPDFtoText(self, file_ids):
        '''Converts all of a user's pdf files into one big text'''
        result = ''
        for file_id in file_ids:
            result += self.convertBucketPDFtoText(file_id)

        return result
        

    def convertBucketPDFtoText(self, file_id):
        bucket_name = 'makerag'
        s3 = boto3.client('s3', 
        aws_access_key_id=self.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY)

        obj = s3.get_object(Bucket=bucket_name, Key=file_id)
        pdf_file=obj['Body'].read()

        return self.convertPDFtoText(pdf_file)
        
    
    def convertPDFtoText(self, pdf_file):
        reader = PdfReader(BytesIO(pdf_file))

        whole_text = ''
        for page in reader.pages:
            whole_text+=page.extract_text()

        return whole_text


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

