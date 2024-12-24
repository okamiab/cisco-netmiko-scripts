from netmiko import ConnectHandler
from getpass import getpass
import time

Username = input("Please Enter username: ")
password = getpass("Please Enter your password: ")

timestr = time.strftime("%Y-%-m-%d-%H.%M.%S") # Time variable, format date/time accordingly.

########################################################################################
# This program checks for the NTP server. If it does not match the latest_ntp list, 
# it will remove the current NTP IPs from the device and apply the latest_ntp IPs to it.
########################################################################################

# Create a device dictionary and pass it the ip from the loop below.
def device_config(device_ip):
    cisco_device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": Username, 
        "password": password
    }
    connect_to_device(cisco_device) # Call the connect_to_device function and pass it the device dictionary value.

# all the Netmiko module and pass it the device dictionary paramter for authenticaiton.
def connect_to_device(cisco_device): 
    try:
        net_connect = ConnectHandler(**cisco_device)
        hostname = net_connect.send_command("sh run | sec hostname").split()[1]
        print(f"Connected to {hostname}")
    
        current_ntp = ntp_details(net_connect) # Call the ntp_deatils function and keep outcome of current_ntp here.
        update_ntp(net_connect, current_ntp) # Call update_ntp function use the paramters from the two functions listed.

    except Exception as e:
        print(f"Failed to connect to {cisco_device['ip']} {e}")

# Gather current NTP information from the device.
def ntp_details(net_connect):
    current_ntp = net_connect.send_command("sh run | sec ntp")
    print(current_ntp)
    return current_ntp # Return ouput, it will be later used inside other functions.

# Validate current_ntp against latest_ntp ips.
def update_ntp(net_connect, current_ntp): 
    # split the ntp output into a list and loop through it.
    ntp_servers = [line.split()[2] for line in current_ntp.splitlines() if "ntp server" in line]

    for ntp_ip in ntp_servers: # Verify current ntp and remove it if not matching.
        if ntp_ip not in latest_ntp:
            print(f"Outdated NTP server: {ntp_ip}")
            net_connect.send_config_set([f"no ntp server {ntp_ip}"])
        else:
            print(f"NTP server is up to date: {ntp_ip}")
    
    for ntp in latest_ntp: # Validate ntp and add new ntp if missing.
        if ntp not in ntp_servers:
            print(f"Adding missing NTP server: {ntp}")
            net_connect.send_config_set([f"ntp server {ntp} prefer"])

latest_ntp = ["10.204.3.1", "10.204.3.1"] # NTP server IPs you would like to apply to your device.

# file contains IP address of the devices that require NTP change.
with open("/path/host1.txt", "r") as file:
    IPAddresses = file.readlines() # Convert text into a list.

for ip in IPAddresses: # loop through the device list and pull each device ip.
    print(f"Connecting to IP: {ip}")
    device_config(ip) # call the device_config function and pass the paramter