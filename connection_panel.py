from PySide6.QtWidgets import QPushButton,QWidget,QHBoxLayout 
from PySide6.QtWidgets import QVBoxLayout,QGroupBox,QGridLayout,QLabel,QComboBox
from serial_manager import SerialManager
from PySide6.QtCore import QThread
from serial_worker import SerialWorker
class ConnectionPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.panel_layout = QVBoxLayout()
        self.setLayout(self.panel_layout)
        self.connection_group=QGroupBox("connection")
        self.connection_layout=QGridLayout()
        self.connection_group.setLayout(self.connection_layout)
        self.port_label=QLabel("COM Port")
        self.baud_rate_label=QLabel("Baud rate")
        self.port_combo=QComboBox()
        self.baud_rate_combo=QComboBox()
        self.connect_button=QPushButton("connect")
        self.disconnect_button=QPushButton("disconnect")
        self.connection_status=QLabel("Status:")
        self.status_result=QLabel("Disconnected")
        self.connection_layout.addWidget(self.port_label,0,0)
        self.connection_layout.addWidget(self.port_combo,0,1)
        self.port_combo.addItems(["COM3","COM4","COM5"])
        self.connection_layout.addWidget(self.baud_rate_label,1,0)
        self.connection_layout.addWidget(self.baud_rate_combo,1,1)
        self.baud_rate_combo.addItems(["9600","115200"])
        self.connection_layout.addWidget(self.connection_status,2,0)
        self.connection_layout.addWidget(self.status_result,2,1)
        self.connection_layout.addWidget(self.connect_button,3,0)
        self.connection_layout.addWidget(self.disconnect_button,3,1)
        
        self.panel_layout.addWidget(self.connection_group)
        # button signals and slots
        self.connect_button.clicked.connect(self.device_connect)
        self.disconnect_button.clicked.connect(self.device_disconnect)
        #create SerialManager object
        self.serial_manager=SerialManager()
       
        
         
    def device_connect(self):
        port=self.port_combo.currentText()
        baud_rate=self.baud_rate_combo.currentText()
        success = self.serial_manager.serial_connect(port, baud_rate)
        
        if success:
             #creat QThread and move SerialWoker into this Thread
            self.thread= QThread()
            self.worker=SerialWorker(self.serial_manager.serial)
            self.worker.data_received.connect(self.update_data)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.data_read)
            self.thread.start()

            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.status_result.setText("Connected")
            
                    
    def device_disconnect(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        success = self.serial_manager.serial_disconnect()
        if success:
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.status_result.setText("Disconnected")

    def update_data(self,measurements):
        print(measurements)
       
