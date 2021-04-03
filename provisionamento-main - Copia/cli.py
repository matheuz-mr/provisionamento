s = input("serial")
n = input('nap:')
 
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
