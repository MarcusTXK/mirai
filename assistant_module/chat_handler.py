from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from config import INDEX_PATH, MODEL_NAME
from flask_module.models import db, Chatlog
from assistant_module.speech_streamer import SpeechStreamer
from langchain_core.callbacks import StdOutCallbackHandler
import langchain 
langchain.debug = True 

class ChatHandler:
    MAX_HISTORY_SIZE = 2
    SYSTEM_MESSAGE = "You are a helpful home assistant. Think before writing and output the response you would like to speak to the user."
    IGNORE_CHUNK = {"<|im_end|>"}

    def __init__(self, app):

        handler = StdOutCallbackHandler()
        self.llm = Ollama(model=MODEL_NAME, verbose=True, callbacks=[handler])
        self.llm.verbose=True
        self.app = app
        self.history = self.load_recent_chats()

    def load_recent_chats(self):
        with self.app.app_context():
            # Fetch the 4 most recent chat logs from the database
            recent_chats = Chatlog.query.order_by(Chatlog.id.desc()).limit(self.MAX_HISTORY_SIZE).all()
            # Convert the chat logs into the desired format and reverse to start with the oldest
            history = [(chat.sentBy, chat.message) for chat in reversed(recent_chats)]
            return history

    def save_message(self, sentBy, message):
        with self.app.app_context():  # Ensures we're operating within the Flask app context
            new_message = Chatlog(sentBy=sentBy, message=message)
            db.session.add(new_message)
            db.session.commit()

    # Used on startup
    def send_initial_chat(self, user_input):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_MESSAGE),
            ("user", "{input}"),
        ])
        chain = prompt | self.llm
        output = ""
        streamer = SpeechStreamer()
        for chunk in chain.stream({"input": user_input}):
            if any(chunk.endswith(ignore) for ignore in self.IGNORE_CHUNK):
                continue
            streamer.process_and_speak(chunk)
            output += chunk 
            
        streamer.flush_and_speak()
        streamer.stop()
        return output

    def send_chat(self, user_input):

        embeddings = OllamaEmbeddings(model=MODEL_NAME)
        vectorDb = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        retriever = vectorDb.as_retriever()

        # prompt = ChatPromptTemplate.from_messages([
        #     ("system", self.SYSTEM_MESSAGE),
        #     MessagesPlaceholder(variable_name="chat_history"),
        #     ("user", """<context>
        #      {context}
        #      </context>
             
        #      User: {input}""")
        # ])

        prompt = ChatPromptTemplate.from_messages([
            ("system", self.SYSTEM_MESSAGE + " Below is some context that might be helpful:\n\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])
        document_chain = create_stuff_documents_chain(self.llm, prompt)

        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        # history_retriever_chain = create_history_aware_retriever(self.llm, retrieval_chain, prompt)
    
        # stream output
        output = ""
        streamer = SpeechStreamer()
        for chunk in retrieval_chain.stream({"input": user_input, "chat_history": self.history}):
            # print("chunk:", chunk)

            if (not "answer" in chunk):
                continue
            text = chunk["answer"]
            print("text: ", text)
            if any(text.endswith(ignore) for ignore in self.IGNORE_CHUNK):
                continue
            streamer.process_and_speak(text)
            output += text 
            
        streamer.flush_and_speak()
        streamer.stop()

        if output.startswith("AI:"): 
            output = output[3:]

        # Update history
        self.save_message("user", user_input)
        self.save_message("assistant", output)

        self.history.append(("user", user_input))
        self.history.append(("assistant", output))
        self.history = self.history[-self.MAX_HISTORY_SIZE:]
        print(output)

        return output
