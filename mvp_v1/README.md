### Attempting to get Virtual ESP32 to communicate with a local LLM

Windows:

```
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

py test.py
```


Linux:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-linux.txt

python3 test.py
```


Run the esp-32 simulator on wokwi [here](https://wokwi.com/projects/375639338149454849)

### Demo
![Turn light on esp32](https://github.com/MarcusTXK/esp32-llm-bridge/assets/50147457/7c92160a-0bed-43ad-b11f-22dee86c2935)
