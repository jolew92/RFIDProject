import board
import board
import digitalio
import busio
import mfrc522

sck = board.GP6
mosi = board.GP7
miso = board.GP4
spi = busio.SPI(sck, MOSI=mosi, MISO=miso)

cs = digitalio.DigitalInOut(board.GP5)
rst = digitalio.DigitalInOut(board.GP8)


def do_read():

	rfid = mfrc522.MFRC522(spi, cs, rst)
	rfid.set_antenna_gain(0x07 << 4)

	print('')
	print("Place card before reader to read from address 0x08")
	print('')

	try:
		while True:

			(stat, tag_type) = rfid.request(rfid.REQIDL)

			if stat == rfid.OK:

				(stat, raw_uid) = rfid.anticoll()

				if stat == rfid.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print('')

					if rfid.select_tag(raw_uid) == rfid.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rfid.auth(rfid.AUTHENT1A, 8, key, raw_uid) == rfid.OK:
							print("Address 8 data: %s" % rfid.read(8))
							rfid.stop_crypto1()
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")
  
while True:
    do_read()