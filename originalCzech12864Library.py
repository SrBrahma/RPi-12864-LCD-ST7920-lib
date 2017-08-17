#!/usr/bin/python
# -*- encoding: utf-8 -*-

# posledni uprava: 15.7.2013

# pripojeni displeje 12864ZW (128x64 bodu) SERIOVE:
# displej vyvod (vyznam)  -    pripojeno na ...
# 1  (GND)                - RasPi (GPIO GND   - pin 6)
# 2  (+ napajeni)         - RasPi (GPIO +5V   - pin 1)
# 3  VO                   - 
# 4  (RS Data/Command)    - +5V (CHIP SELECT - pri seriove komunikaci)
# 5  (R/W Read/Write)     - RasPi (seriova data) - GPIO7 (pin26) 
# 6  (E - Strobe)         - RasPi (seriove hodiny) - GPIO8 (pin24)
# 7  (Data bit0)          - 
# 8  (Data bit1)          - 
# 9  (Data bit2)          - 
# 10 (Data bit3)          - 
# 11 (Data bit4)          - 
# 12 (Data bit5)          - 
# 13 (Data bit6)          - 
# 14 (Data bit7)          - 
# 15 (PSB)                - GND - nastaveni seriove komunikace
# 16 (NC)                 -
# 17 (Reset)              - RasPi - GPIO25(pin22)
# 18 (Vout)               - 
# 19 (Podsvet - A)        - +5V (nebo nejaky regulator jasu LED - odber asi 60mA)
# 20 (Podsvet - K)        - RasPi (GPIO GND - pin 6)


import time              # ruzne operace s casem (pauzy)
import RPi.GPIO as GPIO  # pouziva se jen pri pripojeni signalu E, nebo RS primo na GPIO v RasPi
import math              # vyuziva se jen v prikladech pri kresleni kruznic
import random            # vyuziva se jen v ukazce pro generovani nahodnych souradnic 


# preklad ceskych znaku ze souboru s fontem
cz2={}
cz2[345] = 128      # r s hackem
cz2[237] = 129      # i s carkou
cz2[353] = 130      # s s hackem
cz2[382] = 131      # z s hackem
cz2[357] = 132      # t s hackem
cz2[269] = 133      # c s hackem
cz2[253] = 134      # y s carkou
cz2[367] = 135      # u s krouzkem
cz2[328] = 136      # n s hackem
cz2[250] = 137      # u s carkou
cz2[283] = 138      # e s hackem
cz2[271] = 139      # d s hackem
cz2[225] = 140      # a s carkou
cz2[233] = 141      # e s carkou
cz2[243] = 142      # o s carkou

cz2[344] = 143      # R s hackem
cz2[205] = 144      # I s carkou
cz2[352] = 145      # S s hackem
cz2[381] = 146      # Z s hackem
cz2[356] = 147      # T s hackem
cz2[268] = 148      # C s hackem
cz2[221] = 149      # Y s carkou
cz2[366] = 150      # U s krouzkem
cz2[327] = 151      # N s hackem
cz2[218] = 152      # U s carkou
cz2[282] = 153      # E s hackem
cz2[270] = 154      # D s hackem
cz2[193] = 155      # A s carkou
cz2[201] = 156      # E s carkou
cz2[211] = 157      # O s carkou

cz2[228] = 228      # prehlasovane a
cz2[235] = 235      # prehlasovane e
cz2[239] = 239      # prehlasovane i
cz2[246] = 246      # prehlasovane o
cz2[252] = 252      # prehlasovane u
cz2[196] = 196      # prehlasovane A
cz2[214] = 214      # prehlasovane O
cz2[220] = 220      # prehlasovane U

cz2[176] = 176      # stupen
cz2[177] = 177      # plus minus
cz2[171] = 171      # dvojsipka vlevo
cz2[166] = 166      # prerusene svislitko
cz2[223] = 223      # beta

# prirazeni GPIO pinu
sdata_pin = 7       # (pin 26 = GPIO7)   = DATA    
sclk_pin = 8        # (pin 24 = GPIO8)   = HODINY  
reset_pin = 25      # (pin 22 = GPIO25)  = RESET   

mapa={}             # pamet, do ktere se uklada aktualni stav zobrazenych pixelu na displeji
txtmapa={}          # pamet, do ktere se uklada aktualni stav textu na displeji
font2={}            # pamet, ve ktere je ulozeny font, nacetny z externiho souboru
ikodata={}          # promenna, pres kterou se budou definovat graficke ikony


#==============================================================
# hlavni program
#==============================================================

def main():

  init()              # zakladni HW nastaveni systemu - smery portu na expanderu a reset displeje
  disclear(0)         # kompletni smazani displeje
  nacist_font2("/home/pi/font2.txt")  # nacteni externiho fontu ze souboru



#==============================================================
#              Zacatek ukazky vsech funkci
#==============================================================


#- - - - - - - - - psani textu na displej - - - - - - - - - - - - - - - - - - - -  
  init_text()     # prepnuti do textoveho rezimu

  velky_napis("Ukazka zobrazeni",0,0)   # zobrazeni napisu v textovem rezimu na urcenych souradnicich
  velky_napis("displeje",4,1)
  velky_napis("v textovem",3,2)
  velky_napis("rezimu",5,3)

  time.sleep(2)
  velky_napis("chr(1)...chr(32)", 0 , 1)
  kod_znaku = 0
  for r in range(2,4):
    for s in range (16):
      kod_znaku = kod_znaku + 1
      velky_znak(kod_znaku , s , r)   # zobrazeni znaku v textovem rezimu podle jeho (ASCII)kodu
  time.sleep(3)
  
  velky_napis("chr(33)..chr(64)" , 0 , 1)
  for r in range(2,4):
    for s in range (16):
      kod_znaku = kod_znaku + 1
      velky_znak(kod_znaku , s , r)
     

  time.sleep(3)
  clr_text()               # smazani textove casti displeje
  time.sleep(1)

