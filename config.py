from mqtt_module.iot_device import IoTDevice\

# Config for MQTT
MQTT_SERVER = "mqtt.eclipseprojects.io"
CLIENTID = "esp32-dht22-clientId-cdf7"
PASSWORD = ""
IOT_DEVICES = [
    IoTDevice(topic="esp32-dht22/TEMP_1", unit="°C", location="Kitchen"),
    IoTDevice(topic="esp32-dht22/HUMIDITY_1", unit="g/kg", location="Kitchen"),
    IoTDevice(topic="esp32-dht22/TEMP_2", unit="°C", location="Living Room")
]


# Config for LLM
IS_DEBUG = True
IS_USE_TOOLS = False

IS_USE_CONTEXT = False
MAX_CONTEXT_SIZE = 2

IS_USE_HISTORY = False
MAX_HISTORY_SIZE = 2

IS_USE_IOT_DATA = True
USER_NAME = "Marcus"
WAKE_WORD = "" # Experimental, not recommended to set
MODEL_NAME = "mistral-openorca:7b-q5_K_M"
INDEX_PATH = "./instance/preferences_index"


# Config for scheduling of analysing preferences
SCHEDULED_INDEXING_MODEL_NAME = "solar:10.7b-instruct-v1-q5_K_M" # Recommended to use a larger model as not as time sensitive and has better output
DAILY_SCHEDULED_INDEXING = "0300" # Daily time to schedule analyzing of data and creating new preference. Leave blank to disable.


# Config for whisper
WHISPER_MODEL = "small.en"