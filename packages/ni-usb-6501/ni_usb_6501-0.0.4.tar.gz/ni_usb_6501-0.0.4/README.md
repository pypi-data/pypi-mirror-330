# NI USB 6501 Python Driver

This package provides a Python driver for configuring and controlling the NI USB 6501 I/O module.

## Prerequisites

### Linux

1. **Install PyUSB and libusb:**

   ```bash
   pip install pyusb
   sudo apt-get install libusb-1.0-0-dev
   ```

2. **Set up udev rules to allow non-root access to the device:**

   ```bash
   sudo sh -c 'echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"3923\", ATTRS{idProduct}==\"718a\", MODE=\"0666\"" > /etc/udev/rules.d/99-ni_usb_6501.rules'
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

   This will grant all users read and write permissions to the device.

### Windows
1. **Install the WinUSB driver for the NI USB-6501 device using [Zadig](https://zadig.akeo.ie/).**


## Installation
Download the `.whl` file from the **Releases** page and install it using: `pip install <filename>.whl`

## Usage

```python
from ni_usb_6501 import NIUSB6501

# Instantiate the NIUSB6501 driver
device = NIUSB6501()

# Pin-to-bit mapping:
# Each port has 8 pins, and the most significant bit (MSB) corresponds to the highest pin number:
# Port 0: Pin 7 (MSB) -> Bit 7, Pin 6 -> Bit 6, ..., Pin 0 (LSB) -> Bit 0
# Port 1: Pin 15 -> Bit 7, ..., Pin 8 -> Bit 0
# Port 2: Pin 23 -> Bit 7, ..., Pin 16 -> Bit 0

# Set IO modes: Ports 0 and 1 as output, port 2 as input
# 0xFF -> 11111111: All pins set to output
# 0x00 -> 00000000: All pins set to input
device.set_io_mode(0xFF, 0xFF, 0x00)

# Write to ports 0 and 1:
# Port 0: Set pins 7, 6, 5, 4 to HIGH (1) and pins 3, 2, 1, 0 to LOW (0)
device.write_port(0, 0b11110000)  # 0xF0
print("Port 0: Set pins 7, 6, 5, 4 to HIGH, pins 3, 2, 1, 0 to LOW.")

# Port 1: Set pins 15, 13, 11, 9 to HIGH (1) and pins 14, 12, 10, 8 to LOW (0)
device.write_port(1, 0b10101010)  # 0xAA
print("Port 1: Set alternating HIGH and LOW starting from pin 15 (MSB).")

# Read from port 2:
# The returned value will represent the HIGH/LOW state of pins 23 to 16 (bits 7 to 0 of port 2).
input_value = device.read_port(2)
print(f"Port 2 input (pins 23 to 16): {bin(input_value)}")

# Perform additional operations:
# Toggle port 0 pins between 0b00001111 and 0b11110000
device.write_port(0, 0b00001111)  # Set pins 3, 2, 1, 0 to HIGH
print("Port 0: Set pins 3, 2, 1, 0 to HIGH, pins 7, 6, 5, 4 to LOW.")

# Read and display input from port 2 again
input_value = device.read_port(2)
print(f"Port 2 input after toggle: {bin(input_value)}")

# Release the device resources
device.release_interface()
print("Device released.")

```
