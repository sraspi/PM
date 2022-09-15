import time
import board
import adafruit_tca9548a
from adafruit_bme280 import basic as adafruit_bme280
# Create I2C bus as normal
i2c = board.I2C()
# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)
#--------------------------------------------------------------------
# NOTE!!! This is the "special" part of the code
#
# Create each BME280 using the TCA9548A channel instead of the I2C object
bme1 = adafruit_bme280.Adafruit_BME280_I2C(tca[1]) # TCA Channel 0
bme2 = adafruit_bme280.Adafruit_BME280_I2C(tca[1]) # TCA Channel 1
bme3 = adafruit_bme280.Adafruit_BME280_I2C(tca[2]) # TCA Channel 2
bme4 = adafruit_bme280.Adafruit_BME280_I2C(tca[3]) # TCA Channel 3
bme5 = adafruit_bme280.Adafruit_BME280_I2C(tca[4]) # TCA Channel 4
print("Five BME280 Example")
while True:
    # Access each sensor via its instance
    pressure1 = bme1.pressure
    pressure2 = bme2.pressure
    pressure3 = bme3.pressure
    pressure4 = bme4.pressure
    pressure5 = bme5.pressure
    print()
    temperature1 = bme1.temperature
    temperature2 = bme2.temperature
    temperature3 = bme3.temperature
    temperature4 = bme4.temperature
    temperature5 = bme5.temperature
    print()
    humidity1 = bme1.humidity
    humidity2 = bme2.humidity
    humidity3 = bme3.humidity
    humidity4 = bme4.humidity
    humidity5 = bme5.humidity
    print("-"*20)
    print("BME280 #1 Humidity =", humidity1)
    print("BME280 #2 Humidity =", humidity2)
    print("BME280 #3 Humidity =", humidity3)
    print("BME280 #4 Humidity =", humidity4)
    print("BME280 #5 Humidity =", humidity5)
    print("BME280 #1 Temperature =", temperature1)
    print("BME280 #2 Temperature =", temperature2)
    print("BME280 #3 Temperature =", temperature3)
    print("BME280 #4 Temperature =", temperature4)
    print("BME280 #5 Temperature =", temperature5)
    print("BME280 #1 Pressure =", pressure1)
    print("BME280 #2 Pressure =", pressure2)
    print("BME280 #3 Pressure =", pressure3)
    print("BME280 #4 Pressure =", pressure4)
    print("BME280 #5 Pressure =", pressure5)
    print()
    print()
    time.sleep(10)
