
#!/usr/bin/python
# -*- encoding: utf-8 -*-

# - = - = - = - = - = - = - = - = - = - = - = - = - = -
#
# Notes from translation:
#
# English translation from this translation project:
# https://github.com/SrBrahma/RPi-128x64LCD-ST7920-controller-12864ZW-
#
# Most of the translation is crappy. It is based on Google Translator.
# There is still missing some words that I can't find anywhere, maybe typos from author.
#
# - = - = - = - = - = - = - = - = - = - = - = - = - = -


# Last edit: 15.7.2013

# Display 12864 ZW display (128x64 point) SERIAL:
# Display output (meaning)  -    connected to ...
# 1  (GND)                - RasPi (GPIO GND   - pin 6)
# 2  (+ power supply)         - RasPi (GPIO +5V   - pin 1)
# 3  VO                   - 
# 4  (RS Data/Command)    - +5V (CHIP SELECT - In serial communication)
# 5  (R/W Read/Write)     - RasPi (Serial data) - GPIO7 (pin26) 
# 6  (E - QuickPulse)         - RasPi (serial CLOCK) - GPIO8 (pin24)
# 7  (Data bit0)          - 
# 8  (Data bit1)          - 
# 9  (Data bit2)          - 
# 10 (Data bit3)          - 
# 11 (Data bit4)          - 
# 12 (Data bit5)          - 
# 13 (Data bit6)          - 
# 14 (Data bit7)          - 
# 15 (PSB)                - GND - Set serial communication
# 16 (NC)                 -
# 17 (Reset)              - RasPi - GPIO25(pin22)
# 18 (Vout)               - 
# 19 (Podsvet - A)        - +5V (Or any LED brightness regulator - about 60mA)
# 20 (Podsvet - K)        - RasPi (GPIO GND - pin 6)


import time              # Various operations with time (pauses)
import RPi.GPIO as GPIO  # It can only be used when attaching the E or RS signal to the GPIO in RasPi
import math              # It will only be used in the examples of drawing circles
import random            # It is used only in the indices for generating random coordinates


# Translation of Czech characters from a font file
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

cz2[228] = 228      # pronounced a
cz2[235] = 235      # pronounced e
cz2[239] = 239      # pronounced i
cz2[246] = 246      # pronounced o
cz2[252] = 252      # pronounced u
cz2[196] = 196      # pronounced A
cz2[214] = 214      # pronounced O
cz2[220] = 220      # pronounced U

cz2[176] = 176      # stupen
cz2[177] = 177      # plus minus
cz2[171] = 171      # dvojsipka vlevo
cz2[166] = 166      # prerusene svislitko
cz2[223] = 223      # beta

# Assign GPIO pin
sdata_pin = 7       # (pin 26 = GPIO7)   = DATA    
sclk_pin = 8        # (pin 24 = GPIO8)   = CLOCK  
reset_pin = 25      # (pin 22 = GPIO25)  = RESET   

mapa={}             # Memory to store the current status of the displayed pixels on the display
txtmapa={}          # Memory to which the current text status on the display is saved
font2={}            # The memory in which the font is stored is retrieved from the external file
iconData={}          # The variable through which the graphical Icons will be defined


#==============================================================
# Main program
#==============================================================

def main():

  init()              # Basic HW system setup - port directions on the expander and reset the display
  ClearDisplay(0)         # Complete deletion of the display
  nacist_font2("/home/pi/font2.txt")  # Retrieve an external font from the file



#==============================================================
#              Starts the pointers of all the functions
#==============================================================


#- - - - - - - - - Writing text to the display - - - - - - - - - - - - - - - - - - - -  
  InitTextMode()     # Switch to text mode

  PrintBigString("Viewing pointer",0,0)   # Display the text in the text mode at specified coordinates
  PrintBigString("display",4,1)
  PrintBigString("in text",3,2)
  PrintBigString("mode",5,3)

  time.sleep(2)
  PrintBigString("chr(1)...chr(32)", 0 , 1)
  char_code = 0
  for r in range(2,4):
    for s in range (16):
      char_code = char_code + 1
      PrintCharGreat(char_code , s , r)   # Character display in text mode according to its (ASCII) code
  time.sleep(3)
  
  PrintBigString("chr(33)..chr(64)" , 0 , 1)
  for r in range(2,4):
    for s in range (16):
      char_code = char_code + 1
      PrintCharGreat(char_code , s , r)
     

  time.sleep(3)
  ClearText()               # smazani textove casti displeje
  time.sleep(1)

