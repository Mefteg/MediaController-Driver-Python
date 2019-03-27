import threading
import time
import serial
from serial.tools import list_ports
import keyboard

class SerialPortListener(threading.Thread):
	def __init__(self, port, baudrate):
		threading.Thread.__init__(self)
		self.port = port
		self.baudrate = baudrate
		self.timeout = 1

		self.active = True

		self.sleep_duration = 0.01 # in seconds

	def run(self):
		#serial_instance = serial.Serial(self.port.device, self.baudrate, timeout=1)
		serial_instance = serial.Serial()
		serial_instance.port = self.port.device
		serial_instance.baudrate = self.baudrate
		serial_instance.timeout = self.timeout

		if serial_instance.isOpen():
			serial_instance.close()

		serial_instance.open()

		while self.active:
			data = serial_instance.readline()
			if len(data) > 0:
				self.process_data(str(data))

			time.sleep(self.sleep_duration)

		serial_instance.close()

	def process_data(self, data):
		print(data)

class MediaControllerListener(SerialPortListener):
	def __init__(self, port, baudrate):
		SerialPortListener.__init__(self, port, baudrate)
		self.mode = 0

	def process_data(self, data):
		if self.mode == 0:
			self.process_data_track(data)
		elif self.mode == 1:
			self.process_data_volume(data)

	def process_data_track(self, data):
		if "PLAY" in data:
			keyboard.press_and_release('play/pause media')
		elif "PREVIOUS" in data:
			keyboard.press_and_release('previous track')
		elif "NEXT" in data:
			keyboard.press_and_release('next track')	
		elif "MODE" in data:
			self.mode = (self.mode + 1) % 2

	def process_data_volume(self, data):
		if "PLAY" in data:
			keyboard.press_and_release('volume mute')
		elif "PREVIOUS" in data:
			keyboard.press_and_release('volume down')
		elif "NEXT" in data:
			keyboard.press_and_release('volume up')	
		elif "MODE" in data:
			self.mode = (self.mode + 1) % 2

class MediaControllerDriver:
	def __init__(self):
		self.listeners = []

	def list_ports(self):
		return list_ports.comports()

	def open_port(self, port, baudrate):
		listener = MediaControllerListener(port, baudrate)
		listener.start()
		self.listeners.append(listener)

	def close_port(self, port):
		for listener in self.listeners:
			if listener.port == port:
				listener.active = False
				self.listeners.remove(listener)
				break

	def close(self):
		for listener in self.listeners:
			listener.active = False

		time.sleep(2)

if __name__ == "__main__":
	print("Do something with command line parameters !")
	driver = MediaControllerDriver()
	ports = driver.list_ports()
	for port in ports:
		print(port)

	if len(ports) > 0:
		driver.open_port(ports[0], 9600)
		stop = input("Press any to quit...")