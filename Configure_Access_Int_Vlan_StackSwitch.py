from netmiko import ConnectHandler
from getpass import getpass

Username = input("Please type your username: ")
password = getpass("Please type your password: ")

###################################################################################################
# This pgrogam loops through a stacked switch, configure the Access interface vlan & port security.
###################################################################################################

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

        push_config(net_connect) # Call the function and pass the parameter.
        net_connect.disconnect() # Disconnect from the device.

    except Exception as e: # General exception for password or other sysetem connection.
        print(f"Failed to connect to {cisco_device['ip']} {e}")

# Push the config to devices.
def push_config(net_connect):
    for switch in range(1, 5): # loop through the switch stack.
        for interface in range (25, 37): # loop through the each switch's interfaces.
            config_interface = [f"int gig{switch}/0/{interface}"] + config_list # Concatenate the interfaces & vlan configuation. 
            config_interface = net_connect.send_config_set(config_interface) # Connect to the device and push config change.

# vlan configuration list
config_list = [
    "switchport access vlan 213",
    "description << Printer >>",
    "switchport port-security maximum 5",
    "switchport port-security violation restrict",
    "switchport port-security aging time 60",
    "switchport port-security aging type inactivity",
    "switchport port-security",
    "storm-control broadcast level 30.00",
    "storm-control multicast level 30.00",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable",
    "ip verify source",
    "ip dhcp snooping limit rate 15",
]

# List of switches
device = ['10.20.1.111']

for ip in device: #loop through the device list and pull each device ip.
    print(f"Connecting to IP: {ip}")
    device_config(ip) #call the device_config function and pass the paramter