#- - - - - - - - - Icons - - - - - - - - - - - - - - - - - - - -  
  PrintBigString("Own Icons" , 0 , 0)
 
 
  # Definition of a zig-zag form of 4 own icons:
   # First User-Defined Icon (Focus Crisis)
  iconData[0]  =  0b0011111111111100
  iconData[1]  =  0b0111111111111110
  iconData[2]  =  0b1110000110000111
  iconData[3]  =  0b1100000110000011
  iconData[4]  =  0b1100000110000011
  iconData[5]  =  0b1100000000000011
  iconData[6]  =  0b1100000000000011
  iconData[7]  =  0b1111100110011111
  iconData[8]  =  0b1111100110011111
  iconData[9]  =  0b1100000000000011
  iconData[10] =  0b1100000000000111
  iconData[11] =  0b1100000110000011
  iconData[12] =  0b1100000110000011
  iconData[13] =  0b1110000110000111
  iconData[14] =  0b0111111111111110
  iconData[15] =  0b0011111111111100
  DefineIcon(0 , iconData)

  # Second user-defined icon (square with crash)
  iconData[0]  =  0b1111111111111111
  iconData[1]  =  0b1111111111111111
  iconData[2]  =  0b1110000000000111
  iconData[3]  =  0b1101000000001011
  iconData[4]  =  0b1100100000010011
  iconData[5]  =  0b1100010000100011
  iconData[6]  =  0b1100001001000011
  iconData[7]  =  0b1100000110000011
  iconData[8]  =  0b1100000110000011
  iconData[9]  =  0b1100001001000011
  iconData[10] =  0b1100010000100011
  iconData[11] =  0b1100100000010011
  iconData[12] =  0b1101000000001011
  iconData[13] =  0b1110000000000111
  iconData[14] =  0b1111111111111111
  iconData[15] =  0b1111111111111111
  DefineIcon(1 , iconData)


  # Third user-defined icon (empty square)
  iconData[0]  =  0b1111111111111111
  iconData[1]  =  0b1111111111111111
  iconData[2]  =  0b1100000000000011
  iconData[3]  =  0b1100000000000011
  iconData[4]  =  0b1100000000000011
  iconData[5]  =  0b1100000000000011
  iconData[6]  =  0b1100000000000011
  iconData[7]  =  0b1100000000000011
  iconData[8]  =  0b1100000000000011
  iconData[9]  =  0b1100000000000011
  iconData[10] =  0b1100000000000011
  iconData[11] =  0b1100000000000011
  iconData[12] =  0b1100000000000011
  iconData[13] =  0b1100000000000011
  iconData[14] =  0b1111111111111111
  iconData[15] =  0b1111111111111111
  DefineIcon(2 , iconData) 
  
  # Fourth user-defined icon (crisis in a circle)
  iconData[0]  =  0b0000011111100000
  iconData[1]  =  0b0000100110010000
  iconData[2]  =  0b0011000110001100
  iconData[3]  =  0b0010000110000100
  iconData[4]  =  0b0100000110000010
  iconData[5]  =  0b1000000110000001
  iconData[6]  =  0b1000000110000001
  iconData[7]  =  0b1111111111111111
  iconData[8]  =  0b1111111111111111
  iconData[9]  =  0b1000000110000001
  iconData[10] =  0b1000000110000001
  iconData[11] =  0b0100000110000010
  iconData[12] =  0b0010000110000100
  iconData[13] =  0b0011000110001100
  iconData[14] =  0b0000100110010000
  iconData[15] =  0b0000011111100000
  DefineIcon(3 , iconData) 

  PrintIcon(1 , 0 , 1)    # Icon c.2 at the top of the second row from the top
  for icon in range (7):  # The rest of the row is filled with random icons  
    # When you print the icons for yourself, you do not have to set positions for each
    icon = random.randint(0,3) * 2 # The last parameter is double the number of Icons
    Send2Bytes( 1 ,  0 , icon)    

  PrintIcon(2 , 0 , 2)    # Icon c.3 at the top of the third row from above
  for icon in range (7):  # The rest of the row is filled with random icons
    # When you print the icons for yourself, you do not have to set positions for each
    icon = random.randint(0,3) * 2 # The last parameter is the double-pin number Icons
    Send2Bytes( 1 ,  0 , icon)    

  PrintIcon(3 , 0 , 3)    # icon c.4 na zacatek spodni radky 
  for icon in range (7):  # cely zbytek te radky se zaplni ikonou c.4
    # kdyz se tiskne vic ikon za sebe, tak se nemusi u kazde nastavovat pozice
    Send2Bytes( 1 ,  0 , 6)    # (6 = icon c.4)    



  time.sleep(2)
  PrintBigString(" zmena definice ", 0 , 0)
  time.sleep(2)
  PrintBigString("  ctvrte Icons  ", 0 , 0)
  time.sleep(2)

  
  # When changing the Icons definition, OK to change the appearance of ALL Icons displayed
   # Fourth user-defined icon will now be moved to the shuffle
  iconData[0]  =  0b1111000011110000
  iconData[1]  =  0b1111000011110000
  iconData[2]  =  0b1111000011110000
  iconData[3]  =  0b1111000011110000
  iconData[4]  =  0b0000111100001111
  iconData[5]  =  0b0000111100001111
  iconData[6]  =  0b0000111100001111
  iconData[7]  =  0b0000111100001111
  iconData[8]  =  0b1111000011110000
  iconData[9]  =  0b1111000011110000
  iconData[10] =  0b1111000011110000
  iconData[11] =  0b1111000011110000
  iconData[12] =  0b0000111100001111
  iconData[13] =  0b0000111100001111
  iconData[14] =  0b0000111100001111
  iconData[15] =  0b0000111100001111
  DefineIcon(3 , iconData) 
 
  time.sleep(3)
  ClearText()
  
