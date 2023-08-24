
import adafruit_sdcard
import board
import busio
import digitalio
import storage
import sys
 
# Connect to the card and mount the filesystem for Seeed Studio XIAO .
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D2)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
sys.path.append("/sd")
# sys.path.append("/sd/lib")  ## switch to the path to SD card
