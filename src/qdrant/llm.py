from qdrant.config import Config
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class Query():
    openai_api_key = os.getenv('OPENAI_API_KEY')
    def query(self, query_text, context):
        
        context_text = "\n\n---\n\n".join([doc.metadata['document'] for doc in context])
        prompt_template = Config.PROMPT_TEMPLATE

        prompt = prompt_template.format(context=context_text, question=query_text)

        model = ChatOpenAI()
        response_text = model.invoke(prompt).content
        
        return(response_text)

