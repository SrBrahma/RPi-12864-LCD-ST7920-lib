
#!/usr/bin/python
# -*- encoding: utf-8 -*-

# ==============================================================
# Notes from translation
# ==============================================================
#
# English translation from this translation project:
# https://github.com/SrBrahma/RPi-12864-LCD-ST7920-lib
#
# Most of the translation is crappy. It is based on Google Translator.
# There is still missing some words that I can't find anywhere, maybe typos from author.
# 
# Czech words between "-- --" are words that I was unable to translate.
# There are few czech words followed by --[possible english translation]--
#
# Unknow terms:
#
# - mikrorow (microrow? but why that name)
# -
#
# ==============================================================
# Functions Index
# ==============================================================
#
# Note: the y position is inverted (like most (all?) displays), so the coordinate (0,0) is the top left.
#
# Init()
#   Basic GPIO port settings - just run it once at the beginning of the program
#
# InitTextMode()
#   Switches the display to text mode (display contents can not be displayed --?--)
#
# InitGraphicMode()
#   Switches display to graphic mode (display contents can not be displayed --?--)
#
# ClearText()
#   Deletes the content of the text part of the display (the graphics portion remains unchanged)
#
# ClearGraphic(pattern)
#   Fills the entire contents of the graphical part of the display by the byte.
#   (When 0x00 is deleted, 0xFF will fill it with white dots, other values will
#   fill the display with different vertical lines). The text part of the display remains unchanged.
#
# ClearDisplay()
#   Performs both previous deletions at the same time. After returning the display is switched to text mode.
#
# DefineIcon(iconId, iconData)
#   Defines one of four custom icons
#   iconId = icon identifier number 0 to 3
#   iconData = a variable that contains an array: 16x double-byte value
#
# PrintIcon(iconId, x, y)
#   The [x, y] coordinates print one of the four custom icons.
#   iconId = Icon identifier number 0 to 3
#   x = column 0 to 7
#   y = line 0 to 3
#
# ==== Graphic font 8x8 pixels
#   PrintCharGraphicMode(code, x, supers, inversion)
#     Displays one PrintCharGraphicMode with the ASCII code "code" at the "x" (0 to 15) coordinates,
#     posY (0 to 63) - the y position to
#     When "inverse" = True, a dark PrintCharGraphicMode appears on a light background.
#
#   PrintStringGraphicMode(text, x, supers, inversion)
#     Displays text (multiple characters) at "x" and "supers" (parameters same as "PrintCharGraphicMode ()").

# ==== Inside display font
#   PrintCharGreat(code, x, y) 	Displays one PrintCharGraphicMode in text mode at [x, y].
#     Code is in the range 1 to 127 (from 32 to 126 it is a classic ASCII)
#     X is from 0 to 15
#     Y is a line 0 to 3
#
#  PrintBigStringTextMode(string, x, y)
#     Use large characters to display text on the display. Parameters are the
#     same as for "big_set ()" and apply to the first PrintCharGraphicMode of the text.
#
# Plot(posX, posY, style)
#   At super pixels (0 to 127) and "posY" (0 to 63), it displays, deletes,
#   or inverts one point. If style = 0 , point deletion is performed, 
#   style = 1 is displayed, and style = 2 changes the point status on the display.
#
# MemPlot(posX, posY, style)
#   The same function as the previous " plot () ", just the points do not
#   appear directly on the display, but only in the temporary storage space.
#   This feature allows faster drawing. After use, however, it is necessary to transfer
#   the contents of that temporary memory to the display using the " MemDump () " function.
#
# MemDump()
#   Transfer the memory contents to the display after using the MemPlot() command.
#
# DrawHorizontalLine(posY, fromX, toX, style)
#   Drawing a simple horizontal line at a "supery" distance from the top edge with the
#   ability to define the beginning and end of the line (variables "from" to "to"). 
#   The "style" parameter is the same as the " plot () " function.
#
# DrawHorizontalLine(posY, fromX, toX, pattern)
#   Faster drawing of the horizontal line. In this case, the parameters "fromX" and "toX"
#   are in the range 0 to 7 (they are sixteen pixels on the display). Therefore,
#   the line can begin and end only at the coordinates on which the icons are printed.
#   The minimum length of such a line is 16 points. The "pattern" parameter specifies
#   the style of the line. Depending on the individual bits of that parameter, you can
#   set the line full, dashed, dotted, dashed ...
#
# DrawVerticalLine(posX, fromY, toY, pattern)
#   Vertical line at arbitrary coordinates.
#   posX = X line coordinates in the range 0 to 127
#   fromY, toY = y coordinates of the beginning and end of the line in the range 0 to 63
#   The "pattern" parameter is the same as in the previous case.
#
# LoadBMP12864(fileName)
#   Load a two-color image from the file into the display.
#   Beware of the correct file format!
#
# SendByte(rs, byte) 	Sends 1 byte to the display.
#   The data (1) or the command (0) register is selected using the "rs" parameter.
#
# Send2Bytes(rs, byte1, byte2)
#   It sends 2 bytes at a time.
#   The data (1) or the command (0) register is selected using the "rs" parameter.



# ==== NEW FUNCTIONS! ====
# They are not present on the original code. They aren't so complicated, but are handy.

# DrawGenericLine(fromX, fromY, toX, toY, style = 1)
#   Draws a line from and to the specified coordinates.
#   Based on this code: http://itsaboutcs.blogspot.com.br/2015/04/bresenhams-line-drawing-algorithm.html
#
# DrawCircle(circleCenterX, circleCenterY, radius, startDegree = 0, stopDegree = 360, stepDegree = 1, style = 1):
#   The arguments are self-explaining.
#   Increasing stepDegree increases the speed of drawing, but may result in missing pixels.
#
# DrawRadiusLine(fromX, fromY, degree, radius, style = 1):
#    Draws a line like a clock hand, where you enter the initial coordinate, the angle
#    in degrees and the radius (the size of the line)

