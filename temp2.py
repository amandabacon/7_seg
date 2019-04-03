#!/usr/bin/python3

# temp2.py: Everything the ADC i2c does with the addition of the temperature readout on the 7 segment display
# Author: Amanda & Inigo
# Date: 13/03/2019

import smbus
import RPi.GPIO as GPIO
from time import *

GPIO.setmode(GPIO.BOARD)
bus = smbus.SMBus(1)

#ADC device information
DEVICE_ADDRESS = 0x48
CONFIG_REGISTER = 0x1
CONVERSION_REGISTER = 0x0

#LED i2c backpack information
DEVICE_ADDRESS_2 = 0x70
CONFIG_REGISTER_2 = 0b00100001
CONVERSION_REGISTER_2 = 0x0

clock_enable = 0b00100001
row_int = 0b10100000
dimming = 0b11100111
blinking = 0b10000101

address_setting = 0b01000000
display_ram =  0b000000000
display_on = 0b10000001

def configure_backpack(bus):
	con = [0x0,0x0]
	bus.write_i2c_block_data(DEVICE_ADDRESS_2, clock_enable,con)
	bus.write_i2c_block_data(DEVICE_ADDRESS_2, row_int,con)
	bus.write_i2c_block_data(DEVICE_ADDRESS_2, dimming,con)
	bus.write_i2c_block_data(DEVICE_ADDRESS_2, blinking,con)


#define a function that will take a string value of the temperature and convert it to the number corresponding to the 7-segment display output
def choose_mode(num):
	if (num == '0'):
		return 63

	if (num =='1'):
		return 6

	if (num == '2'):
		return 91

	if (num == '3'):
		return 79

	if (num == '4'):
		return 102

	if (num == '5'):
		return 109

	if (num == '6'):
		return 125

	if (num == '7'):
		return 7

	if (num == '8'):
		return 127

	if (num == '9'):
		return 111

	else:
		return 54

#define a function that will take a string value of the temperature and convert it to the number corresponding to the 7-segment display output with a period
def choose_mode_period(num):
	if (num == '0'):
		return 63+128 #where +128 is to find the period

	if (num =='1'):
		return 6+128

	if (num == '2'):
		return 91+128

	if (num == '3'):
		return 79+128

	if (num == '4'):
		return 102+128

	if (num == '5'):
		return 109+128

	if (num == '6'):
		return 125+128

	if (num == '7'):
		return 7+128

	if (num == '8'):
		return 127+128

	if (num == '9'):
		return 111+128

	else:
		return 54+128

#define a function that will output the temperature (temp)
def write_raw_backpack(bus, temp):
	bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [1])
	bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [1])
	bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_on, [])

#the commented section below was used for debugging purposes
#	i = 128
#	while True:
#		bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [])
#		bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [i,i,i,i,i,i,i,i,i,i,i,i,i])
#		print(i)
#		sleep(1)
#		i=i+1
#	bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_on, [])

#this is where we convert the temperature to a string (and multiply by 1000 in order to move the decimal point)
	temperature = str(temp*1000)
#chooses a temperature range for the different outputs (of course it cannot read the extreme values)
	if (temp >= 100 or temp <= -100): #it should not read under -23
		if (temperature[0]=='-'):
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [])
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [64,0,choose_mode(temperature[1]),0,0,0,choose_mode(temperature[2]),0,choose_mode(temperature[3]),0])

		else:
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [])
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [0,0,choose_mode(temperature[0]),0,0,0,choose_mode(temperature[1]),0,choose_mode(temperature[2]),0])

	elif (temp >= 10 or temp <= -10):
		if (temperature[0]=='-'):
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [])
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [64,0,choose_mode(temperature[1]),0,0,0,choose_mode_period(temperature[2]),0,choose_mode(temperature[3]),0])

		else:
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [])
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [0,0,choose_mode(temperature[0]),0,0,0,choose_mode_period(temperature[1]),0,choose_mode(temperature[2]),0])
	else:
		if (temperature[0]=='-'):
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [])
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [64,0,choose_mode_period(temperature[1]),0,0,0,choose_mode(temperature[2]),0,choose_mode(temperature[3]),0])

		else:
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [])
			bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [0,0,choose_mode_period(temperature[0]),0,0,0,choose_mode(temperature[1]),0,choose_mode(temperature[2]),0])

