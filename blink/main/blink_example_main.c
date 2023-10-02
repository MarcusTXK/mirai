#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "mqtt_client.h"
#include "esp_netif.h"
#include "mqtt_client.h"

static const char *TAG = "MQTT_APP";

#define BLINK_GPIO CONFIG_BLINK_GPIO

static uint8_t s_led_state = 1;

static esp_mqtt_client_handle_t mqtt_client = NULL;
void mqtt_event_handler_cb(void* handler_args, esp_event_base_t base, int32_t event_id, void* event_data) {
    esp_mqtt_event_handle_t event = (esp_mqtt_event_handle_t) event_data;
    
    switch (event->event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");
            esp_mqtt_client_subscribe(mqtt_client, "esp32-dht22/LED", 0);
            break;
        case MQTT_EVENT_DATA:
            ESP_LOGI(TAG, "MQTT_EVENT_DATA");
            if (strncmp(event->topic, "esp32-dht22/LED", event->topic_len) == 0) {
                if (strncmp(event->data, "on", event->data_len) == 0) {
                    s_led_state = 1;
                } else if (strncmp(event->data, "off", event->data_len) == 0) {
                    s_led_state = 0;
                }
            }
            break;
        default:
            break;
    }
}


static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                               int32_t event_id, void* event_data)
{
    if (event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_id == WIFI_EVENT_STA_DISCONNECTED) {
        esp_wifi_connect();
    } else if (event_id == WIFI_EVENT_STA_CONNECTED) {
        // You may want to handle other Wi-Fi related events here
    }
}

void app_main(void)
{
    // Initialize NVS (required for Wi-Fi configuration storage)
    nvs_flash_init();

    esp_netif_init();

    esp_event_loop_create_default();

    // Configure Wi-Fi
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    esp_wifi_set_mode(WIFI_MODE_STA);

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = "Virus",
            .password = "download",
        },
    };

    esp_wifi_set_config(WIFI_IF_STA, &wifi_config);
    esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL);

    esp_wifi_start();

    // MQTT Configuration
    // const esp_mqtt_client_config_t mqtt_cfg = {
    //     .broker.address.uri = "mqtt://broker.hivemq.com",
    //     // .broker.address.hostname = "broker.hivemq.com",
    //     // .broker.address.port = 1883,
    //     // .broker.address.transport = MQTT_TRANSPORT_OVER_TCP,
    //     .credentials.username = "esp32-dht22-clientId-cdf7",
    // };
    const esp_mqtt_client_config_t mqtt_cfg = {
        .broker = {
            .address = {
                .hostname = "broker.hivemq.com",
                .port = 1883,
                .transport = MQTT_TRANSPORT_OVER_TCP,
            }
        },
        .credentials = {
            .username = "esp32-dht22-clientId-cdf7",
        },
    };


    mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(mqtt_client, MQTT_EVENT_ANY, mqtt_event_handler_cb, mqtt_client);
    esp_mqtt_client_start(mqtt_client);


    // Configure the LED
    gpio_reset_pin(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);

    while (1) {
        ESP_LOGI(TAG, "Turning the LED %s!", s_led_state == true ? "ON" : "OFF");
        gpio_set_level(BLINK_GPIO, s_led_state);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}
