import PySimpleGUI as sg
import telnetlib
from time import sleep
from datetime import datetime
import os

#TEMA LAYOUTS
sg.theme('tema') 
###########################################################################################################################################################
#                                                               COLUNA, B0TÕES E INPUTS
###########################################################################################################################################################

col = [    
            [sg.Text('\r')],
            [sg.Text('Username               Password')],
            [sg.InputText(size=(15,1),key='username',border_width=1),sg.InputText(size=(14,1),key='password',border_width=1)],#INPUTS USERNAMEN E PASSWORD
            [sg.Text('Tecnico                   Serial')],
            [sg.Combo(['Caio' ,'Edgar' ,'Felipe' ,'Fernando JK','Fernando RF','Joelson' ,'Jose Cesar' ,'Josivam' ,'Juracy' ,'Leandro' ,'Paulo'  ,'Renardio' ,'Ricardo' ,'Rodrigo' ,'Suporte', 'Vilson' ,'Vitor','Willes'], size=(13,100),key='tecnico'),sg.InputText(' ', size=(14,1),key='serial',border_width=1)],
            [sg.Text('NAP                       Porta')],
            [sg.InputText('',size=(15,1),key='nap',border_width=1),sg.InputText(' ', size=(8,1),key='porta',border_width=1),sg.Button(image_filename='clean.png',button_color='#FFFFFF',key='Limpar',border_width=0)],
            [sg.Text('\r')], 
            [sg.Button(image_filename='prov.png',button_color='#FFFFFF', key='provisionar',border_width=0),
            sg.Button(image_filename='buscar.png',button_color='#FFFFFF',key='buscar',border_width=0)],  
            [sg.Button(image_filename='remove.png',button_color='#FFFFFF', key='remover',border_width=0),
             sg.Button(image_filename='position.png',button_color='#FFFFFF', key='position',border_width=0)],
            [sg.Button(image_filename='unprovision.png',button_color='#FFFFFF', key='unprovision',border_width=0)],
            [sg.Button(image_filename='semuso.png',button_color='#FFFFFF', key='semuso',border_width=0)],
                      
            ]
#COLUNA OUTPUT           
col2 = [
       [sg.Output(text_color='#FFFFFF',size=(90, 30),background_color='#000000',key='saida',font=('hack', 8))],
        ]
###########################################################################################################################################################
#                                                                    TEL4 PRINCIPAL
###########################################################################################################################################################
layout = [         
            [sg.Column(col,vertical_alignment='top',pad=(5,0)),sg.Column(col2,pad=(0,0))]
          ]
           
window = sg.Window('Provisionamento VAMOS', layout,margins=(5,0),icon='hat.ico')
###########################################################################################################################################################
#                                                                   FUNÇ0ES DO SISTEMA                                                                    
###########################################################################################################################################################
#IDENTIFICAÇÃO DE OPERADOR
op = open('trash_position.txt')
ope = op.readlines()
os.system('SYSTEMINFO > trash_position.txt')
for line in ope:
  operador = line[43:54]
  if operador.strip() == 'VITNOTE017':
    operador = 'Matheus'
    break
  elif operador.strip() == 'VITNOTE020':
    operador = 'Amanda'
    break
  elif operador.strip() == 'VITNOTE043':
    operador = 'Thaynara'
    break
  elif operador.strip() == 'VITNOTE012':
    operador = 'Gabryel'
    break
  elif operador.strip() == 'VITNOTE013':
    operador = 'Aline'
    break
  else:
    operador = 'Unknown'
    break

def tl1(command,ip):
    tn = telnetlib.Telnet(ip, '1023', timeout=100)
    tn.read_until(b"< ").decode()
    tn.write(''.encode('ascii') + b"\r\n")
    tn.read_until(b": ")
    tn.write('t'.encode('ascii') + b"\r\n")
    #username
    tn.read_until(b": ")
    tn.write('SUPERUSER'.encode('ascii') + b"\r\n")
    #password
    tn.read_until(b": ")
    tn.write('ANS#150'.encode('ascii') + b"\r\n")

    #commands
    tn.write(command.encode('ascii') + b"\r\n")

    sleep(10)
    n = tn.read_very_eager().decode("utf-8")

    print(n.replace('ACCESS ONLY AUTHORIZED PERSONS. DISCONNECT IMMEDIATELY!#','').replace('#','').replace('Enter Username   : SUPERUSER','').replace('Enter Password   : ','').replace('IP 0','').replace('Bem Vindo a VAMOS','').replace('   /*                           N O K I A                  */','').replace('   /*                         Fixed Networks               */','').replace('=',''))
    print('\n\n PROVISIONADO') 
    sleep(0.1)
    tn.close()


