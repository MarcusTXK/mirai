import paho.mqtt.client as mqtt
from config import MQTT_SERVER, CLIENTID, PASSWORD, IOT_DEVICES
from flask_module.models import db, IoTData
import json
from datetime import datetime

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
        with self.app.app_context():  # Ensuring access to Flask's app context
            try:
                topic = msg.topic
                raw_data = str(msg.payload.decode("utf-8"))
                data_json = json.loads(raw_data)
                
                device_config = self.find_device_config(topic)

                if device_config and data_json:
                    # Try to extract the time from the data, if available
                    time_str = data_json.get('time')
                    time = None
                    if time_str:
                        try:
                            # Assuming the 'time' field is in ISO format; adjust as needed
                            time = datetime.fromisoformat(time_str)
                        except ValueError:
                            print(f"Invalid time format for topic {topic}: {time_str}")

                    data_entry = IoTData(
                        topic=topic,
                        unit=device_config['unit'],
                        location=device_config['location'],
                        data=data_json,
                        time=time,  # This will be None if no valid time is provided
                    )
                    db.session.add(data_entry)
                    db.session.commit()
                    print(f"Data saved for topic {topic}")
            except Exception as e:
                print(f"Failed to save data for topic {topic}: {e}")
