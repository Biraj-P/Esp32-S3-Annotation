"""
fonts.py
========

.. figure:: /_static/fonts.png
  :align: center

  Pages through all characters of four fonts on the Display.
"""

import utime
from machine import Pin, SPI
import gc9a01
import tft_config

import vga1_8x8 as font1
import vga1_8x16 as font2
import vga1_bold_16x16 as font3
import vga1_bold_16x32 as font


def main():
    tft = tft_config.config(tft_config.TALL)

    tft.init()
    tft.fill(gc9a01.BLACK)
    utime.sleep(1)

    tft.fill(gc9a01.BLACK)
            

    tft.text(font, "hdghd", 100, 40, gc9a01.WHITE, gc9a01.BLACK)
    utime.sleep(3)

                


main()
