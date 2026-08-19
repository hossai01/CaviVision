from dataclasses import dataclass

@dataclass
class Measurement:
    flow:float
    volume:float
    pressure:float
    temperature:float

