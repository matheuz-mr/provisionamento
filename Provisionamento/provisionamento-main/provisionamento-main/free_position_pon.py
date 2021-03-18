#-separa posições utilizadas na PON
trash = open('trash_position.txt')
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
print(count)