from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
import pyttsx3
from pywhispercpp.examples.assistant import Assistant
from queue import Queue
from threading import Thread, Lock
import time
import sys
from pydantic import BaseModel, Field
from llama_index.program import LMFormatEnforcerPydanticProgram
from llama_index.llms.llama_cpp import LlamaCPP

MQTT_SERVER = "mqtt.eclipseprojects.io"
CLIENTID = "esp32-dht22-clientId-cdf7"
PASSWORD = ""
SUBTOPIC_LED = "esp32-dht22/LED"
SUBTOPIC_DOOR = "esp32-dht22/DOOR"
SUBTOPIC_TEMP = "esp32-dht22/Temp"
SUBTOPIC_HUMIDITY = "esp32-dht22/Humidity"
MODEL = r"../models/mistral-7b-instruct-v0.2.Q5_K_M.gguf"

# Define your desired data structure.
class State(BaseModel):
    light: int = Field(description="1 for on, 0 for off", ge=0, le=1)
    # door: int = Field(description="1 for open, 0 for closed", ge=0, le=1)
    msg: str = Field(description="Message to reply to the user")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    print(f"Received message from topic {topic}: {payload}")


client = mqtt.Client()
client.username_pw_set(CLIENTID, PASSWORD)
# Subscribe to the topics for temperature and humidity
client.subscribe(SUBTOPIC_TEMP)
client.subscribe(SUBTOPIC_HUMIDITY)
client.connect(MQTT_SERVER, 1883, 60)
client.on_message = on_message

def speak(audio):
    def run_speech(audio_to_speak):
        global isSpeaking
        with speak_lock:
            isSpeaking = True
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)
        engine.say(audio_to_speak)
        engine.runAndWait()    
        time.sleep(0.5)  # Delay to ensure no overlap between speaking and listening
        with speak_lock:
            isSpeaking = False

    speech_thread = Thread(target=run_speech, args=(audio,))
    speech_thread.start()


def send_chat(state, user_input, llm):
    template = f"""
    The current environment data: {state}
    """
    parser = PydanticOutputParser(pydantic_object=State)

    prompt = PromptTemplate(
        template="<s>[INST]\n{format_instructions}\nNo explanations are neded other than the JSON."
        + template
        + "\n[/INST]" 
        + "\n###User Input \n{input}",
        input_variables=["input"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    _input = prompt.format_prompt(input=user_input)

    # print("INPUT: " + _input.to_string())
    output = llm(_input.to_string())

    try:
        return parser.parse(output)
    except Exception as e:
        print(e)
        state.msg = "Sorry, I did not understand that"
        return state
     


def publish_state(state: State):
    print(state.msg)
    speak(state.msg)
    client.publish(SUBTOPIC_LED, "on" if state.light == 1 else "off")
    # client.publish(SUBTOPIC_DOOR, "on" if state.door == 1 else "off")
    return state

# Global state
state = State(light=1, msg="Hi, nice to meet you.")
blank_audio = "[BLANK_AUDIO]"
isSpeaking = False
speak_lock = Lock()

def main():
    global state
    load_dotenv()
    # Start the loop to keep listening for incoming messages
    client.loop_start()
    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCPP(
        # seed=100,
        model_path=MODEL,
        temperature=0,
        # max_tokens=100,
        # top_p=1,
        # f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
        # callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )

    program = LMFormatEnforcerPydanticProgram(
        output_cls=State,
        prompt_template_str=(
            "<s>[INST]Your response should be according to the following json schema: \n"
            "{json_schema}\n"
            "The current state: {state}"
            "[/INST]</s>"
            "[INST] {user_input} [/INST]"
        ),        
        llm=llm,
        verbose=True,
    )
    
    speak("Starting up, please wait")

    output = program(state=state, user_input="Please turn off the lights")
    print(output)
   
    # # cache intial state and instructions
    # state = send_chat(state, "Please output the current state of the house", llm)

    # # callback function that calls send_chat
    # def parse_audio(user_input):
    #     global state
    #     if isSpeaking or len(user_input.strip()) < 10 or user_input.strip() == blank_audio:
    #         return
    #     print("user_input: " + user_input)
    #     state = send_chat(state, user_input, llm)
    #     try:
    #         publish_state(state)
    #     except Exception as e:
    #         print(e)
    
    # # def test(user_input):
    # #     if isSpeaking or len(user_input.strip()) < 10 or user_input.strip() == blank_audio:
    # #         return
    # #     print(user_input)
    # #     print("Speak is being called")
    # #     speak(user_input)

    # my_assistant = Assistant(commands_callback=parse_audio , n_threads=8)    
    # speak("Ready to take in commands")
    # my_assistant.start()

    # while True:
    #     print(state)
    #     user_input = input("> ")
    #     if len(user_input) == 0:
    #         continue

    #     state = send_chat(state, user_input, llm)
    #     try:
    #         publish_state(state)
    #     except Exception as e:
    #         print(e)


if __name__ == "__main__":
    main()

# Prompts to demo:
# Please help to turn on the light
# Please help to turn off the light
