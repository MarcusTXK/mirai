### Install ffmpeg and portaudio library

```
# on Ubuntu or Debian
sudo apt update
sudo apt install ffmpeg
sudo apt-get install libportaudio2
```

### Attempting to get ESP32-S3 to communicate with a local LLM

You need python-3.9 and python3.9-dev

```
sudo apt-get update
sudo apt-get install python3.9 python3.9-dev
```

Linux:

```
python3.9 -m venv env
source env/bin/activate

pip install -r requirements.txt

python main.py
```

### Commands to run for esp32-S3

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
