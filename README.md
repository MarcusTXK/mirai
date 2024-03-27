All instructions below assume you are on on Ubuntu or Debian.

### Install ffmpeg and portaudio library

```
sudo apt update
sudo apt install ffmpeg
sudo apt-get install libportaudio2 espeak
```

### Attempting to get ESP32-S3 to communicate with a local LLM

You need python and python-dev, and a python version >= 3.9

```
python -m venv env
source env/bin/activate

pip install -r requirements.txt

python main.py
```

```
curl -fsSL https://ollama.com/install.sh | sh

sudo ollama serve
ollama pull mistral-openorca:7b-q5_K_M
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