#- - - - - - - - - Ikony - - - - - - - - - - - - - - - - - - - -  
  velky_napis("vlastni ikony" , 0 , 0)
 
 
  # definice zrafické podoby 4 vlastnich ikon:
  # prvni uzivatelsky definovana ikona (zamerovaci kriz)
  ikodata[0]  =  0b0011111111111100
  ikodata[1]  =  0b0111111111111110
  ikodata[2]  =  0b1110000110000111
  ikodata[3]  =  0b1100000110000011
  ikodata[4]  =  0b1100000110000011
  ikodata[5]  =  0b1100000000000011
  ikodata[6]  =  0b1100000000000011
  ikodata[7]  =  0b1111100110011111
  ikodata[8]  =  0b1111100110011111
  ikodata[9]  =  0b1100000000000011
  ikodata[10] =  0b1100000000000111
  ikodata[11] =  0b1100000110000011
  ikodata[12] =  0b1100000110000011
  ikodata[13] =  0b1110000110000111
  ikodata[14] =  0b0111111111111110
  ikodata[15] =  0b0011111111111100
  defikon(0 , ikodata)

  # druha uzivatelsky definovana ikona (ctverec s krizkem)
  ikodata[0]  =  0b1111111111111111
  ikodata[1]  =  0b1111111111111111
  ikodata[2]  =  0b1110000000000111
  ikodata[3]  =  0b1101000000001011
  ikodata[4]  =  0b1100100000010011
  ikodata[5]  =  0b1100010000100011
  ikodata[6]  =  0b1100001001000011
  ikodata[7]  =  0b1100000110000011
  ikodata[8]  =  0b1100000110000011
  ikodata[9]  =  0b1100001001000011
  ikodata[10] =  0b1100010000100011
  ikodata[11] =  0b1100100000010011
  ikodata[12] =  0b1101000000001011
  ikodata[13] =  0b1110000000000111
  ikodata[14] =  0b1111111111111111
  ikodata[15] =  0b1111111111111111
  defikon(1 , ikodata)


  # treti uzivatelsky definovana ikona (prazdny ctverec)
  ikodata[0]  =  0b1111111111111111
  ikodata[1]  =  0b1111111111111111
  ikodata[2]  =  0b1100000000000011
  ikodata[3]  =  0b1100000000000011
  ikodata[4]  =  0b1100000000000011
  ikodata[5]  =  0b1100000000000011
  ikodata[6]  =  0b1100000000000011
  ikodata[7]  =  0b1100000000000011
  ikodata[8]  =  0b1100000000000011
  ikodata[9]  =  0b1100000000000011
  ikodata[10] =  0b1100000000000011
  ikodata[11] =  0b1100000000000011
  ikodata[12] =  0b1100000000000011
  ikodata[13] =  0b1100000000000011
  ikodata[14] =  0b1111111111111111
  ikodata[15] =  0b1111111111111111
  defikon(2 , ikodata) 
  
  # ctvrta uzivatelsky definovana ikona (kriz v krouzku) 
  ikodata[0]  =  0b0000011111100000
  ikodata[1]  =  0b0000100110010000
  ikodata[2]  =  0b0011000110001100
  ikodata[3]  =  0b0010000110000100
  ikodata[4]  =  0b0100000110000010
  ikodata[5]  =  0b1000000110000001
  ikodata[6]  =  0b1000000110000001
  ikodata[7]  =  0b1111111111111111
  ikodata[8]  =  0b1111111111111111
  ikodata[9]  =  0b1000000110000001
  ikodata[10] =  0b1000000110000001
  ikodata[11] =  0b0100000110000010
  ikodata[12] =  0b0010000110000100
  ikodata[13] =  0b0011000110001100
  ikodata[14] =  0b0000100110010000
  ikodata[15] =  0b0000011111100000
  defikon(3 , ikodata) 

  printiko(1 , 0 , 1)    # ikona c.2 na zacatek druhe radky zhora
  for iko in range (7):  # zbytek te radky se zaplni nahodnymi ikonami
    # kdyz se tiskne vic ikon za sebe, tak se nemusi u kazde nastavovat pozice
    ikona = random.randint(0,3) * 2 # posledni parametr je dvojnasobek cisla ikony
    posli_bajt2( 1 ,  0 , ikona)    

  printiko(2 , 0 , 2)    # ikona c.3 na zacatek treti radky zhora
  for iko in range (7):  # zbytek te radky se zaplni nahodnymi ikonami
    # kdyz se tiskne vic ikon za sebe, tak se nemusi u kazde nastavovat pozice
    ikona = random.randint(0,3) * 2 # posledni parametr je dvojnasobek cisla ikony
    posli_bajt2( 1 ,  0 , ikona)    

  printiko(3 , 0 , 3)    # ikona c.4 na zacatek spodni radky 
  for iko in range (7):  # cely zbytek te radky se zaplni ikonou c.4
    # kdyz se tiskne vic ikon za sebe, tak se nemusi u kazde nastavovat pozice
    posli_bajt2( 1 ,  0 , 6)    # (6 = ikona c.4)    



  time.sleep(2)
  velky_napis(" zmena definice ", 0 , 0)
  time.sleep(2)
  velky_napis("  ctvrte ikony  ", 0 , 0)
  time.sleep(2)

  
  # pri zmene definice ikony se OKAMZITE meni vzhled VSECH prave zobrazenych ikon
  # ctvrta uzivatelsky definovana ikona se timto prenastavi na sachovnici 
  ikodata[0]  =  0b1111000011110000
  ikodata[1]  =  0b1111000011110000
  ikodata[2]  =  0b1111000011110000
  ikodata[3]  =  0b1111000011110000
  ikodata[4]  =  0b0000111100001111
  ikodata[5]  =  0b0000111100001111
  ikodata[6]  =  0b0000111100001111
  ikodata[7]  =  0b0000111100001111
  ikodata[8]  =  0b1111000011110000
  ikodata[9]  =  0b1111000011110000
  ikodata[10] =  0b1111000011110000
  ikodata[11] =  0b1111000011110000
  ikodata[12] =  0b0000111100001111
  ikodata[13] =  0b0000111100001111
  ikodata[14] =  0b0000111100001111
  ikodata[15] =  0b0000111100001111
  defikon(3 , ikodata) 
 
  time.sleep(3)
  clr_text()
  
