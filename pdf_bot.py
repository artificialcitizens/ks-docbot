from langchain.document_loaders import PagedPDFSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

import os
import discord
from dotenv import load_dotenv
from typing import Tuple

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ChatVectorDBChain
from langchain.llms import OpenAI

from doc_bot import DocBot

from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class PDFBot:
    def __init__(self, pdf_directory: str):
        self.chat_history = []

        loader = PagedPDFSplitter(pdf_directory)
        pages = loader.load_and_split()
        faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
        self.qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0), faiss_index, return_source_documents=True)

    def pdf_chat(self, question: str) -> Tuple[str, str]:
        result = self.qa({"question": question, "chat_history": self.chat_history})
        self.chat_history.append((question, result["answer"]))
        if len(self.chat_history) > 5:
            self.chat_history.pop(0)
        return (result['source_documents'][0], result["answer"])


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True    
    client = discord.Client(intents=intents)
    bitd_bot = PDFBot('./pdfs/blades_in_the_dark.pdf')
    doc_bot = DocBot()

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        print(message.channel.id)
        if message.author == client.user:
            return
        if message.channel.name == 'blades-in-the-dark':
            answer = bitd_bot.pdf_chat(message.content)
            print(answer[0].metadata['page'])
            await message.channel.send(f'{answer[1]} (Page: {answer[0].metadata["page"] + 1})')
        if message.channel.name == 'knapsack-docs':
            answer = doc_bot.chat(message.content)
            await message.channel.send(f'{answer[1]} Source: {answer[0].metadata["source"]}')
    client.run(os.getenv('DISCORD_TOKEN'))