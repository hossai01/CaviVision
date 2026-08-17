from PySide6.QtCore import QObject

class SerialWorker(QObject):
    def __init__(self,serial):
        super().__init__()
        self.serial=serial
        self.running=True
    def data_read(self):
        while self.running:
            data=self.serial.readline()
            if data:
                    print(data)
    def stop(self):
         self.running=False
