/**
   ESP32 + DHT22 Example for Wokwi
   
   https://wokwi.com/arduino/projects/322410731508073042
*/
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"
#include <ESP32Servo.h>

// WiFi
const char* ssid ="Wokwi-GUEST";
const char* password = "";

// MQTT
const char* mqtt_server = "broker.mqttdashboard.com";

const char* SUBTOPIC_LED = "esp32-dht22/LED";
const char* SUBTOPIC_DOOR = "esp32-dht22/DOOR";
const char* SUBTOPIC_TEMP = "esp32-dht22/Temp";
const char* SUBTOPIC_HUMIDITY = "esp32-dht22/Humidity";

WiFiClient espClient;
PubSubClient client(espClient);

// LED
const int LED_PIN = 13;

// DHT
const int DHT_PIN = 15;
DHTesp dhtSensor;

// Servo
Servo servo;  // create servo object to control a servo

int SERVO_PIN = 2;  // analog pin used to connect the potentiometer

void setup_wifi() {
  delay(10);
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    String clientId = "esp32-dht22-clientId-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("Connected");
      client.subscribe(SUBTOPIC_LED);
      client.subscribe(SUBTOPIC_DOOR);
    } else {
      delay(5000);
    }
  }
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Receive Topic: ");
  Serial.println(topic);

  Serial.print("Payload: ");
  Serial.println((char *)payload);
  if (!strcmp(topic, SUBTOPIC_LED)) {
    if (!strncmp((char *)payload, "on", length)) {
      digitalWrite(LED_PIN, HIGH);
    } else if (!strncmp((char *)payload, "off", length)) {
      digitalWrite(LED_PIN, LOW);
    }
  } else if (!strcmp(topic, SUBTOPIC_DOOR)) {
    if (!strncmp((char *)payload, "on", length)) {
      servo.write(90);
    } else if (!strncmp((char *)payload, "off", length)) {
      servo.write(0);
    }
  }
}

void setup() {
  Serial.begin(115200);
  randomSeed(micros());

  pinMode(LED_PIN, OUTPUT);

  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);

  servo.attach(SERVO_PIN, 500, 2400);  // attaches the servo on pin 13 to the servo object
  
  servo.write(0);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

float old_temperature = 0;
float old_humidity = 0;

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  TempAndHumidity  data = dhtSensor.getTempAndHumidity();
  float temperature = data.temperature;
  float humidity = data.humidity;
  // Serial.println("Temp: " + String(temperature, 2) + "°C");
  // Serial.println("Humidity: " + String(humidity, 1) + "%");

  if (old_temperature != temperature) {
    client.publish(SUBTOPIC_TEMP, String(temperature, 2).c_str());
  }
  old_temperature = temperature;

  if (old_humidity != humidity) {
    client.publish(SUBTOPIC_HUMIDITY, String(humidity, 1).c_str());
  }
  old_humidity = humidity;

  // Serial.println("---");
  delay(1000);
}