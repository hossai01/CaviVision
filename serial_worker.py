from PySide6.QtCore import QObject,Signal


class SerialWorker(QObject):

    data_received=Signal(dict)

    def __init__(self,serial):
        super().__init__()
        self.serial=serial
        self.running=True
    def data_read(self):
        while self.running:
            data=self.serial.readline()
            if data:
                    sensor_data=self.data_parse(data)
                    #print(sensor_data)
                    self.data_received.emit(sensor_data)
    def stop(self):
         self.running=False

    def data_parse(self,data):
         text=data.decode().strip()
         parts=text.split(",")
         measurements={}
         for part in parts:
              key,value=part.split(":")
              measurements[key]=float(value)
         return measurements
        
         