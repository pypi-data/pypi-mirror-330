"""
Copyright (c) 2025 ABB Stotz Kontakt GmbH <daniel.koepping@de.abb.com>

SPDX-License-Identifier: MIT

-------

NIUSB6501 Python Driver

The NI USB-6501 is a digital I/O module for USB from National Instruments.
This Python driver allows you to interact with the device using Python 3.10 and above.

This driver is based on Marc Schutz's work on the C driver:
(https://github.com/schuetzm/ni-usb-6501) under the "Do What The F*** You Want To" license (WTFPL)
"""

import usb.core
import usb.util
import platform

ID_VENDOR = 0x3923
ID_PRODUCT = 0x718A


class NIUSB6501:
    """
    A class to interact with the NI USB-6501 device.
    """

    EP_IN = 0x81
    EP_OUT = 0x01
    HEADER_PACKET = 4
    HEADER_DATA = 4
    INTERFACE = 0

    def __init__(self):
        """
        Initialize the NIUSB6501 instance by finding and configuring the USB device.
        """
        self.device = None
        self._connect_device()

    def _connect_device(self, max_attempts=5, retry_delay=1):
        """
        Find and connect to the USB device with retry logic.

        Args:
            max_attempts (int): Maximum number of connection attempts
            retry_delay (int): Delay between retries in seconds
        """
        for attempt in range(max_attempts):
            try:
                # Find the USB device
                self.device = usb.core.find(idVendor=ID_VENDOR, idProduct=ID_PRODUCT)
                if self.device is None:
                    raise ValueError('NI USB-6501 device not found.')

                # Detach kernel driver if necessary (on non-Windows systems)
                if platform.system() != "Windows":
                    for interface in range(3):  # Try multiple interfaces
                        try:
                            if self.device.is_kernel_driver_active(interface):
                                try:
                                    self.device.detach_kernel_driver(interface)
                                except usb.core.USBError:
                                    pass  # Already detached
                        except usb.core.USBError:
                            pass  # Interface not available

                # Set the active configuration
                try:
                    self.device.set_configuration()
                except usb.core.USBError:
                    # Try to reset the device if configuration fails
                    self.device.reset()
                    time.sleep(0.5)
                    self.device.set_configuration()

                return  # Success, exit the retry loop
            except (usb.core.USBError, ValueError) as e:
                if attempt < max_attempts - 1:
                    import time
                    time.sleep(retry_delay)
                else:
                    raise RuntimeError(f"Failed to connect to NI USB-6501 after {max_attempts} attempts: {str(e)}")


    def set_io_mode(self, port0: int, port1: int, port2: int) -> None:
        """
        Set mode for each IO pin. Modes are given as bitmasks for each port.
        bit = 0: read (input)
        bit = 1: write (output)

        Args:
            port0 (int): Bitmask for port 0 (pins 0-7)
            port1 (int): Bitmask for port 1 (pins 8-15)
            port2 (int): Bitmask for port 2 (pins 16-23)
        """
        # Build the request buffer
        buf = bytearray(16)
        buf[0:16] = b"\x02\x10\x00\x00\x00\x05\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00"
        buf[6] = port0 & 0xFF
        buf[7] = port1 & 0xFF
        buf[8] = port2 & 0xFF

        # Send the request to set I/O mode
        self.send_request(0x12, buf)

    def read_port(self, port: int) -> int:
        """
        Read the value from all read-mode pins on the specified port (0, 1, or 2).
        Returns an integer representing the 8-bit value of the port.

        Args:
            port (int): The port number to read (0, 1, or 2)

        Returns:
            int: 8-bit value representing the state of the pins
        """
        # Build the request buffer
        buf = bytearray(8)
        buf[0:8] = b"\x02\x10\x00\x00\x00\x03\x00\x00"
        buf[6] = port & 0xFF

        # Send the request to read the port
        response = self.send_request(0x0E, buf)

        # Parse and return the port state
        port_state = self.parse_port_state(response)
        return port_state

    def write_port(self, port: int, value: int) -> None:
        """
        Write a value to all write-mode pins on the specified port (0, 1, or 2).
        `value` is an 8-bit integer.

        Args:
            port (int): The port number to write to (0, 1, or 2)
            value (int): 8-bit value to write to the port
        """
        # Build the request buffer
        buf = bytearray(12)
        buf[0:12] = b"\x02\x10\x00\x00\x00\x03\x00\x00\x03\x00\x00\x00"
        buf[6] = port & 0xFF
        buf[9] = value & 0xFF

        # Send the request to write to the port
        self.send_request(0x0F, buf)

    def send_request(self, cmd: int, request: bytes) -> bytes:
        """
        Send a request to the device and return the response with retry logic.

        Args:
            cmd (int): Command code
            request (bytes): Request data

        Returns:
            bytes: Response data from the device
        """
        max_attempts = 3

        for attempt in range(max_attempts):
            try:
                if self.device is None:
                    self._connect_device()

                total_length = len(request) + self.HEADER_PACKET + self.HEADER_DATA
                if total_length > 255:
                    raise ValueError(f'Request too long ({total_length} bytes)')

                # Build the packet header
                buf = bytearray(8)
                buf[0:8] = b"\x00\x01\x00\x00\x00\x00\x01\x00"
                buf[3] = (self.HEADER_PACKET + self.HEADER_DATA + len(request)) & 0xFF
                buf[5] = (self.HEADER_DATA + len(request)) & 0xFF
                buf[7] = cmd & 0xFF

                # Append the request data
                buf += request

                # Write the request to the device
                bytes_written = self.device.write(self.EP_OUT, buf, self.INTERFACE)
                if bytes_written != len(buf):
                    raise IOError('Failed to write the complete buffer to the device')

                # Read the response from the device
                ret = self.device.read(self.EP_IN, 64, self.INTERFACE)

                # Return the response data after the packet header
                return bytes(ret)[self.HEADER_PACKET:]
            except (usb.core.USBError, IOError) as e:
                if "Access denied" in str(e) or "Device not found" in str(e) or "No such device" in str(e):
                    if attempt < max_attempts - 1:
                        # Release and reconnect
                        self.release_interface()
                        import time
                        time.sleep(1)
                        self._connect_device()
                    else:
                        raise
                else:
                    raise

    def parse_port_state(self, response: bytes) -> int:
        """
        Parse the response from the device to extract the port state.

        Args:
            response (bytes): The response data from the device

        Returns:
            int: The port state
        """

        if len(response) == 8:
            # Assuming port state is in the last byte
            port_state = response[-1]
            return port_state
        elif len(response) == 12:
            # Assuming port state is at position 10
            port_state = response[10]
            return port_state
        else:
            # Unknown response length; unable to parse
            raise ValueError(f"Unexpected response length: {len(response)}")

    def release_interface(self) -> None:
        """
        Free all resources; the device can be used again without replugging.
        """
        if self.device:
            usb.util.release_interface(self.device, self.INTERFACE)
            usb.util.dispose_resources(self.device)
            self.device.reset()
            self.device = None
