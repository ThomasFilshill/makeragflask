import argparse
from dataclasses import dataclass
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from config import Config

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

chroma_path = Config.CHROMA_PATH
template = Config.PROMPT_TEMPLATE

def query(query_text):
    results = searchdb(query_text)

    # if len(results) == 0 or results[0][1] < 0.7:
    #     print(f"Unable to find matching results.")
    #     return
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI()
    response_text = model.invoke(prompt).content
    

    return(response_text)


def searchdb(query_text):
    '''Searches the db for the k most relevant chunks'''
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    return results