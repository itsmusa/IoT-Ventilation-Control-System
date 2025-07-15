# Remotely Controlled Ventilation System

## Project Overview

This project integrates **Internet of Things (IoT)** and **fuzzy logic control** to automate and remotely manage air ventilation in enclosed environments. It aims to maintain optimal temperature and humidity levels, improving air quality and energy efficiency. The system is designed for applications in homes, server rooms, greenhouses, and industrial facilities.

## Features

- 🌡️ **Real-time Monitoring** of temperature and humidity
- 🧠 **Fuzzy Logic Control** for fan speed adjustment
- 📶 **Wireless Communication** via Raspberry Pi Pico W
- 💾 **Local Data Logging** on microSD card
- 🌐 **Web-based User Interface** for remote control
- 📲 **WhatsApp Notifications** using CallMeBot API
- 🔌 **Energy-efficient Operation** with automated fan control

## Installation

### Requirements

- Raspberry Pi Pico W (x2)
- DHT11 Temperature & Humidity Sensor
- L298N Motor Driver
- DC Fans (x2)
- MicroSD Card Module
- Power Supply: 12V for fans, 5V for microcontroller
- HTML, CSS, JavaScript (for UI)
- Python (for control logic and server)

### Setup

1. Connect sensors and fans to the Pico W as per schematics.
2. Flash Python code to the Pico W.
3. Configure Wi-Fi credentials.
4. Set up the microSD card for data logging.
5. Host the web interface on the Pico W.
6. Integrate CallMeBot API for notifications.

## Usage

### Workflow

```python
temperature, humidity = read_dht11()
fan_speed = fuzzy_control(temperature, humidity)
update_web_interface(fan_speed)
log_to_sd_card(temperature, humidity, fan_speed)
```
## Web Interface

- Displays live temperature and humidity  
- Shows fan speed and historical data graph  
- Accessible via local network  

## Architecture

### System Block Diagram

![](https://raw.githubusercontent.com/itsmusa/IoT-Ventilation-Control-System/refs/heads/main/images/block.png)

### Key Modules

- **Sensor Unit**: DHT11 sensors connected to Pico W  
- **Fan Controller**: L298N driver adjusts fan speed  
- **Data Logger**: microSD module stores readings  
- **Web Server**: REST API hosted on Pico W  

## Screenshots and Visuals
### Web Interface

![]([interface](https://raw.githubusercontent.com/itsmusa/IoT-Ventilation-Control-System/refs/heads/main/images/interface.png))

### Fuzzy Logic Flowchart

![](https://raw.githubusercontent.com/itsmusa/IoT-Ventilation-Control-System/refs/heads/main/images/fuzzy.png)

### Testing

![]([test](https://raw.githubusercontent.com/itsmusa/IoT-Ventilation-Control-System/refs/heads/main/images/test.png))

## Contributors / Acknowledgements

- **Author**: Musa Magwaza (Student No: 22045698)  
- **Institution**: Department of Electronic and Computer Engineering  
- **Course**: Electronic Design Project 3B (EDPB301)  
- **Supervisor**: Mr J Dlamini
- **Durban University of Technology**

## License

This project is part of an academic submission and may be subject to institutional copyright.  
For reuse or adaptation, please contact the author or institution.
