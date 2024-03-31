from dataclasses import dataclass

@dataclass
class IoTDevice:
    topic: str
    unit: str
    location: str