#- - - - - - - - -Cinské znaky - - - - - - - - - - - - - - - -  
  velky_napis("   Jako ikony   " , 0 , 0)
  velky_napis("  se zobrazuji  " , 0 , 1)
  velky_napis(" i cinske znaky " , 0 , 2)
  time.sleep(3)
  clr_text()

  # tisk CINSTINY obrim fontem 16x16 bodu (v textovem rezimu)
  # Tohle jsou jen nahodne vybrane znaky (cinstina mi nic nerika)
  # Znak je vybran pomoci poslednich dvou cisel funkce "posli_bajt2()"
  # prvni z tech dvou cisel musi byt vyssi, nez 127

  ikopos(2,0)                       # nastaveni pozice prvniho znaku [0,0] az [7,3]
  posli_bajt2( 1 , 200 , 150)   
  posli_bajt2( 1 , 218 , 10)
  posli_bajt2( 1 , 128 , 1)
  posli_bajt2( 1 , 211 , 200)

  ikopos(4,2)                       # nastaveni pozice prvniho znaku [0,0] az [7,3]
  posli_bajt2( 1 , 240 , 4)   
  posli_bajt2( 1 , 240 , 33)
  posli_bajt2( 1 , 240 , 222)

  # svisly ctyrznakovy napis
  ikopos(0,0)                       # nastaveni pozice znaku 
  posli_bajt2( 1 , 128 , 18)   
  ikopos(0,1)                       # nastaveni pozice znaku 
  posli_bajt2( 1 , 154 , 251)
  ikopos(0,2)                       # nastaveni pozice znaku 
  posli_bajt2( 1 , 197 , 37)
  ikopos(0,3)                       # nastaveni pozice znaku 
  posli_bajt2( 1 , 141 , 90)


  time.sleep(3)
  clr_text()


#- - - - - - - - -  text v grafickem rezimu - - - - - - - - - - - - - - - - - - -  
#tisk napisu fontem 8x8 bodu (v grafickem rezimu)

  init_grafika()
  slovo("Displej je možné" , 0 ,  0 , False)  # normalni graficky napis na horni radku
  slovo("provozovat"       , 3 , 15 , False)        
  slovo("i v grafickém"    , 1 , 30 , False) 
  slovo("režimu"           , 5 , 45 , False)  

  time.sleep(2)
  slovo("grafickém"        , 5 , 30 , True)  # inverzne prepsany text  

  time.sleep(3)
  clr_grafika()    # smazani graficke casti displeje


  # ve stejnem rezimu je mozne tisknout jednotlive znaky podle jejich kodu
  for kod in range(32,128):
    sloupec = (kod-32) % 16
    radka = int((kod-32)/16) * 11        # rozestupy mezi radkami jsou 11 bodu
    if (radka / 22.0 == int(radka/22)):  # kazda druha radka je inverzni
      inverze = True
    else:
      inverze = False
      
    znak(kod , sloupec, radka , inverze) # podprogram pro tisk znaku v grafickem rezimu 

  time.sleep(2)
  clr_grafika()

  for kod in range(128,256):
    sloupec = (kod-128) % 16
    radka = int((kod-128)/16) * 8 
    znak(kod , sloupec, radka , False)

  time.sleep(2)
  clr_grafika()


#- - - - - - - tisk bodu a car - - - - - - - - - - - - - - - - - -  

  slovo(" V tomto režimu " ,0, 2,False)  # normalni napis 2 pixely od horniho okraje
  slovo("je možné kreslit" ,0,11,False)        
  slovo("  body a čáry   " ,0,20,False) 

  # oramovani displeje plnou carou
  h_cara (  0 ,  0 , 127 , 1)          # horizontalni cara na libovolne pozici
  h_cara2( 63 ,  0 ,   7 , 0b11111111) # rychla hor. cara v 16-sloupcovem rastru s nastavenim masky
  v_cara (  0 ,  0 ,  63 , 0b11111111) # vertikalni cara v libovolne pozici s nastavenim masky
  v_cara (127 ,  0 ,  63 , 0b11111111)

  # vnitrni mensi obdelnik carkovanou carou
  h_cara2(  31 ,  1 ,   6 , 0b11001100)
  h_cara2( 56 ,   1 ,   6 , 0b11001100)
  v_cara ( 16 ,  31 ,  56 , 0b11001100)
  v_cara (111 ,  31 ,  56 , 0b11001100)


  # nahodne nasypani bodu do maleho obdelniku v inverznim rezimu
  for i in range(2000):
    x= int(random.randint(17,110))
    y= int(random.randint(32,55))
    plot( x , y , 2)   # tisk inverzniho bodu na souradnice [x,y]


#- - - - - - - - - - - - ruzne styly horizontalnich car - - - - - - - - - - - - - - - - -  
  clr_grafika()

  h_cara2(  0 ,  2 ,   5 , 0b11111111) # rychla hor. cara v 16-sloupcovem rastru s nastavenim masky
  h_cara2( 10 ,  3 ,   4 , 0b11001100) # rychla hor. cara v 16-sloupcovem rastru s nastavenim masky
  h_cara2( 20 ,  2 ,   5 , 0b11110000) # rychla hor. cara v 16-sloupcovem rastru s nastavenim masky
  h_cara2( 30 ,  1 ,   6 , 0b10101010) # rychla hor. cara v 16-sloupcovem rastru s nastavenim masky
  h_cara2( 40 ,  0 ,   7 , 0b11110101) # rychla hor. cara v 16-sloupcovem rastru s nastavenim masky
  h_cara2( 50 ,  1 ,   6 , 0b01110101) # rychla hor. cara v 16-sloupcovem rastru s nastavenim masky

  time.sleep(3)

  clr_grafika(0xff)    # cely displej zaplnit bilou barvou

