from netmiko import ConnectHandler
import time
from getpass import getpass

# pass Credentials
Username = input('What is your username: ')
Password = getpass()

timestr = time.strftime("%Y-%-m-%d-%H.%M.%S") #Time variable, format date/time accordingly.

#Open the IP file
with open('/IP_filePath.txt', 'r') as IPfile:
    ipAdd = IPfile.readlines()

#Loop through the IP file and connect to each device
for ip in ipAdd:
    host = ip.strip()
    CiscoSwitch = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': Username,
        'password': Password
    }

    net_connect = ConnectHandler(**CiscoSwitch) #Connect to device
    HostName = net_connect.send_command('sh run | sec hostname').split()[1] #Print device Hostname
    print(f'Connecting to: {HostName}')

    #Initiating the backup command with send_command_timing to handle the interactive nature
    Backup_config = net_connect.send_command_timing('copy running-config tftp:')

    #If below string is inside the Backup variable provide the tftp server ip address
    if 'Address or name of remote host' in Backup_config: 
        Backup_config += net_connect.send_command_timing('1.1.1.1')
        
    #If below string is inside the Backup variable provide what the file name should be.
    if 'Destination filename' in Backup_config:
        #Retrive the host name from the for loop below and apply timestamp
        Backup_config += net_connect.send_command_timing(f'{HostName}-{timestr}\n')


net_connect.disconnect()