import time
from BMP180 import BMP180
import requests
from bs4 import BeautifulSoup
import datetime
import smbus

#API_KEY = "52890dbb0576793b8ae30ac929196d2a"
#CITY = "Fukushima"
#baseURL = "http://api.openweathermap.org/data/2.5/weather"
#URL = f'{baseURL}?q={CITY}&appid={API_KEY}'

# Define some device parameters
I2C_ADDR  = 0x3f # I2C device address, if any error, change this address to 0x27
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

URL = "http://api.openweathermap.org/data/2.5/weather?q=Fukushima&appid=52890dbb0576793b8ae30ac929196d2a"

def get_weather_data():
    response = requests.get(URL)
    data = response.json()
    return data

def display_weather(data):
    weather = data["weather"][0]["main"]
    site_pressure = data["main"]["pressure"]
    
    print("Weather: "+weather)
    #print("Pressure: ")
    #print(site_pressure)
    
def calc_alert(data):
    site_pressure = data["main"]["pressure"]
    
    if site_pressure < 1008:
        return "Headache Warning"
    else:
        return "No Alert"
    
def determine_weather(sensor_pressure, site_pressure):
    print("sensor"+str(sensor_pressure)+"\n")
    print("site"+str(site_pressure)+"\n")
    sensor_pressure = sensor_pressure
    difference = abs(sensor_pressure - site_pressure)
    
    print(difference)
    
    if difference > 0.5:
        return "Sunny"
    elif difference < 0.5:
        return "Rainy"
    else:
        return "Stable"

def get_sensor_pressure():
    bmp = BMP180()
    sensor_pressure = bmp.read_pressure()
    
    return sensor_pressure/100
    
#sensor_pressure = 1013
data = requests.get(URL).json()
weather_data = get_weather_data()
site_pressure = data["main"]["pressure"]
sensor_pressure = get_sensor_pressure()

display_weather(weather_data)
alert_level = calc_alert(weather_data)
print("Alert Level : "+alert_level)
weather = determine_weather(sensor_pressure, site_pressure)
print("Weather : "+weather)

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main():
    
  data = requests.get(URL).json()
  weather_data = get_weather_data()
  site_pressure = data["main"]["pressure"]
  sensor_pressure = get_sensor_pressure()

  #display_weather(weather_data)
  alert_level = calc_alert(weather_data)
  #print("Alert Level : "+alert_level)
  weather = determine_weather(sensor_pressure, site_pressure)
  #print("Weather : "+weather)
    
  # Main program block
  now = datetime.datetime.now()

  # Initialise display
  lcd_init()

# Send some more text
  lcd_string(str(now.year)+"."+str(now.month)+"."+str(now.day),LCD_LINE_1)
  lcd_string(str(now.hour)+"."+str(now.minute)+"."+str(now.second),LCD_LINE_2)
    
  time.sleep(10)
    
  lcd_string("Sensor: "+str(sensor_pressure)+"hPa", LCD_LINE_1)
  lcd_string("Site: "+str(site_pressure)+"hPa", LCD_LINE_2)
    
  time.sleep(10)
    
  lcd_string("Alert : "+str(alert_level), LCD_LINE_1)
  lcd_string("Weather : "+str(weather), LCD_LINE_2)
    
  time.sleep(10)

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)

