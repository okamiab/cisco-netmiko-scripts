from netmiko import ConnectHandler
from getpass import getpass

Username = input("Please type your username: ")
password = getpass("Please type your password: ")

###################################################################################
# This program configures Access port vlan configuration for specific switch ports.
###################################################################################

# Create a device dictionary and pass it the ip from the loop below.
def device_config(device_ip): 
    cisco_device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": Username, 
        "password": password,
    }
    connect_to_device(cisco_device) #Call the connect_to_device function and pass it the device dictionary value.

# Call the Netmiko module and pass it the device dictionary paramter for authenticaiton.
def connect_to_device(cisco_device): 
    try:
        net_connect = ConnectHandler(**cisco_device)
        hostname = net_connect.send_command("show run | sec hostname").split()[1]
        print(f"Connected to {hostname}")

        change_vlan(net_connect) # call change_vlan function and pass it the net_connect parameter.
        net_connect.disconnect() # Disconnect from device

    except Exception as e: # General Error exception
        print(f"Failed to connect to {cisco_device['ip']} {e}")

# Change interface vlan config.
def change_vlan(net_connect):
    for int in switch_interfaces: #loop through interfaces and apply change.
        # concatenate first list & 2nd into a new list and pass the list to config_set command.
        commands = [f"int {int}"] + vlan_detail
        net_connect.send_config_set(commands)

# Interface vlan config.
vlan_detail = [
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

switch_interfaces = ["gig1/0/25", "gig1/0/26"] # List of interfaces part of the vlan change.

device = ['10.20.1.111'] # List of device to apply change to.

for ip in device: # loop through the device list and pull each device ip.
    print(f"Connecting to IP: {ip}")
    device_config(ip) # call the device_config function and pass the paramter