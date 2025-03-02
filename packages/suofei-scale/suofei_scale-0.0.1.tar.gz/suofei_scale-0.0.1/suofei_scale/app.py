import serial
import time
import json
import os
import threading
import sys
import paho.mqtt.client as mqtt

serialError = False

def on_connect(client, userdata, flags, reason_code, properties):
    print("MQTT CLIENT CONNECTED. Starting scale communication")
    thread = threading.Thread(target=communicate_with_scale, args=(client, serialPortInstance))
    thread.daemon = True 
    thread.start()

def on_message(client, userdata, msg):
    print("COMMAND RECEIVED")

def bytes_to_hex(data):
    return ' '.join(f'0x{b:02X}' for b in data)

def data_parser(data):
    hex_string = data.hex()
    if len(hex_string) == 6:
        sign_value = int(hex_string[2:4],16)
        dec_value = int(hex_string[4:10], 16)
        if sign_value == 68:
            return -1*dec_value
        else:
            return dec_value
        
def communicate_with_scale(mqttClient,serialPortInstance):
    global serialError
    ser = serialPortInstance
    try:
        while True:
            try:
                ser.write(b'\x5A')
                print("→ TO TARGET: 0x5A")
                response = ser.read(1)
                if response == b'\xA5':
                    print("← FROM TARGET: 0xA5 (weight connected)")
                    while True:
                        data = ser.read(6)
                        if data:
                            ser.write(b'\x9F')
                            dec_val = data_parser(data)
                            dataObject = {"weight":dec_val,"timestamp":int(time.time())}
                            dataString = json.dumps(dataObject)
                            print(dataString)
                            mqttClient.publish(topic, dataString)
                time.sleep(10)
            except serial.SerialException as e:
                print(f"Serial communication error: {e}")
                break
    except KeyboardInterrupt:
        print("Closing connection...")
    finally:
        print("Closing serial connection...")
        serialError = True
        mqttClient.disconnect()
        try:
            ser.close()
        except:
            pass
        

if __name__ == "__main__":
    broker = os.getenv("MQTT_BROKER", "localhost")
    port = int(os.getenv("MQTT_PORT", "1883"))
    topic = os.getenv("MQTT_TOPIC", "scale/data")
    serialPORT = os.getenv("SERIALPORT", "/dev/ttyUSB-SCALE")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        serialPortInstance = serial.Serial(serialPORT, baudrate=9600, timeout=1)
    except serial.SerialException as e:
        print(f"ERROR: Cannot open serial port {port}: {e}")
        sys.exit(1)

    try:
        client.connect(broker, port, 60)
        client.loop_start()
    except Exception as e:
        print(f"ERROR: Cannot connect to MQTT broker: {e}")
        sys.exit(1)

    try:
        while True:
            if serialError is True:
                print("SERIAL ERROR OCCURED. STOP GRACEFULLY")
                sys.exit(0)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        serialPortInstance.write(b'\x3A')
        serialPortInstance.close()
        client.loop_stop()
        client.disconnect()
        sys.exit(0)