#- - - - - - - - -Cinske charactery - - - - - - - - - - - - - - - -  
  PrintBigString("   Jako Icons   " , 0 , 0)
  PrintBigString("  se zobrazuji  " , 0 , 1)
  PrintBigString(" i cinske charactery " , 0 , 2)
  time.sleep(3)
  ClearText()

  # tisk CINSTINY obrim fontem 16x16 bodu (v textovem mode)
  # Tohle jsou jen nahodne vybrane charactery (cinstina mi nic nerika)
  # character je vybran pomoci poslednich dvou cisel funkce "Send2Bytes()"
  # prvni z tech dvou cisel musi byt vyssi, nez 127

  SetIconPos(2,0)                       # nastaveni pozice prvniho characteru [0,0] az [7,3]
  Send2Bytes( 1 , 200 , 150)   
  Send2Bytes( 1 , 218 , 10)
  Send2Bytes( 1 , 128 , 1)
  Send2Bytes( 1 , 211 , 200)

  SetIconPos(4,2)                       # nastaveni pozice prvniho characteru [0,0] az [7,3]
  Send2Bytes( 1 , 240 , 4)   
  Send2Bytes( 1 , 240 , 33)
  Send2Bytes( 1 , 240 , 222)

  # svisly ctyrcharacterovy napis
  SetIconPos(0,0)                       # nastaveni pozice characteru 
  Send2Bytes( 1 , 128 , 18)   
  SetIconPos(0,1)                       # nastaveni pozice characteru 
  Send2Bytes( 1 , 154 , 251)
  SetIconPos(0,2)                       # nastaveni pozice characteru 
  Send2Bytes( 1 , 197 , 37)
  SetIconPos(0,3)                       # nastaveni pozice characteru 
  Send2Bytes( 1 , 141 , 90)


  time.sleep(3)
  ClearText()


#- - - - - - - - -  Text in the graphics mode - - - - - - - - - - - - - - - - - - -  
# Print 8x8 dot font (in graphic mode)

  InitGraphicMode()
  slovo("Displej je y" , 0 ,  0 , False)  # normalni graficky napis na horni radku
  slovo("provozovat"       , 3 , 15 , False)        
  slovo("i v grafickem"    , 1 , 30 , False) 
  slovo("mode"           , 5 , 45 , False)  

  time.sleep(2)
  slovo("grafickem"        , 5 , 30 , True)  # inverzne prepsany text  

  time.sleep(3)
  ClearGraphic()    # smazani graficke casti displeje


  # ve stejnem mode je y tisknout jednotlive charactery podle jejich kodu
  for kod in range(32,128):
    column = (kod-32) % 16
    row = int((kod-32)/16) * 11        # rozestupy mezi rowmi jsou 11 bodu
    if (row / 22.0 == int(row/22)):  # kazda druha row je inverzni
      inverze = True
    else:
      inverze = False
      
    character(kod , column, row , inverze) # podprogram pro tisk characteru v grafickem mode 

  time.sleep(2)
  ClearGraphic()

  for kod in range(128,256):
    column = (kod-128) % 16
    row = int((kod-128)/16) * 8 
    character(kod , column, row , False)

  time.sleep(2)
  ClearGraphic()


#- - - - - - - tisk bodu a car - - - - - - - - - - - - - - - - - -  

  slovo(" V tomto mode " ,0, 2,False)  # normalni napis 2 pixely od horniho okraje
  slovo("je y kreslit" ,0,11,False)        
  slovo("  body a line   " ,0,20,False) 

  # oramovani displeje plnou carou
  h_line (  0 ,  0 , 127 , 1)          # horizontalni line na libovolne pozici
  h_line2( 63 ,  0 ,   7 , 0b11111111) # Speed mountains. Line in a 16-column raster with mask setting
  v_line (  0 ,  0 ,  63 , 0b11111111) # vertikalni line v libovolne pozici s nastavenim masky
  v_line (127 ,  0 ,  63 , 0b11111111)

  # vnitrni mensi obdelnik carkovanou carou
  h_line2(  31 ,  1 ,   6 , 0b11001100)
  h_line2( 56 ,   1 ,   6 , 0b11001100)
  v_line ( 16 ,  31 ,  56 , 0b11001100)
  v_line (111 ,  31 ,  56 , 0b11001100)


  # nahodne nasypani bodu do maleho obdelniku v inverznim mode
  for i in range(2000):
    x= int(random.randint(17,110))
    y= int(random.randint(32,55))
    plot( x , y , 2)   # tisk inverzniho bodu na souradnice [x,y]


#- - - - - - - - - - - - ruzne styly horizontalnich car - - - - - - - - - - - - - - - - -  
  ClearGraphic()

  h_line2(  0 ,  2 ,   5 , 0b11111111) # Speed mountains. Line in a 16-column raster with mask setting
  h_line2( 10 ,  3 ,   4 , 0b11001100) # Speed mountains. Line in a 16-column raster with mask setting
  h_line2( 20 ,  2 ,   5 , 0b11110000) # Speed mountains. Line in a 16-column raster with mask setting
  h_line2( 30 ,  1 ,   6 , 0b10101010) # Speed mountains. Line in a 16-column raster with mask setting
  h_line2( 40 ,  0 ,   7 , 0b11110101) # Speed mountains. Line in a 16-column raster with mask setting
  h_line2( 50 ,  1 ,   6 , 0b01110101) # Speed mountains. Line in a 16-column raster with mask setting

  time.sleep(3)

  ClearGraphic(0xff)    # To fill the screen with white ink

