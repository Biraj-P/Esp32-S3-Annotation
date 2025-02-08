import time, utime, qmi8658a
import cst816
from machine import Pin, SPI
import gc9a01 as gc9a01
import vga2_16x32 as font

qmi8658 = qmi8658a.QMI8658()

# Getting user data from the text file
def read_user_data():
    try:
        with open("user_data.txt", "r") as file:
            data = file.readlines()

        # Parse the data
        user_data = {}
        for line in data:
            key, value = line.strip().split(": ")
            user_data[key] = value

        return user_data

    except FileNotFoundError:
        print("User data file not found. Please collect the data first.")
        return None

# Read user data from the file
user_data = read_user_data()

if user_data:
    Name = user_data['Name']
    log_file_path = f"{Name}_ActivityLogging.csv"
else:
    print("Unable to read user data.")

header = "timestamp,duration,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,activity\n"


def initialize_log_file():
    try:
        with open(log_file_path, 'r') as log_file:
            pass  # File exists, do nothing
    except OSError:
        # File does not exist, create it and write the header
        with open(log_file_path, 'w') as log_file:
            log_file.write(header)


initialize_log_file()

# Initialize touch sensor
touch = cst816.CST816()
if touch.who_am_i():
    print("CST816 detected.")
else:
    print("CST816 not detected.")

# Initialize display
spi = SPI(2, baudrate=60000000, sck=Pin(10), mosi=Pin(11))
tft = gc9a01.GC9A01(
    spi,
    dc=Pin(8, Pin.OUT),
    cs=Pin(9, Pin.OUT),
    reset=Pin(14, Pin.OUT),
    backlight=Pin(2, Pin.OUT),
    rotation=0)

tft.fill(gc9a01.BLACK)

message_Ano = "Annotating"
message_noAno = "Not Annotating"

# For text to be shown in device
text_width1 = len(message_Ano) * font.WIDTH
x_pos1 = (tft.width - text_width1) // 2
y_pos1 = (tft.height - font.HEIGHT) // 2

text_width2 = len(message_noAno) * font.WIDTH
x_pos2 = (tft.width - text_width2) // 2
y_pos2 = (tft.height - font.HEIGHT) // 2

log_file = open(log_file_path, 'a')


while True:
    touch_gesture = touch.get_gesture()
    timestamp = time.ticks_ms()
    acc_xyz = qmi8658.Read_acclXYZ()
    gyro_xyz = qmi8658.Read_gyroXYZ()
    
    activity = "None"
    elapsed_sec = 0
    if touch_gesture in (1, 2, 3, 4):
        start_time = utime.ticks_ms()
        new_gesture = touch_gesture
        # Annotating display
        tft.fill(0)
        tft.text(font, message_Ano, x_pos1, y_pos1, gc9a01.GREEN)

        if touch_gesture == 1:
            activity = "Walking"
        elif touch_gesture == 2:
            activity = "Sitting"
        elif touch_gesture == 3:
            activity = "Standing"
        elif touch_gesture == 4:
            activity = "Running"
        
        tft.text(font, f"{activity}", x_pos1 + 20, y_pos1 + font.HEIGHT + 10, gc9a01.YELLOW)
        
        # Record the start time and calculate the elapsed time continuously
        while touch.get_gesture() in (1, 2, 3, 4):
            end_time = utime.ticks_ms()
            elapsed = utime.ticks_diff(end_time, start_time)
            elapsed_sec = elapsed / 1000  # Convert to seconds
            
            acc_xyz = qmi8658.Read_acclXYZ()
            gyro_xyz = qmi8658.Read_gyroXYZ()
            # Update elapsed time on display
            tft.text(font, f"Time: {elapsed_sec:.2f}s", x_pos1, font.HEIGHT + 30, gc9a01.CYAN)
            
            log_data = f"{timestamp},{elapsed_sec},{acc_xyz[0]},{acc_xyz[1]},{acc_xyz[2]},{gyro_xyz[3]},{gyro_xyz[4]},{gyro_xyz[5]},{activity}\n"
            print(log_data.strip())

            log_file.write(log_data)
            log_file.flush()
            time.sleep(0.01)  # Small delay to prevent excessive CPU usage
            

    else:
        tft.fill(0)  # background black
        tft.text(font, "User: " + f"{Name}", 20, 50, gc9a01.WHITE)
        tft.text(font, message_noAno, x_pos2, y_pos2, gc9a01.RED)
        tft.text(font, "Swipe U/D/L/R", x_pos2 + 10, y_pos2 + font.HEIGHT, gc9a01.MAGENTA)
    
    
    log_data = f"{timestamp},{elapsed_sec},{acc_xyz[0]},{acc_xyz[1]},{acc_xyz[2]},{gyro_xyz[3]},{gyro_xyz[4]},{gyro_xyz[5]},{activity}\n"
    print(log_data.strip())

    log_file.write(log_data)
    log_file.flush()
    # Sleep to maintain 100Hz logging rate
    time.sleep(0.01)

