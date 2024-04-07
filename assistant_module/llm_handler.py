from datetime import datetime, timedelta
import timeit
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from sqlalchemy import asc, desc
from config import INDEX_PATH, IOT_DEVICES, IS_DEBUG, IS_USE_CONTEXT, IS_USE_HISTORY, IS_USE_IOT_DATA, MAX_CONTEXT_SIZE, MAX_HISTORY_SIZE, MODEL_NAME, SCHEDULED_INDEXING_MODEL_NAME
from flask_module.controllers.preferences_controller import generate_index
from flask_module.models import ChatParticipant, Preference, db, Chatlog, IoTData
from assistant_module.speech_streamer import SpeechStreamer
from langchain_core.callbacks import StdOutCallbackHandler
from langchain_core.output_parsers import JsonOutputParser
import langchain 
import json
from typing import List

# Define your desired data structure.
class Observations(BaseModel):
    observation: List[str] = Field(description="Observation from that will be VERY useful to an assistant")


langchain.debug = IS_DEBUG 

class LLMHandler:
    SYSTEM_MESSAGE = "You are a helpful home assistant. Think before writing and output the response you would like to speak to the user."
    IGNORE_CHUNK = {"<|im_end|>"}

    def __init__(self, app):
        self.llm = Ollama(model=MODEL_NAME)
        self.app = app
        self.history = self.load_recent_chats()

    def load_recent_chats(self):
        with self.app.app_context():
            # Fetch the 4 most recent chat logs from the database
            recent_chats = Chatlog.query.order_by(Chatlog.id.desc()).limit(MAX_HISTORY_SIZE).all()
            # Convert the chat logs into the desired format and reverse to start with the oldest
            history = [(chat.sentBy, chat.message) for chat in reversed(recent_chats)]
            return history

    def save_message(self, sentBy, message):
        with self.app.app_context(): 
            new_message = Chatlog(sentBy=sentBy, message=message)
            db.session.add(new_message)
            db.session.commit()

    def update_preference_index(self):        
        output_parser = JsonOutputParser(pydantic_object=Observations)
        format_instructions = output_parser.get_format_instructions()
        with self.app.app_context():
           # Calculate the time 24 hours ago from the current moment
            twenty_four_hours_ago = datetime.utcnow() - timedelta(days=1)
            
            # Fetch chat logs from the last 24 hours, adjust the query according to your schema
            recent_chats = Chatlog.query.filter(Chatlog.time >= twenty_four_hours_ago).order_by(asc(Chatlog.time)).all()
            
            # Format the fetched chat logs for the prompt
            # This assumes chat logs have 'sentBy' and 'message' attributes and are stored as a list of tuples
            chat_logs_formatted = "\n ".join([f"{chat.sentBy}: {chat.message}" for chat in recent_chats])
            print("chat_logs_formatted")
            prompt = langchain.PromptTemplate(
               template="List 0 to 3 useful user observations that you think would be absolutely useful as context for future conversations for an AI assistant, based on the chat logs below. Good example of observation: \n EXAMPLE 1: The user loves [ACTIVITY] in [CONDITION].\n EXAMPLE 2: The user does [THING] as [REASON]. \nUse the Chat Logs below:\n{chat_logs}\n====\n{format_instructions}" ,
               input_variables=["chat_logs"],
               partial_variables={"format_instructions": format_instructions},
            )
            model = Ollama(model=SCHEDULED_INDEXING_MODEL_NAME)
            chain = prompt | model| output_parser
            output = chain.invoke({"chat_logs": chat_logs_formatted})
            
            for obs in output['observation']:
                new_pref = Preference(description=obs, updatedBy=ChatParticipant.ASSISTANT.value)
                db.session.add(new_pref)
            
            db.session.commit()
            generate_index()

    # Used on startup
    def send_initial_chat(self, user_input):
        prompt = ChatPromptTemplate.from_messages([
            (ChatParticipant.SYSTEM.value, self.SYSTEM_MESSAGE),
            (ChatParticipant.USER.value, "{input}"),
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
    
    def get_iot_data(self):
        if not IS_USE_IOT_DATA:
            return ""
        start = timeit.default_timer()
        # Fetch the latest data for each IoT device
        device_messages = []
        with self.app.app_context():
            for device in IOT_DEVICES:
                latest_data = IoTData.query.filter_by(topic=device.topic).order_by(IoTData.time.desc()).first()
                if latest_data:
                    data_str = json.dumps(latest_data.data).replace("{", "{{").replace("}", "}}")
                    message = f"{device.topic}: {data_str} {device.unit} in {device.location}"
                    device_messages.append(message)

        # Append device messages to the system message
        additional_context = "\n".join(device_messages) 
        print("additional_context", additional_context)
        print("get_iot_data time: ", timeit.default_timer() - start)
        return "\nIOT Sensor data that might be helpful: \n" + additional_context


    def send_chat(self, user_input):
        context = "{context}" if IS_USE_CONTEXT else ""
        context_message = " Below is some context that might be helpful:\n\n" if IS_USE_CONTEXT or IS_USE_IOT_DATA else ""

        prompt = ChatPromptTemplate.from_messages([
            (ChatParticipant.SYSTEM.value, self.SYSTEM_MESSAGE + context_message + context + self.get_iot_data()),
            MessagesPlaceholder(variable_name="chat_history"),
            (ChatParticipant.USER.value, "{input}"),
        ])

        if IS_USE_CONTEXT:
            start = timeit.default_timer()
            embeddings = OllamaEmbeddings(model=MODEL_NAME)
            vectorDb = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
            retriever = vectorDb.as_retriever(search_kwargs={"k": MAX_CONTEXT_SIZE})
            document_chain = create_stuff_documents_chain(self.llm, prompt)
            retrieval_chain = create_retrieval_chain(retriever, document_chain)
            print("get preference embeddings time: ", timeit.default_timer() - start)

        else:
            retrieval_chain = prompt | self.llm           
    
        # stream output
        output = ""
        isFirstChunk = True
        isSkipNext = False
        streamer = SpeechStreamer()
        history_start = timeit.default_timer()
        history = self.history if IS_USE_HISTORY else []
        print("get history time: ", timeit.default_timer() - history_start)
        for chunk in retrieval_chain.stream({"input": user_input, "chat_history": history}):
            # print("chunk:", chunk)

            if isSkipNext:
                isSkipNext = False
                continue

            if (IS_USE_CONTEXT and not "answer" in chunk):
                continue
            text = chunk["answer"] if IS_USE_CONTEXT else chunk
            print("text: ", text)
            if isFirstChunk and text.endswith("AI"):
                isSkipNext = True
                continue

            isFirstChunk = False
            if any(text.endswith(ignore) for ignore in self.IGNORE_CHUNK):
                continue
            streamer.process_and_speak(text)
            output += text 
            
        streamer.flush_and_speak()
        streamer.stop()

        if output.startswith(" AI:"): 
            output = output[4:]

        # Update history
        self.save_message(ChatParticipant.USER.value, user_input)
        self.save_message(ChatParticipant.ASSISTANT.value, output)

        self.history.append((ChatParticipant.USER.value, user_input))
        self.history.append((ChatParticipant.ASSISTANT.value, output))
        self.history = self.history[-MAX_HISTORY_SIZE:]
        print(output)

        return output