#- - - - - - - - - - drawing - - - - - - - - - - - - - - - - - - - -  
  # Draw a double circle using the first print point on the display (slowly)
  for circle in range(0,6283,4):
    x = int(((math.sin(circle/1000.0) * 30.0)) + 32)
    y = int(((math.cos(circle/1000.0) * 30.0)) + 32)
    plot(x,y,0)
    x = int(((math.sin(circle/1000.0) * 20.0)) + 32)
    y = int(((math.cos(circle/1000.0) * 20.0)) + 32)
    plot(x,y,0)

  # vykresleni peti kruznic s vyuzitim zapisu do pameti
  #    a nasledneho presypani cele pameti na displej  (rychle)
  for circle in range(0,6283,4):
    x = int(((math.sin(circle/1000.0) * 30.0)) + 96)
    y = int(((math.cos(circle/1000.0) * 30.0)) + 32)
    mem_plot(x,y,0)
    x = int(((math.sin(circle/1000.0) * 25.0)) + 96)
    y = int(((math.cos(circle/1000.0) * 25.0)) + 32)
    mem_plot(x,y,0)
    x = int(((math.sin(circle/1000.0) * 20.0)) + 96)
    y = int(((math.cos(circle/1000.0) * 20.0)) + 32)
    mem_plot(x,y,0)
    x = int(((math.sin(circle/1000.0) * 15.0)) + 96)
    y = int(((math.cos(circle/1000.0) * 15.0)) + 32)
    mem_plot(x,y,0)
    x = int(((math.sin(circle/1000.0) * 10.0)) + 96)
    y = int(((math.cos(circle/1000.0) * 10.0)) + 32)
    mem_plot(x,y,0)

  MemDump()    # presypani dat z pameti na displej



  time.sleep(2)
  ClearGraphic()

#- - - - - - - - - - Overwrite text and graphic mode - - - - - - - - - -  

  slovo("    Graficky    " , 0 ,  0 , False)
  slovo("a  textovy rezim" , 0 , 10 , False) 
  slovo("je  y pouzit" , 0 , 20 , False) 
  slovo("     zaroven    " , 0 , 30 , False) 

  time.sleep(2)
  ClearGraphic()
 
  InitTextMode()      # Switch the display to text mode
  PrintBigString("Velky  napis" , 2 , 0)
  PrintBigString("v textovem"   , 3 , 1)
  PrintBigString("mode"       , 5 , 2)
  PrintIcon(1 , 0 , 2)
  PrintIcon(1 , 7 , 2)  


  time.sleep(2)

  InitGraphicMode()  # Switch display to graphic mode
  h_line2( 53 ,  0 ,   7 , 0b10011001) 
  slovo("Graficka row" , 1 , 56 , False)   


  
  # When combining text and graphic mode, the common area on the XOR displays
  # Example: 4 points thick sikma line over the entire screen

  for x in range(128):
    plot(x ,x/2      , 1)
    plot(x,(x/2) + 1 , 1)
    plot(x,(x/2) + 2 , 1)
    plot(x,(x/2) + 3 , 1)

  time.sleep(2)
  slovo("Delete graphics" , 0 , 56 , True)   

  time.sleep(2)
  ClearGraphic()   # The graphic is deleted separately, so the original text remains

  slovo("  Text zustava  " , 0 , 56 , True)   
  time.sleep(2)
  slovo("Dokresleni  line" , 0 , 56 , True)   

  for x in range(128):
    plot(127-x ,x/2      , 1)
    plot(127-x,(x/2) + 1 , 1)
    plot(127-x,(x/2) + 2 , 1)
    plot(127-x,(x/2) + 3 , 1)

  time.sleep(2)
  slovo(" Smazani  textu " , 0 , 56 , True)   
  time.sleep(1)

  ClearText()                # textovy displej je y take smazat samostatne
  InitGraphicMode()
  MemDump()                # graphic se ale v tom pripade musi obnovit z pameti
  
  time.sleep(1)
  slovo("graphic  zustava" , 0 , 56 , True)   
  time.sleep(2)
  ClearGraphic()

#- - - - - - - - - nahrani obrazku - - - - - - - - - - - - - - - - - -  

  slovo("   zobrazeni    " ,0,  0,False)  # 
  slovo("    souboru     " ,0, 10,False)  # 
  slovo("  s  obrazkem   " ,0, 20,False)  # 
  time.sleep(2)
  LoadBMP12864("/home/pi/pokladnik.bmp")  # nahrani bitmapy o velikosti 128x64 bodu na displej 

  time.sleep(4)

  # zaplneni displeje svislymi linemi (pattern = 0b10101010)
  ClearDisplay(0b10101010) # po funkci ClearDisplay() zustava displej v textovem mode
  InitGraphicMode()       # proto je treba ho pred dalsi grafickou funkci prepnout do grafickeho mode

  slovo(" K O N E C " , 2 , 25 , True)   
 
  exit(0)




#==============================================================
#               All subroutines are:
#==============================================================



#==============================================================
# One of the 4 defined 16 x 16 pixel icons at position [x, y]
# X is in the range 0 to 7
# Y ranges from 0 to 3
def PrintIcon(number , x , y):
  shift = x
  if (y == 1) : shift = shift + 16
  if (y == 2) : shift = shift + 8
  if (y == 3) : shift = shift + 24
  SendByte( 0, 0b10000000 + shift)  # Address Counter to the required position
  Send2Bytes( 1 ,  0 , number * 2)



