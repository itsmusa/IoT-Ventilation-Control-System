import network, time

class WiFiConnector:
    def __init__(self, ssid="", password=""):
        self.ssid = ssid
        self.password = password
        self.wifi = network.WLAN(network.STA_IF)

    def connect(self):
        """Connect to the Wi-Fi network."""
        try:
            if not self.wifi.isconnected():
                print(f'Connecting to {self.ssid}...')
                self.wifi.active(True)
                self.wifi.connect(self.ssid, self.password)

                # Wait for connection
                while not self.wifi.isconnected():
                    print("Waiting for connection...")
                    time.sleep(1)

        except Exception as e:
            print(f'An error occurred while connecting: {e}')

        finally:
            print(f"Connected IP: {self.wifi.ifconfig()[0]}")

    def disconnect(self):
        """Disconnect from the Wi-Fi network."""
        try:
            if self.wifi.isconnected():
                self.wifi.disconnect()
                print('Disconnected from Wi-Fi')
            else:
                print('Not connected to any Wi-Fi network.')

        except Exception as e:
            print(f'An error occurred while disconnecting: {e}')

    def is_connected(self):
        """Check if connected to Wi-Fi."""
        return self.wifi.isconnected()


if __name__ == '__main__':
    ssid = ''
    password = ''

    wifi = WiFiConnector()
    wifi.connect()
