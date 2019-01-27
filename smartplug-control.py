from pyHS100 import SmartPlug
from pprint import pformat as pf
import time
import re
import datetime
import subprocess

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

hostup = False

print("Scanning hosts...")

for host in hosts["hosts"]:
	print(host["Name"] + "...")
	# windows
	nmap = subprocess.Popen(["ping",host["IP"], "-n", "1" ], stdout=subprocess.PIPE)
	output = nmap.stdout.read().decode('utf-8')

	if ("Reply from " + host["IP"]) not in output:
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

if hostup:
	if plug.state == "ON":
		plug.turn_off()
		print("turning off plug...")
		writelog("turning off plug")
else:
	if plug.state == "OFF":
		plug.turn_on()
		print("turning on plug...")
		writelog("turning on plug ")
	
	
	
