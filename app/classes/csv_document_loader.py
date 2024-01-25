from langchain_community.document_loaders.csv_loader import CSVLoader
from app.classes.base_document_loader import BaseDocumentLoader
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

class CsvDocumentLoader(BaseDocumentLoader):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        load_dotenv()

    def load_document(self):
        loader = CSVLoader(file_path=self.file_path)
        return loader.load()

    def make_query(self, documents=None, question=None):
        try:
            self.openai_key_environ()

            qa_chain = RetrievalQA.from_chain_type(
                llm=OpenAI(),
                chain_type="stuff",
                retriever=self.get_vectordb_retriever(documents=documents),
                return_source_documents=True,
                input_key="question"
            )

            llm_return_object = qa_chain({"question": question})
            json_response = self.build_json_response(llm_return_object)

            return json_response

        except Exception as e:
            return {"error": str(e)}

    def build_json_response(self, llm_return_object):
        response = {}
        response['query'] = llm_return_object['question']
        response['result'] = llm_return_object['result']

        source_doc = llm_return_object['source_documents'][0]
        response['page_content'] = source_doc.page_content
        response['row'] = source_doc.metadata.get('row', None)
        response['source'] = source_doc.metadata.get('source', None)

        return response