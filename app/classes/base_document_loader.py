from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

import os

class BaseDocumentLoader:
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_MAX_TOKENS = 500
    DEFAULT_TEMPERATURE = 0.1

    @staticmethod
    def get_result_from_response(response=None):
        return response['result'] if response else "Error"

    def openai_key_environ(self):
        os.environ["OPENAI_API_KEY"] = os.getenv('openai_api_key')
    
    def text_splitter(self, chunk_size=1000, documents=None):
        text = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        return text.split_documents(documents)
    
    def get_vectordb_retriever(self, documents=None):
        persist_directory = 'db'
        embedding = OpenAIEmbeddings()

        vectordb = Chroma.from_documents(
            documents=documents,
            embedding=embedding,
            persist_directory=persist_directory
        )
        
        retriever = vectordb.as_retriever()
        return retriever