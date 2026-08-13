from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
import sys
from connection_panel import ConnectionPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CaviVision")
        self.resize(800, 600)
        self.central_widget=QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout=QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.connection_panel=ConnectionPanel()
        self.main_layout.addWidget(self.connection_panel)
      

app=QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()