# ==============================================================


# Last edit: 15.7.2013 (from the original czech code)

# Display 12864 ZW display (128x64 point) SERIAL:
# Display output (purpouse) -    connected to ...
# 1  (GND)                  - RasPi (GPIO GND   - pin 6)
# 2  (+ power supply)       - RasPi (GPIO +5V   - pin 1)
# 3  VO                     - 
# 4  (RS Data/Command)      - +5V (CHIP SELECT - In serial communication)
# 5  (R/W Read/Write)       - RasPi (Serial data) - GPIO7 (pin26) 
# 6  (E - Strobe)           - RasPi (serial CLOCK) - GPIO8 (pin24)
# 7  (Data bit0)            - 
# 8  (Data bit1)            - 
# 9  (Data bit2)            - 
# 10 (Data bit3)            - 
# 11 (Data bit4)            - 
# 12 (Data bit5)            - 
# 13 (Data bit6)            - 
# 14 (Data bit7)            - 
# 15 (PSB)                  - GND - Set serial communication
# 16 (NC)                   -
# 17 (Reset)                - RasPi - GPIO25(pin22)
# 18 (Vout)                 - 
# 19 (Podsvet - A)          - +5V (Or any LED brightness regulator - about 60mA)
# 20 (Podsvet - K)          - RasPi (GPIO GND - pin 6)

import os
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
cz2[367] = 135      # u With a ring
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
cz2[366] = 150      # U With a ring
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

cz2[176] = 176      # degree
cz2[177] = 177      # plus minus
cz2[171] = 171      # Double arrow on the left
cz2[166] = 166      # Interrupted vertically
cz2[223] = 223      # beta

# Assign GPIO pin
sData_Pin = 7       # (pin 26 = GPIO7)   = DATA    
sClk_Pin = 8        # (pin 24 = GPIO8)   = CLOCK  
reset_Pin = 25      # (pin 22 = GPIO25)  = RESET   

mapa={}             # Memory to store the current status of the displayed pixels on the display
txtmapa={}          # Memory to which the current text status on the display is saved
font2={}            # The memory in which the font is stored is retrieved from the external file
iconData={}         # The variable through which the graphical Icons will be defined


#==============================================================
# Main program
#==============================================================

def main():

    Init()              # Basic HW system setup - port directions on the expander and reset the display
    ClearDisplay(0)     # Complete deletion of the display
    nacist_font2("font2.txt")  # Retrieve an external font from the file



#==============================================================
#              Starts the default examples
#==============================================================


#- - - - - - - - - Writing text to the display - - - - - - - - - - - - - - - - - - - -  
    InitTextMode()     # Switch to text mode

    PrintBigStringTextMode("Viewing pointer",0,0)   # Display the text in the text mode at specified coordinates
    PrintBigStringTextMode("display",4,1)
    PrintBigStringTextMode("in text",3,2)
    PrintBigStringTextMode("mode",5,3)

    time.sleep(2)
    PrintBigStringTextMode("chr(1)...chr(32)", 0 , 1)
    charCode = 0
    for r in range(2, 4):
        for s in range (16):
            charCode = charCode + 1
            PrintCharGreat(charCode, s, r)   # PrintCharGraphicMode display in text mode according to its (ASCII) code
    time.sleep(3)
    
    PrintBigStringTextMode("chr(33)..chr(64)", 0, 1)
    for r in range(2, 4):
        for s in range (16):
            charCode = charCode + 1
            PrintCharGreat(charCode, s, r)
         

    time.sleep(3)
    ClearText()               # Delete the text part of the display
    time.sleep(1)

#- - - - - - - - - Icons - - - - - - - - - - - - - - - - - - - -  
    PrintBigStringTextMode("Own Icons", 0, 0)
 
 
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
    DefineIcon(0, iconData)

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
    DefineIcon(1, iconData)


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
    DefineIcon(2, iconData) 
    
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
    DefineIcon(3, iconData) 

    PrintIcon(1, 0, 1)    # Icon c.2 at the top of the second row from the top
    for icon in range (7):  # The rest of the row is filled with random icons  
        # When you print the icons for yourself, you do not have to set positions for each
        icon = random.randint(0, 3) * 2 # The last parameter is double the number of Icons
        Send2Bytes(1, 0,icon)    

    PrintIcon(2, 0, 2)    # Icon c.3 at the top of the third row from above
    for icon in range (7):  # The rest of the row is filled with random icons
        # When you print the icons for yourself, you do not have to set positions for each
        icon = random.randint(0, 3) * 2 # The last parameter is the double-pin number Icons
        Send2Bytes(1, 0, icon)    

    PrintIcon(3, 0, 3)    # Icon c.4 at the bottom of the bottom row
    for icon in range (7):  # The rest of the lines are filled with c.4
        # When you print the icons for yourself, you do not have to set positions for each
        Send2Bytes(1, 0, 6)    # (6 = icon c.4)    



    time.sleep(2)
    PrintBigStringTextMode("Change of definition", 0, 0)
    time.sleep(2)
    PrintBigStringTextMode(" Fourth Icons ", 0 , 0)
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
    DefineIcon(3, iconData) 
 
    time.sleep(3)
    ClearText()
    