#==============================================================
# Displaying one character from the 8x8 point font
# Zn_x = X-axis character position (0 to 15), supery = 0 to 63 (microrow on top of character)

def character(kod , zn_x , supery , inverze=False):  

  # kontrola svtupnich parametru a jejich pripadne prenastaveni na krajni meze
  if (kod    <  32) : kod = 32
  if (kod    > 255) : kod = 255
  if (zn_x   <   0) : zn_x = 0  
  if (zn_x   >  15) : zn_x = 15  
  if (supery >  63) : supery = 63
  if (supery <   0) : supery = 0

  kod = kod - 32     # v souboru s fontem je jako prvni character definovana mezera s kodem 32
  superx = zn_x * 8

  # obraz characteru z fontu se bude postupne prenaset na displej byte po byteu v 8 krocich (zhora dolu) 
  for adr_font in range(kod*8,(kod*8)+8):

    # vypocet horizontalni a vertikalni adresy v pameti displeje
    horiz = int(superx / 16)  
    dis_adr_y = supery
    if (dis_adr_y >= 32):
      dis_adr_y = dis_adr_y - 32
      horiz = horiz + 8
  
    minibit = superx % 16     # poloha bitu, se kterym se bude pracovat, v dvojbyteu
   
    Send2Bytes( 0, 0b10000000 + dis_adr_y , 0b10000000 + horiz )  # Setting the graphics address
  
    orignal_leva  = mapa[horiz,dis_adr_y,0]  # zjisteni aktualniho stavu dvojbyteu na displeji
    orignal_prava = mapa[horiz,dis_adr_y,1]

    if(minibit < 8):  # kdyz je minibit < 8, meni se jen left byte z dvojbyteu 
      if (inverze == False):  # normalni text (prepise vsechno, co je pod textem)
        leftByte = font2[adr_font]
      if (inverze == True):   # inverzni text (prepise vsechno, co je pod textem)
        leftByte = ~font2[adr_font]
        
      rightByte = orignal_prava   # right byte z dvojbyteu bude beze zmeny
  
    else:  # kdyz je minibit >= 8, meni se jen right byte z dvojbyteu
      if (inverze == False):  # normalni text (prepise vsechno, co je pod textem)
        rightByte = font2[adr_font]
      if (inverze == True):   # inverzni text (prepise vsechno, co je pod textem)
        rightByte = ~font2[adr_font]

      leftByte = orignal_leva     # left byte z dvojbyteu bude beze zmeny
  
    Send2Bytes( 1, leftByte, rightByte)       # prepise dvojbyte na zadane adrese v displeji  
    mapa[horiz,dis_adr_y,0] = leftByte             # stejne hodnoty si zapamatuje do promenne mapa[]
    mapa[horiz,dis_adr_y,1] = rightByte

    supery = supery + 1   # shift aktualni mikroradky o jednu nize



#==============================================================
# Draw a horizontal line point by point
def h_line(supery, od=0 , do=127, style=1):  
  for x in range(od, do+1):
    plot(x,supery,style)



#==============================================================
# nakresleni vertikalni line s vyuzitim bitove masky
def v_line(superx, od=0 , do=63, pattern = 255):  
  poz_pat = 0                              # pozice bitu v patternu
  for y in range(od , do+1 ):
    maska = (0b10000000 >> (poz_pat % 8))  # podle zadaneho patternu vybira jednotlive bity
    bitpat= pattern & maska
    if (bitpat == 0):                      # ktere na displeji bud zobrazi, nebo smaze
      style = 0
    else:
      style = 1

    plot(superx,y,style)
    poz_pat = poz_pat + 1



#==============================================================
# Draw horizontal line from the edge to the edge after the bytes
def h_line2(supery = 0, fromByte = 0, toByte = 5, pattern = 0b11111111):  
  shift=fromByte
  if (supery >= 32):
    supery = supery - 32
    shift = shift + 8     

  Send2Bytes( 0, 0b10000000 + supery , 0b10000000 + shift )     
  for r in range(toByte - fromByte + 1):
      Send2Bytes( 1, pattern , pattern )     
      mapa[shift + r , supery,0] = pattern 
      mapa[shift + r , supery,1] = pattern 
  


#==============================================================
# Displaying several characters behind the 8x8 font
# Zn_x = the position of the first character in the text is in column 0 to 15; Supers = 0 to 63 (upper margin of the character)

def slovo(text , zn_x , supery , inverze=False):  

  if (isinstance(text, unicode) == False):  # If the text is not in unicode, then transfer it
    text = unicode(text, "utf-8")           # Convert text from UTF-8 to unicode

  # All the text scroll character after character and print
  for zn in range (len(text)):
    if (zn_x < 16): # Screen overlay
      if (ord(text[zn:zn + 1]) > 127):   # As for the ASCII character, proceed as described in the table above
        try:                    # If there is no special code defined in the table, ...
          character(cz2[ord(text[zn:zn + 1])], zn_x, supery, inverze)
        except:                 # ... the program will terminate the error of the non-existent index of the variable cz2 [].
          character(164, zn_xx, supery , inverze)  # In this case, replace the undefined character character "wheel with teckama"
      else:
        character(ord(text[zn:zn + 1]), zn_x, supery , inverze) # ASCII charactery tisknout normalne
      zn_x = zn_x + 1



