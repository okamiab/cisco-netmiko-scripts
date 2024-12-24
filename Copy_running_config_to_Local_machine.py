from netmiko import ConnectHandler
from getpass import getpass
import time

Username = input('What is your username: ')
Password = getpass()

timestr = time.strftime("%Y-%-m-%d-%H.%M.%S") #Time variable, format date/time accordingly.

##########################################################################
# This program allows you to view the current device configuration and back 
# it up to a text file on your local drive.
##########################################################################

#Open the IP file that contains a list of ip addresses. This can be a simple txt file.
with open('/filepath.txt', 'r') as IPFile:
    Address = IPFile.readlines() #Convert the content of the file into a list
    
    for IP in Address: #Loop through list and remove any leading spaces.
        host = IP.strip()
        CiscoSwitch = { #Dictionary defining device type and other attributes
            'device_type': 'cisco_ios',
            'ip': host,
            'username': Username,
            'password': Password
        }
        try: #Try Connecting to the device, and run the commands below.
            net_connect = ConnectHandler(**CiscoSwitch)
            ShowRunningConfig = net_connect.send_command('show running-config')
            HostName = net_connect.send_command('show run | sec hostname').split()[1] #split the out and print first attribute
            print(f'printing running-config for {host}')
            print(f'Connecting to Host: {HostName}')
            print(ShowRunningConfig)
            
            # Open a new file to write the output from the above command.
            with open(f'/filepath/{HostName}-{timestr}.txt', 'w') as BKP:
                BKP.write(ShowRunningConfig)
                BKP.close()

        except Exception as e: #General exception for any error due to password, or command incorrect.
            print(f'Cannot connect to host {host}: {e}')

    net_connect.disconnect()