#- - - - - - - - -Cinske charactery - - - - - - - - - - - - - - - -  
    PrintBigStringTextMode("   Like Icons   " , 0 , 0)
    PrintBigStringTextMode("  Are displayed  " , 0 , 1)
    PrintBigStringTextMode(" And Czech chars " , 0 , 2)
    time.sleep(3)
    ClearText()

    # Print CINSTINY --["nothing"?]-- with 16x16 point font (in text mode)
    # These are just randomly chosen charters (nothing to me --nerika--)
    # PrintCharGraphicMode is selected with the help of the last two functions "Send2Bytes()"
    # The first of these two numbers must be higher than 127

    SetIconPos(2, 0)                       # Setting the first PrintCharGraphicMode position [0,0] to [7,3]
    Send2Bytes(1, 200, 150)   
    Send2Bytes(1, 218, 10)
    Send2Bytes(1, 128, 1)
    Send2Bytes(1, 211, 200)

    SetIconPos(4, 2)                       # nastaveni pozice prvniho characteru [0,0] az [7,3]
    Send2Bytes(1, 240, 4)   
    Send2Bytes(1, 240, 33)
    Send2Bytes(1, 240, 222)

    # Vertical four-letter writing
    SetIconPos(0, 0)                       # PrintCharGraphicMode position setting
    Send2Bytes(1, 128, 18)   
    SetIconPos(0, 1)                       # PrintCharGraphicMode position setting 
    Send2Bytes(1, 154, 251)
    SetIconPos(0, 2)                       # PrintCharGraphicMode position setting 
    Send2Bytes(1, 197, 37)
    SetIconPos(0, 3)                       # PrintCharGraphicMode position setting 
    Send2Bytes(1, 141, 90)


    time.sleep(3)
    ClearText()


#- - - - - - - - -  Text in the graphics mode - - - - - - - - - - - - - - - - - - -  
# Print 8x8 dot font (in graphic mode)

    InitGraphicMode()
    PrintStringGraphicMode("The display is y", 0,  0, False)  # Normal graphic on the top row
    PrintStringGraphicMode("operate",          3, 15, False)        
    PrintStringGraphicMode("also in graphics", 1, 30, False) 
    PrintStringGraphicMode("mode",             5, 45, False)  

    time.sleep(2)
    PrintStringGraphicMode("graphics", 5, 30, True)  # Inversely rewritten text  

    time.sleep(3)
    ClearGraphic()    # Delete the graphical parts of the display


    # In the same mode, y print individual characters according to their code
    for code in range(32, 128):
        column = (code - 32) % 16
        row = int((code - 32)/16) * 11      # The spacing between the lines is 11 points
        if (row / 22.0 == int(row / 22)):  # Every other row is inverse
            invert = True
        else:
            invert = False
            
        PrintCharGraphicMode(code, column, row, invert) # PrintCharGraphicMode subroutine in graphics mode

    time.sleep(2)
    ClearGraphic()

    for code in range(128, 256):
        column = (code - 128) % 16
        row = int((code - 128) / 16) * 8 
        PrintCharGraphicMode(code, column, row, False)

    time.sleep(2)
    ClearGraphic()


#- - - - - - - Point printing and car - - - - - - - - - - - - - - - - - -  

    PrintStringGraphicMode("In this mode",         0,  2,False)  # Normal writing 2 pixels from the top edge
    PrintStringGraphicMode("Is y to draw",         0, 11,False)        
    PrintStringGraphicMode("Points and line",      0, 20, False) 

    # Oramovani --[Window?]-- display with full car
    DrawHorizontalLine (  0, 0, 127, 1)          # Horizontal line at any position
    DrawHorizontalLine2( 63, 0,   7, 0b11111111) # Speed mountains. Line in a 16-column raster with mask setting
    DrawVerticalLine (  0, 0,  63, 0b11111111) # Vertical line in any position with mask setting
    DrawVerticalLine (127, 0,  63, 0b11111111)

    # Internal small rectangle with a carcass
    DrawHorizontalLine2(31, 1,  6, 0b11001100)
    DrawHorizontalLine2(56, 1,  6, 0b11001100)
    DrawVerticalLine ( 16, 31, 56, 0b11001100)
    DrawVerticalLine (111, 31, 56, 0b11001100)


    # Randomly popping a point into a small rectangle in inverse mode
    for i in range(2000):
        x= int(random.randint(17, 110))
        y= int(random.randint(32, 55))
        Plot(x, y, 2)   # Print an inverse point at the coordinates [x, y]


#- - - - - - - - - - - - Different styles of --horizontalnich-- cars - - - - - - - - - - - - - - - - -  
    ClearGraphic()

    DrawHorizontalLine2( 0, 2, 5, 0b11111111) # Speed mountains. Line in a 16-column raster with mask setting
    DrawHorizontalLine2(10, 3, 4, 0b11001100) # Speed mountains. Line in a 16-column raster with mask setting
    DrawHorizontalLine2(20, 2, 5, 0b11110000) # Speed mountains. Line in a 16-column raster with mask setting
    DrawHorizontalLine2(30, 1, 6, 0b10101010) # Speed mountains. Line in a 16-column raster with mask setting
    DrawHorizontalLine2(40, 0, 7, 0b11110101) # Speed mountains. Line in a 16-column raster with mask setting
    DrawHorizontalLine2(50, 1, 6, 0b01110101) # Speed mountains. Line in a 16-column raster with mask setting

    time.sleep(3)

    ClearGraphic(0xff)    # To fill the screen with white ink

