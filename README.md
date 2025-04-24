The "Fire Alarm and Suppression System" is an Internet of Things (IoT) project developed to detect fire hazards and initiate appropriate suppression measures. The system comprises a web-based interface that allows users to monitor fire alarm sensors and manage system settings.

**Key Features:**

- **Real-Time Monitoring:** Users can view the status of fire alarm sensors in real-time through the web interface.

- **User Authentication:** The system includes login and signup functionalities to ensure secure access for authorized personnel.

- **Alarm Notifications:** Upon detecting a fire, the system triggers an alarm and notifies registered users.

**Web Interface:**

The web application is accessible at [https://vgufirealarm.pythonanywhere.com/](https://vgufirealarm.pythonanywhere.com/). The homepage provides options to log in or sign up, and displays information about the development team.

**Repository Contents:**

The GitHub repository [https://github.com/MinhLuong1006/IOTweb2.0](https://github.com/MinhLuong1006/IOTweb2.0) contains the following key files and directories:

- `app.py`: The main application script that runs the web server.

- `templates/`: Directory containing HTML templates for the web pages.

- `static/`: Directory for static files such as CSS, JavaScript, and images.

- `requirements.txt`: Lists the Python dependencies required to run the application.

**Getting Started:**

To set up the system locally:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/MinhLuong1006/IOTweb2.0.git
   ```


2. **Install Dependencies:**

   Navigate to the project directory and install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```


3. **Run the Application:**

   Execute the following command to start the web server:

   ```bash
   python app.py
   ```


   The application will be accessible at `http://127.0.0.1:5000/`.

**Note:** Ensure that you have Python installed on your system and that all dependencies are properly configured.

**Project Details:**

- **Primary Programming Language:** Python
- **Primary IDE:** Visual Studio Code (VS Code)
- **Primary Framework:** Flask
- **Database and Authentication:** Firebase

For more details, visit the [GitHub repository](https://github.com/MinhLuong1006/IOTweb2.0) and the [live web application](https://vgufirealarm.pythonanywhere.com/).
