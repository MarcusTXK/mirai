import paho.mqtt.client as mqtt
from config import MQTT_SERVER, CLIENTID, PASSWORD, SUBTOPICS

class MQTTClient:
    def __init__(self, on_message_callback):
        self.client = mqtt.Client()
        self.client.username_pw_set(CLIENTID, PASSWORD)
        self.client.on_message = on_message_callback

    def connect(self):
        self.client.connect(MQTT_SERVER, 1883, 60)
        for subtopic in SUBTOPICS:
            self.client.subscribe(subtopic)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
