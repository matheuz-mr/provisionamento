import telnetlib
from time import sleep
HOST = "10.65.100.11"
prov = ('''ENT-ONT::ONT-1-1-2-6-99::::DESC1="tainarapdas",DESC2="NAP-8621 | 8",SERNUM=ALCLB1A2C107,SWVERPLND=AUTO,OPTICSHIST=ENABLE,PLNDCFGFILE1=AUTO,DLCFGFILE1=AUTO,VOIPALLOWED=VEIP;
ED-ONT::ONT-1-1-2-6-99:::::IS;
ENT-ONTCARD::ONTCARD-1-1-2-6-99-14:::VEIP,1,0::IS;
ENT-LOGPORT::ONTL2UNI-1-1-2-6-99-14-1:::;
ED-ONTVEIP::ONTVEIP-1-1-2-6-99-14-1:::::IS;
SET-QOS-USQUEUE::ONTL2UNIQ-1-1-2-6-99-14-1-0::::USBWPROFNAME=HSI_1G_UP ;
SET-VLANPORT::ONTL2UNI-1-1-2-6-99-14-1:::MAXNUCMACADR=4,CMITMAXNUMMACADDR=1;
ENT-VLANEGPORT::ONTL2UNI-1-1-2-6-99-14-1:::0,309:PORTTRANSMODE=SINGLETAGGED;
ENT-VLANEGPORT::ONTL2UNI-1-1-2-6-99-14-1:::0,102:PORTTRANSMODE=SINGLETAGGED;
ENT-HGUTR069-SPARAM::HGUTR069SPARAM-1-1-2-6-99-1::::PARAMNAME=InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.X_CT-COM_WANGponLinkConfig.VLANIDMark,PARAMVALUE=309;
ENT-HGUTR069-SPARAM::HGUTR069SPARAM-1-1-2-6-99-2::::PARAMNAME=InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.Username,PARAMVALUE="tainarapdas";
ENT-HGUTR069-SPARAM::HGUTR069SPARAM-1-1-2-6-99-3::::PARAMNAME=InternetGatewayDevice.WANDevice.1.WANConnectionDevice.1.WANPPPConnection.1.Password,PARAMVALUE="642e6a";
''')
#conexão telnet
tn = telnetlib.Telnet(HOST, '1023', timeout=100)
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
tn.write(prov.encode('ascii') + b"\r\n")

sleep(10)
n = tn.read_very_eager().decode("utf-8")

print(n) 
sleep(0.1)
tn.close()