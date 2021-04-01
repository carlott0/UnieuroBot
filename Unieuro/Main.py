import Check
import time
import datetime

link = []
budget = []
tempo= int(input("Inserisci ogni quanti secondi aggiornare il bot: "))


f = open("credenziali.txt", "r")
linea=[]
for x in f:
  linea.append(x)
  
gMailF=linea[0].split(':')[1]
pMailF=linea[1].split(':')[1]
email=linea[2].split(':')[1]
pwd=linea[3].split(':')[1]
gMailT=linea[4].split(':')[1]
cont=0
linea=[]
f = open("unieuro.txt", "r")
for x in f:
  linea.append(x)
  cont+=1
N_elementi = cont
j = 0
while (j<N_elementi):
  #Find ',' and split linea in budget and link
  prodotto=linea[j].split(',')
  link.append(prodotto[1])
  budget.append(float(prodotto[0]))
  j += 1
print("\n")



while (True):
  j = 0
  x = datetime.datetime.now()
  print(x.strftime("%d/%m/%y %X"))
  while (j<N_elementi):
    res=Check.check_price(budget[j], link[j], email, pwd, gMailF, pMailF, gMailT)
    if res == "ok":
        quit()
        
    j += 1
  print("\n---------------------------------------------------------\n")
  # loop that allows the program to regularly check for prices
  time.sleep(tempo)
