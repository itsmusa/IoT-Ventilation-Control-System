import urequests, ntptime, dht, time
import uasyncio as asyncio
from machine import Pin, PWM
from wifi import WiFiConnector
from fuzzycontroller import fan_speed
from dcmotor import DCMotor

# Connect to WIFI
wifi = WiFiConnector("", "")
wifi.connect()

# set up fan
frequency = 1000
pinB1 = Pin(3, Pin.OUT)
pinB2 = Pin(4, Pin.OUT)
enableB = PWM(Pin(2), frequency)
dc_motorB = DCMotor(pinB1, pinB2, enableB)

pinA1 = Pin(12, Pin.OUT)
pinA2 = Pin(13, Pin.OUT)
enableA = PWM(Pin(11), frequency)
dc_motorA = DCMotor(pinA1, pinA2, enableA)

# set up sensor
sensor = dht.DHT11(Pin(16))

phone_number = ""
api_key = ""

# Synchronize time with an NTP server
ntptime.settime()
TIMEZONE_OFFSET = 2 * 3600
def get_current_time():
    now = time.localtime(time.time() + TIMEZONE_OFFSET)

    # YYYY:MM:DD, HH:MM:SS
    return "{:04}-{:02}-{:02}, {:02}:{:02}:{:02}".format(now[0],now[1],now[2],now[3],now[4],now[5])

system_data = {"temperature": 0, "humidity": 0, "date_time": 0, "intake_speed": 0, "exhaust_speed": 0}

async def post_data():
    global system_data
    while 1:
        response = urequests.post("http://{Ip}/submit", json=system_data)

        if response.status_code == 200:
            print("Request successful")
        else:
            print("Request failed with status code:", response.status_code)  
        await asyncio.sleep(5)


def read_env():
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    return temp, hum


def send_message(phone_number, api_key, message):
    # set url
    url = f"https://api.callmebot.com/whatsapp.php?phone={phone_number}&text={message}&apikey={api_key}"

    # Make Request
    response = urequests.get(url)

    # check if it was successful
    print(response.status_code)

message = f"System%20is%20online%21"
send_message(phone_number, api_key, message)


async def main():
    global system_data, dc_motor
    asyncio.create_task(post_data())

    while True:
        try:
            temp, humidity = read_env()

            # Calculate and set fan speed
            fs = fan_speed(temp, humidity)

            print(f"Temperature: {temp}, Humidity: {humidity}")
            print(f"Fan Speed: {fs}")

            dc_motorB.backwards(fs)
            dc_motorA.backwards(fs)

            # print(f"Sent Data: {system_data}%")

            system_data["temperature"] = temp
            system_data["humidity"] = humidity
            system_data["date_time"] = get_current_time()
            system_data["intake_speed"] = fs
            system_data["exhaust_speed"] = fs

            await asyncio.sleep(5)
        except Exception as e:
            print(f"Something is wrong! {e}")
            message = f"System%20error%21"
            send_message(phone_number, api_key, message)


# Create an Event Loop
loop = asyncio.get_event_loop()
# Create a task to run the main function
loop.create_task(main())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
except KeyboardInterrupt:
    print('Program Interrupted by the user')
finally:
    dc_motorB.stop()
    dc_motorA.stop()
    print("Fan stopped")
