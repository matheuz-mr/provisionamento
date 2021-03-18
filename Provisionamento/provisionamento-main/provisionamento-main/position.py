cto = input('nap: ').upper()
def position(cto):
    nap = cto.replace('NAP-','')
    global ip
    global slot
    global pon
#PON
    if (len(nap) == 5):
        pon = nap[:2]
    else:
        pon = nap[:1]
#HOST
    if (int(nap) <= 6524):
        ip = '10.65.100.11'
    elif(int(nap) <= 19924):
        ip = '10.65.100.12'
    elif(int(nap) <= 29924):
        ip = '10.65.100.13'
    else:
        ip = '10.65.100.14'

position(cto)
        
print(ip)
print(pon)