#notes below here for debugging purposes
#
#		bus.write_i2c_block_data(device address, address_setting, [does nothing])
#                bus.write_i2c_block_data(device address, display_ram, [chunck of LED 1, nonsense number, chunck of LED 2, nonsense number, colon, nonsense number,chunck of LED 3, nonsense number,chunck of LED 4, nonsense number,])

#	for i in range(70):
#		bus.write_i2c_block_data(DEVICE_ADDRESS_2, address_setting, [1])
#		bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_ram, [i])
#		sleep(2)
#	bus.write_i2c_block_data(DEVICE_ADDRESS_2, display_on, [])
#end of notes

#defines a function that will configure the ADC
def configure_adc(bus):
	config_bytes = [0xc0, 0x83]
	bus.write_i2c_block_data(DEVICE_ADDRESS, CONFIG_REGISTER, config_bytes)

#defines a function that will get the raw data info.
def get_raw_adc_reading(bus):
	raw_reading = bus.read_i2c_block_data(DEVICE_ADDRESS,CONVERSION_REGISTER)
	MSB = raw_reading[0] << 8
	raw = MSB + raw_reading[1]
	rawstr = str(bin(raw))
	if raw >= (2**15):
		raw = 0
	return raw

#defines a function that takes the raw data and converts it to a voltage
def convert_raw_reading(raw):
	voltage = raw * 0.00015259254
	return voltage

#defines a function that converts voltage to temperature
def convert_voltage_to_temp(voltage):
	temp = voltage * 5
	return temp

#converts raw to temperature
def convert_raw_to_temp(raw):
	temp = (raw* .0035)-23
	return temp

#defines a function that initialises the GPIO pins for the 5 LEDs
def initialize_GPIO(): #sets all GPIO pins in use for LEDs
	GPIO.setup(11, GPIO.OUT)
	GPIO.setup(13, GPIO.OUT)
	GPIO.setup(15, GPIO.OUT)
	GPIO.setup(16, GPIO.OUT)
	GPIO.setup(18, GPIO.OUT)
	for i in range(3): #blinks all LEDs three times
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(13, GPIO.HIGH)
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(16, GPIO.HIGH)
		GPIO.output(18, GPIO.HIGH)
		sleep(1)
		GPIO.output(11, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
		sleep(1)

#defines a function that shines specific LEDs in ranges defined below depending on temperature
def shine_temp(temp):
	if temp < 0: #all off
		GPIO.output(11, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
	elif temp >= 0 and temp < 20: #only pin 11 on
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(13, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
	elif temp >= 20 and temp < 40: #pin 11 and 13 on (room T range)
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(13, GPIO.HIGH)
		GPIO.output(15, GPIO.LOW)
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
	elif temp >= 40 and temp < 60: #pin 11,13,15 on (fire)
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(13, GPIO.HIGH)
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(16, GPIO.LOW)
		GPIO.output(18, GPIO.LOW)
	elif temp >= 60 and temp < 80: #pin 11,13,15,16 on (fire fire)
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(13, GPIO.HIGH)
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(16, GPIO.HIGH)
		GPIO.output(18, GPIO.LOW)
	else: #anything beyond bounds--turns on (sun temp)
		GPIO.output(11, GPIO.HIGH)
		GPIO.output(13, GPIO.HIGH)
		GPIO.output(15, GPIO.HIGH)
		GPIO.output(16, GPIO.HIGH)
		GPIO.output(18, GPIO.HIGH)

#initialises the blinking in binary of the LED
def blink_initialize():
	GPIO.setup(36, GPIO.OUT)

#blinks the temperature in binary on the single LED
def blink(temp):
	print(bin(int(temp)))
	print(int(temp))
	binary_str = str(bin(int(temp)))
	for i in range(len(binary_str)):
		if binary_str[i] == '1':
			GPIO.output(36, GPIO.HIGH)
		else:
			GPIO.output(36, GPIO.LOW)
		sleep(1)
	for i in range(2):
		GPIO.output(36, GPIO.HIGH)
		sleep(.2)
		GPIO.output(36, GPIO.LOW)

#main
configure_adc(bus)
raw_ADC = get_raw_adc_reading(bus)
voltage = convert_raw_reading(raw_ADC)
temp = convert_raw_to_temp(raw_ADC)
configure_backpack(bus)

initialize_GPIO()
blink_initialize()

#infinite loop checking and printing of values
while True:
	raw_ADC = get_raw_adc_reading(bus)
	temp = convert_raw_to_temp(raw_ADC)
	print(temp)
	write_raw_backpack(bus,temp)
	shine_temp(temp)
	blink(temp)
	sleep(5)