#- - - - - - - - - - drawing - - - - - - - - - - - - - - - - - - - -  
    # Draw a double circle using the first print point on the display (slowly)
    for circle in range(0, 6283, 4):
        x = int(((math.sin(circle / 1000.0) * 30.0)) + 32)
        y = int(((math.cos(circle / 1000.0) * 30.0)) + 32)
        Plot(x, y, 0)
        x = int(((math.sin(circle / 1000.0) * 20.0)) + 32)
        y = int(((math.cos(circle / 1000.0) * 20.0)) + 32)
        Plot(x, y, 0)

    # Draw five of the circles using the memo
    # And then swipe the memory to the display (fast)
    for circle in range(0, 6283, 4):
        x = int(((math.sin(circle / 1000.0) * 30.0)) + 96)
        y = int(((math.cos(circle / 1000.0) * 30.0)) + 32)
        MemPlot(x, y, 0)
        x = int(((math.sin(circle / 1000.0) * 25.0)) + 96)
        y = int(((math.cos(circle / 1000.0) * 25.0)) + 32)
        MemPlot(x, y, 0)
        x = int(((math.sin(circle / 1000.0) * 20.0)) + 96)
        y = int(((math.cos(circle / 1000.0) * 20.0)) + 32)
        MemPlot(x, y, 0)
        x = int(((math.sin(circle / 1000.0) * 15.0)) + 96)
        y = int(((math.cos(circle / 1000.0) * 15.0)) + 32)
        MemPlot(x, y, 0)
        x = int(((math.sin(circle / 1000.0) * 10.0)) + 96)
        y = int(((math.cos(circle / 1000.0) * 10.0)) + 32)
        MemPlot(x, y, 0)

    MemDump()    # Spraying data from memory to display



    time.sleep(2)
    ClearGraphic()

#- - - - - - - - - - Overwrite text and graphic mode - - - - - - - - - -  

    PrintStringGraphicMode("     Graphic    ",  0,  0, False)
    PrintStringGraphicMode("  And text mode ", 0, 10, False) 
    PrintStringGraphicMode("    Y is used   ",     0, 20, False) 
    PrintStringGraphicMode("  In particular ", 0, 30, False) 

    time.sleep(2)
    ClearGraphic()
 
    InitTextMode()      # Switch the display to text mode
    PrintBigStringTextMode("Big writing", 2, 0)
    PrintBigStringTextMode("  In text  ", 3, 1)
    PrintBigStringTextMode("    mode   ", 5, 2)
    PrintIcon(1, 0, 2)
    PrintIcon(1, 7, 2)  


    time.sleep(2)

    InitGraphicMode()  # Switch display to graphic mode
    DrawHorizontalLine2(53, 0, 7, 0b10011001) 
    PrintStringGraphicMode("Graphic row", 1, 56, False)   


    
    # When combining text and graphic mode, the common area on the XOR displays
    # Example: 4 points thick sikma line over the entire screen

    for x in range(128):
        Plot(x ,x/2     , 1)
        Plot(x,(x/2) + 1, 1)
        Plot(x,(x/2) + 2, 1)
        Plot(x,(x/2) + 3, 1)

    time.sleep(2)
    PrintStringGraphicMode("Delete graphics", 0, 56, True)   

    time.sleep(2)
    ClearGraphic()   # The graphic is deleted separately, so the original text remains

    PrintStringGraphicMode("The text remains", 0, 56, True)   
    time.sleep(2)
    PrintStringGraphicMode("Make a line ", 0, 56, True)   

    for x in range(128):
        Plot(127-x ,x/2     , 1)
        Plot(127-x,(x/2) + 1, 1)
        Plot(127-x,(x/2) + 2, 1)
        Plot(127-x,(x/2) + 3, 1)

    time.sleep(2)
    PrintStringGraphicMode(" Delete text ", 0, 56, True)   
    time.sleep(1)

    ClearText()                # The display will be deleted separately
    InitGraphicMode()
    MemDump()                # graphic se ale v tom pripade musi obnovit z pameti
    
    time.sleep(1)
    PrintStringGraphicMode("Graphic remains", 0, 56, True)   
    time.sleep(2)
    ClearGraphic()

#- - - - - - - - - nahrani obrazku - - - - - - - - - - - - - - - - - -  

    PrintStringGraphicMode("   display    " ,0,  0,False)  # 
    PrintStringGraphicMode("     file     " ,0, 10,False)  # 
    PrintStringGraphicMode(" with a image " ,0, 20,False)  # 
    time.sleep(2)
    LoadBMP12864("./pokladnik.bmp")  # Upload bitmaps of 128x64 pixels on the display 

    time.sleep(4)

    # Fill the display with vertical lines (pattern = 0b10101010)
    ClearDisplay(0b10101010) # The ClearDisplay () function remains in the text mode
    InitGraphicMode()       # So you have to switch it to the graphical mode before the next graphic function

    PrintStringGraphicMode("END OF EXAXMPLES :)" , 2 , 25 , True)   
 
    exit(0)




#==============================================================
#               All subroutines are:
#==============================================================



#==============================================================
# One of the 4 defined 16 x 16 pixel icons at position [x, y]
# X is in the range 0 to 7 (translated to 0, 16, 32, 48, 64, 80, 96, 112)
# Y ranges from 0 to 3 (translated to 0, 16, 32, 48)
def PrintIcon(iconId, x, y):
    shift = x
    if (y == 1): shift = shift + 16
    if (y == 2): shift = shift + 8
    if (y == 3): shift = shift + 24
    SendByte(0, 0b10000000 + shift)  # Address Counter to the required position
    Send2Bytes(1, 0, iconId * 2)







#==============================================================
# Draw a horizontal line point by point
def DrawHorizontalLine(posY, fromX = 0, toX=127, style = 1):  
    for posX in range(fromX, toX + 1):
        Plot(posX, posY, style)


