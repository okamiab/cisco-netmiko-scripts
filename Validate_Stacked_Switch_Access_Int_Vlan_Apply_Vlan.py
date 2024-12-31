from netmiko import ConnectHandler
from getpass import getpass

Username = input("Please type your username: ")
password = getpass("Please type your password: ")

##############################################################################################
# This program loops through a switch stack verify current access interface vlan configuration
# and applies the correct vlan to each interface if the current vlan is not valid.
##############################################################################################

# Create a device dictionary and pass it the ip address.
def device_config(device_ip):
    cisco_device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": Username, 
        "password": password
    }
    # Call the function and pass it the device dictionary argument.
    connect_to_device(cisco_device)

# Connect to device, output the device name.
def connect_to_device(cisco_device):
    try:
        net_connect = ConnectHandler(**cisco_device)
        hostname = net_connect.send_command("show run | sec hostname").split()[1]
        print(f"Connected to {hostname}")

        validate_current_config(net_connect) # Call the function and pass the argument.

        net_connect.disconnect() # Disconnect from the device.
        print(f"Disconnected from {hostname}")

    except Exception as e: # General exception for password or other sysetem connection.
        print(f"Failed to connect to {cisco_device['ip']} {e}")

# Validate current interface config.
def validate_current_config(net_connect):
    valid_vlan = "switchport access vlan 213" # Valid vlan config the switch interface should have.
    config_list = [ # vlan configuration list
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

    for switch in range(1, 3): # loop through the switch stack.
        for interface in range (30, 32): # loop through the each switch's interfaces.
            int_list = f"interface gig{switch}/0/{interface}"
            validate_vlan = net_connect.send_command(f"show run {int_list} | include switchport access vlan") # Extract current int vlan config.
            print(f"Validating {int_list}: {validate_vlan}") # Print output

            # Validate if current int vlan matching valid_vlan variable.
            if valid_vlan not in validate_vlan or validate_vlan == " ":
                print(f"Incorrect VLAN for {int_list}. Reconfiguring...")
                reconfigure_interface(int_list, config_list, net_connect, validate_vlan) # Call the function and pass the argument.
            else:
                print(f"{int_list} is configured with the correct VLAN.")

# Apply the correct vlan to each interface. 
def reconfigure_interface(int_list, config_list, net_connect, validate_vlan):
    commands = [f"{int_list}"] + config_list # Concatenate the two list 
    response = net_connect.send_config_set(commands) # push the commands to device.
    
    validate_vlan = net_connect.send_command(f"show run {int_list} | include switchport access vlan") # Extract current int vlan config.
    print(f"Updated Vlan for {int_list}: is {validate_vlan}") # Print output
    
# List of switches
device = ['10.20.1.100', '10.20.1.101']

for ip in device: #loop through the device list and pull each device ip.
    print(f"Connecting to IP: {ip}")
    device_config(ip) #call the device_config function and pass the paramter