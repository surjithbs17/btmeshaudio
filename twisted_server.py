from __future__ import print_function
import time
import bluetooth
from bluetooth.ble import DiscoveryService
import socket

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
import sys 

host_ip =socket.gethostbyname(socket.gethostname())

UDP_PORT = 14000
global device_name
device_name = 'Bose'

IP = ['localhost','localhost','localhost']
PORT = [10000,11000,12000]


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

class Echo(Protocol,LineReceiver):
	def __init__(self):
		global device_name
		self.device_name = device_name
		self.device_mac = self.discover_device()

	def dataReceived(self, data):
		"""
		As soon as any data is received, write it back.
		"""
		print("recieved " + str(data))
		if "req" in data:
			msg = "BLE_" + str(id) + "_" + self.device_mac
			print(msg)
			#self.transport.write(msg)
			self.sendLine(msg)
		elif "post" in data:
			parsed_string = data.split('_')
			print(parsed_string[2])
			self.device_mac = parsed_string[2]

	
		else:
			self.sendLine("Not valid")

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

def main():
	global id 
	if(len(sys.argv) < 2):
		print("Usage sudo python server.py 1")
	else:
		id = int(sys.argv[1])
		f = Factory()
		f.protocol = Echo
		print("Running server on " + str(PORT[int(sys.argv[1])]))
		reactor.listenTCP(PORT[int(sys.argv[1])], f)
		reactor.run()

if __name__ == '__main__':
	main()