#- - - - - - - - - - kresleni - - - - - - - - - - - - - - - - - - - -  
  # vykresleni dvojite kruznice pomoci primeho tisku bodu na displej (pomale)
  for kruh in range(0,6283,4):
    x = int(((math.sin(kruh/1000.0) * 30.0)) + 32)
    y = int(((math.cos(kruh/1000.0) * 30.0)) + 32)
    plot(x,y,0)
    x = int(((math.sin(kruh/1000.0) * 20.0)) + 32)
    y = int(((math.cos(kruh/1000.0) * 20.0)) + 32)
    plot(x,y,0)

  # vykresleni peti kruznic s vyuzitim zapisu do pameti
  #    a nasledneho presypani cele pameti na displej  (rychle)
  for kruh in range(0,6283,4):
    x = int(((math.sin(kruh/1000.0) * 30.0)) + 96)
    y = int(((math.cos(kruh/1000.0) * 30.0)) + 32)
    mem_plot(x,y,0)
    x = int(((math.sin(kruh/1000.0) * 25.0)) + 96)
    y = int(((math.cos(kruh/1000.0) * 25.0)) + 32)
    mem_plot(x,y,0)
    x = int(((math.sin(kruh/1000.0) * 20.0)) + 96)
    y = int(((math.cos(kruh/1000.0) * 20.0)) + 32)
    mem_plot(x,y,0)
    x = int(((math.sin(kruh/1000.0) * 15.0)) + 96)
    y = int(((math.cos(kruh/1000.0) * 15.0)) + 32)
    mem_plot(x,y,0)
    x = int(((math.sin(kruh/1000.0) * 10.0)) + 96)
    y = int(((math.cos(kruh/1000.0) * 10.0)) + 32)
    mem_plot(x,y,0)

  mem_dump()    # presypani dat z pameti na displej



  time.sleep(2)
  clr_grafika()

#- - - - - - - - - - prepinani textoveho a grafickeho rezimu - - - - - - - - - -  

  slovo("    Grafický    " , 0 ,  0 , False)
  slovo("a  textový režim" , 0 , 10 , False) 
  slovo("je  možné použít" , 0 , 20 , False) 
  slovo("     zároveň    " , 0 , 30 , False) 

  time.sleep(2)
  clr_grafika()
 
  init_text()      # prepnuti displeje do textoveho rezimu
  velky_napis("Velky  napis" , 2 , 0)
  velky_napis("v textovem"   , 3 , 1)
  velky_napis("rezimu"       , 5 , 2)
  printiko(1 , 0 , 2)
  printiko(1 , 7 , 2)  


  time.sleep(2)

  init_grafika()  # prepnuti displeje do grafickeho rezimu
  h_cara2( 53 ,  0 ,   7 , 0b10011001) 
  slovo("Grafická řádka" , 1 , 56 , False)   


  
  # pri kombinaci textoveho a grafickeho rezimu se spolecna oblast na displeji XORuje
  # priklad:  4 body tlusta sikma cara pres cely displej

  for x in range(128):
    plot(x ,x/2      , 1)
    plot(x,(x/2) + 1 , 1)
    plot(x,(x/2) + 2 , 1)
    plot(x,(x/2) + 3 , 1)

  time.sleep(2)
  slovo("Smazání  grafiky" , 0 , 56 , True)   

  time.sleep(2)
  clr_grafika()   # grafiku je mozne smazat samostatne, takze puvodni text zustava

  slovo("  Text zůstává  " , 0 , 56 , True)   
  time.sleep(2)
  slovo("Dokreslení  čáry" , 0 , 56 , True)   

  for x in range(128):
    plot(127-x ,x/2      , 1)
    plot(127-x,(x/2) + 1 , 1)
    plot(127-x,(x/2) + 2 , 1)
    plot(127-x,(x/2) + 3 , 1)

  time.sleep(2)
  slovo(" Smazání  textu " , 0 , 56 , True)   
  time.sleep(1)

  clr_text()                # textovy displej je mozne take smazat samostatne
  init_grafika()
  mem_dump()                # grafika se ale v tom pripade musi obnovit z pameti
  
  time.sleep(1)
  slovo("Grafika  zůstává" , 0 , 56 , True)   
  time.sleep(2)
  clr_grafika()

#- - - - - - - - - nahrani obrazku - - - - - - - - - - - - - - - - - -  

  slovo("   zobrazení    " ,0,  0,False)  # 
  slovo("    souboru     " ,0, 10,False)  # 
  slovo("  s  obrázkem   " ,0, 20,False)  # 
  time.sleep(2)
  load_bmp12864("/home/pi/pokladnik.bmp")  # nahrani bitmapy o velikosti 128x64 bodu na displej 

  time.sleep(4)

  # zaplneni displeje svislymi carami (pattern = 0b10101010)
  disclear(0b10101010) # po funkci disclear() zustava displej v textovem rezimu
  init_grafika()       # proto je treba ho pred dalsi grafickou funkci prepnout do grafickeho rezimu

  slovo(" K O N E C " , 2 , 25 , True)   
 
  exit(0)




#==============================================================
#               vsechny podprogramy jsou nize:
#==============================================================



#==============================================================
# zobrazeni jedne ze 4 nadefinovanych ikon o velikosti 16x16 bodu na pozici [x, y]
# x je v rozsahu 0 az 7
# y je v rozsahu 0 az 3
def printiko(cislo , x , y):
  posun = x
  if (y == 1) : posun = posun + 16
  if (y == 2) : posun = posun + 8
  if (y == 3) : posun = posun + 24
  posli_bajt1( 0, 0b10000000 + posun)  # Address Counter na pozadovanou pozici
  posli_bajt2( 1 ,  0 , cislo * 2)



