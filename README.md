All instructions below assume you are on on Ubuntu or Debian.

### Install ffmpeg and portaudio library

```
sudo apt update
sudo apt install ffmpeg
sudo apt-get install libportaudio2 espeak
sudo apt install portaudio19-dev
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

systemctl stop ollama
sudo ollama serve
# on a seperate terminal
ollama pull mistral-openorca:7b-q5_K_M
```

### [Optional] Frontend setup

If you want a frontend client UI, you will need nodeJS and yarn
Install Dependencies

```
# installs NVM (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# download and install Node.js
nvm install 20

# verifies the right Node.js version is in the environment
node -v # should print `v20.12.0`

# verifies the right NPM version is in the environment
npm -v # should print `10.5.0`
```

```
cd frontend_module
# install dependencies
npm install
npm run dev
```

To access on other devices

```
sudo ufw allow 5000
sudo ufw allow 3000

# Setup Zeroconf
sudo apt-get install avahi-daemon
sudo systemctl enable avahi-daemon
sudo systemctl start avahi-daemon
sudo ufw allow 5353/udp

# Now you can access on other devices on your network via <hostname_here>.local:300, where hostname is from the command below
hostname
```

Windows supports Zeroconf networking through a service called Bonjour

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