#==============================================================
# 1-point display / deletion / inversion at superx coordinates (0 to 127) and supers (0 to 63)
def plot(superx , supery , style=1):

  # Checking for the correct range of coordinates and optionally adjusting them to the extreme values
  if (superx > 127): superx = 127
  if (superx < 0  ): superx = 0
  if (supery > 63 ): supery = 63
  if (supery < 0  ): supery = 0

  horiz = int (superx / 16)
  if (supery >= 32):
    supery = supery - 32
    horiz = horiz + 8

  minibit = superx % 16
 
  Send2Bytes ( 0, 0b10000000 + supery , 0b10000000 + horiz )  # Setting the graphics address

  orignal_leva  = mapa[horiz,supery,0]
  orignal_prava = mapa[horiz,supery,1]

  if (minibit < 8):
      if (style == 1):  # Draw a point
        leftByte = (0b10000000 >> minibit) | orignal_leva
      if (style == 0):  # Delete point
        leftByte = ~(0b10000000 >> minibit) & orignal_leva
      if (style == 2):  # Delete point
        leftByte = (0b10000000 >> minibit) ^ orignal_leva

      rightByte = orignal_prava
  else:
      if (style == 1):  # Draw a point
        rightByte = (0b10000000 >> (minibit-8)) | orignal_prava
      if (style == 0):  # Delete point
        rightByte = ~(0b10000000 >> (minibit-8)) & orignal_prava
      if (style == 2):  # Delete point
        rightByte = (0b10000000 >> (minibit-8)) ^ orignal_prava

      leftByte = orignal_leva

  Send2Bytes( 1, leftByte, rightByte)
  mapa[horiz,supery,0] = leftByte
  mapa[horiz,supery,1] = rightByte



#==============================================================
# 1-point display / deletion / inversion at superx coordinates (0 to 127) and supers (0 to 63)
def mem_plot(superx , supery , style=1):
  horiz = int(superx / 16)
  
  if (supery >= 32):
    supery = supery - 32
    horiz = horiz + 8

  minibit = superx % 16
 
  orignal_leva  = mapa[horiz,supery,0]
  orignal_prava = mapa[horiz,supery,1]

  if (minibit < 8):
      if (style == 1):  # Draw a point
        leftByte = (0b10000000 >> minibit) | orignal_leva
      if (style == 0):  # Delete point
        leftByte = ~(0b10000000 >> minibit) & orignal_leva
      if (style == 2):  # Delete point
        leftByte = (0b10000000 >> minibit) ^ orignal_leva

      rightByte = orignal_prava
  else:
      if (style == 1):  # Draw a point
        rightByte = (0b10000000 >> (minibit-8)) | orignal_prava
      if (style == 0):  # Delete point
        rightByte = ~(0b10000000 >> (minibit-8)) & orignal_prava
      if (style == 2):  # Delete point
        rightByte = (0b10000000 >> (minibit-8)) ^ orignal_prava

      leftByte = orignal_leva

  mapa[horiz,supery,0] = leftByte
  mapa[horiz,supery,1] = rightByte



#==============================================================
# Load 8x8 point font from file to list "font2 []"
def nacist_font2(jmenosouboru):
  fontfile=file(jmenosouboru,"r")
  adresafontu=0
  for row in fontfile:
    rozlozeno = row.split(",")                   # vysosani jednotlivych byteu z jedne radky ...
    for byte in range(8):                          # 8 byte on one row in a file
      font2[adresafontu] = int(rozlozeno[byte][-4:],0) # ... and save everyone on the list
      adresafontu = adresafontu + 1
  fontfile.close()
  


#==============================================================
# Subroutine for text display obrim font (8x16 point)
# Font definition is a part of the ROM in the display - therefore not Czech characters
# Zn_x = Initial column where the text will begin to print [0 to 16]
# Row is in the range [0 to 3]
def PrintBigString(text , zn_x , row): 

  if (len(text)+ zn_x > 16):      # pokud je na radce text delsi, nez 16 characteru,
    text = text[0:16 - zn_x]        # ... tak se konec odsekne
 
  SetTextCursorPos(zn_x , row)         # startovni poloha textu se posle do displeje
  for character in range(len(text)):
    SendByte( 1, ord(text[character:character+1]))  # charactery z textu se postupne posilaji do displeje
    pomtext = txtmapa[row][:zn_x+character] + text[character:character+1] + txtmapa[row][zn_x+character+1:]
    txtmapa[row] = pomtext      # pamet pro textovy rezim



#==============================================================
# Single character display in text mode
def PrintCharGreat(code, zn_x, row): 

  SetTextCursorPos(zn_x , row)         # The start position of the text is sent to the display
  SendByte(1, code)            # The character code is sent to the display
  pomtext = txtmapa[row][:zn_x] + chr(code) + txtmapa[row][zn_x+1:]
  txtmapa[row] = pomtext        # Memory for text mode



