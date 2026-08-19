
import serial

class SerialManager():
    def __init__(self):
        self.serial=None
        
    def serial_connect(self,port,baud_rate):
        self.port=port
        self.baud_rate=int(baud_rate)
        try:
            self.serial=serial.Serial(port=self.port,baudrate=self.baud_rate,timeout=0.2) #creats a Serial object. 
            #timeout=0.2 sec means the readline() waits at most 0.2 sec before it returns a data. if no data is availble within
            #this time it returns b'' which is considered as False in python
            print("Connected to:", self.port)
            print("Baud rate:", self.baud_rate)
            return True
        except serial.SerialException as e:
            print("connection faield",e)
            return False
        

    def serial_disconnect(self):
        if self.serial is not None and self.serial.is_open:
            self.serial.close()
            print("Disconnected")
            return True
        return False