#==============================================================
# zobrazeni jednoho znaku z fontu 8x8 bodu
# zn_x= pozice znaku v ose X (0 az 15) ,supery = 0 az 63 (mikroradka, na ktere je horni okraj znaku)
def znak(kod , zn_x , supery , inverze=False):  

  # kontrola svtupnich parametru a jejich pripadne prenastaveni na krajni meze
  if (kod    <  32) : kod = 32
  if (kod    > 255) : kod = 255
  if (zn_x   <   0) : zn_x = 0  
  if (zn_x   >  15) : zn_x = 15  
  if (supery >  63) : supery = 63
  if (supery <   0) : supery = 0

  kod = kod - 32     # v souboru s fontem je jako prvni znak definovaná mezera s kodem 32
  superx = zn_x * 8

  # obraz znaku z fontu se bude postupne prenaset na displej bajt po bajtu v 8 krocich (zhora dolu) 
  for adr_font in range(kod*8,(kod*8)+8):

    # vypocet horizontalni a vertikalni adresy v pameti displeje
    horiz = int(superx / 16)  
    dis_adr_y = supery
    if (dis_adr_y >= 32):
      dis_adr_y = dis_adr_y - 32
      horiz = horiz + 8
  
    minibit = superx % 16     # poloha bitu, se kterym se bude pracovat, v dvojbajtu
   
    posli_bajt2( 0, 0b10000000 + dis_adr_y , 0b10000000 + horiz )  # nastaveni adresy grafiky
  
    puvodni_leva  = mapa[horiz,dis_adr_y,0]  # zjisteni aktualniho stavu dvojbajtu na displeji
    puvodni_prava = mapa[horiz,dis_adr_y,1]

    if(minibit < 8):  # kdyz je minibit < 8, meni se jen levy bajt z dvojbajtu 
      if (inverze == False):  # normalni text (prepise vsechno, co je pod textem)
        levy_bajt = font2[adr_font]
      if (inverze == True):   # inverzni text (prepise vsechno, co je pod textem)
        levy_bajt = ~font2[adr_font]
        
      pravy_bajt = puvodni_prava   # pravy bajt z dvojbajtu bude beze zmeny
  
    else:  # kdyz je minibit >= 8, meni se jen pravy bajt z dvojbajtu
      if (inverze == False):  # normalni text (prepise vsechno, co je pod textem)
        pravy_bajt = font2[adr_font]
      if (inverze == True):   # inverzni text (prepise vsechno, co je pod textem)
        pravy_bajt = ~font2[adr_font]

      levy_bajt = puvodni_leva     # levy bajt z dvojbajtu bude beze zmeny
  
    posli_bajt2( 1, levy_bajt, pravy_bajt)       # prepise dvojbajt na zadane adrese v displeji  
    mapa[horiz,dis_adr_y,0] = levy_bajt             # stejne hodnoty si zapamatuje do promenne mapa[]
    mapa[horiz,dis_adr_y,1] = pravy_bajt

    supery = supery + 1   # posun aktualni mikroradky o jednu nize



#==============================================================
# nakresleni horizontalni cary bod po bodu
def h_cara(supery, od=0 , do=127, styl=1):  
  for x in range(od, do+1):
    plot(x,supery,styl)



#==============================================================
# nakresleni vertikalni cary s vyuzitim bitove masky
def v_cara(superx, od=0 , do=63, pattern = 255):  
  poz_pat = 0                              # pozice bitu v patternu
  for y in range(od , do+1 ):
    maska = (0b10000000 >> (poz_pat % 8))  # podle zadaneho patternu vybira jednotlive bity
    bitpat= pattern & maska
    if (bitpat == 0):                      # ktere na displeji bud zobrazi, nebo smaze
      styl = 0
    else:
      styl = 1

    plot(superx,y,styl)
    poz_pat = poz_pat + 1



#==============================================================
# nakresleni horizontalni cary od kraje ke kraji po bajtech
def h_cara2(supery = 0, odbajtu = 0, dobajtu = 5, pattern = 0b11111111):  
  posun=odbajtu
  if (supery >= 32):
    supery = supery - 32
    posun = posun + 8     

  posli_bajt2( 0, 0b10000000 + supery , 0b10000000 + posun )     
  for r in range(dobajtu - odbajtu + 1):
      posli_bajt2( 1, pattern , pattern )     
      mapa[posun + r , supery,0] = pattern 
      mapa[posun + r , supery,1] = pattern 
  


#==============================================================
#zobrazeni nekolika znaku za sebou fontem 8x8
# zn_x = pozice prvního znaku v textu je ve sloupci 0 az 15 ; supery = 0 az 63 (horni okraj znaku)

def slovo(text , zn_x , supery , inverze=False):  

  if (isinstance(text, unicode) == False):  # pokud text neni v unicode, tak ho preved
    text=  unicode(text, "utf-8")           # prevod textu z UTF-8 na unicode

  # cely text prochazet znak po znaku a tisknout
  for zn in range (len(text)):
    if (zn_x < 16): # kontrola prekroceni sirky displeje
      if (ord(text[zn:zn + 1]) > 127):   # pokud jde o neASCII znak, provest prekodovani podle tabulky
        try:                    # pokud neni specialni kod nadefinovany v tabulce, ...
          znak(cz2[ord(text[zn:zn + 1])], zn_x, supery, inverze)
        except:                 # ... skoncil by program chybou neexistujiciho indexu promenne cz2[].
          znak(164, zn_xx, supery , inverze)  # V tom pripade se nahradi nedefinovany znak znakem "kolecko s teckama"
      else:
        znak(ord(text[zn:zn + 1]), zn_x, supery , inverze) # ASCII znaky tisknout normalne
      zn_x = zn_x + 1



