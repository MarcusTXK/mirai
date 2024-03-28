import threading

# Define a global state manager
class GlobalStateManager:
    def __init__(self):
        self._isSpeaking = False
        self.lock = threading.Lock()
    
    def set_speaking(self, isSpeaking):
        with self.lock:
            self._isSpeaking = isSpeaking
    
    def is_speaking(self):
        with self.lock:
            return self._isSpeaking
        

global_state_manager = GlobalStateManager()
