# 🔥 IoT Real-time Fire Detection Project

## Overview

IoT Real-time Fire Detection Project is a web-based application designed for Internet of Things (IoT) device management and monitoring. The project integrates a Flask backend with a responsive frontend to facilitate real-time data visualization and control of connected devices.

## Features

-   **User Authentication**: Secure login system to manage user access.
    
-   **Real-Time Monitoring**: Display of sensor data and device statuses.
    
-   **Device Control**: Interface to send commands to IoT devices.
    
-   **Responsive Design**: Optimized for various screen sizes and devices.
    
-   **Arduino Integration**: Sensor data collection and transmission using ESP32-based microcontrollers.
    

## Hardware Components

The project utilizes the following Arduino-compatible hardware:

-   2x **ESP32 Devkit V1** boards (Wi-Fi enabled microcontrollers)
    
-   2x **ESP32 GPIO Expanders** for additional input/output pins
    
-   4x **MQ4 Gas Sensors** for detecting methane and other gases
    
-   4x **DS18B20 Temperature Sensors** for precise temperature readings
    
-   4x **Flame Sensors** to detect fire or high-heat sources
    
-   Jumper wires and breadboards for circuit connections
    

### Arduino Functionality

-   The ESP32 boards collect sensor data (gas, temperature, flame) and transmit it to the Flask backend using HTTP or Firebase.
    
-   Each `.ino` file (Arduino sketch) defines logic for initializing sensors, connecting to Wi-Fi, and sending data.
    
-   Example sketches:
    
    -   `firebasetest1.ino`: Manages sensor input and sends data to Firebase.
        
    -   `firebasetest2.ino`: Secondary board support or sensor expansion.
        

## Technologies Used

### Programming Languages

-   **HTML (61.3%)**: Structure of web pages.
    
-   **CSS (22.8%)**: Styling and layout.
    
-   **SCSS (9.7%)**: Enhanced CSS with variables and nesting.
    
-   **Python (5.6%)**: Backend logic and server-side operations.
    
-   **JavaScript (0.6%)**: Client-side interactivity.
    

### Frameworks and Libraries

-   **Flask**: Lightweight Python web framework for backend development.
    
-   **Jinja2**: Templating engine used with Flask for dynamic HTML rendering.
    
-   **Bootstrap**: CSS framework for responsive design.
    

### Development Tools

-   **IDEs**: Visual Studio Code, Arduino
    
-   **Version Control**: Git, GitHub
    



## Project Structure

```
IOTweb2.0/
├── app.py
├── requirements.txt
├── templates/
├── static/
├── users.txt
├── alarm.mp3
├── README.md
└── Arduino/
    ├── firebasetest1.ino
    └── firebasetest2.ino

```

-   `app.py`: Main Flask application file.
    
-   `templates/`: HTML templates rendered by Flask.
    
-   `static/`: CSS, JS, and static assets.
    
-   `users.txt`: Stores user credentials.
    
-   `alarm.mp3`: Audio alert file.
    
-   `Arduino/`: Contains Arduino sketches for ESP32 devices.
    

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
