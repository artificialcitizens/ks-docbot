import os
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ChatVectorDBChain
from langchain.llms import OpenAI
from flask import Flask, request

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

class DocBot:
    def __init__(self):
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        loader = DirectoryLoader('./knapsack', glob="**/*.txt")
        docs = loader.load()
        for i, d in enumerate(docs):
            newRl = self.convert_url(d.metadata['source'])
            d.metadata["source"] = newRl
            d.page_content = f'{d.page_content}{newRl}'
        text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
        self.documents = text_splitter.split_documents(docs)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma.from_documents(self.documents, self.embeddings)
        self.qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0), self.vectorstore, return_source_documents=True)
        self.chat_history = []

    def convert_url(self, input_str):
        components = input_str.split("/")
        article = components[-1].split(".")[0]
        output_url = f"https://help.knapsack.cloud/article/{article}"
        return output_url

    def chat(self, question):
        result = self.qa({"question": question, "chat_history": self.chat_history})
        self.chat_history.append((question, result["answer"]))
        if len(self.chat_history) > 5:
            self.chat_history.pop(0)
        return (result['source_documents'][0], result["answer"])

app = Flask(__name__)
doc_bot = DocBot()

@app.route("/chat", methods=["POST"])
def chat():
    question = request.json["question"]
    answer = doc_bot.chat(question)
    return {
        "answer": answer[1],
        "source_document": answer[0].metadata["source"]
    }

if __name__ == "__main__":
    app.run()