import board
import busio
import digitalio
from time import sleep
from adafruit_circuitpython_mfrc522 import MFRC522

def read_rfid(reader):
    uid = None
    while uid is None:
        try:
            uid = reader.read_uid()
        except RuntimeError:
            pass
    return uid

def tohexstring(v):
    s = "["
    for i in v:
        if i != v[0]:
            s = s + ", "
        s = s + "0x{:02X}".format(i)
    s = s + "]"
    return s

# Set up SPI
spi = busio.SPI(board.GP6, MOSI=board.GP7, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP5)
rst = digitalio.DigitalInOut(board.GP22)

# Set up MFRC522
reader = MFRC522(spi, cs, rst)

print("Bring TAG closer...")
print("")

while True:
    reader.init()
    (stat, tag_type) = reader.request(MFRC522.REQIDL)
    if stat == MFRC522.OK:
        (stat, uid) = reader.select_tag_sn()
        if stat == MFRC522.OK:
            card = int.from_bytes(bytes(uid), "little", False)
            print("CARD ID:", tohexstring(uid))
    
    sleep(0.5)  # To avoid reading the same card repeatedly in a short time
