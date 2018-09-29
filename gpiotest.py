import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

CLK = 18
MISO = 23
MOSI = 24
CS = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK,cs=CS,miso=MISO,mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

signal_reads = 16
print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.

def get_read():
	values = [0]*8
	for j in range(signal_reads):
		for i in range(8):
			values[i] += mcp.read_adc(i)
	for i in range(8):
		values[i] = values[i] / signal_reads
	return values

while True:
    # Read all the ADC channel values in a list.
    values = [0]*8
    #for i in range(8):
    #    # The read_adc function will get the value of the specified channel (0-7).
    #    values[i] = mcp.read_adc(i)
    values = get_read()
    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.1)
