from __future__ import print_function
import time
import bluetooth
from bluetooth.ble import DiscoveryService
import socket


host_ip =socket.gethostbyname(socket.gethostname())

UDP_PORT = 14000
device_name = 'Bose'

class server:
	def __init__(self,port_number,device_name):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
		self.sock.bind((host_ip,port_number))
		self.device_name = device_name

	def listen(self):
		while True:
			data,addr = self.sock.recvfrom(1024)
			print(data,addr)
			if data == 'TEST':
				reply = str(self.discover_device())
				self.sock.sendto(reply,addr)

	def discover_device(self):
		service = DiscoveryService()
		devices = service.discover(2)
		mac_addr = None
		for address, name in devices.items():
			#print(address,name)
			#print("name: {}, address: {}".format(name, address))
			if device_name in name:
				mac_addr = address
		return mac_addr
				
local_server = server(UDP_PORT,device_name)
local_server.listen()