#==============================================================
# zobrazeni / smazani / inverze 1 bodu na souradnicich superx (0 az 127) a supery (0 az 63)
def plot(superx , supery , styl=1):

  # kontrola na spravny rozsah souradnic a jejich pripadne upraveni na krajni hodnoty
  if (superx > 127): superx = 127
  if (superx < 0  ): superx = 0
  if (supery > 63 ): supery = 63
  if (supery < 0  ): supery = 0

  horiz = int(superx / 16)
  if (supery >= 32):
    supery = supery - 32
    horiz = horiz + 8

  minibit = superx % 16
 
  posli_bajt2( 0, 0b10000000 + supery , 0b10000000 + horiz )  # nastaveni adresy grafiky

  puvodni_leva  = mapa[horiz,supery,0]
  puvodni_prava = mapa[horiz,supery,1]

  if (minibit < 8):
      if (styl == 1):  # nakreslit bod
        levy_bajt = (0b10000000 >> minibit) | puvodni_leva
      if (styl == 0):  # smazat bod
        levy_bajt = ~(0b10000000 >> minibit) & puvodni_leva
      if (styl == 2):  # smazat bod
        levy_bajt = (0b10000000 >> minibit) ^ puvodni_leva

      pravy_bajt = puvodni_prava
  else:
      if (styl == 1):  # nakreslit bod
        pravy_bajt = (0b10000000 >> (minibit-8)) | puvodni_prava
      if (styl == 0):  # smazat bod
        pravy_bajt = ~(0b10000000 >> (minibit-8)) & puvodni_prava
      if (styl == 2):  # smazat bod
        pravy_bajt = (0b10000000 >> (minibit-8)) ^ puvodni_prava

      levy_bajt = puvodni_leva

  posli_bajt2( 1, levy_bajt, pravy_bajt)
  mapa[horiz,supery,0] = levy_bajt
  mapa[horiz,supery,1] = pravy_bajt



#==============================================================
# zobrazeni / smazani / inverze 1 bodu na souradnicich superx (0 az 127) a supery (0 az 63)
def mem_plot(superx , supery , styl=1):
  horiz = int(superx / 16)
  
  if (supery >= 32):
    supery = supery - 32
    horiz = horiz + 8

  minibit = superx % 16
 
  puvodni_leva  = mapa[horiz,supery,0]
  puvodni_prava = mapa[horiz,supery,1]

  if (minibit < 8):
      if (styl == 1):  # nakreslit bod
        levy_bajt = (0b10000000 >> minibit) | puvodni_leva
      if (styl == 0):  # smazat bod
        levy_bajt = ~(0b10000000 >> minibit) & puvodni_leva
      if (styl == 2):  # smazat bod
        levy_bajt = (0b10000000 >> minibit) ^ puvodni_leva

      pravy_bajt = puvodni_prava
  else:
      if (styl == 1):  # nakreslit bod
        pravy_bajt = (0b10000000 >> (minibit-8)) | puvodni_prava
      if (styl == 0):  # smazat bod
        pravy_bajt = ~(0b10000000 >> (minibit-8)) & puvodni_prava
      if (styl == 2):  # smazat bod
        pravy_bajt = (0b10000000 >> (minibit-8)) ^ puvodni_prava

      levy_bajt = puvodni_leva

  mapa[horiz,supery,0] = levy_bajt
  mapa[horiz,supery,1] = pravy_bajt



#==============================================================
# nacteni fontu 8x8 bodu ze souboru do seznamu "font2[]"
def nacist_font2(jmenosouboru):
  fontfile=file(jmenosouboru,"r")
  adresafontu=0
  for radka in fontfile:
    rozlozeno = radka.split(",")                   # vysosani jednotlivych bajtu z jedne radky ...
    for bajt in range(8):                          # 8 bajtu na jedne radce v souboru
      font2[adresafontu] = int(rozlozeno[bajt][-4:],0) # ... a ulozeni kazdeho toho bajtu do seznamu
      adresafontu = adresafontu + 1
  fontfile.close()
  


#==============================================================
# podprogram pro zobrazeni textu obrim fontem (8x16 bodu)
# definice fontu je soucasti ROM v displeji - neumi tedy ceske znaky
# zn_x = pocatecni sloupec, na který se zacne text vypisovat [0 az 16]
# radka je v rozsahu [0 az 3]
def velky_napis(text , zn_x , radka): 

  if (len(text)+ zn_x > 16):      # pokud je na radce text delsi, nez 16 znaku,
    text=text[0:16 - zn_x]        # ... tak se konec odsekne
 
  txt_start(zn_x , radka)         # startovni poloha textu se posle do displeje
  for znak in range(len(text)):
    posli_bajt1( 1, ord(text[znak:znak+1]))  # znaky z textu se postupne posilaji do displeje
    pomtext=txtmapa[radka][:zn_x+znak] + text[znak:znak+1] + txtmapa[radka][zn_x+znak+1:]
    txtmapa[radka] = pomtext      # pamet pro textovy rezim



#==============================================================
# zobrazeni jednoho znaku v textovem rezimu
def velky_znak(kod , zn_x, radka): 

  txt_start(zn_x , radka)         # startovni poloha textu se posle do displeje
  posli_bajt1( 1, kod)            # kod znaku se posle do displeje
  pomtext=txtmapa[radka][:zn_x] + chr(kod) + txtmapa[radka][zn_x+1:]
  txtmapa[radka] = pomtext        # pamet pro textovy rezim