def command_prov(host,position,vlan,nap,count):
    posição = (position + '-') + str(count)
    username = values['username'].strip()
    senha = values['password'].strip()
    porta = values['porta'].strip()
    serial = values['serial'].strip()


    prov = f'''ENT-ONT::ONT-{posição}::::DESC1="{username}",DESC2="{nap} | {porta}",SERNUM={serial.replace(':','')},SWVERPLND=AUTO,OPTICSHIST=ENABLE,PLNDCFGFILE1=AUTO,DLCFGFILE1=AUTO,VOIPALLOWED=VEIP;
ED-ONT::ONT-{posição}:::::IS;
ENT-ONTCARD::ONTCARD-{posição}-14:::VEIP,1,0::IS;
ENT-LOGPORT::ONTL2UNI-{posição}-14-1:::;
ED-ONTVEIP::ONTVEIP-{posição}-14-1:::::IS;
SET-QOS-USQUEUE::ONTL2UNIQ-{posição}-14-1-0::::USBWPROFNAME=HSI_1G_UP ;
SET-VLANPORT::ONTL2UNI-{posição}-14-1:::MAXNUCMACADR=4,CMITMAXNUMMACADDR=1;
ENT-VLANEGPORT::ONTL2UNI-{posição}-14-1:::0,{vlan}:PORTTRANSMODE=SINGLETAGGED;
ENT-VLANEGPORT::ONTL2UNI-{posição}-14-1:::0,102:PORTTRANSMODE=SINGLETAGGED;
ENT-HGUTR069-SPARAM::HGUTR069SPARAM-{posição}-1::::PARAMNAME=InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.X_CT-COM_WANGponLinkConfig.VLANIDMark,PARAMVALUE={vlan};
ENT-HGUTR069-SPARAM::HGUTR069SPARAM-{posição}-2::::PARAMNAME=InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.Username,PARAMVALUE="{username}";
ENT-HGUTR069-SPARAM::HGUTR069SPARAM-{posição}-3::::PARAMNAME=InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.Password,PARAMVALUE="{senha}";
'''
    
   
    tl1(prov,host)


#=======================POS1Ç03S D1SP0N1VE1S NA PON - PROVISIONAMENT0
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
         
    print('Posição livre:',count)
    
    log = open('log_prov.txt','a')
    username = values['username']
    date = datetime.now().strftime('%d/%m/%y %H:%M')
    tecnico = values['tecnico']
    serial = values['serial']
    os.system('SYSTEMINFO > trash_position.txt')
    op = open('trash_position.txt')
    ope = op.readlines()
    for line in ope:
      operador = line[43:54]
      if operador.strip() == 'VITNOTE017':
        operador = 'Matheus'
        break

    log.write(f'\n{date}  {tecnico}  {nap}  {serial}  {position,count}  {host}  {username} {operador}')
    log.close()
    op.close()

    command_prov(host,position,vlan,nap,count)


#======================EX3CUT4 COMAND0S NO CLI
def cli(command,host,event=0,vlan=0,nap=0):
    trash = open('trash_position.txt','w')

    #conexão telnet
    tn = telnetlib.Telnet(host,'23', timeout=5)

    tn.read_until(b": ")
    tn.write('isadmin'.encode('ascii') + b"\r\n")
    #password
    tn.read_until(b": ")
    tn.write('ANS#150'.encode('ascii') + b"\r\n")
    #commands
    tn.write('environment inhibit-alarms'.encode('ascii') + b"\n")
    tn.write(command.encode('ascii') + b"\n")
    
   
    n = tn.read_all().decode("utf-8")
    
    trash.write(n)
    
    trash.close()
    if event == 1:
      print('')
    else:
       print(n.replace('ACCESS ONLY AUTHORIZED PERSONS. DISCONNECT IMMEDIATELY!#','').replace('typ:isadmin>environment','').replace('#','').replace('login: isadmin','').replace('password: ','').replace('Bem Vindo a VAMOS','').replace('=',''))
    sleep(0.1)
    tn.close()
    

