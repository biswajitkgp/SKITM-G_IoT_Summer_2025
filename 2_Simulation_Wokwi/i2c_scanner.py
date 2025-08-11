# i2c_scanner.py
from machine import Pin, I2C

# Use the same pins as your main project
I2C_SDA_PIN = 21
I2C_SCL_PIN = 22

i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)

print('Scanning I2C bus...')
devices = i2c.scan()

if len(devices) == 0:
    print("No I2C devices found!")
else:
    print('I2C devices found:', len(devices))
    for device in devices:
        # The address is printed in hexadecimal format
        print("Device found at address: " + hex(device))