import subprocess
import os
import random
from getmac import get_mac_address
import netifaces
import time
import platform
from colorama import Fore, init
init(autoreset = True)




def Banner() -> None:
	print(Fore.CYAN + "    __  ______   ______   _____                   ____")
	print(Fore.CYAN + "   /  |/  /   | / ____/  / ___/____  ____  ____  / __/__  _____")
	print(Fore.CYAN + "  / /|_/ / /| |/ /       \__ \/ __ \/ __ \/ __ \/ /_/ _ \/ ___/")
	print(Fore.CYAN + " / /  / / ___ / /___    ___/ / /_/ / /_/ / /_/ / __/  __/ /")
	print(Fore.CYAN + "/_/  /_/_/  |_\____/   /____/ .___/\____/\____/_/  \___/_/ ")
	print(Fore.CYAN + "                           /_/")
	print(Fore.RED + "Advanced MAC Spoofer v1.0.0.1")
	print(Fore.RED + "Developed By HackPure\n\n")



def detectOS() -> str:
	'Returns The Current Operating System.' 
	operatingSystem = platform.system()
	time.sleep(1)
	return operatingSystem


def clrsrc() -> None:
	'Clears The Terminal.'
	checkOS =  detectOS()
	if(checkOS == 'Linux'):
		subprocess.call("clear", shell = True)
	elif(checkOS == 'Windows'):
		subprocess.call("cls", shell = True)


def checkInterfaceByUser(interface: str) -> bool:
	'Checks For The Interface That Is Passed By The User is Present or Not.'
	interfaces = netifaces.interfaces()
	if (interface not in interfaces):
		return False
	else:
		return True

def truncatePreviousErrors(errorFile = 'errors.txt') -> None:
	file = open(errorFile, 'w')
	file.truncate()
	file.close()


def getInterfaces() -> None:
	'Gets All The Interfaces Present On The Device.'
	interfaces = netifaces.interfaces()
	print(Fore.CYAN + "\n[+] Attempting To Get All The Interfaces ...")
	for interface in interfaces:
		time.sleep(1)
		print(Fore.GREEN + "[+]", interface)


def changeMAC(interface : str, macAddress : str) -> None:
	print(Fore.CYAN + "[+] Attempting To Get Current MAC Address Of The Interface", interface)
	currentMACAddress = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
	time.sleep(1)
	print(Fore.GREEN + "[+] Current MAC Address For", interface, "Is", currentMACAddress)
	print(Fore.CYAN + "[+] Attempting To  Change The State Of", interface, "from Up to Down")
	subprocess.call("ifconfig " + interface + " down", shell = True)
	time.sleep(1)
	print(Fore.GREEN + "[+] Interface Down Success !")
	time.sleep(1)
	print(Fore.CYAN + "[+] Attempting To Change MAC Adress From", currentMACAddress, "To", macAddress)
	truncatePreviousErrors()
	try:
		errorFile = open("errors.txt", "a")
		subprocess.run("ifconfig " + interface + " hw ether " + macAddress, shell = True, check = True, stderr = errorFile)
	except:
		print(Fore.RED + "[-] Error Changing MAC Address !")
		time.sleep(2)
		print(Fore.RED + "[+] Generating Error Logs \n[+] Errors Saved In", os.getcwd()+"/errors.txt")
		time.sleep(2)
		print(Fore.CYAN + "[+] Attempting To Switch Back State From Down To Up")
		subprocess.call("ifconfig " + interface + " up", shell = True)
		print(Fore.GREEN + "[+] Interface State Change SuccessFull !")
	else:
		time.sleep(1)
		print(Fore.GREEN + "[+] Attempt SucessFull \n[+] MAC Changed SuccessFully !")
		time.sleep(1.5)
		print(Fore.CYAN + "[+] Attempting To Switch Back State From Down To Up")
		subprocess.call("ifconfig " + interface + " up", shell = True)
		time.sleep(0.5)
		print(Fore.GREEN + "[+] Interface State Change SuccessFull !")
		time.sleep(1)
		print(Fore.CYAN + "[+] Getting Updated MAC Address...")
		time.sleep(2)
		updatedMACAddress = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
		print(Fore.GREEN + "[+] Updated MAC Address", updatedMACAddress)


