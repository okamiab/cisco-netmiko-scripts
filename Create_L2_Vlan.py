from netmiko import ConnectHandler
from getpass import getpass

Username = input("Enter username: ")
Password = getpass("Enter password: ")

###################################################################
# This program loops through a list of switch IPs inside a text file
# And apply L2 vlan config to each device.
###################################################################

# Create a device dictionary and pass it the ip from the loop below.
def device_config(device_ip): 
    cisco_device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": Username, 
        "password": Password
    }
    # Call the connect_to_device function and pass it the device dictionary value.
    connect_to_device(cisco_device)

# Call the Netmiko module and pass it the device dictionary paramter for authenticaiton.    
def connect_to_device(cisco_device):
    try:
        net_connect = ConnectHandler(**cisco_device)
        hostname = net_connect.send_command("show run | sec hostname").split()[1]
        print(f"Connected to {hostname}")
        
        vlan_info(net_connect) # pass the net_connect to device_loop function.
        net_connect.disconnect() # Disconnect from device.

    except Exception as e: # Handle password or other general errors.
        print(f"Failed to connect to {cisco_device['ip']} {e}")

# Loop through vlan dictionary, get it's key value.
def vlan_info(net_connect): 
    for vlan in vlan_list:
        id = vlan.get('id')
        name = vlan.get('name')

        # get the id & name values pass it to get_command dictionary
        vlan_commands = get_commands(id, name)
        apply_vlan(vlan_commands, net_connect) #Pass the paramters value to apply_vlan.

# Retrive vlan information & return it in a list format.
def get_commands(id, name):
   return [f"vlan {id}", f"name {name}"]

# Apply vlan to switch.
def apply_vlan(vlan_commands, net_connect):
      net_connect.send_config_set(vlan_commands)

if __name__ == "__main__":
    # Vlan dictionary
    vlan_list = [{"id": "500", "name": "Test1"}, {"id": "501", "name": "Test2"}]

    # List of devices IP file.
    with open("/directorypath/host1.txt", "r") as file:
        ip_add = file.readlines()

    for ip in ip_add: # loop through the device list and pull each device ip.
        print(f"Connecting to IP: {ip}")
        device_config(ip) # call the device_config function and pass the paramter