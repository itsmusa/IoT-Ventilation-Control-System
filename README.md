# Remotely Controlled Ventilation System

## Project Overview

This project introduces a remotely controlled ventilation system powered by the Internet of Things (IoT) and fuzzy logic. Designed to optimize indoor environmental conditions, the system automatically monitors and adjusts temperature and humidity levels in real-time. A user-friendly web interface provides live feedback and control, enhancing comfort and energy efficiency. Applications range from homes and server rooms to greenhouses and industrial facilities.

---

## Features

- Real-time temperature and humidity monitoring
- Automated fan control using fuzzy logic
- Local data logging on microSD card
- Web-based user interface with live sensor data display
- Wireless communication via Raspberry Pi Pico W
- WhatsApp notifications using CallMeBot API
- Compact, breadboard-based prototype with recyclable housing
- Simulation and implementation using MATLAB and Python

---

## Installation

### Requirements

- **Microcontroller:** Raspberry Pi Pico W  
- **Sensors:** DHT11 (Temperature and Humidity)  
- **Fan Driver:** L298N Motor Driver  
- **Storage:** microSD Card + Module  
- **Power:** 12V for fans, 5V for Pico W

### Software Dependencies

- Python 3.x
- HTML, CSS, JavaScript (for the web UI)
- MATLAB (for fuzzy logic simulation)
- CallMeBot API access (for notifications)

### Setup Steps

1. **Hardware Assembly:**
   - Connect DHT11 sensors and DC fans to the Pico W.
   - Use L298N to control fan speed.
   - Set up the microSD card module with SPI.

2. **Flashing Code:**
   - Write the Python control algorithm to the Pico W using Thonny or equivalent.
   - Include fuzzy logic-based control, data logging, and communication modules.

3. **Web Interface:**
   - Host HTML/CSS/JavaScript files on the Pico W.
   - Configure the server to serve live sensor data and graphs.

4. **Power Supply:**
   - Ensure 12V supply for fans and 5V regulated power for Pico W.

---

## Usage

### System Operation

```python
# Pseudocode for basic operation
read_temperature_humidity()
fuzzy_logic_control()
adjust_fan_speed()
log_data_to_sd()
update_web_dashboard()
```

### Accessing the Dashboard

1. Connect to the same Wi-Fi network as the Pico W.
2. Open a browser and navigate to the Pico W’s IP address.
3. View live readings, control fan behavior, and check historical data.

### Retrieving Stored Data

- Eject the microSD card from the unit.
- Use a card reader to access `.txt` logs from any PC.

---

## Architecture

### System Block Diagram

![System Block Diagram](images/system_block_diagram.png)

### Functional Breakdown

- **Sensor Unit:** Reads temperature and humidity via DHT11 sensors.
- **Fan Controller:** Uses fuzzy logic to set fan speed.
- **Data Logging:** Saves periodic readings to a local microSD card.
- **Web Server:** Hosts dashboard and handles REST API communication.

---

## Screenshots and Visuals

| Image | Description |
|-------|-------------|
| ![Breadboard Prototype](images/breadboard_prototype.png) | Breadboard assembly of prototype. |
| ![User Interface](images/user_interface.png) | Web dashboard showing real-time data and controls. |
| ![Data Stored](images/data_stored.png) | Sample view of locally logged data. |
| ![Testing Setup](images/heating_test.png) | Prototype undergoing environmental simulation with hot water. |

---

## Contributors / Acknowledgements

**Author:**  
- Magwaza MST (Student No. 22045698)  
**Institution:**  
- Department of Electronic and Computer Engineering  
**Supervisor(s):**  
- [Not listed in document]

---

## License

This project is academic and does not include a formal license. Please contact the author for reuse permissions.

---

### Notes

- All images should be placed in an `/images` directory within the repository.
- Ensure any sensitive data (e.g., API keys) are excluded from version control.
- For production, consider adding cloud backup and user download capabilities.
