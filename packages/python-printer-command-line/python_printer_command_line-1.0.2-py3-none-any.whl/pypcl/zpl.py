#!/usr/bin/env python
# -*- coding: utf8 -*-
"""zpl.py

Class to print Zebra PCL document on my Zebra Label Printer LP 2824 Plus.

This class exposes method to help in generating ZPL command enclosed
within the Text Stream to print.

Copyright 2015 DMeurisse <info@mchobby.be> MC Hobby SPRL

Licence: CC-BY-SA-NC

Cannot be reused for commercial product without agreement.
Please, contact us at <info@mchobby.be>

------------------------------------------------------------------------
History:
  07 feb 2015 - Dominique - v 0.1 (première release)
"""

from .pypcl import *


class ZplDocument(PclDocument):
    """Class with helper function to generate ZPL content for
    Zebra printer supporting ZCL.

    Have been tested on a Zebra LP 2824 Plus Label Printer and
    Direct Thermal Paper Zipship labels "Z-select 2000d Label
    32x25mm 2580/roll" """

    PRINTER_CRLF = chr(10)  # CR/LF for Zebra can be a #10 LineFeed char
    # PRINTER_CR   = chr(13)         # return at the begin of the same line
    PRINTER_ESC = chr(0x5E)  # ^ escape command for ZPL

    # Font Information - coming from ZPL II programming Guide, pg 373
    # The tuple is formatted as follow
    #    (Heigh,Width) - default Height and Height in dots
    #    [types]       - list of types U=uppercase,L=Lowercase, D=descenders (goes below the base line)
    #    IntercharGap  - int, space between characters in dots. -1 for Proportional.
    #    BaseLine      - lambda, define where is positionned the baseline from the top of the matrix.
    #                         this is important for Descenders font where some characters like "p" can go under the base line.
    #                    The parameter of lambda function is Height. May return an int or a float
    #
    # Note that some definitions are missing and remplaced by None
    # See also wikipedia Typograpgy article:
    #    http://en.wikipedia.org/wiki/Descender
    PRINTER_FONT = {
        "A": ((9, 5), ["U", "L", "D"], 1, lambda h: 7),
        "B": ((11, 7), ["U"], 2, lambda h: 11),
        "C": ((18, 10), ["U", "L", "D"], 2, lambda h: 14),
        "D": ((18, 10), ["U", "L", "D"], 2, lambda h: 14),
        "E": ((28, 15), ["OCR-B"], 5, lambda h: 23),
        "F": ((26, 13), ["U", "L", "D"], 3, lambda h: 21),
        "G": ((60, 40), ["U", "L", "D"], 8, lambda h: 48),
        "H": ((21, 13), ["OCR-A"], 6, lambda h: 21),
        "O": ((15, 12), [], -1, lambda h: 3 * h / 4),
        "GS": ((24, 24), ["SYMBOL"], -1, lambda h: 3 * h / 4),
        "P": None,
        "Q": None,
        "R": None,
        "S": None,
        "T": None,  # Use 17, 8 as size for a nice Bold effect
        "U": None,
        "V": None,
        "0": None,
    }

    PRINTER_ORIENTATION_NORMAL = "N"
    PRINTER_ORIENTATION_ROTATED = "R"  # rotated 90 degrees (clockwise)
    PRINTER_ORIENTATION_INVERTED = "I"  # inverted 180 degrees
    PRINTER_ORIENTATION_BOTTOMUP = "B"  # read from bottom up, 270 degrees

    PRINTER_ORIENTATION = [
        PRINTER_ORIENTATION_NORMAL,
        PRINTER_ORIENTATION_ROTATED,
        PRINTER_ORIENTATION_INVERTED,
        PRINTER_ORIENTATION_BOTTOMUP,
    ]

    PRINTER_TEXT_JUSTIFICATION_LEFT = "L"  # text will be left-justified left
    PRINTER_TEXT_JUSTIFICATION_CENTER = "C"  # text will be centered
    PRINTER_TEXT_JUSTIFICATION_RIGHT = "R"  # text will be right-justified
    PRINTER_TEXT_JUSTIFICATION_JUSTIFIED = "J"  # text will be justified

    PRINTER_TEXT_JUSTIFICATION = [
        PRINTER_TEXT_JUSTIFICATION_LEFT,
        PRINTER_TEXT_JUSTIFICATION_CENTER,
        PRINTER_TEXT_JUSTIFICATION_RIGHT,
        PRINTER_TEXT_JUSTIFICATION_JUSTIFIED,
    ]

    PRINT_MODE_TEAR_OFF = "T"
    PRINT_MODE_PEEL_OFF = "P"
    PRINT_MODE_REWIND = "R"
    PRINT_MODE_APPLICATOR = "A"
    PRINT_MODE_CUTTER = "C"
    PRINT_MODE_DELAYED_CUTTER = "D"
    PRINT_MODE_RFID = "F"
    PRINT_MODE_KIOSK = "K"

    MEDIA_TRACKING_CONTINUOUS = "N"  # continous label (like receipt ticket)
    MEDIA_TRACKING_WEB_SENSING = "Y"  # non-continuous
    MEDIA_TRACKING_WEB_SENSING_W = "W"  # non-continuous
    MEDIA_TRACKING_MARK_SENSING = "M"  # non-continuous
    MEDIA_TRACKING_AUTO = "A"  # Auto-detect during the calibration
    MEDIA_TRACKING_CONTINUOUS_V = "V"  # Continuous media, variable length

    # === Override ===
    def sending(self):
        """sending() is called when PclDocument.send() want  me to
        send the data to the printer over the medium"""
        for pcl_line_tuple in self:
            if pcl_line_tuple[0] == PCL_DATA_TYPE.PCL:
                # Escape sequences are in UTF8
                self.printer_adapter.send(bytes(pcl_line_tuple[1].encode("UTF-8")))
            elif pcl_line_tuple[0] == PCL_DATA_TYPE.TEXT:
                self.printer_adapter.send(
                    bytes(pcl_line_tuple[1].encode(self.target_encoding))
                )
            else:  # Binary
                # Tuple[1] already contains a bytes() type
                self.printer_adapter.send(pcl_line_tuple[1])

    # === Tools ===
    def print_quantity(self, qty):
        self.writeln("^PQ%i,0,0,Y" % qty)

    def print_mode(self, mode, prepeel=False):
        """Zebra Print Mode.

        :param mode: one of the PRINT_MODE_xx constant.
        :param prepeel: prepeel select (depend on mode)"""
        self.writeln("^MM%s,%s" % (mode, "1" if prepeel else "0"))

    def media_tracking(self, tracking, offset=0):
        """specifies the media type being used and the black mark offset in dots

        :param tracking: type of black mark tracking on the media. One of the TRACKING_xxx constant.
        :param offset: This sets the expected location of the media mark relative to the point of separation between documents.
        """
        self.writeln("^MN%s,%s" % (tracking, offset))

    def label_length(self, length_dots=None, length_mm=None, resolution=203.2):
        """Specify length of the label for continuous paper. Must be issued before a field separator!
        Length can be specified in dots or in mm (with vertical resolution parameter)

        :param length_dots: vertical length in dots (length_mm can then be omitted).
        :param length_mm: vertical length in mm (length_dots can then be omitted).
        :param resolution: vertical resolution in dots per inch 203.2 by default.
        """
        if length_mm:
            length_dots = int(length_mm * resolution / 25.4)
        assert 1 <= length_dots <= 32000, "Invalid length."

        self.writeln("^LL%s" % length_dots)

    def label_home(self, x_mm, y_mm, resolution=203.2):
        """Start position of printing on a pre-printed label."""
        # See label_length for calculation details between mm and dots
        x_dots = int(x_mm * resolution / 25.4)
        y_dots = int(y_mm * resolution / 25.4)

        self.writeln("^LH%s,%s" % (x_dots, y_dots))

    def format_start(self, encoding=None):
        self.writeln("^XA")
        if encoding == None:
            encoding = self.target_encoding
        if encoding == "UTF-8":
            self.writeln("^CI28")

    def format_end(self):
        self.writeln("^XZ")

    def field(self, origin, font, block=None, data=""):
        """allows to write a field data in one shot

        origin (tuple) = (x_position_dots, y_position_dots). (50,50) or (50,100) for 1.25" x 1" label on LP 2824.
        font (tuple) = (font_type, font_height_dots, font_width_dots, font_orientation ). See definition of field_font() for more info.
        block (tuble) = (block_width, max_lines, space_between_lines, text_justification). See definition of field_block() for more info.
        data (unicode) = Data to print out."""

        self.field_origin(origin)
        if font != None:
            # font type, font width dot, font height dots
            self.field_font(font)
        if block != None:
            # block_width, max_lines, space_between_lines, text_justification
            self.field_block(
                block_width=block[0],
                max_lines=block[1],
                space_between_lines=block[2],
                text_justification=block[3],
            )
        self.field_data(data)
        self.field_separator()

    def barcode39(self, origin, data, height_dots=50):
        """allows to draw a barcode 39 on the label"""
        assert (
            isinstance(origin, tuple) and len(origin) == 2
        ), "origin must be a tuple (x-dots,y-dots)"
        assert isinstance(origin[0], int) and isinstance(
            origin[1], int
        ), "origin must contains integers values"
        assert isinstance(data, str), "Data must be string"
        assert isinstance(height_dots, int), "height_dots must be an interger"

        self.field_origin(origin)
        self.field_barcode39(
            ZplDocument.PRINTER_ORIENTATION_NORMAL, False, height_dots, True, False
        )
        self.field_data(data)
        self.field_separator()

    def qrcode(self, origin, data, magnification=6):
        """allows to draw a QR code on the label"""
        assert (
            isinstance(origin, tuple) and len(origin) == 2
        ), "origin must be a tuple (x-dots,y-dots)"
        assert isinstance(origin[0], int) and isinstance(
            origin[1], int
        ), "origin must contains integers values"
        assert isinstance(data, str), "Data must be string"
        assert isinstance(magnification, int), "height_dots must be an interger"

        self.field_origin(origin)
        self.field_qrcode(
            ZplDocument.PRINTER_ORIENTATION_NORMAL, 2, magnification, "Q", 7
        )
        self.field_data(data)
        self.field_separator()

    def ean13(self, origin, ean, height_dots=50):
        """allows to draw a ean13 on the label"""
        assert (
            isinstance(origin, tuple) and len(origin) == 2
        ), "origin must be a tuple (x-dots,y-dots)"
        assert isinstance(origin[0], int) and isinstance(
            origin[1], int
        ), "origin must contains integers values"
        assert isinstance(ean, str), "Data must be string"
        assert (len(ean) == 13) and (ean.isdigit()), "ean must have 13 digits only"
        assert isinstance(height_dots, int), "height_dots must be an integer"

        self.field_origin(origin)
        self.field_ean13(
            ZplDocument.PRINTER_ORIENTATION_NORMAL, height_dots, True, False
        )
        self.field_data(ean)
        self.field_separator()

    def field_origin(self, origin):
        """set the origin of a field data"""
        assert (
            isinstance(origin, tuple) and len(origin) == 2
        ), "origin must be a tuple (x-dots,y-dots)"
        assert isinstance(origin[0], int) and isinstance(
            origin[1], int
        ), "origin must contains integers values"

        self.write("^FO%i,%i" % origin)

    def field_block(
        self,
        block_width=200,
        max_lines=1,
        space_between_lines=0,
        text_justification=PRINTER_TEXT_JUSTIFICATION_LEFT,
    ):
        """The ^FB command allows you to print text into a defined block type format. This command formats an ^FD or ^SN string into a block of text using the origin, font, and rotation specified for the text string. The ^FB command also contains an automatic word-wrap function."""
        assert (
            isinstance(block_width, int) and block_width > 0
        ), "block width should be greater than 0, otherwise text does not print"
        assert (
            isinstance(max_lines, int) and max_lines >= 1 and max_lines <= 9999
        ), "the number of lines should be in the range of 1 to 9999"
        assert (
            isinstance(space_between_lines, int)
            and space_between_lines >= -9999
            and max_lines <= 9999
        ), "space between lines should be in the range of -9999 to 9999"
        assert (
            text_justification in self.PRINTER_TEXT_JUSTIFICATION
        ), "Invalid text justification %s not in range %s" % (
            text_justification,
            self.PRINTER_TEXT_JUSTIFICATION.keys(),
        )

        self.write(
            "^FB%i,%i,%i,%s"
            % (block_width, max_lines, space_between_lines, text_justification)
        )

    def field_barcode39(
        self,
        orientation=PRINTER_ORIENTATION_NORMAL,
        mod43_checksum=False,
        height_dots=50,
        interpretation_line=True,
        interpretation_above=False,
    ):
        """Write a field entry for barcode 39. Data must be send into a field_data()"""
        assert (
            orientation in self.PRINTER_ORIENTATION
        ), "Invalid orientation %s not in range %s" % (
            orientation,
            self.PRINTER_ORIENTATION.keys(),
        )

        self.write(
            "^B3%s,%s,%i,%s,%s"
            % (
                orientation,
                "Y" if mod43_checksum else "N",
                height_dots,
                "Y" if interpretation_line else "N",
                "Y" if interpretation_above else "N",
            )
        )

    def field_qrcode(
        self,
        orientation=PRINTER_ORIENTATION_NORMAL,
        model=2,
        magnification=6,
        reliability_level="Q",
        nabk=7,
    ):
        """Write a field entry for QR code. Data must be send into a field_data()"""
        assert (
            orientation in self.PRINTER_ORIENTATION
        ), "Invalid orientation %s not in range %s" % (
            orientation,
            self.PRINTER_ORIENTATION.keys(),
        )

        self.write(
            "^BQ%s,%i,%i,%s,%i"
            % (orientation, model, magnification, reliability_level, nabk)
        )

    def field_ean13(
        self,
        orientation=PRINTER_ORIENTATION_NORMAL,
        height_dots=50,
        interpretation_line=True,
        interpretation_above=False,
    ):
        assert (
            orientation in self.PRINTER_ORIENTATION
        ), "Invalid orientation %s not in range %s" % (
            orientation,
            self.PRINTER_ORIENTATION.keys(),
        )

        self.write(
            "^BE%s,%i,%s,%s"
            % (
                orientation,
                height_dots,
                "Y" if interpretation_line else "N",
                "Y" if interpretation_above else "N",
            )
        )

    def field_font(self, font):
        """Set the font of a field

        font (tuple) - (zebra-font-code, font-height-dots, font-width-dots)
                                   see PRINTER_FONT dictionnary for available values.
                                   Smallest font is 18,10 -> 180, 100

                                   You can use the function font() to create the tuple.
        """
        assert (
            isinstance(font, tuple) and len(font) == 4
        ), "font must be a tuple (font-code,height-dots,width-dots)"
        assert isinstance(font[0], str), "font code must be str"
        assert font[0] in self.PRINTER_FONT, "invalid font %s" % font[0]
        assert isinstance(font[2], int) and isinstance(
            font[3], int
        ), "font height and width must contains integers values"

        self.write("^A%s%s,%i,%i" % font)

    def font(
        self,
        font_code,
        font_height_dots=None,
        font_width_dots=None,
        font_orientation=PRINTER_ORIENTATION_NORMAL,
    ):
        """Create a font tuple for field_font().

        It is better to use this function because we could improve font
        support in the future ;-)

        Good documentation on font can be found in "ZPL II programming Guide"
           pg 371, "Fonts and bar codes".
        See also Font Typography on wikipedia
           http://en.wikipedia.org/wiki/Descender
        See also the PRINTER_FONT structure

        A good font sample is font('D',36,20) which fit into a 1.25" x 1.00" label"""

        assert isinstance(font_code, str), "font_code must be string"
        assert ((font_height_dots == None) or isinstance(font_height_dots, int)) and (
            (font_width_dots == None) or isinstance(font_width_dots, int)
        ), "height and width must be integers"
        assert (
            font_code in self.PRINTER_FONT
        ), "invalid font %s, not in PRINTER_FONT %s" % (
            font_code,
            self.PRINTER_FONT.keys(),
        )
        # assert (font_height_dots == None) or (18 <= font_height_dots <= 180), "height must be in between 18..180"
        # assert (font_width_dots == None) or (10 <= font_width_dots <= 100), "width must be in between 10..100"

        if font_height_dots == None:
            if self.PRINTER_FONT[font_code] == None:
                raise PyPclError(
                    "cannot resolve default height for font %s" % font_code
                )
            else:
                # PRINTER_FONT[font_code][0] -> first tuple item => (default_height,default_width)
                font_height_dots = self.PRINTER_FONT[font_code][0][0]
        if font_width_dots == None:
            if self.PRINTER_FONT[font_code] == None:
                raise PyPclError("cannot resolve default width for font %s" % font_code)
            else:
                # PRINTER_FONT[font_code][0] -> first tuple item => (default_height,default_width)
                font_width_dots = self.PRINTER_FONT[font_code][0][1]

        return (font_code, font_orientation, font_height_dots, font_width_dots)

    def use_new_font(self, newFontCode, fontName):
        """Writes a command that sets new font, until printer will be turnded off.
        Example command: ^CWQ,E:TT0003M_.FNT"""
        assert isinstance(newFontCode, str), "font code must be str"
        assert isinstance(fontName, str), "font name must be str"
        if not newFontCode in self.PRINTER_FONT:
            self.PRINTER_FONT[newFontCode] = None
        self.write("^CW%s,%s" % (newFontCode, fontName))

    def field_data(self, data):
        """just send the data of the field. Should be followed by field
        separator"""
        assert isinstance(data, str), "Data must be string"

        self.writeln("^FD%s" % data)

    def field_separator(self):
        """each field (starting with field_origin() must ends with field_separator()"""
        self.writeln("^FS")

    def draw_box(self, x, y, w, h, tickness=1, color="B"):
        """Draw a box or a line"""
        self.field_origin((x, y))
        self.writeln("^GB%s,%s,%i,%s" % (w, h, tickness, color))
        self.field_separator()

    def draw_circle(self, x, y, d, tickness=2, color="B"):
        """Draw a circle of diameter d"""
        self.field_origin((x, y))
        self.writeln("^GC%s,%i,%s" % (d, tickness, color))
        self.field_separator()
