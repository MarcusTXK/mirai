from threading import Thread, Lock
import pyttsx3
import time

class Speech:
    def __init__(self):
        self.speak_lock = Lock()
        self.isSpeaking = False
        self.language = b'\x02en-gb'
        self.gender = 'male'
        self.engine = pyttsx3.init('espeak')
        self.engine.setProperty('rate', 170)
        self.change_voice(self.engine)

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
                
                self.engine.say(audio_to_speak)
                self.engine.runAndWait()
                time.sleep(0.5)  # Delay to ensure no overlap between speaking and listening
            except Exception as e:
                print(f"Error in speech engine: {e}")
            finally:
                print("Resetting isSpeaking flag")
                # engine.stop()
                self.isSpeaking = False

    def change_voice(self, engine):
        for voice in engine.getProperty('voices'):
            if self.language in voice.languages and self.gender == voice.gender:
                engine.setProperty('voice', voice.id)
                return True

        raise RuntimeError("Language '{}' for gender '{}' not found".format(self.language, self.gender))
