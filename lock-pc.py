#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON VERSION: 2.7

import bluetooth
import os
import time
import datetime

target_address = None
lock_cmd       = "loginctl lock-session"
unlock_cmd     = "loginctl unlock-session"

SLEEP_TIME = 1
ARROW      = '➔'

def scan():
	try:
		global target_address
		target_name = raw_input(" Ingrese nombre de dispositivo " + ARROW + " ")
		nearby_devices = bluetooth.discover_devices()
		for bdaddr in nearby_devices:
			if target_name == bluetooth.lookup_name(bdaddr):
				target_address = bdaddr
				break
	except KeyboardInterrupt:
		pass

def settings():
	try:
		global lock_cmd, unlock_cmd
		print(" Por defecto: [{0}]".format(lock_cmd))
		input = raw_input(" Ingrese comando para bloquear " + ARROW + " ")

		if input != "":
			lock_cmd = input

		print(" Por defecto: [{0}]".format(unlock_cmd))
		input = raw_input(" Ingrese comando para desbloquear " + ARROW + " ")

		if input != "":
			unlock_cmd = input
	except KeyboardInterrupt:
		pass

def play():
	check = False
	state = 1
	print(" Para volver al menú presionar Ctrl+C... ")
	try:
		while True:
			nearby_devices = bluetooth.discover_devices()
			for bdaddr in nearby_devices:
				if bdaddr == target_address:
					check = True
					break
				check = False

			event = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

			if check == True:
				if state == 0:
					os.system(unlock_cmd)
					print(" [{0}] {1} [DESBLOQUEADO]".format(event, ARROW))
				state = 1
			else:
				if state == 1:
					os.system(lock_cmd)
					print(" [{0}] {1} [BLOQUEADO]".format(event, ARROW))
				state = 0

			time.sleep(SLEEP_TIME)
	except KeyboardInterrupt:
		pass

def menu():
	while True:
		os.system('clear')
		print('''\033[1;31m
  ╔══════════════════════════════════╗
  ║ ★ L O C K / U N L O C K   P C  ★ ║
  ╚══════════════════════════════════╝
 \033[0;37m
 \033[1;37m ❶\033[0;37m  BUSCAR DISPOSITIVO\033[0;37m
 \033[1;37m ❷\033[0;37m  ACTIVAR LOCK/UNLOCK\033[0;37m
 \033[1;37m ❸\033[0;37m  CONFIGURAR COMANDOS\033[0;37m
 \033[1;37m ❹\033[0;37m  SALIR\033[0;37m
''')
		if target_address != None:
			print(' Dispositivo encontrado: {0}'.format(target_address))

		opt = raw_input(" Ingrese Opción " + ARROW + " ")

		if opt == "1":
			scan()
		elif opt == "2":
			play()
		elif opt == "3":
			settings()
		elif opt == "4":
			print('\033[1;32m¡ H A S T A  L U E G O !\033[0;37m')
			break

if __name__ == "__main__":
	menu()
