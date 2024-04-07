import timeit
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import threading
import queue
from assistant_module.global_state_manager import global_state_manager

class SpeechStreamer:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.playback_complete = threading.Event()
        self.playback_thread = threading.Thread(target=self.audio_player, daemon=True)
        self.buffered_text = ""
        self.playback_thread.start()
        self.isSpeaking = False
        self.start_time = timeit.default_timer()

    def audio_player(self):
        """Plays audio segments from the queue sequentially."""
        while True:
            self.playback_complete.clear()  # Reset the event at the start of each loop iteration
            audio_segment = self.audio_queue.get()
            if audio_segment is None:
                break  # Check for the stop signal
            global_state_manager.set_speaking(True)            
            print("speech spoken time taken: ", timeit.default_timer() - self.start_time)
            play(audio_segment)  # Play the audio segment using blocking play function
            self.playback_complete.set()  # Signal that playback is complete
            self.audio_queue.task_done()
            global_state_manager.set_speaking(False)

    def stream_speech(self, text_chunk):
        """Converts text chunks to speech and queues them for playback."""
        text_chunk = text_chunk.strip()
        if text_chunk:  # Ensure the text chunk is not empty
            mp3_fp = BytesIO()
            tts = gTTS(text_chunk, lang='en')
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            segment = AudioSegment.from_file(mp3_fp, format="mp3")
            print(f"Queuing: {text_chunk}")
            self.audio_queue.put(segment)  # Add the segment to the queue
            self.playback_complete.wait()  # Wait for the playback to complete before returning


    def process_and_speak(self, text_chunk):
        """Processes text chunks for speech, handling punctuation-induced pauses."""
        pause_punctuations = {",", ";", ":", "—"}
        end_punctuations = {".", "?", "!"}
        # ignore_chunk = {"<|im_end|>"}
        
        # if any(text_chunk.endswith(ignore) for ignore in ignore_chunk):
        #     return
        
        # Accumulate text in the buffer
        self.buffered_text += text_chunk

        # Decide when to speak based on the punctuation
        if any(text_chunk.endswith(punct) for punct in end_punctuations):
            self.stream_speech(self.buffered_text.strip())
            self.buffered_text = ""  # Reset buffer after speaking
        elif any(text_chunk.endswith(punct) for punct in pause_punctuations):
            # Future implementation may handle shorter pauses directly
            self.stream_speech(self.buffered_text.strip())
            self.buffered_text = ""  # Reset buffer after speaking
            pass

    def flush_and_speak(self):
        """Speaks any remaining text in the buffer."""
        if self.buffered_text.strip():
            self.stream_speech(self.buffered_text.strip())
            self.buffered_text = ""  # Reset buffer after speaking

    def stop(self, is_beep = True):
        """Stops the audio player thread."""
        if is_beep:
            beep_sound_path=r"./resources/sounds/beep.mp3"
            beep_sound = AudioSegment.from_file(beep_sound_path)
            self.audio_queue.put(beep_sound)  # Queue the beep sound to indicate its complete
        print("speech stop time taken: ", timeit.default_timer() - self.start_time)
        self.audio_queue.put(None)  # Signal the thread to stop

        self.playback_thread.join()