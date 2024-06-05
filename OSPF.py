import telnetlib
import getpass
import os

Devices = ['192.168.179.132', '192.168.179.131', '192.168.179.129']

username = input("Please enter your username: ")
password = getpass.getpass("Please enter your password: ")

for x in Devices:
    response = os.system('ping -n 2 ' + x)  # Use '-n' for Windows systems

    if response == 0:
        print(f"Device {x} is reachable")

        tn = telnetlib.Telnet(x)

        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        a = tn.read_until(b">", timeout=10).decode('ascii')

        if "#" in a:
            tn.write(b"configure terminal\n")
            tn.read_until(b"(config)#")
        elif ">" in a:
            tn.write(b"enable\n")
            tn.read_until(b"Password: ")
          #  tn.write(password.encode('ascii') + b"\n")
            tn.write(b"\n")
            tn.read_until(b"#")
            tn.write(b"configure terminal\n")
            tn.read_until(b"(config)#")
        else:
            print(f"Failed to determine the prompt type for device {x}")
            tn.close()
            continue

        process_id = input("Please enter the process ID: ")
        network = input("Please enter the network you want to advertise in OSPF: ")
        wildcard = input("Please enter the wildcard/subnet mask bits: ")
        area_id = input("Please enter the area id: ")

        tn.write(f"router ospf {process_id}\n".encode('ascii'))
        tn.read_until(b"(config-router)#")
        tn.write(f"network {network} {wildcard} area {area_id}\n".encode('ascii'))
        tn.read_until(b"(config-router)#")

        tn.write(b"end\n")
        tn.read_until(b"#")

        if "asa" in a.lower():
            tn.write(b"terminal pager 0\n")
        else:
            tn.write(b"terminal length 0\n")
        tn.read_until(b"#")

        tn.write(b"show running-config\n")
        output = tn.read_until(b"#").decode('ascii')
        print(output)

        tn.write(b"exit\n")
        tn.close()

    else:
        print(f"Device {x} is not reachable.")
