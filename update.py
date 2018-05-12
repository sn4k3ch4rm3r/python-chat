#!/usr/bin/env python3
import urllib
from os import system

def main():
	try:
		chat = urllib.urlopen('https://raw.githubusercontent.com/toth-boldizsar/python-chat/master/chat.py').read().decode('utf-8')
		version = urllib.urlopen('https://raw.githubusercontent.com/toth-boldizsar/python-chat/master/version.txt').read().decode('utf-8')
	except urllib.URLError as e:
		print('Connection failed')
		exit()
	oldversion = open('version.txt', 'r').read()

	system('mkdir versions')
	system('mkdir versions/'+oldversion)
	system('mv chat.py versions/'+oldversion)
	system('mv version.txt versions/'+oldversion)

	chatFile = open('chat.py', 'w+')
	versionFile = open('version.txt', 'w+')

	chatFile.write(chat)
	versionFile.write(version)
	chatFile.close()
	versionFile.close()

	system('chmod +x chat.py')

	print("\nUpdate ready")
	exit()

if __name__ == "__main__":
	main()