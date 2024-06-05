
import telnetlib
import getpass
import os


Devices = ['192.168.179.129', '192.168.179.131', '192.168.179.132']


username = input("Please enter your username: ")
password = getpass.getpass("Please enter your password: ")


for x in Devices:
    response = os.system('ping -n 2 ' + x)

    if response == 0:

        print("Device is reachable")

        tn = telnetlib.Telnet(x)

        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        print("Telnet connection has been established with ", x)

        a = tn.read_until(b">", timeout=10).decode("ascii")

        if ">" in a:
            commands = b"""
            enable

            terminal pager 0
            show running-config
            exit
            """

            tn.write(commands)
            print(tn.read_all().decode("ascii"))
        
        elif '#' in a:
            commands = b"""
            terminal length 0
            show running-config
            exit
            """
            tn.write(commands)
            print(tn.read_all().decode("ascii"))
        
        else:
            print("Device type is unknown")

else:
    print("List is completed.")
