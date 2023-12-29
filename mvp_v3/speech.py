from threading import Thread, Lock
import pyttsx3
import time

class Speech:
    def __init__(self):
        self.speak_lock = Lock()
        self.isSpeaking = False

    def speak(self, audio):
        if not self.isSpeaking:
            print("Starting new speech thread")
            speech_thread = Thread(target=self.run_speech, args=(audio,))
            speech_thread.daemon = True  # Set the thread as a daemon
            speech_thread.start()

    def run_speech(self, audio_to_speak):
        with self.speak_lock:
            self.isSpeaking = True
            print("Speech thread acquired lock, speaking...")
            try:
                engine = pyttsx3.init("sapi5")
                voices = engine.getProperty("voices")
                engine.setProperty("voice", voices[1].id)
                engine.say(audio_to_speak)
                engine.runAndWait()
                time.sleep(0.5)  # Delay to ensure no overlap between speaking and listening
            except Exception as e:
                print(f"Error in speech engine: {e}")
            finally:
                print("Resetting isSpeaking flag")
                self.isSpeaking = False