#========================PR0CUR4 NAP NO BANCO DE DADOS - PROVISIONAMENT0
def nap_data_prov():
    n = values['nap'].strip()  
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
    if nap != n:
      print('Essa NAP não existe')
    else:     
      print(f'\n PROVISIONANDO...\n')
      command = f'show equipment ont status pon {position_barra}'
      operação = 'prov'
      cli(command,ip,position_hifen,vlan,nap)
      free_position(ip,position_hifen,vlan,nap)


def remove(host,serial,nap):
    trash = open('trash_position.txt','r')
    n = trash.readlines()
    for line in n: 
      if line[:3] =='sn:' and line[3:16] == serial:
        print('\nAGUARDE')
        rm = line[18:30].strip()
    
    command = f'''configure equipment ont interface {rm} admin-state down
configure equipment ont no interface {rm}
'''
    cli(command,host)

    print('\n\nPROVISIONAMENTO REMOVIDO\n')
    log = open('log_rm.txt','a')
    date = datetime.now().strftime('%d/%m/%y %H:%M')
    serial = values['serial']
    os.system('SYSTEMINFO > trash_position.txt')
    op = open('trash_position.txt')
    ope = op.readlines()
    for line in ope:
      operador = line[43:54]
      if operador.strip() == 'VITNOTE017':
        operador = 'Matheus'
        break

    log.write(f'\n{date}  {nap}  {serial}  {rm}  {host} {operador}')
    log.close()
    op.close()
    

def nap_data_rm():
    n = values['nap'].strip()  
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
    if nap != n:
      print('Essa NAP não existe')
    else:
      serial = values['serial'].strip()     
      if len(serial) == 12:
         serial = 'ALCL:'+serial[4:12]

      print('\n REMOVENDO...\n')
      command = f'show equipment ont index sn:{serial}'

      cli(command,ip)
      trash = open('trash_position.txt','r')
      n = trash.readlines()
      for line in n:
        c = line[:15].strip()
        if  c == 'index count : 0':
          break

      if c =='index count : 0':
        print('\nESTA ONU NÃO ESTA PROVISIONADA')
      else:
        remove(ip,serial,nap)
  

def unprovision():
    n = values['nap'].strip()
    if n[:5] != 'teste' and n[:3] != 'NAP':
      n = 'NAP-' + n.replace('nap-','')  
    data = open('data.txt')
    naps = data.readlines()
    for line in naps:
        nap = line[:9].replace(',','').strip()
        ip = line[30:43].replace(',','').strip()
        if nap == n:
             break
    if nap != n:
      print('Essa NAP não existe')

    command = 'show pon unprovision-onu'
    print('\n\nAGUARDE...\n')
    event = 1
    cli(command, ip, event)
    trash = open('trash_position.txt')
    t = trash.readlines()
    for line in t:
      print(line.replace('-[','').replace('1D','').replace('|','').replace('\\','').replace('[','').replace('','').replace('/','').replace('\n','').replace('\r','').replace('//',''))


def buscar():
    n = values['nap'].strip()
    if n[:5] != 'teste' and n[:3] != 'NAP':
      n = 'NAP-' + n.replace('nap-','')  
    data = open('data.txt')
    naps = data.readlines()
    for line in naps:
        nap = line[:9].replace(',','').strip()
        ip = line[30:43].replace(',','').strip()
        if nap == n:
             break
    if nap != n:
      print('Essa NAP não existe')
    serial = values['serial'].strip()
    if serial[:5] != 'ALCL:':
       serial = 'ALCL:'+ serial[4:13]
    print('\n\nAGUARDE...\n')
    command = f'show equipment ont index sn:{serial.strip()}'
    cli(command,ip)