#==============================================================
# Draw horizontal line from the edge to the edge after the bytes
def DrawHorizontalLine2(posY = 0, fromByte = 0, toByte = 5, pattern = 0b11111111):  
    shift = fromByte
    if (posY >= 32):
        posY = posY - 32
        shift = shift + 8     

    Send2Bytes( 0, 0b10000000 + posY, 0b10000000 + shift )     
    for r in range(toByte - fromByte + 1):
        Send2Bytes(1, pattern, pattern)     
        mapa[shift + r, posY, 0] = pattern 
        mapa[shift + r, posY, 1] = pattern 
    
    
#==============================================================
# Draw a vertical line using bit masks
def DrawVerticalLine(posX, fromY = 0, toY = 63, pattern = 255):  
    poz_pat = 0                              # The bit position in the pattern
    for posY in range(fromY , toY + 1):
        maska = (0b10000000 >> (poz_pat % 8))  # According to the given pattern, selects individual bits
        bitpat = pattern & maska
        if (bitpat == 0):                      # Which will either be displayed or deleted on the display
            style = 0
        else:
            style = 1

        Plot(posX, posY, style)
        poz_pat = poz_pat + 1


#==============================================================
# Displaying one PrintCharGraphicMode from the 8x8 point font
# bytePosX = x PrintCharGraphicMode position (0 to 15, translated to multiples of 8 up to 128), posY = 0 to 63
def PrintCharGraphicMode(ascii8bitCode, bytePosX, posY , invert = False):  

    # Control of lightning parameters and their possible override at the limit
    if (ascii8bitCode    <  32): ascii8bitCode = 32
    if (ascii8bitCode    > 255): ascii8bitCode = 255
    if (bytePosX   <   0): bytePosX = 0  
    if (bytePosX   >  15): bytePosX = 15  
    if (posY >  63): posY = 63
    if (posY <   0): posY = 0

    ascii8bitCode = ascii8bitCode - 32     # In the font file, the space with the 32 code is defined as the first PrintCharGraphicMode
    posX = bytePosX * 8

    # The font of the PrintCharGraphicMode from the font will be gradually transferred to the byte byte display in 8 steps (top down)
    for adr_font in range(ascii8bitCode * 8, (ascii8bitCode * 8) + 8):

        # Calculate the horizontal and vertical addresses in the display memory
        horiz = int(posX / 16)  
        dis_adr_y = posY
        if (dis_adr_y >= 32):
            dis_adr_y = dis_adr_y - 32
            horiz = horiz + 8
    
        minibit = posX % 16     # The position of the bit to work with, in the double-bin
     
        Send2Bytes(0, 0b10000000 + dis_adr_y, 0b10000000 + horiz)  # Setting the graphics address
    
        orignal_leva  = mapa[horiz,dis_adr_y, 0]  # To find out the current status of the two-byte on the display
        orignal_prava = mapa[horiz,dis_adr_y, 1]

        if(minibit < 8):         # When the minibit is <8, change only the left byte from the double byte
            if (invert == False):  # Normal text (write everything that is below the text)
                leftByte = font2[adr_font]
            if (invert == True):   # Inverse text (write everything that is below the text)
                leftByte = ~font2[adr_font]
                
            rightByte = orignal_prava   # right byte z dvojbyteu bude beze zmeny
    
        else:  # When the minibit >= 8, change only the right byte from the double-bin
            if (invert == False):  # Normal text (write everything that is below the text)
                rightByte = font2[adr_font]
            if (invert == True):   # Inverse text (write everything that is below the text)
                rightByte = ~font2[adr_font]

            leftByte = orignal_leva     # The left byte of the two-bit will be unchanged
    
        Send2Bytes(1, leftByte, rightByte)       # Prepress the two bytes to enter the address in the display
        mapa[horiz, dis_adr_y, 0] = leftByte        # The same value remembers the variable map []
        mapa[horiz, dis_adr_y, 1] = rightByte

        posY = posY + 1   # Change the current micro-bars by one



#==============================================================
# Displaying several characters behind the 8x8 font
# bytePosX = the position of the first PrintCharGraphicMode in the text is in column 0 to 15; posY = 0 to 63 (upper margin of the PrintCharGraphicMode)
def PrintStringGraphicMode(string, bytePosX, posY, invert = False):  

    if (isinstance(string, unicode) == False):   # If the string is not in unicode, then transfer it
        string = unicode(string, "utf-8")          # Convert string from UTF-8 to unicode

    # All the string scroll PrintCharGraphicMode after PrintCharGraphicMode and print
    for zn in range (len(string)):
        if (bytePosX < 16): # Screen overlay
            if (ord(string[zn:zn + 1]) > 127):   # As for the ASCII PrintCharGraphicMode, proceed as described in the table above
                try:                    # If there is no special code defined in the table, ...
                    PrintCharGraphicMode(cz2[ord(string[zn:zn + 1])], bytePosX, posY, invert)
                except:                 # ... the program will terminate the error of the non-existent index of the variable cz2 [].
                    PrintCharGraphicMode(164, bytePosX, posY, invert)  # In this case, replace the undefined PrintCharGraphicMode PrintCharGraphicMode "wheel with teckama"
            else:
                PrintCharGraphicMode(ord(string[zn:zn + 1]), bytePosX, posY, invert) # ASCII charactery tisknout normalne
            bytePosX = bytePosX + 1





#==============================================================
# Load 8x8 point font from file to list "font2 []"
def nacist_font2(fileName):

    fullPathFileName = os.path.join(os.path.dirname(os.path.realpath('__file__')), fileName)
    print (fullPathFileName)
    fontfile = open(fullPathFileName, "r")
    adresafontu = 0
    for row in fontfile:
        rozlozeno = row.split(",")                          # Saturation of individual bytes from one line ...
        for byte in range(8):                               # 8 byte on one row in a file
            font2[adresafontu] = int(rozlozeno[byte][-4:], 0) # ... and save everyone on the list
            adresafontu = adresafontu + 1
    fontfile.close()
    