#==============================================================
# nastaveni pozice tisku pro textovy rezim (pro znaky 8x16 bodu)
# sloupec (0 az 15) a radku (0 az 3)
def txt_start(sloupec , radka):  
  posun = sloupec
  if (radka == 1) : posun = sloupec + 32
  if (radka == 2) : posun = sloupec + 16
  if (radka == 3) : posun = sloupec + 48

  posli_bajt1( 0, 0b10000000 + int(posun / 2))  # Address Counter na pozadovanou pozici

  # pri lichem sloupci se musi napis doplnit o znak, ktery je na displeji pred nove tisknutym napisem 
  if (sloupec / 2.0 != sloupec/2):
    puvodni_predznak = txtmapa[radka][sloupec - 1:sloupec] # "predznak" se zjistuje z pomocne textove pameti
    posli_bajt1( 1, ord(puvodni_predznak)) 



#==============================================================
# nacteni dvoubarevneho BMP obrazku 128x64 bodu do promenne mapa[]
# POZOR: Bez jakychkoli testu na korektni format BMP souboru!
def load_bmp12864(jmeno_obrazku):
  soubor=open(jmeno_obrazku, "rb")  # nacteni obrazku do promenne data[]
  data = soubor.read()  
  soubor.close()                    # uzavreni souboru

  # podrobna specifikace hlavicky BMP souboru je tady:
  # http://www.root.cz/clanky/graficky-format-bmp-pouzivany-a-pritom-neoblibeny
  # zacatek obrazovych dat urcuji 4 bajty v souboru na pozicich 10 az 13 (desitkove) od zacatku souboru
  zacatekdat = ord(data[10]) + (ord(data[11]) * 256) + (ord(data[12]) * 65536) + (ord(data[13]) * 16777216)
  bajt=zacatekdat

  for mikroradka in range (63,-1,-1):  # cteni promenne data[] bajt po bajtu a postupne ukladani do pameti (mapa[])
    supery = mikroradka
    if (mikroradka > 31):
      supery = supery - 32
      posun = 8
    else:
      posun = 0
    posli_bajt2( 0, 0b10000000 + supery , 0b10000000 + posun )  # nastaveni adresy grafiky
    for sloupec in range (8):
      levy_bajt = (ord(data[bajt]))
      pravy_bajt = (ord(data[bajt+1]))
      posli_bajt2( 1, levy_bajt, pravy_bajt)     # 
      mapa[sloupec+posun , supery,0] = levy_bajt
      mapa[sloupec+posun , supery,1] = pravy_bajt

      bajt = bajt + 2          # prejde na dalsi dvojbajt z grafickych dat



#==============================================================
# presypani cele graficke pameti (promenne mapa[]) na displej
def mem_dump():

  for mikroradka in range(32):
    posli_bajt2( 0, 0b10000000 + mikroradka , 0b10000000 )  # nastaveni adresy grafiky
    for horizontal in range (16):
      levy_bajt  = mapa[horizontal , mikroradka , 0] 
      pravy_bajt = mapa[horizontal , mikroradka , 1]
      posli_bajt2( 1, levy_bajt, pravy_bajt)    
       
       

#==============================================================
# smazani graficke casi displeje
def clr_grafika(pattern = 0): 

  init_grafika()
  posli_bajt1( 0, 0b00110110)  # function set (extend instr.set)
  posli_bajt1( 0, 0b00110100)  # function set (grafika OFF) - aby nebylo videt postupne mazani displeje
  posli_bajt1( 0, 0b00001000)  # displ.=OFF , cursor=OFF , blik=OFF
  
  for vertikal in range(32):  
    posli_bajt2( 0, 0b10000000 + vertikal, 0b10000000 )  # nastaveni adresy na displeji na zacatek mikroradky
    for horizontal in range (16):
      posli_bajt2( 1, pattern , pattern )     # po dvojbajtech zaplni cely displej stejnym kodem   
 
      # a tento kod se jeste zapise na jednotlive pozice do pomocne pameti
      mapa[horizontal,vertikal,0]=pattern    
      mapa[horizontal,vertikal,1]=pattern
      
  posli_bajt1( 0, 0b00110110)  # function set (grafika ON) - smazany displej se zobrazi okamzite



#==============================================================
# smazani textove casti displeje 
def clr_text(): 
  posli_bajt1( 0, 0b00110000)  # function set (8 bit)
  posli_bajt1( 0, 0b00110000)  # function set (basic instr. set)
  posli_bajt1( 0, 0b00001100)  # displ.=ON , cursor=OFF , blik=OFF
  posli_bajt1( 0, 0b00000001)  # clear

  # vymazani pomocne textove pameti
  txtmapa[0] = "                "
  txtmapa[1] = "                "
  txtmapa[2] = "                "
  txtmapa[3] = "                "



#==============================================================
# smazani graficke a zaroven i textove casti displeje.
# POZOR: po navratu je displej nastaven v TEXTOVEM rezimu
def disclear(pattern=0):
  clr_grafika(pattern)
  clr_text()



#==============================================================
# nastavi displej do grafickeho rezimu
def init_grafika():  
  posli_bajt1( 0, 0b00110010)  # function set (8 bit)
  posli_bajt1( 0, 0b00110110)  # function set (extend instr. set)
  posli_bajt1( 0, 0b00110110)  # function set (grafika ON)
  posli_bajt1( 0, 0b00000010)  # enable CGRAM po prenastaveni do BASIC instr.set



#==============================================================
# nastavi displej do textoveho rezimu
def init_text():  
  posli_bajt1( 0, 0b00110000)  # function set (8 bit)
  posli_bajt1( 0, 0b00110100)  # function set (extend instr. set)
  posli_bajt1( 0, 0b00110110)  # function set (grafika OFF)
  posli_bajt1( 0, 0b00000010)  # enable CGRAM (po prenastaveni do BASIC instr.set)
  posli_bajt1( 0, 0b00110000)  # function set (basic instr. set)
  posli_bajt1( 0, 0b00001100)  # displ.=ON , cursor=OFF , blik=OFF
  posli_bajt1( 0, 0b10000000)  # Address Counter na levy horni roh



