# Config for MQTT
MQTT_SERVER = "mqtt.eclipseprojects.io"
CLIENTID = "esp32-dht22-clientId-cdf7"
PASSWORD = ""
SUBTOPICS = ["esp32-dht22/LED", "esp32-dht22/DOOR", "esp32-dht22/Temp", "esp32-dht22/Humidity"]

# Config for LLM
IS_USE_TOOLS = False
USER_NAME = "Marcus"
WAKE_WORD = "" # Experimental, not recommended to set
MODEL_NAME = "mistral-openorca:7b-q5_K_M"
INDEX_PATH = "./instance/preferences_index"