#==============================================================
# Subroutine for string display obrim font (8x16 point)
# Font definition is a part of the ROM in the display - therefore not Czech characters
# bytePosX = Initial column where the string will begin to print [0 to 16]
# Row is in the range [0 to 3]
def PrintBigStringTextMode(string, column, row): 

    if (len(string) + column > 16):    # If the line is longer than 16 characters,
        string = string[0:16 - column]  # ... so the end is cut off
 
    SetTextCursorPos(column, row)     # The start position of the text is sent to the display
    for PrintCharGraphicMode in range(len(string)):
        SendByte(1, ord(string[PrintCharGraphicMode:PrintCharGraphicMode+1]))  # Characters from the text are gradually streaked into the display
        pomtext = txtmapa[row][:column + PrintCharGraphicMode] + string[PrintCharGraphicMode:PrintCharGraphicMode + 1] + txtmapa[row][column+PrintCharGraphicMode+1:]
        txtmapa[row] = pomtext            # Memory for text mode



#==============================================================
# Single PrintCharGraphicMode display in text mode
def PrintCharGreat(code, bytePosX, row): 
    SetTextCursorPos(bytePosX, row)  # The start position of the text is sent to the display
    SendByte(1, code)                # The PrintCharGraphicMode code is sent to the display
    pomtext = txtmapa[row][:bytePosX] + chr(code) + txtmapa[row][bytePosX + 1:]
    txtmapa[row] = pomtext           # Memory for text mode



#==============================================================
# Print position setting for text mode (for characters 8x16 point)
# Column (0 to 15) and line (0 to 3)
def SetTextCursorPos(column , row):  
    shift = column
    if (row == 1): shift = column + 32
    if (row == 2): shift = column + 16
    if (row == 3): shift = column + 48

    SendByte( 0, 0b10000000 + int(shift / 2))  # Address Counter na pozadovanou pozici

    # In the case of --lichen-- columns, the PrintCharGraphicMode must be filled in with the PrintCharGraphicMode on the display before the new printout
    if (column / 2.0 != column / 2):
        orignal_predcharacter = txtmapa[row][column - 1:column] # "Predcharacter" is determined from the auxiliary text memory
        SendByte(1, ord(orignal_predcharacter)) 

#==============================================================
# New function.
# Draws a line from and to the specified coordinates.
# Based on this code: http://itsaboutcs.blogspot.com.br/2015/04/bresenhams-line-drawing-algorithm.html
def DrawGenericLine(fromX, fromY, toX, toY, style = 1):
    # Bresenham Line Drawing Algorithm For All Kind Of Slopes Of Line
    dx = abs(fromX - toX)
    dy = abs(toY - fromY)
    if (float(dx) == 0): slope = 10
    else: slope = dy/float(dx)
    
    x, y = fromX, fromY   

    Plot(x, y, style)
    
    # checking the slope if slope > 1 
    # then interchange the role of x and y
    if slope > 1:
        inverted = True
        dx, dy = dy, dx
        x, y = y, x
        toX, toY = toY, toX
    else: inverted = False
    # initialization of the inital decision parameter
    p = 2 * dy - dx
    
    for k in range(2, dx):
        if p > 0:
            y = y + 1 if y < toY else y - 1
            p = p + 2*(dy - dx)
        else:
            p = p + 2*dy
 
        x = x + 1 if x < toX else x - 1
        if inverted:
            Plot(y, x, style)
            
        else:
            Plot(x, y, style)
            
#==============================================================
# New function.
# Draws a rectangle. If fill, all the internal part will be painted.
def DrawRectangle(fromX, fromY, toX, toY, fill = 0, style = 1):
    if (fromX > toX):
        fromX, toX = toX, fromX
    if (fromY > toY):
        fromY, toY = toY, fromY
    
    for xPos in range (fromX, toX + 1):
        Plot(xPos, fromY, style)
        Plot(xPos, toY, style)
        
    for yPos in range (fromY + 1, toY):
        Plot(fromX, yPos, style)
        Plot(toX, yPos, style)
        
    if fill:
        for yPos in range (fromY + 1, toY):
            for xPos in range (fromX + 1, toX):
                Plot(xPos, yPos, style)
        
    
#==============================================================
# New function.
# The arguments are self-explaining.
# Increasing stepDegree increases the speed of drawing, but may result in missing pixels.
def DrawCircle(circleCenterX, circleCenterY, radius, startDegree = 0, stopDegree = 360, stepDegree = 1, style = 1):
    for degree in range (startDegree, stopDegree + 1, stepDegree)
        posX = int(round(math.cos(math.radians(degree)) * radius + circleCenterX))
        posY = int(round(math.sin(math.radians(degree)) * (- radius) + circleCenterY))
        Plot (posX, posY, style)
        
#==============================================================
# New function.
# Draws a line like a clock hand, where you enter the initial coordinate, the angle
# in degrees and the radius (the size of the line)
def DrawRadiusLine(fromX, fromY, degree, radius, style = 1):
        targetX = int(round(math.cos(math.radians(degree)) * radius + fromX))
        targetY = int(round(math.sin(math.radians(degree)) * (- radius) + fromY))
        graphicLCD.DrawGenericLine(fromX, fromY, targetX, targetY, style)

