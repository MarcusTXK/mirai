from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel, Field
import pyttsx3
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentType

MQTT_SERVER = "mqtt.eclipseprojects.io"
CLIENTID = "esp32-dht22-clientId-cdf7"
PASSWORD = ""
SUBTOPIC_LED = "esp32-dht22/LED"
SUBTOPIC_DOOR = "esp32-dht22/DOOR"
SUBTOPIC_TEMP = "esp32-dht22/Temp"
SUBTOPIC_HUMIDITY = "esp32-dht22/Humidity"
MODEL = r"models\mistral-7b-instruct-v0.1.Q8_0.gguf"


# Define your desired data structure.
class State(BaseModel):
    light: int = Field(description="1 for on, 0 for off", ge=0, le=1)
    # door: int = Field(description="1 for open, 0 for closed", ge=0, le=1)
    msg: str = Field(description="Response to the user's commands")


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

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def send_chat(state, user_input, llm):
    template = f"""
    The current environment data: {state}
    """
    parser = PydanticOutputParser(pydantic_object=State)

    prompt = PromptTemplate(
        template="<s>[INST]\n{format_instructions}\n{input}\nNo explanations are neded other than the JSON."
        + template
        + "[/INST]",
        input_variables=["input"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    _input = prompt.format_prompt(input=user_input)

    print("INPUT: " + _input.to_string())
    output = llm(_input.to_string())

    return parser.parse(output)


def publish_state(state: State):
    print(state.msg)
    speak(state.msg)
    client.publish(SUBTOPIC_LED, "on" if state.light == 1 else "off")
    # client.publish(SUBTOPIC_DOOR, "on" if state.door == 1 else "off")
    return state


def main():
    load_dotenv()
    # Start the loop to keep listening for incoming messages
    client.loop_start()
    state = State(light=1, msg="The light is currently on")
    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    # wikipedia = WikipediaAPIWrapper()
    # wikipedia_tool = Tool(
    #     name="wikipedia",
    #     func=wikipedia.run,
    #     description="Useful for when you need to look up a specific company",
    # )
    search = DuckDuckGoSearchRun()
    duckduckgo_tool = Tool(
        name="Search",
        func=search.run,
        description="Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input.",
    )
    tools = [duckduckgo_tool]  # wikipedia_tool

    llm = LlamaCpp(
        seed=100,
        model_path=MODEL,
        temperature=0,
        max_tokens=100,
        top_p=1,
        f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
        n_ctx=1024,
    )

    research_agent = initialize_agent(
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=5,
    )

    # state = send_chat(state, "Please output the current state of the house", llm)

    while True:
        print(state)
        user_input = input("> ")
        if len(user_input) == 0:
            continue

        if user_input.lower().startswith("tell me"):
            response = research_agent.run(user_input)
            speak(response)
        else:
            state = send_chat(state, user_input, llm)
            try:
                publish_state(state)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    main()

# Prompts to demo:
# Please help to turn on the light
# Please help to turn off the light
# Tell me who is Professor Ambuj Varshney
