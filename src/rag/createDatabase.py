from pdftomd import PdfToMD
# from config import Config

class CreateDatabase():
    '''handles the creation of the vector database'''

    def createDatabase(self):
        '''handles the process of creating the database'''
        self.convertAllToMarkdown() # First we must convert all data formats into markdown


    def convertAllToMarkdown(self):
        '''Converts all of the data in the data folder into a markdown'''
        pdftomd = PdfToMD()
        pdftomd.convertAllPDFtoMD()

 


c = CreateDatabase()
c.createDatabase()