#==============================================================
# Uploading a two-color BMP image of a 128x64 point to a variable map []
# CAUTION: Without any test for a correct BMP file format!
def LoadBMP12864(imageRelativePath):
    fileBMP = open(imageRelativePath, "rb")  # Load an image into a data variable []
    data = fileBMP.read()  
    fileBMP.close()                          # File closure

    # The detailed BMP master file specification is here:
    # http://www.root.cz/clanky/graficky-format-bmp-pouzivany-a-pritom-neoblibeny
    # The start of the image data determines 4 bytes in a file in positions 10 to 13 (ten) from the beginning of the file
    zacatekdat = ord(data[10]) + (ord(data[11]) * 256) + (ord(data[12]) * 65536) + (ord(data[13]) * 16777216)
    byte = zacatekdat

    for mikrorow in range (63, -1, -1):  # Read data variables [] byte after byte and store in memory (map [])
        posY = mikrorow
        if (mikrorow > 31):
            posY = posY - 32
            shift = 8
        else:
            shift = 0
        Send2Bytes(0, 0b10000000 + posY, 0b10000000 + shift)  # Setting the graphics address
        for column in range (8):
            leftByte = (ord(data[byte]))
            rightByte = (ord(data[byte+1]))
            Send2Bytes(1, leftByte, rightByte)     # 
            mapa[column + shift , posY,0] = leftByte
            mapa[column+shift , posY,1] = rightByte

            byte = byte + 2          # Passes to another double-out of graphical data


#==============================================================
# 1-point display / deletion / inversion at posX coordinates (0 to 127) and posY (0 to 63)
def Plot(posX, posY, style = 1):

    # Checking for the correct range of coordinates and optionally adjusting them to the extreme values
    if (posX > 127): posX = 127
    if (posX < 0  ): posX = 0
    if (posY > 63 ): posY = 63
    if (posY < 0  ): posY = 0

    horiz = int (posX / 16)
    if (posY >= 32):
        posY = posY - 32
        horiz = horiz + 8

    minibit = posX % 16
 
    Send2Bytes (0, 0b10000000 + posY, 0b10000000 + horiz)  # Setting the graphics address

    orignal_leva  = mapa[horiz, posY, 0]
    orignal_prava = mapa[horiz, posY, 1]

    if (minibit < 8):
        if (style == 1):  # Draw a point
            leftByte = (0b10000000 >> minibit) | orignal_leva
        elif (style == 0):  # Delete point
            leftByte = ~(0b10000000 >> minibit) & orignal_leva
        else:  # Delete point
            leftByte = (0b10000000 >> minibit) ^ orignal_leva

        rightByte = orignal_prava
        
    else:
        if (style == 1):  # Draw a point
            rightByte = (0b10000000 >> (minibit-8)) | orignal_prava
        elif (style == 0):  # Delete point
            rightByte = ~(0b10000000 >> (minibit-8)) & orignal_prava
        else:  # Delete point
            rightByte = (0b10000000 >> (minibit-8)) ^ orignal_prava

        leftByte = orignal_leva

    Send2Bytes( 1, leftByte, rightByte)
    mapa[horiz, posY, 0] = leftByte
    mapa[horiz, posY, 1] = rightByte



#==============================================================
# 1-pixel [display/deletion/inversion] at posX coordinates (0 to 127) and posY (0 to 63)
def MemPlot(posX, posY, style = 1):
    horiz = int(posX / 16)
    
    if (posY >= 32):
        posY = posY - 32
        horiz = horiz + 8

    minibit = posX & 15
 
    orignal_leva  = mapa[horiz, posY, 0]
    orignal_prava = mapa[horiz, posY, 1]

    if (minibit < 8):
        if (style == 1):  # Draw a point
            leftByte = (0b10000000 >> minibit) | orignal_leva
        elif (style == 0):  # Delete point
            leftByte = ~(0b10000000 >> minibit) & orignal_leva
        elif (style == 2):  # Invert point
            leftByte = (0b10000000 >> minibit) ^ orignal_leva

        rightByte = orignal_prava
        
    else:
        if (style == 1):  # Draw a point
            rightByte = (0b10000000 >> (minibit-8)) | orignal_prava
        elif (style == 0):  # Delete point
            rightByte = ~(0b10000000 >> (minibit-8)) & orignal_prava
        elif (style == 2):  # Invert point
            rightByte = (0b10000000 >> (minibit-8)) ^ orignal_prava

        leftByte = orignal_leva

    changedMemPlot = mapa[horiz, posY, 0] = leftByte
    changedMemPlot = mapa[horiz, posY, 1] = rightByte


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
# Delete graphical display time
def ClearGraphic(pattern = 0): 
    InitGraphicMode()
    SendByte(0, 0b00110110)  # function set (extend instruction set)
    SendByte(0, 0b00110100)  # function set (graphic OFF) - aby nebylo videt postupne mazani displeje
    SendByte(0, 0b00001000)  # displ.=OFF , cursor=OFF , blink=OFF
    
    for vertical in range(32):  
        Send2Bytes(0, 0b10000000 + vertical, 0b10000000 )  # Setting the address on the display at the beginning of the micro-bar
        for horizontal in range (16):
            Send2Bytes(1, pattern, pattern)     # Double-bits fill the entire display with the same code   
 
            # And this code still writes to individual positions in the cache
            mapa[horizontal, vertical, 0] = pattern    
            mapa[horizontal, vertical, 1] = pattern
            
    SendByte( 0, 0b00110110)  # function set (graphic ON) - smazany displej se zobrazi okamzite