def scanNetwork() -> None:
	mac_list = []
	gatewayIP = netifaces.gateways()['default'][2][0]
	print_ip = gatewayIP[:gatewayIP.rfind(".")] + ".0"
	print(Fore.YELLOW + "[+] Broadcasting ARP Request with range of IP Addresses", print_ip, "with Subnet Of /24")
	for ip in range(256):
		scan_ip = gatewayIP[:gatewayIP.rfind(".")] + "."+str(ip)
		ipMAC = get_mac_address(ip=scan_ip)
		if(ipMAC):
			mac_list.append()
			if(scan_ip == gatewayIP):
				print(Fore.GREEN + "[+] Packet Recieved From", scan_ip, "Having MAC", ipMAC, "[Default Gateway]")
			else:
				print(Fore.GREEN + "[+] Packet Recieved From", scan_ip, "Having MAC", ipMAC)
		else:
			pass
	print(Fore.GREEN + "[+] Scan Completed")
	return mac_list



def randomMACChange(interface) -> None:
	time.sleep(0.8)
	print(Fore.CYAN + "\n[+] Attempting To Get A Random MAC")
	time.sleep(0.8)
	print(Fore.CYAN + "[+] Getting Random MAC Address From Pool Of MAC Addresses ...")
	randomMACFile = open("randomMAC.txt", "r").read().splitlines()
	randomMAC = random.choice(randomMACFile)
	time.sleep(1.5)
	print(Fore.CYAN + "[+] Performing A Basic Check ...")
	time.sleep(0.5)
	print(Fore.CYAN + "[+] Attempting To Capture Your Current MAC For Interface", interface)
	flag = True
	while flag:
		if(netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr'] != randomMAC):
			print(Fore.CYAN + "[+] Attempting To Change The MAC Address.\n[+] Hold Tight")
			changeMAC(interface, randomMAC)
			flag = False
		else:
			print(Fore.RED + "[-] Error Failed Due To Current MAC is Same As Random MAC ...")
			print(Fore.RED + "[+] Retrying ...")
			time.sleep(1.2)
			continue

def Documentation() -> None:
	time.sleep(1)
	docs = open("documentation.txt", "r").read()
	print(docs)


try:
	def driverCode() -> None:
		clrsrc()
		time.sleep(0.8)
		print(Fore.CYAN + "[+] Perofrming OS Detection ...")
		time.sleep(1.5)
		print(Fore.CYAN + "[+] Operating System Detected", detectOS())
		time.sleep(1)
		clrsrc()
		Banner()
		time.sleep(1.5)
		print(Fore.YELLOW + "[1] Random MAC Spoof")
		print(Fore.YELLOW + "[2] NetScan")
		print(Fore.YELLOW + "[3] Custom MAC Spoof")
		print(Fore.YELLOW + "[4] Documentation")
		print(Fore.YELLOW + "[5] Exit\n")
		while True:
			try:
				userChoice = int(input(Fore.YELLOW + "MACSpoofer ~# "))
			except ValueError:
				print(Fore.RED + "[-] Invalid Input Detected !")
				continue
			else:
				if userChoice == 1:
					getInterfaces()
					userInterface = input(Fore.YELLOW + "\nEnter Interface Name ~# ")
					if(checkInterfaceByUser(userInterface)):
						randomMACChange(userInterface)
					else:
						print(Fore.RED + "[-] An Unknown Error Occured !!\n[-] Try Again")
						clrsrc()
						driverCode()
				elif userChoice == 2:
					getInterfaces()
					scanNetwork()
					userInterface = input(Fore.YELLOW + "Enter Interface Name ~# ")
					if(checkInterfaceByUser(userInterface)):
						newMAC = input("Enter Any MAC Recieved From Above Scan ~# ")
						changeMAC(userInterface, newMAC)
					else:
						print(Fore.RED + "[-] An Unknown Error Occured !!\n[-] Try Again")
						clrsrc()
						driverCode()
				elif userChoice == 3:
					getInterfaces()
					userInterface = input(Fore.YELLOW + "Enter Interface Name ~# ")
					if(checkInterfaceByUser(userInterface)):
						randomMAC = input("Enter New Random MAC [Format = 00:11:22:33:44:55] ~# ")
						changeMAC(userInterface, randomMAC)
					else:
						print(Fore.RED + "[-] An Unknown Error Occured !!\n[-] Try Again")
						clrsrc()
						driverCode()
				elif userChoice == 4:
					Documentation()
				elif userChoice == 5:
					print("Thanks For Using MACSpoofer \nHappy Hacking ;)")
					time.sleep(0.5)
					exit()
	driverCode()
except KeyboardInterrupt:
	print(Fore.RED + "\n[-] KeyBoard Interrupt Key Detected \nexit code 1")
	time.sleep(0.5)
	exit()