def pon():
    n = values['nap'].strip()
    if n[:5] != 'teste' and n[:3] != 'NAP':
      n = 'NAP-' + n.replace('nap-','')  
    data = open('data.txt')
    naps = data.readlines()
    for line in naps:
        nap = line[:9].replace(',','').strip()
        ip = line[30:43].replace(',','').strip()
        position_barra = line[10:18].replace(',','' ).strip()
        if nap == n:
             break
    if nap != n:
      print('Essa NAP não existe')
    command = f'show equipment ont status pon {position_barra}'
    print('\n\nAGUARDE...\n')
    cli(command,ip)


def semuso():
    n = values['nap'].strip()
    if n[:5] != 'teste' and n[:3] != 'NAP':
      n = 'NAP-' + n.replace('nap-','')  
    data = open('data.txt')
    naps = data.readlines()
    for line in naps:
        nap = line[:9].replace(',','').strip()
        ip = line[30:43].replace(',','').strip()
        position_barra = line[10:18].replace(',','' ).strip()
        if nap == n:
             break
    if nap != n:
      print('Essa NAP não existe')
    command = f'show pon ber-stats {position_barra} | match exact:not-ranged'
    print('\n\nAGUARDE...\n')
    cli(command,ip)


###########################################################################################################################################################
#                                                                  EVENT0S
###########################################################################################################################################################
while True:
    event, values = window.read()
#EVENTO FECHAR 
    if event == sg.WIN_CLOSED:
        break
#EVENTO DO BOTÃO LIMPAR INPUT E OUTPUT
    if event == 'Limpar':
        window.FindElement('username').Update('')
        window.FindElement('password').Update('')
        window.FindElement('tecnico').Update('')
        window.FindElement('serial').Update('')
        window.FindElement('nap').Update('')
        window.FindElement('porta').Update('')
        window.FindElement('saida').Update('')  
#EVENTO DO BOTÃO PROVISIONAMENTO
    if event == 'provisionar':
      n = values['nap'].strip()
      serial = values['serial'].strip()
      if values['username'].strip() == '' or values['password'].strip() == '' or values['tecnico'].strip() == '' or values['serial'].strip() == '' or values['nap'].strip() == '' or values['porta'].strip() == '':
        print('Preencha todos os campos')
      elif n[:4] == 'NAP-' or n == 'teste' or n == 'teste II':
        if serial[:4] == 'ALCL':
          nap_data_prov()
        else:
          print('Digite um serial valido')
      else:
        print('Digite uma NAP valida ')  
        
      
    if event == 'remover':
      n = values['nap'].strip()
      serial = values['serial'].strip()
      if values['serial'].strip() == '' or values['nap'].strip() == '':
          print('Didige todos os campos')
      
      elif n[:4] == 'NAP-' or n == 'teste' or n == 'teste II':
        if serial[:4] == 'ALCL':
          nap_data_rm()
        else:
          print('Digite um serial valido')
      else:
        print('Digite uma NAP valida ')


    if event == 'buscar':
      n = values['nap'].strip()
      serial = values['serial'].strip()
      if values['serial'].strip() == '' or values['nap'].strip() == '':
          print('Didige todos os campos')
      
      elif n[:4] == 'NAP-' or n == 'teste' or n == 'teste II':
        if serial[:4] == 'ALCL':
          buscar()
        else:
          print('Digite um serial valido')
      else:
        print('Digite uma NAP valida ')
      

    if event == 'unprovision':
      n = values['nap'].strip()     
      if n[:4] == 'NAP-' or n == 'teste' or n == 'teste II':
        unprovision()
      else:
        print('Digite uma NAP valida ')
    
    if event == 'position':
      n = values['nap'].strip()     
      if n[:4] == 'NAP-' or n == 'teste' or n == 'teste II':
        pon()
      else:
        print('Digite uma NAP valida ')

    if event == 'semuso':
      n = values['nap'].strip()     
      if n[:4] == 'NAP-' or n == 'teste' or n == 'teste II':
        semuso()
      else:
        print('Digite uma NAP valida ')
window.close()