#==============================================================
# definice grafickeho tvaru 4 ikon o velikosti 16x16 bodu
# ikona = cislo ikony 0 az 3
# ikodata = pole 16 x dvojbajtova hodnota 
def defikon(ikona,ikodata):
  init_text()
  posli_bajt1( 0, 64 + (ikona * 16) )  # nastaveni adresy grafiky
  for dat in range(16):
    levy_bajt  = ikodata[dat] / 256
    pravy_bajt = ikodata[dat] % 256
    posli_bajt2( 1, levy_bajt , pravy_bajt)



#==============================================================
# rozblikani kurzoru za poslednim zadanym znakem v textovem rezimu
# je urceny pro cinske znaky, takze blika velky ctverec 16x16 bodu
# (pro evropske znaky (8x16 bodu) je to tedy nepouzitelne)
def blikkurzor(stav):
  init_tetx()
  if (stav == True):
    posli_bajt1( 0, 0b00001111)  # displ.=ON , cursor=ON , blik=ON
  else:
    posli_bajt1( 0, 0b00001100)  # displ.=ON , cursor=OFF , blik=OFF
  


#==============================================================
#nastavi pozici na prislusny sloupec (0 az 7) a radku (0 az 3)
# pro velké znaky a ikony (16x16 bodu)
def ikopos(sloupec , radka): 
  posun = sloupec
  if (radka == 1) : posun = sloupec + 16
  if (radka == 2) : posun = sloupec + 8
  if (radka == 3) : posun = sloupec + 24

  posli_bajt1( 0, 0b10000000 + posun)  # Address Counter na pozadovanou pozici



#==============================================================
# nastaveni datoveho pinu pri seriove komunikaci na "0" nebo "1" 
def serd(bit):
  if (bit == 1):
     GPIO.output(sdata_pin, True)
  else:
     GPIO.output(sdata_pin, False)



#==============================================================
# kratky jednickovy impulz na hodinovem pinu pri seriove komunikaci
def strobe():
     GPIO.output(sclk_pin, True)
     time.sleep(0.0000001)
     GPIO.output(sclk_pin, False)
     time.sleep(0.0000001)
  


#==============================================================
# podprogram pro odeslani dvou bajtu po seriove komunikaci bez preruseni mezi jednotlivymi bajty
def posli_bajt2(  rs,  bajt1, bajt2):

  serd(1)                # zacatek komunikace se provadi "synchro" sekvenci 5 jednicek
  for i in range (5):
    strobe()
  
  serd(0)                # pak se odesle RW bit (pri zapisu je nastaven na "0")
  strobe()
  serd(rs)               # pak se posle RS bit (prikazy = "0" ; data = "1")
  strobe()
  serd(0)                # nasleduje nulovy bit
  strobe()
 
  for i in range(7,3,-1):     # a pak horni ctyri bity z prvniho bajtu
    bit = (bajt1 & (2**i)) >> i
    serd(bit)
    strobe()

  serd(0)                     # dale je oddelovaci sekvence 4x "0"
  for i in range (4):
    strobe()

  for i in range(3,-1,-1):    # a pak nasleduje zbytek z prvniho bajtu (nizsi 4 bity)
    bit = (bajt1 & (2**i)) >> i
    serd(bit)
    strobe()

  serd(0)                      # potom je zase oddelovaci sekvence 4x "0"
  for i in range (4):
    strobe()

  # druhy bajt se odesila okamzite bez "hlavicky" (bez 5x "1" + RW bit + RS bit + "0")
  for i in range(7,3,-1):        # i tento druhy bajt je rozdeleny na 2 casti (horni 4 bity)
    bit = (bajt2 & (2**i)) >> i
    serd(bit)
    strobe()

  serd(0)                        # oddelovaci sekvence 4x "0"
  for i in range (4):
    strobe()

  for i in range(3,-1,-1):       # spodni 4 bity
    bit = (bajt2 & (2**i)) >> i
    serd(bit)
    strobe()

  serd(0)                         # posledni oddelovaci sekvence 4x "0"
  for i in range (4):
    strobe()



#==============================================================
# odeslani jednoho bajtu po seriove komunikaci
def posli_bajt1(  rs,  bajt):

  serd(1)                # zacatek komunikace se provadi "synchro" sekvenci 5 jednicek
  for i in range (5):
    strobe()
  
  serd(0)                    # pak se odesle RW bit (pri zapisu je nastaven na "0")        
  strobe()                                                                                  
  serd(rs)                    # pak se posle RS bit (prikazy = "0" ; data = "1")            
  strobe()                                                                                                                                           
  serd(0)                     # nasleduje nulovy bit                                                        
  strobe()
  
  for i in range(7,3,-1):     # a pak horni ctyri bity z odesilaneho bajtu
    bit = (bajt & (2**i)) >> i
    serd(bit)
    strobe()

  serd(0)                     # potom se odesle oddelovaci sekvence 4x "0"
  for i in range (4):
    strobe()

  for i in range(3,-1,-1):    # po ni nasleduje zbytek dat (spodni 4 bity z odesilaneho bajtu)
    bit = (bajt & (2**i)) >> i
    serd(bit)
    strobe()

  serd(0)                      # na zaver opet oddelovaci sekvence 4x "0"
  for i in range (4):
    strobe()



#==============================================================
# pocatecni nastaveni HW + reset displeje
def init():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(sdata_pin, GPIO.OUT)    # (pin 26 = GPIO7)   = DATA
  GPIO.setup(sclk_pin, GPIO.OUT)     # (pin 24 = GPIO8)   = HODINY
  GPIO.setup(reset_pin, GPIO.OUT)    # (pin 22 = GPIO25)  = RESET

  GPIO.output(sdata_pin, False)      # DATA do "0"
  GPIO.output(sclk_pin, False)       # HODINY do "0"
  GPIO.output(reset_pin, False)      # RESET do "0"
  time.sleep(0.1)   
  GPIO.output(reset_pin, True)       # RESET do "1"


#==============================================================
if __name__ == '__main__':
  main()
