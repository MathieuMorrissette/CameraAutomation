from pyHS100 import SmartPlug
from pprint import pformat as pf
import time
import re
import datetime
import subprocess

is_windows = False

def writelog(string):
	now = datetime.datetime.now()
	with open('camera_log.txt', 'a') as logfile: # a == append
		logfile.write(string + " - " + str(now) + "\n")

# you can add multiple hosts here
hosts = {
	"hosts" : [
		{
			"Name" : "mathmo_phone",
			"MAC" : "",
			"IP" : "192.168.1.108" # must be static
		}
	]
}

plug = SmartPlug("192.168.1.114")

is_switch_online = False
try:
	switch_disabler = SmartPlug("192.168.1.142") # indoor cam disabler
	print(switch_disabler.state_information)
	is_switch_online = True
except:
	is_switch_online = False


hostup = False

print("Scanning hosts...")

for host in hosts["hosts"]:
	print(host["Name"] + "...")
	# windows
	if is_windows:
		command = subprocess.Popen(["ping",host["IP"], "-n", "1" ], stdout=subprocess.PIPE)
	else:
		command = subprocess.Popen(["ping",host["IP"], "-c", "1" ], stdout=subprocess.PIPE)

	output = command.stdout.read().decode('utf-8')

	if (("Reply from " + host["IP"]) not in output and is_windows) or \
	    (("bytes from " + host["IP"]) not in output and not is_windows):
		print("is DOWN")
		continue
	else:
		hostup = True
		print("is UP")
		break



# TODO add overide with hidden smart switch for people without device ( backdoor ) - ordered
# https://www.bestbuy.ca/en-ca/product/tp-link-hs200-wi-fi-smart-light-switch/13044491.aspx


print("Current plug state :")
print(plug.state)

if is_switch_online and switch_disabler.is_on: # do not record overriden
	if plug.state == "ON":
		plug.turn_off()
		print("turning off plug because switch is telling so...")
		writelog("turning off plug because of switch disabler")
else:
	if not is_switch_online and hostup: # should not happen but just in case electricity losse or something
		if plug.state == "OFF":
			plug.turn_on()
			print("turning on plug because of unusual activity...")
			writelog("turning on plug because of unusual activity")
	elif hostup:
		if plug.state == "ON": # do not record
			plug.turn_off()
			print("turning off plug...")
			writelog("turning off plug")
	else:
		if plug.state == "OFF": # host isnt there start recording
			plug.turn_on()
			print("turning on plug...")
			writelog("turning on plug ")

print("Done")
	
	
	
