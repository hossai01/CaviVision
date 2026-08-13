\# CaviVision



\## Overview



CaviVision is a Python-based application under active development for controlling and monitoring a vision and measurement system.



The project is being developed with a modular architecture that separates the graphical user interface from hardware communication and device-management logic.



\## Current Features



\* Graphical user interface built with \*\*PySide6\*\*

\* Serial communication using \*\*PySerial\*\*

\* Dedicated serial manager for communication handling

\* Connection panel for controlling and displaying the connection state

\* Connection status indication:



&#x20; \* \*\*Connected\*\*

&#x20; \* \*\*Not connected\*\*

\* Modular separation between GUI and serial communication components



\## Technologies



\* \*\*Python\*\*

\* \*\*PySide6\*\*

\* \*\*PySerial\*\*

\* Object-oriented programming

\* Modular software architecture



\## Project Structure



```text

CaviVision/

├── connection\_panel.py

├── main.py

├── main\_window.py

├── serial\_manager.py

├── .gitignore

└── README.md

```



\### Main Components



\*\*`main.py`\*\*



Application entry point.



\*\*`main\_window.py`\*\*



Defines the main application window and integrates the different GUI components.



\*\*`connection\_panel.py`\*\*



Implements the connection interface and displays the current connection status.



\*\*`serial\_manager.py`\*\*



Handles serial communication and connection management.



\## Architecture



The current application separates the graphical interface from the serial communication layer.



```text

&#x20;       CaviVision

&#x20;            │

&#x20;            ▼

&#x20;      Main Window

&#x20;            │

&#x20;            ▼

&#x20;    Connection Panel

&#x20;            │

&#x20;            ▼

&#x20;     Serial Manager

&#x20;            │

&#x20;            ▼

&#x20;     Serial Device

```



This separation makes the application easier to maintain and provides a foundation for adding additional hardware and image-processing functionality.



\## Development Status



CaviVision is currently under active development.



The initial software architecture and serial connection management have been implemented. Further functionality will be added incrementally as the project develops.



\## Planned Features



Future development may include:



\* Camera integration

\* Image acquisition and processing

\* Real-time image analysis

\* Hardware control

\* Measurement and visualization functionality

\* Additional device communication

\* Improved user interface



\## How to Run



\### Requirements



\* Python 3.x

\* PySide6

\* PySerial



Install the required Python packages with:



```bash

pip install PySide6 pyserial

```



\### Run the Application



From the project directory:



```bash

python main.py

```



\## License



This project is currently intended as a personal engineering and software-development project.



