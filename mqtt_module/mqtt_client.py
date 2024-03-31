import paho.mqtt.client as mqtt
from config import MQTT_SERVER, CLIENTID, PASSWORD, IOT_DEVICES
from flask_module.models import db, IoTData
import json

class MQTTClient:
    def __init__(self, app):
        self.app = app  
        self.client = mqtt.Client()
        self.client.username_pw_set(CLIENTID, PASSWORD)
        self.client.on_message = self.on_mqtt_message

    def connect(self):
        self.client.connect(MQTT_SERVER, 1883, 60)
        for device in IOT_DEVICES:
            self.client.subscribe(device.topic)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def find_device_config(self, topic):
        for device in IOT_DEVICES:
            if device['topic'] == topic:
                return device
        return None

    def on_mqtt_message(self, client, userdata, msg):
        with self.app.app_context():
            try:
                topic = msg.topic
                raw_data = str(msg.payload.decode("utf-8"))
                device_config = self.find_device_config(topic)

                if device_config and raw_data:
                    data_entry = IoTData(
                        topic=topic,
                        unit=device_config['unit'],
                        location=device_config['location'],
                        data=json.loads(raw_data)  # Ensure `raw_data` is in the correct format
                    )
                    db.session.add(data_entry)
                    db.session.commit()
                    print(f"Data saved for topic {topic}")
            except Exception as e:
                print(f"Failed to save data for topic {topic}: {e}")