import telnetlib
from time import sleep
trash = open('trash_position.txt','w')
HOST = "10.65.100.11"
#conexão telnet
tn = telnetlib.Telnet(HOST,'23', timeout=10)

tn.read_until(b": ")
tn.write('isadmin'.encode('ascii') + b"\r\n")
#password
tn.read_until(b": ")
tn.write('ANS#150'.encode('ascii') + b"\r\n")
#commands
tn.write('show equipment ont status pon 1/1/3/12'.encode('ascii') + b"\n")
sleep(8)
n = tn.read_very_eager().decode("utf-8")
trash.write(n)
print(n) 
sleep(0.1)
tn.close()