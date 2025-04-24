
# IOTweb2.0

## Overview

**IOTweb2.0** is a web-based application designed for Internet of Things (IoT) device management and monitoring. The project integrates a Flask backend with a responsive frontend to facilitate real-time data visualization and control of connected devices.

## Features

-   **User Authentication**: Secure login system to manage user access.
    
-   **Real-Time Monitoring**: Display of sensor data and device statuses.
    
-   **Device Control**: Interface to send commands to IoT devices.
    
-   **Responsive Design**: Optimized for various screen sizes and devices.
    

## Technologies Used

### Programming Languages

-   **HTML** (61.3%): Structure of web pages.
    
-   **CSS** (22.8%): Styling and layout.
    
-   **SCSS** (9.7%): Enhanced CSS with variables and nesting.
    
-   **Python** (5.6%): Backend logic and server-side operations.
    
-   **JavaScript** (0.6%): Client-side interactivity.
    

### Frameworks and Libraries

-   **Flask**: Lightweight Python web framework for backend development.
    
-   **Jinja2**: Templating engine used with Flask for dynamic HTML rendering.
    
-   **Bootstrap**: CSS framework for responsive design (assumed based on common practices).
    

### Development Tools

-   **Integrated Development Environments (IDEs)**:
    
    -   _Visual Studio Code_: Versatile code editor suitable for both frontend and backend development.
        
    -   _PyCharm_: IDE tailored for Python development.
        
-   **Version Control**:
    
    -   _Git_: Distributed version control system.
        
    -   _GitHub_: Hosting platform for version control and collaboration.
        

## Installation

1.  **Clone the Repository**:
    
    ```bash
    git clone https://github.com/MinhLuong1006/IOTweb2.0.git
    cd IOTweb2.0
    
    ```
    
2.  **Create a Virtual Environment**:
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    ```
    
3.  **Install Dependencies**:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
4.  **Run the Application**:
    
    ```bash
    python app.py
    
    ```
    
5.  **Access the Application**: Open your web browser and navigate to `http://localhost:5000`.
    

## Project Structure

```
IOTweb2.0/
├── app.py
├── requirements.txt
├── templates/
│   └── ... (HTML templates)
├── static/
│   ├── css/
│   ├── js/
│   └── ... (Static assets)
├── users.txt
├── alarm.mp3
└── README.md

```

-   `app.py`: Main Flask application file.
    
-   `requirements.txt`: Lists Python dependencies.
    
-   `templates/`: Contains HTML templates rendered by Flask.
    
-   `static/`: Holds static files like CSS, JavaScript, and images.
    
-   `users.txt`: Stores user credentials or related data.
    
-   `alarm.mp3`: Audio file used within the application.
    

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.
