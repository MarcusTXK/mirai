from assistant import Assistant
from config import IS_USE_TOOLS
from mqtt_client import MQTTClient
from chat_handler import ChatHandler, State
from chat_handler_with_tools import ChatHandlerWithTools, State
from speech import Speech

def on_mqtt_message(client, userdata, msg):
    # Process MQTT messages here
    pass

blank_audio = "[BLANK_AUDIO]"

def main():
    mqtt_client = MQTTClient(on_message_callback=on_mqtt_message)
    chat_handler = ChatHandler()
    # if IS_USE_TOOLS:
    #     chat_handler = ChatHandlerWithTools()


    speech = Speech()

    # Connect and start the MQTT client
    mqtt_client.connect()
    mqtt_client.start()

    # Initialize state
    global state
    state = State(light=1, msg="Hello, nice to meet you.")
    speech.speak("Starting up, please wait")
    print(chat_handler.send_chat(state, "Hi, my name is Marcus, nice to meet you."))
    speech.speak("Ready to take in input")


    def parse_audio(user_input): 
        global state
        print("pre-parsed user_input: ", user_input)
        print("isSpeaking", speech.isSpeaking)
        if speech.isSpeaking or len(user_input.strip()) < 10 or user_input.strip() == blank_audio:
            return
        print("parsed user_input: ", user_input)
        resp = chat_handler.send_chat(state, user_input)
        try:
            print("resp", resp)
            speech.speak(resp)
            # client.publish(SUBTOPIC_LED, "on" if state.light == 1 else "off")
        except Exception as e:
            print(e)

    # Main application loop
    try:
        my_assistant = Assistant(commands_callback=parse_audio , n_threads=8, model='base.en')    
        speech.speak("Ready to take in commands")
        my_assistant.start()
    finally:
        mqtt_client.stop()

if __name__ == "__main__":
    main()
