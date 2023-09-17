from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import json
from "langchain/output_parsers" import { StructuredOutputParser } 

MQTT_SERVER = "broker.hivemq.com"
CLIENTID = "esp32-dht22-clientId-cdf7"
PASSWORD = ""
SUBTOPIC_LED = "esp32-dht22/LED"
SUBTOPIC_DOOR = "esp32-dht22/DOOR"
SUBTOPIC_TEMP = "esp32-dht22/Temp"
SUBTOPIC_HUMIDITY = "esp32-dht22/Humidity"
MODEL = r"C:\Users\user\Documents\Programming\NUS\FYP\esp32-llm-bridge\models\llama-2-7b.Q4_K_M.gguf"


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")

    print(f"Received message from topic {topic}: {payload}")


client = mqtt.Client()
client.username_pw_set(CLIENTID)
client.connect(MQTT_SERVER, 1883, 60)
client.on_message = on_message
# Subscribe to the topics for temperature and humidity
client.subscribe(SUBTOPIC_TEMP)
client.subscribe(SUBTOPIC_HUMIDITY)


# llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
# k = 0  # keep last k interactions in memory
# memory = ConversationBufferWindowMemory(k=k, return_messages=True)


def send_chat(state, user_input):
    prompt = f"""
    The current environment is represented in JSON:
    {{{json.dumps(state)}}}
    Please check the environment and update JSON.
    1 represents on and 0 represents off
    Format your response as a JSON object with "msg", "light", "door" keys
    No explanations are required other than the json
    {user_input}
    """


    
    # prompt = PromptTemplate(template=template, input_variables=["input"])
    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(
        model_path=MODEL,
        temperature=0.75,
        max_tokens=2000,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )

    # conversation = ConversationChain(
    #     prompt=prompt, llm=llm, verbose=True  # memory=memory,
    # )
    return llm(prompt)


def get_state(response):
    state = json.loads(response[response.find("{") : response.find("}") + 1])
    client.publish(SUBTOPIC_LED, "on" if state["light"] == 1 else "off")
    client.publish(SUBTOPIC_DOOR, "on" if state["door"] == 1 else "off")
    # state = json.loads(response)
    return state


def main():
    load_dotenv()
    # Start the loop to keep listening for incoming messages
    client.loop_start()

    state = {"light": 0, "door": 0, "msg": "The light is off, the door is closed"}

    while True:
        print(json.dumps(state))
        user_input = input("> ")
        if len(user_input) == 0:
            continue

        response = send_chat(state, user_input)
        # response = conversation.predict(input=user_input)
        print(f"Assistant: {response}\n")
        try:
            state = get_state(state)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()


# while True:
#     print("Enter 'on' to turn on the light, 'off' to turn it off, or 'quit' to exit.")
#     user_input = input("> ").strip().lower()

#     if user_input == "quit":
#         print("Exiting program.")
#         break
#     elif user_input in ["on", "off"]:
#         client.publish(SUBTOPIC_LED, user_input)
#         print(f"Sent '{user_input}' to topic {SUBTOPIC_LED}")
#     else:
#         print("Invalid input. Please enter 'on', 'off', or 'quit'.")
