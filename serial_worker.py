from PySide6.QtCore import QObject,Signal
from measurement import Measurement
import time

class SerialWorker(QObject):

    data_received=Signal(Measurement) # The Signal carries a Measurement object #in the earlier version we used a dict object
    error_occured=Signal(str)  # The Signal carries a string object if some error occurs
    data_timeout=Signal()

    def __init__(self,serial):
        super().__init__()
        self.serial=serial
        self.running=True
        self.last_data_time=time.monotonic()
        self.timeout_reported=False
    def data_read(self):
        while self.running:
            data=self.serial.readline()
            if data:
                    #bad_data = b"Temp:26.75,Pressure:11.14,Flow:abc,Volume:0.00\r\n"
                    sensor_data=self.data_parse(data)
                    
                    #print(sensor_data)
                    if sensor_data is not None:
                        self.last_data_time=time.monotonic()
                        if self.timeout_reported:
                             self.timeout_reported=False
                        self.data_received.emit(sensor_data)
            else:
                 elapsed=time.monotonic()-self.last_data_time
                 if elapsed > 3 and not self.timeout_reported:
                      self.timeout_reported=True
                      self.data_timeout.emit()
            
    def stop(self):
         self.running=False

    # data parsing that returns a dict object

    # def data_parse(self,data):
    #      text=data.decode().strip()
    #      parts=text.split(",")
    #      measurements={}
    #      for part in parts:
    #           key,value=part.split(":")
    #           measurements[key]=float(value)
    #      return measurements
    
    # data parsing that returns a Measurement object
    
    def data_parse(self,data):
         try:
            text=data.decode().strip()
            parts=text.split(',')
            values={}
            for part in parts:
                key,value=part.split(':')
                values[key]=float(value)
            measurement=Measurement(flow=values["Flow"],
                                    volume=values["Volume"],
                                    pressure=values["Pressure"],
                                    temperature=values["Temp"]
                                    )
            return measurement
         except (ValueError,KeyError) as e:
              error_message=f"Invalid serial data: {e}"
              print(error_message)
              self.error_occured.emit(error_message)
              return None
         