from netmiko import ConnectHandler
from getpass import getpass

Username = input("Please type your username: ")
password = getpass("Please type your password: ")

################################################################################
# This program copies the device running configuration to startup configuration.
################################################################################

# Create a device dictionary and pass it the ip from the loop below.
def device_config(device_ip):
    cisco_device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": Username, 
        "password": password
    }

    # Call the connect_to_device function and pass it the device dictionary value.
    connect_to_device(cisco_device)

# Call the Netmiko module and pass it the device dictionary paramter for authenticaiton.
def connect_to_device(cisco_device):
    try:
        net_connect = ConnectHandler(**cisco_device)
        hostname = net_connect.send_command("show run | sec hostname").split()[1]
        print(f"Connected to {hostname}")
        
        bkp_run_to_startup(net_connect) # Pass the argument to function below.
        net_connect.disconnect() # Disconnect from the device.

    except Exception as e:
        print(f"Failed to connect to {cisco_device['ip']} {e}")

# Copy running device configuration to startup config.
def bkp_run_to_startup(net_connect):
    SaveRunToStart = net_connect.send_command_timing('copy running-config startup-config')
    if 'Destination filename' in SaveRunToStart:
        SaveRunToStart += net_connect.send_command_timing('\n')  # apply the next line command to accept the default config name.
        
        # Validate if startup config database is updated.
        validate_update = net_connect.send_command('show startup-config')
        for line in validate_update.splitlines(): # Search for the keyword & print the entire line.
            if "Last configuration change at" in line:
                print (line)
                break

device = ['10.205.12.13'] #List of devices IP.

for ip in device: # loop through the device list and pull each device ip.
    print(f"Connecting to IP: {ip}")
    device_config(ip) # call the device_config function and pass the argument.