#==============================================================
# Print position setting for text mode (for characters 8x16 point)
# Column (0 to 15) and line (0 to 3)
def SetTextCursorPos(column , row):  
  shift = column
  if (row == 1) : shift = column + 32
  if (row == 2) : shift = column + 16
  if (row == 3) : shift = column + 48

  SendByte( 0, 0b10000000 + int(shift / 2))  # Address Counter na pozadovanou pozici

  # In the case of --lichen-- columns, the character must be filled in with the character on the display before the new printout
  if (column / 2.0 != column/2):
    orignal_predcharacter = txtmapa[row][column - 1:column] # "Predcharacter" is determined from the auxiliary text memory
    SendByte( 1, ord(orignal_predcharacter)) 



#==============================================================
# Uploading a two-color BMP image of a 128x64 point to a variable map []
# CAUTION: Without any test for a correct BMP file format!
def LoadBMP12864(imageRelativePath):
  fileBMP = open(imageRelativePath, "rb")  # Load an image into a data variable []
  data = fileBMP.read()  
  fileBMP.close()                    # File closure

  # The detailed BMP master file specification is here:
  # http://www.root.cz/clanky/graficky-format-bmp-pouzivany-a-pritom-neoblibeny
  # The start of the image data determines 4 bytes in a file in positions 10 to 13 (ten) from the beginning of the file
  zacatekdat = ord(data[10]) + (ord(data[11]) * 256) + (ord(data[12]) * 65536) + (ord(data[13]) * 16777216)
  byte = zacatekdat

  for mikrorow in range (63,-1,-1):  # Read data variables [] byte after byte and store in memory (map [])
    supery = mikrorow
    if (mikrorow > 31):
      supery = supery - 32
      shift = 8
    else:
      shift = 0
    Send2Bytes( 0, 0b10000000 + supery , 0b10000000 + shift )  # Setting the graphics address
    for column in range (8):
      leftByte = (ord(data[byte]))
      rightByte = (ord(data[byte+1]))
      Send2Bytes( 1, leftByte, rightByte)     # 
      mapa[column+shift , supery,0] = leftByte
      mapa[column+shift , supery,1] = rightByte

      byte = byte + 2          # Passes to another double-out of graphical data



#==============================================================
# Overwrite the graphical memory (variable map []) to the display
def MemDump():

  for mikrorow in range(32):
    Send2Bytes( 0, 0b10000000 + mikrorow , 0b10000000 )  # Setting the graphics address
    for horizontal in range (16):
      leftByte  = mapa[horizontal , mikrorow , 0] 
      rightByte = mapa[horizontal , mikrorow , 1]
      Send2Bytes( 1, leftByte, rightByte)    
       
       

#==============================================================
# smazani graficke casi displeje
def ClearGraphic(pattern = 0): 

  InitGraphicMode()
  SendByte( 0, 0b00110110)  # function set (extend instr.set)
  SendByte( 0, 0b00110100)  # function set (graphic OFF) - aby nebylo videt postupne mazani displeje
  SendByte( 0, 0b00001000)  # displ.=OFF , cursor=OFF , blink=OFF
  
  for vertical in range(32):  
    Send2Bytes( 0, 0b10000000 + vertical, 0b10000000 )  # Setting the address on the display at the beginning of the micro-bar
    for horizontal in range (16):
      Send2Bytes( 1, pattern , pattern )     # Double-bits fill the entire display with the same code   
 
      # And this code still writes to individual positions in the cache
      mapa[horizontal,vertical,0]=pattern    
      mapa[horizontal,vertical,1]=pattern
      
  SendByte( 0, 0b00110110)  # function set (graphic ON) - smazany displej se zobrazi okamzite



#==============================================================
# Delete the text part of the display
def ClearText(): 
  SendByte( 0, 0b00110000)  # function set (8 bit)
  SendByte( 0, 0b00110000)  # function set (basic instruction set)
  SendByte( 0, 0b00001100)  # displ.=ON , cursor=OFF , blink=OFF
  SendByte( 0, 0b00000001)  # clear

  # Erase the text memo
  txtmapa[0] = "                "
  txtmapa[1] = "                "
  txtmapa[2] = "                "
  txtmapa[3] = "                "



#==============================================================
# Delete the graphical text and the text part of the display.
# CAUTION: the display is set in the TEXT mode
def ClearDisplay(pattern=0):
  ClearGraphic(pattern)
  ClearText()



#==============================================================
# Set the display to the graphic mode
def InitGraphicMode():  
  SendByte(0, 0b00110010)  # function set (8 bit)
  SendByte(0, 0b00110110)  # function set (extend instruction set)
  SendByte(0, 0b00110110)  # function set (graphic ON)
  SendByte(0, 0b00000010)  # enable CGRAM po prenastaveni do BASIC instr.set



#==============================================================
# Set the display to text mode
def InitTextMode():  
  SendByte(0, 0b00110000)  # function set (8 bit)
  SendByte(0, 0b00110100)  # function set (extend instruction set)
  SendByte(0, 0b00110110)  # function set (graphic OFF)
  SendByte(0, 0b00000010)  # Enable CGRAM (after reset to BASIC instruction set)
  SendByte(0, 0b00110000)  # function set (basic instruction set)
  SendByte(0, 0b00001100)  # displ.=ON , cursor=OFF , blink=OFF
  SendByte(0, 0b10000000)  # Address Counter na left horni roh



