# RPi-12864-LCD-ST7920-lib

An english translation and improvement from this czech code: http://www.astromik.org/raspi/42.htm

>Quick [Czech -> English] Google Translator link: https://translate.google.com/translate?hl=&sl=cs&tl=en&u=http%3A%2F%2Fwww.astromik.org%2Fraspi%2F42.htm

>(Wayback Machine: https://web.archive.org/web/20160323175419/http://www.astromik.org/raspi/42.htm)

![alt text](http://www.astromik.org/raspi/glcd12864-zw-a.jpg)
>(Image displayed on original website)


# HISTORY:

I searched a lot on the internet but I couldn't find a single library for my 128x64 LCD display (I was only finding OLED ones), until I found this czech site, with a working code for it. The problem is, that it was in czech.

So, I did my best to translate it and improve its performance and add a few functionalities.


# THE LIBRARY:

The library is working, most is in english, and almost everything you can understand.

The first part of the code, as the original code, is a demonstration of its working. Then are the functions you can use.

There is also a python3 version of the library that I ported, but as I tested in August of 2017, it was something like 25~30% slower than the python2 version. This surely doesn't apply anymore (2020+).


## New functions:

#### drawGenericLine

The original code only had drawHorizontal and vertical lines, so I added this, that draws from a coord to another.

#### drawCircle

Draws a circle!

#### drawRadiusLine

Draws a line like a clock hand, where you enter the initial coordinate, the angle in degrees and the radius (the size of the line)

#### printString3x5

The 12864 LCD have a built-in display text function, but the chars are big (16x8 pixels each char, max of 20x4 chars in screen).

The original version of this code had a smaller version of text (8x8 pixels each char), but for my purposes they were still big.

So I coded this function, which prints small chars, 3x5 pixels each.



# CREDITS:

Translation and improvements by Henrique Bruno Fantauzzi de Almeida (it's-a me!) - Federal University of Rio de Janeiro - Brazil

The credits for the original code goes to the author. Thanks, Milan Krúpa!


