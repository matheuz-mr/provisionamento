import PySimpleGUI as sg
import telnetlib
from time import sleep
from datetime import datetime
import os
#TEMA LAYOUTS
sg.theme('tema') 
#███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#                                             COLUNA, B0TÕES E INPUTS
#███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
col = [     
            [sg.Frame('Frame',[[sg.Text('Username              Password')],
            [sg.InputText(' ', size=(15,1),key='username'),sg.InputText(' ', size=(15,1),key='password')],#INPUTS USERNAMEN E PASSWORD
            [sg.Text('Tecnico                  Serial')],
            [sg.Combo(['Caio' ,'Edgar' ,'Felipe' ,'Fernando','Joelson' ,'Jose Cesar' ,'Josivam' ,'Juracy' ,'Leandro' ,'Paulo'  ,'Renardio' ,'Ricardo' ,'Rodrigo' ,'Suporte', 'Vilson' ,'Vitor','Willes'], size=(13,100),key='tecnico'),sg.InputText(' ', size=(15,1),key='serial')],
            [sg.Text('NAP                      Porta')],
            [sg.InputText('', size=(15,1),key='nap'),sg.InputText(' ', size=(15,1),key='porta')],], key='-COL1-')],
            [sg.Text('\r')],
            [sg.Button(image_filename='prov.png',button_color='#FFFFFF', key='provisionar',border_width=0),
            sg.Button(image_filename='buscar.png',button_color='#FFFFFF',key='buscar',border_width=0)],  
            [sg.Button(image_filename='remove.png',button_color='#FFFFFF', key='remover',border_width=0),
             sg.Button(image_filename='clean.png',button_color='#FFFFFF',key='Limpar',border_width=0),
             sg.Button(image_filename='position.png',button_color='#FFFFFF', key='position',border_width=0)],
            [sg.Text('            Comandos Adicionais')], 
            [sg.Button(image_filename='unprovision.png',button_color='#FFFFFF', key='semuso',border_width=0)],
            [sg.Button(image_filename='semuso.png',button_color='#FFFFFF', key='remover',border_width=0)],
                      
            ]
#COLUNA OUTPUT           
col2 = [
       [sg.Output(text_color='#DCDCDC',size=(105, 31),background_color='#000000',key='saida',font=('hack', 8))],
        ]

#███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#                                              TEL4 PRINCIPAL
#███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
layout = [         
            [sg.Column(col,vertical_alignment='top',pad=(5,0)),sg.Column(col2,pad=(0,0))]
          ]
           
window = sg.Window('hat', layout,margins=(5,0),icon='_hat.ico')
#███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#                                              FUNÇ0ES DO SISTEMA
#███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

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

    print(n)
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
    print(100*'=')
    
    
    log = open('log.txt','a')
    username = values['username']
    date = datetime.now().strftime('data: %d/%m/%y %H:%M')
    tecnico = values['tecnico']
    serial = values['serial']
    log.write(f'\n{date}  {tecnico}  {nap}  {serial}  {position, count}  {host}  {username}')
    log.close()

    command_prov(host,position,vlan,nap,count)


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
    tn.write('environment inhibit-alarms'.encode('ascii') + b"\n")
    tn.write(command.encode('ascii') + b"\n")
    sleep(8)
    n = tn.read_very_eager().decode("utf-8")
    
    trash.write(n)
    
    trash.close()
    print(n) 
    sleep(0.1)
    tn.close()

    print(100*'=')
    

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
      print('\n PROVISIONANDO...\n')
      command = f'show equipment ont status pon {position_barra}'

      cli(command,ip,position_hifen,vlan,nap)
      #free_position(ip,position_hifen,vlan,nap)


def remove(host,serial):
    trash = open('trash_position.txt','r')
    n = trash.readlines()
    for line in n: 
      if line[:3] =='sn:' and line[3:16] == serial:
        print(line[3:16])
      
        rm = line[18:30].strip()

    command = f'''configure equipment ont interface {rm} admin-state down
configure equipment ont no interface {rm}
'''
    
    cli(command,host)

    print('\n\nPROVISIONAMENTO REMOVIDO')
    

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
      remove(ip,serial)
  
    
#███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
#                                                                  EVENT0S
#███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
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
window.close()

