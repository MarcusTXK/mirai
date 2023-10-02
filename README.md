### Attempting to get ESP32 to communicate with a local LLM

Windows:

```
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

py test.py
```

Run the esp-32 simulator on wokwi [here](https://wokwi.com/projects/375639338149454849)

### Commands to run for esp32

```
idf.py set-target esp32s3
idf.py menuconfig
https://github.com/espressif/esp-idf/tree/272b4091f1f1ff169c84a4ee6b67ded4a005a8a7/examples/protocols
To configure the example to use Wi-Fi, Ethernet or both connections, open the project configuration menu (idf.py menuconfig) and navigate to "Example Connection Configuration" menu. Select either "Wi-Fi" or "Ethernet" or both in the "Connect using" choice.


(Top) → Component config → ESP-TLS
[*] Allow potentially insecure options
[*]     Skip server certificate verification by default (WARNING: ONLY FOR TESTING PURPOSE, READ HELP)

idf.py build

idf.py -p COM5 flash
idf.py -p COM5 monitor
```
