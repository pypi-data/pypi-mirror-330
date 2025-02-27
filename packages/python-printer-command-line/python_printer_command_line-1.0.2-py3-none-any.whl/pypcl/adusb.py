"""adusb.py

USB Adaptater to send PclDocument (or derivated class) over an
USB connection (for example when there is no posibility to use CUPS or serial connection).

Copyright 2024 Oskar Jaskólski <oskarrro90@gmail.com>

Licence: CC-BY-SA-NC
"""

import usb.core
import usb.util

from . import *


class PrinterUsbAdapter(PrinterAdapter):
    """Used to send the print stream over an USB connection."""

    def __init__(
        self, idVendor, idProduct, usb_args=None, timeout=0, in_ep=0x82, out_ep=0x01
    ):
        """
        :param idVendor: Vendor ID
        :param idProduct: Product ID
        :param usb_args: Optional USB arguments (e.g. custom_match)
        :param timeout: Is the time limit of the USB operation. Default without timeout.
        :param in_ep: Input endpoint
        :param out_ep: Output endpoint
        """
        PrinterAdapter.__init__(self)
        self.timeout = timeout
        self.in_ep = in_ep
        self.out_ep = out_ep

        self.device = None
        self.device_endpoint = None

        self.usb_args = usb_args or {}
        if idVendor:
            self.usb_args["idVendor"] = idVendor
        if idProduct:
            self.usb_args["idProduct"] = idProduct

    @property
    def printer_socket(self):
        return self.__printer_socket

    def open(self):
        """Search device on USB tree and set it to be used to stream the data over USB."""
        self.device = usb.core.find(**self.usb_args)
        if self.device is None:
            raise USBNotFoundError(
                f"Device {self.device} not found or cable not plugged in."
            )

        self.idVendor = self.device.idVendor
        self.idProduct = self.device.idProduct

        # Detach kernel driver if needed
        if self.device.is_kernel_driver_active(0):
            self.device.detach_kernel_driver(0)

        try:
            self.device.set_configuration()
        except usb.core.USBError as e:
            print("Could not set configuration: {0}".format(str(e)))

        # # get an endpoint instance
        # cfg = self.__device.get_active_configuration()
        # intf = cfg[(0, 0)]

        # self.__device_endpoint = usb.util.find_descriptor(
        #     intf,
        #     # match the first OUT endpoint
        #     custom_match=lambda e: \
        #     usb.util.endpoint_direction(e.bEndpointAddress) == \
        #     usb.util.ENDPOINT_OUT)

        # assert self.__device_endpoint is not None

        # Change the isopen flag when every went right
        PrinterAdapter.open(self)

    def close(self):
        """Release USB interface"""
        if self.device:
            usb.util.dispose_resources(self.device)
        self.device = None

        # change internal flag
        PrinterAdapter.close(self)

    def get(self):
        """Reads a data buffer and returns it."""
        return self.device.read(self.in_ep, 16)

    def send(self, bytes_to_send):
        """User did call send on the PclDocument. We have to
        send the bytes of the document

        :param bytes_to_send: arbitrary data to be printed
        :type bytes_to_send: bytes
        """

        PrinterAdapter.send(self, bytes_to_send)

        # self.__device_endpoint.write(bytes_to_send, self.timeout)
        self.device.write(self.out_ep, bytes_to_send, self.timeout)
