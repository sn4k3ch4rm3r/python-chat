#!/usr/bin/env python3
import urllib
from os import system

def main():
	try:
		chat = urllib.request.urlopen('https://raw.githubusercontent.com/toth-boldizsar/python-chat/master/chat.py').read().decode('utf-8')
		updater = urllib.requesr.urlopen('https://raw.githubusercontent.com/toth-boldizsar/python-chat/master/update.py').read().decode('utf-8')
		version = urllib.request.urlopen('https://raw.githubusercontent.com/toth-boldizsar/python-chat/master/version.txt').read().decode('utf-8')
	except urllib.request.URLError as e:
		print('Connection failed')
		exit()
	oldversion = open('version.txt', 'r').read()

	try:
		system('mkdir versions')
	except Exception:
		pass
	try:
		system('mkdir versions/'+oldversion)
	except Exception:
		pass

	system('mv chat.py versions/'+oldversion)
	system('mv version.txt versions/'+oldversion)

	chatFile = open('chat.py', 'w+')
	updaterFile = open('update.py', 'w')
	versionFile = open('version.txt', 'w+')

	chatFile.write(chat)
	updaterFile.write(updater)
	versionFile.write(version)
	chatFile.close()
	updaterFile.close()
	versionFile.close()

	system('chmod +x chat.py')

	print("\nUpdate ready")
	exit()

if __name__ == "__main__":
	main()