import os
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ChatVectorDBChain
from langchain.llms import OpenAI
import os
import discord
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
load_dotenv()

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

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True    
    client = discord.Client(intents=intents)
    doc_bot = DocBot()

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        print(message.channel.id)
        if message.author == client.user:
            return
        if message.channel.name == 'knapsack-docs':
            answer = doc_bot.chat(message.content)
            await message.channel.send(f'{answer[1]} Source: {answer[0].metadata["source"]}')
    client.run(os.getenv('DISCORD_TOKEN'))