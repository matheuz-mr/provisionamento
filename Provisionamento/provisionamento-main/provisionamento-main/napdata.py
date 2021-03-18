n = input(('NAP: '))
data = open('data.txt')
naps = data.readlines()
for line in naps:
    nap = line[:9].strip()
    p = line[12:20]
    if nap == n:
        break
        
print(nap)
print(p)
            
