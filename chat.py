#!/usr/bin/env python3
import socket
import threading
import argparse
import random
import os
import sys
import subprocess
import urllib.request as urllib
from time import sleep

class colors:
	RED = '\033[31m'
	GREEN = '\033[32m'
	BLUE = '\033[34m'
	CYAN = '\033[36m'
	BOLD = '\033[1m'
	ORANGE = '\033[33m'
	YELLOW = '\033[33;1m'
	ENDBOLD = '\033[22m'
	ENDC = '\033[0m'

def main():
	os.system('cls' if os.name=='nt' else 'clear')

	checkForUpdates()

	parser = argparse.ArgumentParser(description='Simple python chat.')
	option = parser.add_mutually_exclusive_group()
	option.add_argument('-s', '--server', help='Start a chat server', action='store_true')
	option.add_argument('-c', '--connect', help='Connect to a server', type=str, metavar="IP")
	parser.add_argument('-p', '--port', metavar='PORT', type=int, default=5555)
	args = parser.parse_args()

	if args.connect:
		client = Client(args.connect, args.port)
	else:
		server = Server(args.port)
		server.start()

def checkForUpdates():
	print(colors.BLUE + "Checking for updates..." + colors.ENDC)
	try:
		newest = urllib.urlopen('https://raw.githubusercontent.com/toth-boldizsar/python-chat/master/version.txt')
		connection = True
	except urllib.URLError as e:
		print(colors.RED + "No internet connection" + colors.ENDC)
		connection = False
	if connection:
		newest = float(newest.read().decode('utf-8'))
		current = float(open('version.txt', 'r').read())

		if current == newest:
			print(colors.GREEN + "Script is already up to date" + colors.ENDC)
		elif current < newest:
			print(colors.ORANGE + "There is an update available")
			sleep(0.2)
			print(colors.YELLOW + 'Current version: ' + str(current))
			print('Newest version : ' + str(newest) + colors.ENDC)
			sleep(0.2)
			while True:
				update = input(colors.GREEN + 'Do you want to update?' + colors.BOLD + ' [Y/n] ' + colors.ENDC)

				if update == 'y' or update == 'Y' or update == 'n' or update == 'N' or update == '':
					break
				else:
					print(colors.ORANGE + "Invalid option selected: '" +update+"'")

			if update == 'y' or update == 'Y' or update == '':
				Update()
			else:
				return

		elif current > newest:
			print(colors.RED + colors.BOLD + "You're a wizard!" + colors.ENDC)
			sleep(0.2)
			print(colors.YELLOW + 'Current version: ' + str(current))
			print('Newest version : ' + str(newest) + colors.ENDC)
			sleep(0.2)

def Update():
	subprocess.Popen(["python3", "./update.py"])
	sys.exit(0)

class Server:

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port = 0
	termStr = ""
	
	connections = []
	running = True

	def __init__(self, port):
		self.port = port
		try:
			self.sock.bind(('0.0.0.0', port))
		except Exception as e:
			if str(e) == "[Errno 98] Address already in use":
				print(colors.RED + "Port " + colors.BOLD + str(port) + colors.ENDBOLD + " is already in use" + colors.ENDC)
			self.sock.close()
			exit()
		print (colors.CYAN + "Starting server on port " + colors.BOLD + str(port) + colors.ENDC)
		self.sock.listen(1)

		for i in range(50):
			self.termStr += chr(random.randint(0,200))
	
	def start(self):
		runThread = threading.Thread(target=self.run)
		runThread.deamon = True
		runThread.start()
		while True:
			srv = input ("")

			if srv == "/stop":
				print(colors.ORANGE + "Stopping Server..." + colors.ENDC)
				for c in self.connections:
					c.send("/exit".encode())
				sThread = threading.Thread(target=self.terminate, name="Terminator")
				sThread.deamon = True
				sThread.start()
				sleep(2)
				self.sock.close()
				break
			else:
				for c in self.connections:
					c.send(str(colors.RED + colors.BOLD + "SERVER: " + colors.ENDBOLD + srv + colors.ENDC + "\n").encode())

	def terminate(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('127.0.0.1', self.port))
		s.send(self.termStr.encode())

	def handler(self, c, a, nickname):
		while True:
			if not self.running:
				break
			data = c.recv(1024).decode('utf-8')
			if data.split("\n")[0] == "/exit":
				print(colors.RED + colors.BOLD + nickname + colors.ENDBOLD + " disconnected" + colors.ENDC)
				self.connections.remove(c)
				c.close()
				break
			else:
				print(colors.BLUE + colors.BOLD + nickname + ": " + colors.ENDBOLD + data.split("\n")[0] + colors.ENDC)
				for connection in self.connections:
					connection.send(str(colors.BLUE + colors.BOLD + nickname + ": " + colors.ENDBOLD + data + colors.ENDC + "\n").encode())
			if not data:
				print(colors.RED + colors.BOLD + nickname + colors.ENDBOLD + " disconnected" + colors.ENDC)
				self.connections.remove(c)
				c.close()
				break

	def run(self):
		while True:
			c, a = self.sock.accept()
			c.send(("version=" + str(open('version.txt', 'r').read())).encode())
			c.send("Please enter a nickname: ".split("\n")[0].encode())
			nickname = c.recv(1024).decode('utf-8').split("\n")[0]
			if nickname == self.termStr:
				break
			c.send(str(colors.GREEN + "Welcome " + colors.BOLD + nickname + colors.ENDC + "\n").encode())
			cThread = threading.Thread(target=self.handler, args=(c, a, nickname))
			cThread.deamon = True
			cThread.start()
			self.connections.append(c)
			print(colors.GREEN + colors.BOLD + nickname + colors.ENDBOLD + " connected" + colors.ENDC)

class Client:

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ip, port = None, None
	running = True
	
	def __init__(self, ip, port):
		try:
			self.sock.connect((ip, port))
		except Exception as e:
			print(colors.RED + "Couldn't connect to the server at " + colors.BOLD + ip + ":" + str(port) + colors.ENDC)
			return
		self.ip = ip
		self.port = port

		iThread = threading.Thread(target=self.send)
		iThread.deamon = True

		while self.running:
			data = self.sock.recv(1024).decode('utf-8')
			if data == "Please enter a nickname: ":
				name = input("Please enter a nickname: ")
				self.sock.send(bytes(name, 'utf-8'))
				iThread.start()
			elif data == "/exit":
				print(colors.RED + colors.BOLD + "Server closed" + colors.ENDC)
				self.running = False
				self.sock.send("/exit".encode())
				break
			elif data.split("=")[0] == "version":
				print(colors.ORANGE + "The server is running a diferent version (v" + data.split("=")[1] + ")" + colors.ENDC)

				if float(data.split("=")[1]) > open('version.txt', 'r').read():
					print(colors.BLUE + "Try updating")
				else:
					print(colors.BLUE + "Try running versions/" + data.split("=")[1] + "/chat.py")

				self.running = False
				self.sock.send("/exit".encode())
				break
			else:
				print(data.split("\n")[0])
			if not data:
				break

	def send(self):
		while self.running:
			msg = input("")
			if self.running:
				try:
					self.sock.send(bytes(msg, 'utf-8'))
				except Exception as e:
					if str(e) == "[Errno 32] Broken pipe":
						print(colors.RED + "Connection failed" + colors.ENDC)
					break
			else:
				break
			if msg == "/exit":
				break
			else:
				print("\033[s\033[2A")

if __name__ == '__main__':
	main()