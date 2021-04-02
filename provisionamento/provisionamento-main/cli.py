import PySimpleGUI as sg
import telnetlib
from time import sleep
from datetime import datetime

def free_position(host,position,vlan,nap):
    #-separa posiçõEs utilizadas na PON 
    trash = open('trash_position.txt','r')
    clean = open("clean_position.txt","w")
    n = trash.readlines()
    for line in n: 
      if (line[:4] == "1/1/"): 
        if(line[19] == "/"):
          clean.write(line[20:23])
          clean.write("\n")
        elif(line[20] == "/"):
          clean.write(line[21:24])
          clean.write("\n")
        elif(line[21] == "/"):
          clean.write(line[22:25])
          clean.write("\n")  
        else:
          clean.write(line[19:22])     
          clean.write("\n")       
    clean.write("0")
    clean.close()
    trash.close()

    #-procura posição sem uso na PON
    clean = open("clean_position.txt","r")
    positions = clean.readlines()
    count = 0

    for line in positions:
      count = count + 1 
      free = line[:3]
      if (int(free) - count != 0):
      
        break
    clean.close()
    if (count == 129):
        print("PON Lotada")
      
        
    print(100*'=')    
    print('Posição livre:',count)
    print(100*'=')
    
    
    log = open('log.txt','a')
    username = values['username']
    date = datetime.now().strftime('data: %d/%m/%y %H:%M')
    tecnico = values['tecnico']
    serial = values['serial']
    log.write(f'\n{date}  {tecnico}  {nap}  {serial}  {position, count}  {host}  {username}')
    log.close()

    


#======================EX3CUT4 COMAND0S NO CLI
def cli(command,host,position=0,vlan=0,nap=0):
    trash = open('trash_position.txt','w')

    #conexão telnet
    tn = telnetlib.Telnet(host,'23', timeout=20)

    tn.read_until(b": ")
    tn.write('isadmin'.encode('ascii') + b"\r\n")
    #password
    tn.read_until(b": ")
    tn.write('ANS#150'.encode('ascii') + b"\r\n")
    #commands
    tn.write(command.encode('ascii') + b"\n")
    sleep(8)
    n = tn.read_very_eager().decode("utf-8")
    
    trash.write(n)
    
    trash.close()
    print(n) 
    sleep(0.1)
    tn.close()

    print(100*'=')
    
    free_position(host,position,vlan,nap)


#========================PR0CUR4 NAP NO BANCO DE DADOS - PROVISIONAMENT0
def nap_data():
    n = input('nap: ')
    if n[:5] != 'teste' and n[:3] != 'NAP':
      n = 'NAP-' + n.replace('nap-','')
    data = open('data.txt')
    naps = data.readlines()
    for line in naps:
        nap = line[:9].replace(',','').strip()
        position_barra = line[10:18].replace(',','' ).strip()
        vlan = line[19:22].replace(',','').strip()
        position_hifen = line[22:30].replace(',','').strip()
        ip = line[30:43].replace(',','').strip()
        if nap == n:
             break
         
    
    print('\n AGUARDE...\n')
    command = f'show equipment ont status pon {position_barra}'

    cli(command,ip,position_hifen,vlan,nap)
nap_data()