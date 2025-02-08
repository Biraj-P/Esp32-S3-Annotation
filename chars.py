"""
display_text_center.py

Displays a single text message in the center of the screen.
"""
import cst816
import time, utime
from machine import Pin, SPI
import gc9a01 as gc9a01
from fonts import vga2_16x32 as font  # Choose your font

def main():
    touch = cst816.CST816()
    
    if touch.who_am_i():
        print("CST816 detected.")
    else:
        print("CST816 not detected.")
    
    
    spi = SPI(2, baudrate=60000000, sck=Pin(10), mosi=Pin(11))
    tft = gc9a01.GC9A01(
        spi,
        dc=Pin(8, Pin.OUT),
        cs=Pin(9, Pin.OUT),
        reset=Pin(14, Pin.OUT),
        backlight=Pin(2, Pin.OUT),
        rotation=0)
    
    # Clear the screen and set background color
    tft.fill(gc9a01.BLACK)

    # Message to display
    message = "Hello, World!"

    # Calculate text position to center it
    text_width = len(message) * font.WIDTH
    x_pos = (tft.width - text_width) // 2
    y_pos = (tft.height - font.HEIGHT) // 2

    # Display the message
    tft.text(font, message, x_pos, y_pos, gc9a01.WHITE)

    # Keep the text on the screen
    while True:
        point = touch.get_point()
        gesture = touch.get_gesture()
        press = touch.get_touch()
        distance = touch.get_distance()
        print("Position: {0},{1} - Gesture: {2} - Pressed? {3} - Distance: {4},{5}".format(point.x_point, point.y_point, gesture, press, distance.x_dist, distance.y_dist))
        time.sleep(0.05)

main()
