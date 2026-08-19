from PySide6.QtWidgets import QPushButton,QWidget,QHBoxLayout 
from PySide6.QtWidgets import QVBoxLayout,QGroupBox,QGridLayout,QLabel,QComboBox
from serial_manager import SerialManager
from PySide6.QtCore import QThread
from serial_worker import SerialWorker
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Qt

class ConnectionPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.panel_layout = QVBoxLayout()
        self.setLayout(self.panel_layout)
        self.connection_group=QGroupBox("Connection")
        self.connection_layout=QGridLayout()
        self.connection_group.setLayout(self.connection_layout)
        #self.connection_group.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed) #create a size for the widget
        self.port_label=QLabel("COM Port")
        self.baud_rate_label=QLabel("Baud rate")
        self.port_combo=QComboBox()
        self.baud_rate_combo=QComboBox()
        self.connect_button=QPushButton("connect")
        self.disconnect_button=QPushButton("disconnect")
        self.connection_status=QLabel("Status:")
        self.status_result=QLabel("Disconnected")
        self.data_lebel=QLabel("Data:")
        self.data_status=QLabel("--")
        self.connection_layout.addWidget(self.port_label,0,0)
        self.connection_layout.addWidget(self.port_combo,0,1)
        self.port_combo.addItems(["COM3","COM4","COM5"])
        self.connection_layout.addWidget(self.baud_rate_label,1,0)
        self.connection_layout.addWidget(self.baud_rate_combo,1,1)
        self.baud_rate_combo.addItems(["9600","115200"])
        self.connection_layout.addWidget(self.connection_status,2,0)
        self.connection_layout.addWidget(self.status_result,2,1)
        self.connection_layout.addWidget(self.data_lebel,3,0)
        self.connection_layout.addWidget(self.data_status,3,1)
        self.connection_layout.addWidget(self.connect_button,4,0)
        self.connection_layout.addWidget(self.disconnect_button,4,1)
        self.panel_layout.addWidget(self.connection_group,1) # here 1 is stretch factor. this factor applies only to the available xtra space
        # button signals and slots
        self.connect_button.clicked.connect(self.device_connect)
        self.disconnect_button.clicked.connect(self.device_disconnect)
        #create SerialManager object
        self.serial_manager=SerialManager()

        #create a widget for displaying measurements results
        self.measurement_group=QGroupBox("Measurements")
        self.measurement_layout=QGridLayout()
        self.measurement_group.setLayout(self.measurement_layout)
        #self.measurement_layout.setColumnStretch(0,1)
        #self.measurement_layout.setColumnStretch(1,1)
        #self.measurement_group.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding) #set the size of the widget
        self.flow_label=QLabel("Flow")
        self.measurement_layout.addWidget(self.flow_label,0,0,alignment=Qt.AlignLeft)
        self.flow_value=QLabel("--")
        self.measurement_layout.addWidget(self.flow_value,0,1,alignment=Qt.AlignRight)
        self.volume_label=QLabel("Volume")
        self.measurement_layout.addWidget(self.volume_label,1,0,alignment=Qt.AlignLeft)
        self.volume_value=QLabel("--")
        self.measurement_layout.addWidget(self.volume_value,1,1,alignment=Qt.AlignRight)
        self.pressue_label=QLabel("Pressure")
        self.measurement_layout.addWidget(self.pressue_label,2,0,alignment=Qt.AlignLeft)
        self.pressure_value=QLabel("--")
        self.measurement_layout.addWidget(self.pressure_value,2,1,alignment=Qt.AlignRight)
        self.temperature_label=QLabel("Temperature")
        self.measurement_layout.addWidget(self.temperature_label,3,0,alignment=Qt.AlignLeft)
        self.temperature_value=QLabel("--")
        self.measurement_layout.addWidget(self.temperature_value,3,1,alignment=Qt.AlignRight)
        self.panel_layout.addWidget(self.measurement_group,3) #stretch factor is 3. i.e, connection_group : measurement group = 1:3 on the extra vertical space here

    def device_connect(self):
        port=self.port_combo.currentText()
        baud_rate=self.baud_rate_combo.currentText()
        success = self.serial_manager.serial_connect(port, baud_rate)
        
        if success:
            #creat QThread and move SerialWoker into this Thread
            
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.status_result.setText("Connected")
            self.data_status.setText("Waiting")

            self.thread= QThread()
            self.worker=SerialWorker(self.serial_manager.serial)
            self.worker.data_received.connect(self.update_data)
            self.worker.error_occured.connect(self.show_data_error)
            self.worker.data_timeout.connect(self.show_data_timeout)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.data_read)
            self.thread.start()

                    
    def device_disconnect(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        success = self.serial_manager.serial_disconnect()
        if success:
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.status_result.setText("Disconnected")
            self.data_status.setText("--")
    # update_data method when passed argument was a dict object
    # def update_data(self,measurements):
    #     print(measurements)
    #     self.flow_value.setText(f"{measurements['Flow']:.2f} L/min")
    #     self.volume_value.setText(f"{measurements['Volume']:.2f} L")
    #     self.pressure_value.setText(f"{measurements['Pressure']:.2f} Bar")
    #     self.temperature_value.setText(f"{measurements['Temp']:.2f} °C")
    
    # update_data method when passed argument is a Measurement object
    def update_data(self,measurement):
            print(measurement)
            self.flow_value.setText(f"{measurement.flow:.2f} L/min")
            self.volume_value.setText(f"{measurement.volume:.2f} L")
            self.pressure_value.setText(f"{measurement.pressure:.2f} Bar")
            self.temperature_value.setText(f"{measurement.temperature:.2f} °C")
            self.data_status.setText("OK")

    def show_data_error(self,error_message):
          print("GUI received error:", error_message)
          self.data_status.setText("Error")
    def show_data_timeout(self):
         print("No data availabel")
         self.data_status.setText("Timeout")