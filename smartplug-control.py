from pyHS100 import SmartPlug
from pprint import pformat as pf
import time
import re
import datetime
import subprocess
from enum import Enum
import os

is_windows = False

class State(Enum):
	OFFLINE = 0
	ON = 1
	OFF = 2

class HostState(Enum):
	AWAY = 0
	ONLINE = 1

def writelog(string):
	now = datetime.datetime.now()
	with open(os.path.expanduser('~/camera_log.txt'), 'a') as logfile: # a == append
		logfile.write(string + " - " + str(now) + "\n")

# get tp link smart device state
def getdevicestate(device):
	try:
		test = device.state_information
		
		if device.state == "ON":
			return State.ON
		else:
			return State.OFF

		return device.state
	except:
		return State.OFFLINE

def gethoststate():
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

	print("Scanning hosts...")

	for host in hosts["hosts"]:
		print(host["Name"] + "...")
		# windows
		if is_windows:
			command = subprocess.Popen(["ping",host["IP"], "-n", "4" ], stdout=subprocess.PIPE)
		else:
			command = subprocess.Popen(["ping",host["IP"], "-c", "4" ], stdout=subprocess.PIPE)

		output = command.stdout.read().decode('utf-8')

		if (("Reply from " + host["IP"]) not in output and is_windows) or \
			(("bytes from " + host["IP"]) not in output and not is_windows):
			print("is DOWN")
			continue
		else:
			return HostState.ONLINE
			break

	return HostState.AWAY

plug = SmartPlug("192.168.1.114")
plug_state = getdevicestate(plug)

if plug_state == State.OFFLINE:
	print("Unexpected error plug is offline")
	writelog("Unexpected error plug is offline")
	exit(0)

# disabler switch -> force disable the recording of the indoor cameras
disabler_switch = SmartPlug("192.168.1.142")
disabler_switch_state = getdevicestate(disabler_switch)

# force record switch
force_record_switch = SmartPlug("192.168.1.147") 
force_record_switch_state = getdevicestate(force_record_switch)

host_state = gethoststate()

max_retry = 4
retry_count = 0

# sometimes device doesnt respond so making really sure it is really away
while host_state == HostState.AWAY and retry_count < max_retry:
	time.sleep(10) # sleep 10 seconds
	host_state = gethoststate()
	retry_count = retry_count + 1


print("Current states :")
print("host " + host_state.name)
print("smartplug " + plug_state.name)
print("disabler switch " + disabler_switch_state.name)
print("force record switch " + force_record_switch_state.name)

if force_record_switch_state == State.ON:
	if plug_state == State.OFF:
		plug.turn_on()
		print("turning on plug because of force record switch...")
		writelog("turning on plug because of force record switch")

elif disabler_switch_state == State.ON:
	if plug_state == State.ON:
		plug.turn_off()
		print("turning off plug because of disabler switch...")
		writelog("turning off plug because of disabler switch")

elif disabler_switch_state == State.OFFLINE or force_record_switch_state == State.OFFLINE:
	if plug_state == State.OFF:
		plug.turn_on()
		print("turning on plug because of unusual activity...")
		writelog("turning on plug because of unusual activity disabler: ")

elif host_state == HostState.ONLINE:
	if plug_state == State.ON: 
		plug.turn_off()
		print("turning off plug because host is online...")
		writelog("turning off plug because host is online")

else:
	if plug_state == State.OFF: 
		plug.turn_on()
		print("turning on plug because host is away...")
		writelog("turning on plug because host is away")
			
print("Printing Final States :")
print("host " + host_state.name)
print("smartplug " + plug_state.name)
print("disabler switch " + disabler_switch_state.name)
print("force record switch " + force_record_switch_state.name)

print("Done")
	
	
	
