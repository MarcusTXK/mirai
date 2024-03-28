from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever

from assistant_module.speech_streamer import SpeechStreamer

class State(BaseModel):
    light: int = Field(description="1 for on, 0 for off", ge=0, le=1)
    msg: str = Field(description="Response to the user's commands")

class ChatHandler:
    def __init__(self):
        self.llm = Ollama(model="mistral-openorca:7b-q5_K_M")
        self.history=[]


    def send_chat(self, user_input):

        # embeddings = OllamaEmbeddings(model="mistral-openorca:7b-q5_K_M")
        # documents = [Document(page_content="langsmith can let you visualize test results")]
        # vectorDb = FAISS.from_documents(documents, embeddings)

        # retriever = vectorDb.as_retriever()
        output_parser = StrOutputParser()

        # prompt = ChatPromptTemplate.from_messages([
        #     ("system", "You are mirai, a helpful home assistant. Write out your reasoning step-by-step to be sure you get the right answers! Answer the user's questions based on the below context:\n\n"),
        #     MessagesPlaceholder(variable_name="chat_history"),
        #     ("user", "{input}"),
        # ])
        # history_retriever_chain = create_history_aware_retriever(self.llm, retriever, prompt)

        # # document_chain = create_stuff_documents_chain(self.llm, prompt)

        # # retrieval_chain = create_retrieval_chain(history_retriever_chain, document_chain) | output_parser
        
        # # output = retrieval_chain.invoke({"input": user_input, "chat_history": self.history})
        # output = history_retriever_chain.invoke({"input": user_input, "chat_history": self.history}) | output_parser

        # self.history.append(("user", user_input))
        # self.history.append(("assistant", output))
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful home assistant. Think before writing and output the response you would like to speak to the user."),
            ("user", "{input}")
        ])
        chain = prompt | self.llm
        output = ""
        streamer = SpeechStreamer()
        for chunk in chain.stream({"input": user_input}):
            streamer.process_and_speak(chunk)
            output += chunk 
            
        streamer.flush_and_speak()
        streamer.stop()
        return output
    

        