#==============================================================
# Delete the text part of the display
def ClearText(): 
    SendByte(0, 0b00110000)  # function set (8 bit)
    SendByte(0, 0b00110000)  # function set (basic instruction set)
    SendByte(0, 0b00001100)  # displ.=ON , cursor=OFF , blink=OFF
    SendByte(0, 0b00000001)  # clear

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
    SendByte(0, 0b00000010)  # nable CGRAM after being reset to BASIC instruction set



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
def DefineIcon(iconId, iconData):
    InitTextMode()
    SendByte(0, 64 + (iconId * 16) )  # Setting the graphics address
    for dat in range(16):
        leftByte  = iconData[dat] / 256
        rightByte = iconData[dat] % 256
        Send2Bytes(1, leftByte, rightByte)



#==============================================================
# Blink cursor after the last PrintCharGraphicMode entered in text mode
# Is designed for Chinese characters, so a 16x16-dot large square
# (It's useless for European characters (8x16 points))
def BlinkLastChineseChar(state):
    InitTextMode()
    if (state == True):
        SendByte(0, 0b00001111)  # displ.=ON , cursor=ON , blink=ON
    else:
        SendByte(0, 0b00001100)  # displ.=ON , cursor=OFF , blink=OFF



#==============================================================
# Set the position to the appropriate column (0 to 7) and the row (0 to 3)
# For big characters and Icons (16x16 points)
def SetIconPos(column, row): 

    shift = column
    if (row == 1): shift = column + 16
    if (row == 2): shift = column + 8
    if (row == 3): shift = column + 24

    SendByte(0, 0b10000000 + shift)  # Address Counter to the desired position



#==============================================================
# Set the data pin for serial communication to "0" or "1"
def setDataPin(bit):

    if (bit):
        GPIO.output(sData_Pin, True)
    else:
        GPIO.output(sData_Pin, False)



#==============================================================
# A short one-clock pulse on serialized communications
# I was able to run changing the time.sleep() values, but rarely I was getting some
# artifacts on display, so I decided to leave them there.
# Before Strobe4 and 5, this library was using a "for x in range (4): Strobe()"
# It was called so many times that it was taking a considerably amount of time
# Now the code runs a little faster.
def Strobe():
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)

def Strobe4():
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
  
def Strobe5():
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, True)
    time.sleep(0.0000001)
    GPIO.output(sClk_Pin, False)
    time.sleep(0.0000001)
  
#==============================================================
# Subprogram for sending two bytes after serial communication without interrupting between individual bytes
def Send2Bytes(rs, byte1, byte2):
        
    setDataPin(1)                # The beginning of the communication is done with the "synchro" sequence of 5 singles
    Strobe5()
    
    setDataPin(0)                # Then the RW bit is sent (when set to "0")
    Strobe()
    setDataPin(rs)               # Then the RS bit is sent (commands = "0"; data = "1")
    Strobe()
    setDataPin(0)                # Followed by zero bit
    Strobe()
 
    for i in range(7, 3, -1):         # And then top four bits from the first byte
        setDataPin(byte1 & (1 << i))    # The original code used "bit = (byte1 & (2**i)) >> i"
        Strobe()                        # I removed the "bit" var (putted the expression directly at the function)
                                                                        # And changed the expression. Well, thess improvements made code runs faster.

    setDataPin(0)                     # The next is the 4x "0"
    Strobe4()

    for i in range(3, -1, -1):    # And then the remainder of the first byte (lower 4 bits)
        setDataPin(byte1 & (1 << i))
        Strobe()

    setDataPin(0)                      # Then the separation sequence is again 4x "0"
    Strobe4()

    # Byte types were sent immediately without "head" (without 5x "1" + RW bit + RS bit + "0")
    for i in range(7, 3, -1):        # Even this kind of byte is divided into 2 parts (upper 4 bits)
        setDataPin(byte1 & (1 << i))
        Strobe()

    setDataPin(0)                        # Separation sequence 4x "0"
    Strobe4()

    for i in range(3, -1, -1):       # Bottom 4 bits
        setDataPin(byte2 & (1 << i))
        Strobe()

    setDataPin(0)                        # Last separating sequence 4x "0"
    Strobe4()



#==============================================================
# Send one byte after serial communication
def SendByte(rs,  byte):

    setDataPin(1)                # the beginning of the communication is done with the "synchro" sequence of 5 singles
    Strobe5()
    
    setDataPin(0)                    # Then the RW bit is sent (when set to "0")        
    Strobe()                                                                                  
    setDataPin(rs)                    # Then send the RS bit (commands = "0"; data = "1")            
    Strobe()                                                                                                                                           
    setDataPin(0)                     # Followed by zero bit                                                        
    Strobe()
    
    for i in range(7, 3, -1):     # And then up four bits of the sent byte
        setDataPin(byte1 & (1 << i))
        Strobe()

    setDataPin(0)                     # Then the separation sequence is sent 4x "0"
    Strobe4()

    for i in range(3, -1, -1):    # Followed by the rest of the data (the bottom 4 bits of the sent byte)
        setDataPin(byte1 & (1 << i))
        Strobe()

    setDataPin(0)                      # To restart the separation sequence 4x "0"
    Strobe4()



#==============================================================
# HW initial setting + reset the display
def Init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sData_Pin, GPIO.OUT)    # (pin 26 = GPIO7)   = DATA
    GPIO.setup(sClk_Pin, GPIO.OUT)     # (pin 24 = GPIO8)   = CLOCK
    GPIO.setup(reset_Pin, GPIO.OUT)    # (pin 22 = GPIO25)  = RESET

    GPIO.output(sData_Pin, False)      # DATA to "0"
    GPIO.output(sClk_Pin, False)       # CLOCK to "0"
    GPIO.output(reset_Pin, False)      # RESET to "0"
    time.sleep(0.1)   
    GPIO.output(reset_Pin, True)       # RESET to "1"


#==============================================================
if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
