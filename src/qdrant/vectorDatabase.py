from qdrant_client import QdrantClient
from qdrant.userDataMethods import PDFMethods
from qdrant.config import Config

class VectorDatabase():
    '''
    This class contains 2 fundamental methods:
    1. createDatabase: 
        - Takes in the user's ID and uses the pdf files in data/pdf to create a qdrant vector database
        #TODO Get the files directly from that user's S3 bucket
    2. searchDatabase:
        - Gets the k most relevant chunks from the qdrant database based on the user's query 
    '''

    markdown_path = Config.MARKDOWN_ROOT
    chunk_size = Config.CHUNK_SIZE
    client = QdrantClient(host='localhost', port=6333)

    client.set_model("sentence-transformers/all-MiniLM-L6-v2")
    

    def createDatabase(self, user_id):
        '''handles the process of creating the database'''
        client = self.client

        client.recreate_collection( # Recreates even if it already exists, good for remaking it when user uploads new docs.
            collection_name=user_id, 
            vectors_config=client.get_fastembed_vector_params(),
        )

        pdm = PDFMethods()
        texts = pdm.convertAllPDFtoText()
        split_texts = self.split_text(texts, self.chunk_size)

        self.embed(client, split_texts, user_id)


    def split_text(self, text, chunk_size):
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    
    def embed(self, client, docs, user_id):
        client.add(
            collection_name=user_id,
            documents=docs
        )

    def searchDatabase(self, user_id, query_text):
        client = self.client
        
        return client.query(
            collection_name=user_id,
            query_text=query_text,
            limit=3
        )


# c = VectorDatabase()
# c.createDatabase("dweidiwnpionq")
# top3 = c.searchDatabase("dweidiwnpionq", "What happened to Thomas")
# print(top3)

