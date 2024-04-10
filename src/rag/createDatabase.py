from pdftomd import PdfToMD
from config import Config
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import shutil
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

class CreateDatabase():
    '''handles the creation of the vector database'''
    markdown_path = Config.MARKDOWN_ROOT
    chroma_path = Config.CHROMA_PATH
    

    def createDatabase(self):
        '''handles the process of creating the database'''
        self.convertAllToMarkdown() # First we must convert all data formats into markdown
        documents = self.loadDocuments()
        chunks = self.splitText(documents)
        self.saveToChroma(chunks)


    def convertAllToMarkdown(self):
        '''Converts all of the data in the data folder into a markdown'''
        pdftomd = PdfToMD()
        pdftomd.convertAllPDFtoMD()

    def loadDocuments(self):
        '''loads markdown documents from markdown folder in data'''
        loader = DirectoryLoader(self.markdown_path, glob="*.md")
        documents=loader.load()

        return documents
    
    def splitText(self, documents: list[Document]):
        '''Splits the text of the documents into chunks'''
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

        return chunks
    
    def saveToChroma(self, chunks: list[Document]):
        # Clear out the database first.
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)
        
        # Create a new DB from the documents.
        db = Chroma.from_documents(
            chunks, OpenAIEmbeddings(), persist_directory=self.chroma_path
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {self.chroma_path}.")



c = CreateDatabase()
c.createDatabase()