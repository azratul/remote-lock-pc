#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PYTHON VERSION: 2.7

import bluetooth
import os
import time
import datetime

target_address = None
lock_cmd       = ["loginctl lock-session", "gnome-screensaver-command --lock"]
unlock_cmd     = ["loginctl unlock-session", "gnome-screensaver-command -d"]
total_services = 0

CMD           = 1 # POR DEFECTO SE UTILIZA EL PRIMER COMANDO DE LA LISTA("lock_cmd", "unlock_cmd")
SLEEP_TIME    = 1
DISCOVER_TIME = 4
DEBUG_MODE    = False
ARROW         = '➔'

def scan():
	try:
		global target_address, total_services
		target_name = raw_input(" Ingrese nombre de dispositivo " + ARROW + " ")

		for bdaddr in bluetooth.discover_devices(duration = DISCOVER_TIME):
			if DEBUG_MODE == True:
				print(" [{0}]".format(bdaddr))

			if target_name == bluetooth.lookup_name(bdaddr):
				target_address = bdaddr
				total_services = len(bluetooth.find_service(address = bdaddr))
				break
	except KeyboardInterrupt:
		pass

def settings():
	try:
		global lock_cmd, unlock_cmd
		print(" Por defecto: [{0}]".format(lock_cmd[CMD]))
		input = raw_input(" Ingrese comando para bloquear " + ARROW + " ")

		if input != "":
			lock_cmd[CMD] = input

		print(" Por defecto: [{0}]".format(unlock_cmd[CMD]))
		input = raw_input(" Ingrese comando para desbloquear " + ARROW + " ")

		if input != "":
			unlock_cmd[CMD] = input
	except KeyboardInterrupt:
		pass

def play():
	state = 1
	file  = open('lock.log', 'w')
	print(" Para volver al menú presionar Ctrl+C... ")
	try:
		while True:
			check    = False
			device   = bluetooth.lookup_name(target_address, timeout = 20)
			services = bluetooth.find_service(address = target_address)

			if device != None and len(services) >= total_services:
				check = True

			event = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

			if DEBUG_MODE == True:
				print(" [{0}] [{1}] [{2}] [{3}]".format(event, check, device, len(services)))

			# I DON'T WANT TO USE A FUNCTION FOR THIS, BECAUSE THE COST IS TOO HIGH(WE'RE IN A LOOP HERE)
			if check == True:
				if state == 0:
					os.system(unlock_cmd[CMD])
					output = " [" + event + "] " + ARROW + " [DESBLOQUEADO]"
					print(output)
					file.write(output + '\n')
					file.flush()
				state = 1
			else:
				if state == 1:
					os.system(lock_cmd[CMD])
					output = " [" + event + "] " + ARROW + " [BLOQUEADO]"
					print(output)
					file.write(output + '\n')
					file.flush()
				state = 0

			time.sleep(SLEEP_TIME)
	except KeyboardInterrupt:
		pass
	finally:
		file.close()

def menu():
	try:
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
				print(' Dispositivo encontrado: {0}, Servicios: {1}'.format(target_address, total_services))

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
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	menu()
