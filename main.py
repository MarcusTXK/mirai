from threading import Thread
from assistant_module.whisper_assistant import WhisperAssistant
from config import DAILY_SCHEDULED_INDEXING, IS_USE_TOOLS, USER_NAME, WAKE_WORD, WHISPER_MODEL
from flask_module.app import create_app
from mqtt_module.mqtt_client import MQTTClient
from assistant_module.llm_handler import LLMHandler
from assistant_module.global_state_manager import global_state_manager
from assistant_module.speech_streamer import SpeechStreamer
from utils.scheduler import run_scheduler, schedule_task
import re

app = create_app()

def run_app():
    app.run(host='0.0.0.0')

blank_audio_regex = r"\[[^\]]*\]| \([^)]*\)"

def should_ignore_user_input(user_input):
    parsed_user_input = user_input.strip()
    if global_state_manager.is_speaking() or len(parsed_user_input) < 10:
        return True

    # Use regex to check for text between brackets
    # user input between brackets such as the following are ingored: "[BLANK_AUDIO]", "[ Silence ]", "(upbeat music)"
    if re.search(blank_audio_regex, parsed_user_input):
        return True

    if WAKE_WORD and not parsed_user_input.startswith(WAKE_WORD):
        return True
    
    return False


def main():
    mqtt_client = MQTTClient(app)
    llm_handler = LLMHandler(app)

    # Connect and start the MQTT client
    mqtt_client.connect()
    mqtt_client.start()

    speech_streamer = SpeechStreamer()
    speech_streamer.stream_speech("Starting up. Please wait.")
    speech_streamer.stop(False)

    if DAILY_SCHEDULED_INDEXING:
        schedule_task(DAILY_SCHEDULED_INDEXING, llm_handler.update_preference_index)
        # Start the scheduler in a separate thread
        scheduler_thread = Thread(target=run_scheduler)
        scheduler_thread.start()
    
    llm_handler.send_initial_chat("Hi, my name is " + USER_NAME )

    def parse_audio(user_input): 
        print("user_input: ", user_input)
        if should_ignore_user_input(user_input):
            return
        try:
            resp = llm_handler.send_chat(user_input)
            print("resp", resp)
            # In future, use tools here
        except Exception as e:
            print(e)

    # Main application loop
    try:
        my_assistant = WhisperAssistant(commands_callback=parse_audio, n_threads=8, model=WHISPER_MODEL)    
        my_assistant.start()
    finally:
        mqtt_client.stop()
    
if __name__ == "__main__":
    t = Thread(target=run_app)
    t.start()
    main()