#==============================================================
# Definition of a graphical shape of 4 icons with the size of 16x16 points
# Icon = Number Icons 0 to 3
# iconData = 16-byte double-byte value
def DefineIcon(icon, iconData):
  InitTextMode()
  SendByte(0, 64 + (icon * 16) )  # Setting the graphics address
  for dat in range(16):
    leftByte  = iconData[dat] / 256
    rightByte = iconData[dat] % 256
    Send2Bytes(1, leftByte, rightByte)



#==============================================================
# Blink cursor after the last character entered in text mode
# Is designed for Chinese characters, so a 16x16-dot large square
# (It's useless for European characters (8x16 points)
def BlinkCursor(state):
  InitTextMode()
  if(state == True):
    SendByte(0, 0b00001111)  # displ.=ON , cursor=ON , blink=ON
  else:
    SendByte(0, 0b00001100)  # displ.=ON , cursor=OFF , blink=OFF
  


#==============================================================
# Set the position to the appropriate column (0 to 7) and the row (0 to 3)
# For big characters and Icons (16x16 points)
def SetIconPos (column, row): 
  shift = column
  if (row == 1) : shift = column + 16
  if (row == 2) : shift = column + 8
  if (row == 3) : shift = column + 24

  SendByte( 0, 0b10000000 + shift)  # Address Counter to the desired position



#==============================================================
# Set the data pin for serial communication to "0" or "1"
def serd(bit):
  if (bit == 1):
     GPIO.output(sdata_pin, True)
  else:
     GPIO.output(sdata_pin, False)



#==============================================================
# A short one-clock pulse on serialized communications
def QuickPulse():
     GPIO.output(sclk_pin, True)
     time.sleep(0.0000001)
     GPIO.output(sclk_pin, False)
     time.sleep(0.0000001)
  


#==============================================================
# Subprogram for sending two bytes after serial communication without interrupting between individual bytes
def Send2Bytes(  rs,  byte1, byte2):

  serd(1)                # The beginning of the communication is done with the "synchro" sequence of 5 singles
  for i in range (5):
    QuickPulse()
  
  serd(0)                # Then the RW bit is sent (when set to "0")
  QuickPulse()
  serd(rs)               # Then the RS bit is sent (commands = "0"; data = "1")
  QuickPulse()
  serd(0)                # Followed by zero bit
  QuickPulse()
 
  for i in range(7,3,-1):     # And then top four bits from the first byte
    bit = (byte1 & (2**i)) >> i
    serd(bit)
    QuickPulse()

  serd(0)                     # The next is the 4x "0"
  for i in range (4):
    QuickPulse()

  for i in range(3,-1,-1):    # And then the remainder of the first byte (lower 4 bits)
    bit = (byte1 & (2**i)) >> i
    serd(bit)
    QuickPulse()

  serd(0)                      # Then the separation sequence is again 4x "0"
  for i in range (4):
    QuickPulse()

  # Byte types were sent immediately without "head" (without 5x "1" + RW bit + RS bit + "0")
  for i in range(7,3,-1):        # Even this kind of byte is divided into 2 parts (upper 4 bits)
    bit = (byte2 & (2**i)) >> i
    serd(bit)
    QuickPulse()

  serd(0)                        # Separation sequence 4x "0"
  for i in range (4):
    QuickPulse()

  for i in range(3,-1,-1):       # Bottom 4 bits
    bit = (byte2 & (2**i)) >> i
    serd(bit)
    QuickPulse()

  serd(0)                         # Last separating sequence 4x "0"
  for i in range (4):
    QuickPulse()



#==============================================================
# Send one byte after serial communication
def SendByte(  rs,  byte):

  serd(1)                # the beginning of the communication is done with the "synchro" sequence of 5 singles
  for i in range (5):
    QuickPulse()
  
  serd(0)                    # Then the RW bit is sent (when set to "0")        
  QuickPulse()                                                                                  
  serd(rs)                    # Then send the RS bit (commands = "0"; data = "1")            
  QuickPulse()                                                                                                                                           
  serd(0)                     # Followed by zero bit                                                        
  QuickPulse()
  
  for i in range(7,3,-1):     # And then up four bits of the sent byte
    bit = (byte & (2**i)) >> i
    serd(bit)
    QuickPulse()

  serd(0)                     # Then the separation sequence is sent 4x "0"
  for i in range (4):
    QuickPulse()

  for i in range(3,-1,-1):    # Followed by the rest of the data (the bottom 4 bits of the sent byte)
      
    bit = (byte & (2**i)) >> i
    serd(bit)
    QuickPulse()

  serd(0)                      # To restart the separation sequence 4x "0"
  for i in range (4):
    QuickPulse()



#==============================================================
# HW initial setting + reset the display
def init():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(sdata_pin, GPIO.OUT)    # (pin 26 = GPIO7)   = DATA
  GPIO.setup(sclk_pin, GPIO.OUT)     # (pin 24 = GPIO8)   = CLOCK
  GPIO.setup(reset_pin, GPIO.OUT)    # (pin 22 = GPIO25)  = RESET

  GPIO.output(sdata_pin, False)      # DATA do "0"
  GPIO.output(sclk_pin, False)       # CLOCK do "0"
  GPIO.output(reset_pin, False)      # RESET do "0"
  time.sleep(0.1)   
  GPIO.output(reset_pin, True)       # RESET do "1"


#==============================================================
if __name__ == '__main__':
  main()
