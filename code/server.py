import json, uos, sdcard
import uasyncio as asyncio
from wifi import WiFiConnector

# System data
system_data = {"temperature": 0, "humidity": 0, "date_time": 0, "intake_speed": 0, "exhaust_speed": 0}

# Connect to WIFI
wifi = WiFiConnector("", "")
wifi.connect()

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(13, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(14),
                  mosi=machine.Pin(15),
                  miso=machine.Pin(12))

try:
    # Initialize SD card
    sd = sdcard.SDCard(spi, cs)

    # Mount filesystem
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")

    print("SD card mounted")
except Exception as e:
    print("SD card mount failed:", e)

# Write to file
def write_data(data):
    with open("/sd/data_file.txt", "a") as file:
        file.write(f"{data}\r\n")

# Asynchronous Send Response
async def send_response(writer, content, content_type):
    try:
        if content_type in ["application/javascript", "text/html"]:
            with open(content, 'rb') as f:
                response = f.read()
        elif content_type == "application/json":
            response = json.dumps(content).encode()

        writer.write(f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n")
        writer.write(response)

    except Exception as e:
        print(f"Error sending response: {e}")
        writer.write('HTTP/1.1 500 Internal Server Error\r\n\r\n')

    finally:
        await writer.drain()
        await writer.wait_closed()


async def handle_client(reader, writer):
    global system_data
    try:
        request_line = await reader.readline()

        method, path, _ = request_line.decode().split()

        headers = {}
        while 1:
            header_line = await reader.readline()
            if header_line == b'\r\n':
                break
            header_key, header_value = header_line.decode().split(":", 1)
            headers[header_key.strip()] = header_value.strip()

        body = None
        if method == 'POST':
            content_length = int(headers.get("Content-Length", 0))
            body = await reader.read(content_length)
            print("POST data:", body.decode())

        if path == '/':
            await send_response(writer, 'index.html', 'text/html')
        elif path == '/jquery.js':
            pass
        elif path == '/app.js':
            await send_response(writer, 'app.js', 'application/javascript')
        elif path == '/data':
            await send_response(writer, system_data, "application/json")
        elif path == '/submit' and method == 'POST':
            if body:
                data = json.loads(body.decode())
                print("Received POST data:", data)
                system_data = data
                write_data(data)
                response_data = {"status": "success", "message": "Data received"}
                await send_response(writer, response_data, "application/json")
        else:
            await send_response(writer, 'index.html', 'text/html')

    except Exception as e:
        writer.write('HTTP/1.1 500 Internal Server Error\r\n\r\n')
        await writer.drain()
        await writer.wait_closed()


async def main():
    # Start the server and run the event loop
    server = asyncio.start_server(handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)


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
    uos.umount("/sd")
    print("SD card unmounted")
