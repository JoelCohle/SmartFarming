# Smart Farming Codebase

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Code Structure](#code-structure)
7. [License](#license)
8. [Contact](#contact)

## Introduction
The Smart Farming Codebase enables the collection and monitoring of data from sensors deployed in a farming environment. The system gathers sensor data using Arduino-based microcontrollers and updates the collected values onto Thingspeak and Onem2m databases. Additionally, it provides a web-based dashboard built using Python Flask and a SQLite database for visualizing and analyzing the collected data.

## Features
- Data collection from deployed sensors.
- Updating sensor data onto Thingspeak and Onem2m databases.
- Web-based dashboard for data visualization and analysis.
- Real-time monitoring of sensor readings.
- Historical data analysis.
- User Registration and Login with proper User Authentication and Route Protection.

## Prerequisites
Before using this codebase, make sure you have the following prerequisites installed:

- Arduino IDE and compatible hardware for sensor data collection.
- Python 3.x
- Flask framework
- SQLite database
- Other necessary dependencies specified in the project's requirements.

## Installation
To set up the Smart Farming Codebase, follow these steps:

1. Clone the repository to your local machine.
2. Install the necessary dependencies specified in requirements.txt.
3. Set up the Arduino-based sensors according to the provided documentation and connect them to the microcontrollers.
4. Configure the Thingspeak and Onem2m credentials in the Arduino code for data updates.
5. Set up the Flask application and SQLite database for the dashboard in the Dashboard folder.
6. Start the Arduino code on the microcontrollers and run the Flask application for the dashboard.

## Usage
Once the codebase is set up and the sensors are deployed, the data collection process will begin automatically. The Arduino code will update the collected sensor values onto the Thingspeak and Onem2m databases.

To access the dashboard, start the Flask application and navigate to the provided URL in your web browser. The dashboard will provide real-time monitoring of the sensor readings, historical data analysis, and alerts/notifications based on the specified thresholds.

The dashboard interface is intuitive and user-friendly, allowing users to explore and visualize the collected data, generate reports, and customize the dashboard's appearance and functionalities.

## Code Structure
The codebase is structured as follows:

- `Arduino/`: Contains the code for data collection from the sensors and updating the values onto Thingspeak and Onem2m databases.
- `Dashboard/`: Includes the code for the web-based dashboard built using Python Flask and a SQLite database. This folder contains the necessary files and configurations for data processing, visualization, and user interface.

Please refer to the individual folders and files for detailed documentation and comments.

## License
This codebase is released under the [MIT License](LICENSE).

For further questions or inquiries, please contact [insert contact information here].
