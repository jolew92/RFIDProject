import time
import board
import digitalio
import busio
import mfrc522
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import time

laptopPin = ""

# Initialize Keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

arr = ['zero','one','two','three','four','five','six','seven','eight','nine']

relay = digitalio.DigitalInOut(board.GP3)
relay.switch_to_output()

sck = board.GP6
mosi = board.GP7
miso = board.GP4
spi = busio.SPI(sck, MOSI=mosi, MISO=miso)

cs = digitalio.DigitalInOut(board.GP5)
rst = digitalio.DigitalInOut(board.GP8)
rfid = mfrc522.MFRC522(spi, cs, rst)
rfid.set_antenna_gain(0x07 << 4)

print("\n***** Scan your RFid tag/card *****\n")

prev_data = ""
prev_time = 0
timeout = 1

def digit2text(n):
    return arr[int(n)]   

def spell(text):
    for x in range(len(text)):
        if text[x].isdigit():
            command = getattr(Keycode, str.upper(digit2text(text[x])))
        else:
            command = getattr(Keycode, str.upper(text[x]))
        kbd.press(command)
        time.sleep(.09)
        kbd.release(command)   
        
             

while True:
    (status, tag_type) = rfid.request(rfid.REQALL)

    if status == rfid.OK:
        (status, raw_uid) = rfid.anticoll()

        if status == rfid.OK:
            rfid_data = "{:02x}{:02x}{:02x}{:02x}".format(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])

            if rfid_data != prev_data:
                prev_data = rfid_data

                #print("Card detected! UID: {}".format(rfid_data))

                if rfid_data == "7386600f":
                    print("Karta plaska")
                    kbd.press(Keycode.ENTER)
                    time.sleep(.09)
                    kbd.release(Keycode.ENTER)  
                    time.sleep(1)
                    layout.write(laptopPin)
                    time.sleep(1)
                elif rfid_data == "e30b84f5":
                    print("Brylok")
                    kbd.press(Keycode.WINDOWS, Keycode.R)
                    time.sleep(.09)
                    kbd.release(Keycode.WINDOWS, Keycode.R)
                    layout.write("cmd")
                    kbd.press(Keycode.ENTER)
                    time.sleep(.09)
                    kbd.release(Keycode.ENTER) 
                    time.sleep(1)
                    layout.write("\"C:\Program Files\Google\Chrome\Application\chrome.exe\" \"https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley\"")
                    kbd.press(Keycode.ENTER)
                    time.sleep(.09)
                    kbd.release(Keycode.ENTER) 
                    
            prev_time = time.monotonic()

    else:
        if time.monotonic() - prev_time > timeout:
            prev_data = ""