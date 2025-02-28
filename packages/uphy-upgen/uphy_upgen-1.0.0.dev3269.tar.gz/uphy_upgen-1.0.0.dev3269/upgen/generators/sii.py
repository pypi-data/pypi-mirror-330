from io import BufferedIOBase
import logging
from pathlib import Path
import os

from ctypes import LittleEndianStructure, sizeof, c_ubyte, c_ushort, c_uint
from crc8 import crc8

from ..model import Adapter

_logger = logging.getLogger(__name__)


def str2hex(str):
    try:
        return int(str.replace('#', '0'), base=0)
    except (ValueError, AttributeError):
        return 0


def eeprom_size(nbytes):
    bits = nbytes * 8
    kbits = bits // 1024
    return kbits - 1


class Category:
    DC = 60
    RXPDO = 51
    TXPDO = 50
    SYNCM = 41
    FMMU = 40
    GENERAL = 30
    STRINGS = 10


class SIIElement(LittleEndianStructure):

    def write(self, f):
        f.write(self)


class SIIHeader(SIIElement):
    _fields_ = [
        ("category", c_ushort),
        ("wordSize", c_ushort)
    ]

    def __init__(self, category, size):
        self.category = category
        self.is_odd = size & 0x01
        if self.is_odd:
            # Pad data to even number of bytes
            size += 1
        self.wordSize = size // 2


class SIIPdi(SIIElement):
    _fields_ = [
        ("pdiControl", c_ushort),
        ("pdiConfiguration", c_ushort),
        ("syncImpulseLen", c_ushort),
        ("pdiConfiguration2", c_ushort),
        ("stationAlias", c_ushort),
        ("asicConfig", c_ushort),
        ("reserved1", c_ushort),
        ("checksum", c_ushort),
        ("vendorID", c_uint),
        ("productCode", c_uint),
        ("revisionNumber", c_uint),
        ("serialNumber", c_uint),
        ("reserved2", c_ubyte * 8),
        ("bootRecvMboxOffset", c_ushort),
        ("bootRecvMboxSize", c_ushort),
        ("bootSendMboxOffset", c_ushort),
        ("bootSendMboxSize", c_ushort),
        ("standardRecvMboxOffset", c_ushort),
        ("standardRecvMboxSize", c_ushort),
        ("standardSendMboxOffset", c_ushort),
        ("standardSendMboxSize", c_ushort),
        ("mboxProtocol", c_ushort),
        ("reserved3", c_ubyte * 66),
        ("eepromSize", c_ushort),
        ("version", c_ushort),
    ]

    def write(self, f):
        # Calculate CRC8 checksum of first 7 words
        hash = crc8(initial_start=0xFF)
        b = bytearray(self)
        hash.update(b[0:14])
        self.checksum = ord(hash.digest())
        f.write(self)


class SIICategoryGeneral(SIIElement):
    _fields_ = [
        ("groupIdx", c_ubyte),
        ("imgIdx", c_ubyte),
        ("orderIdx", c_ubyte),
        ("nameIdx", c_ubyte),
        ("reserved1", c_ubyte),
        ("coeDetails", c_ubyte),
        ("foeDetails", c_ubyte),
        ("eoeDetails", c_ubyte),
        ("reserved2", c_ubyte * 3),
        ("flags", c_ubyte),
        ("currentOnEbus", c_ushort),
        ("reserved3", c_ubyte * 2),
        ("physicalPort", c_ushort),
        ("reserved4", c_ubyte * 14),
    ]

    def write(self, f):
        header = SIIHeader(Category.GENERAL, sizeof(self))
        f.write(header)
        f.write(self)


class SIIFmmu(SIIElement):
    _fields_ = [
        ("fmmu", c_ubyte),
    ]


class SIICategoryFmmu:

    def __init__(self, fmmus):
        self.fmmus = fmmus
        self.size = sum(map(sizeof, fmmus))

    def write(self, f):
        header = SIIHeader(Category.FMMU, self.size)
        f.write(header)
        for fmmu in self.fmmus:
            f.write(fmmu)
        if header.is_odd:
            f.write(c_ubyte())


class SIISyncM(SIIElement):
    _fields_ = [
        ("start", c_ushort),
        ("length", c_ushort),
        ("control", c_ubyte),
        ("status", c_ubyte),
        ("enable", c_ubyte),
        ("type", c_ubyte),
    ]


class SIICategorySyncM:

    def __init__(self, syncms):
        self.syncms = syncms
        self.size = sum(map(sizeof, syncms))

    def write(self, f):
        header = SIIHeader(Category.SYNCM, self.size)
        f.write(header)
        for syncm in self.syncms:
            f.write(syncm)


def sii_string(string):
    '''Factory function for strings, as the length depends on the string'''
    class SIIString(SIIElement):
        _fields_ = [
            ("length", c_ubyte),
            ("string", c_ubyte * len(string)),
        ]

        def __init__(self, string):
            self.length = len(string)
            self.string = (c_ubyte*len(string))(*bytearray(string, "utf-8"))

    return SIIString(string)


class SIICategoryString:

    def __init__(self, strings):
        self.strings = strings
        self.size = sum(map(sizeof, strings))

    def write(self, f):
        header = SIIHeader(Category.STRINGS, self.size + 1)
        f.write(header)
        f.write(c_ubyte(len(self.strings)))
        for string in self.strings:
            f.write(string)
        if header.is_odd:
            f.write(c_ubyte())


class SIIGenerator:

    def __init__(self, model):
        self.model = model
        self.device = self.model.devices[0]

    def select_device(self, device_name):
        if device_name == None:
            self.device = self.model.devices[0]
        else:
            self.device = self.model.get_device(device_name)

        if self.device == None:
            raise Exception(f'{device_name} not found in model')

    def export_file(self):
        if Adapter.ETHERCAT not in self.model.adapters:
            _logger.debug("EtherCAT is not enabled")
            return

        if not self.model.ethercat:
            _logger.warn('Model does not include a valid EtherCAT configuration')
            return

        _logger.info("Exporting EtherCAT SII eeprom contents")

        filename = str(Path(os.getcwd()) / "eeprom.bin")
        with open(filename, "wb") as f:
            self.export_data(f)

    def export_data(self, f):
        ecat = self.model.ethercat
        device = self.device

        pdi = SIIPdi()
        pdi.pdiControl = ecat._pdi_control
        pdi.pdiConfiguration = ecat._pdi_configuration
        pdi.asicConfig = ecat._asic_config
        pdi.vendorID = str2hex(ecat.vendor_id)
        pdi.productCode = str2hex(device.ethercat.product_code)
        pdi.revisionNumber = str2hex(device.ethercat.revision)
        pdi.serialNumber = str2hex(device.serial)
        pdi.bootRecvMboxOffset = ecat._boot_recv_mbox.offset
        pdi.bootRecvMboxSize = ecat._boot_recv_mbox.size
        pdi.bootSendMboxOffset = ecat._boot_send_mbox.offset
        pdi.bootSendMboxSize = ecat._boot_send_mbox.size
        pdi.standardRecvMboxOffset = ecat._standard_recv_mbox.offset
        pdi.standardRecvMboxSize = ecat._standard_recv_mbox.size
        pdi.standardSendMboxOffset = ecat._standard_send_mbox.offset
        pdi.standardSendMboxSize = ecat._standard_send_mbox.size
        pdi.mboxProtocol = ecat._mbox_control
        pdi.eepromSize = eeprom_size(ecat._eeprom_size)
        pdi.version = 1

        strings = SIICategoryString([
            # The string addition order is important, since SOEM will
            # choose the first string as the name
            sii_string(device.name),                 # Name
            sii_string(self.model.ethercat.group)    # Group
        ])

        general = SIICategoryGeneral()

        # Set index into strings array (index starts at 1)
        general.groupIdx = 2  # model.ethercat.group
        general.orderIdx = 1  # device.name
        general.nameIdx = 1  # device.name

        general.reserved1 = 5  # Port 0 & 1: MII
        general.coeDetails = ecat._coe
        general.foeDetails = ecat._foe

        fmmu = SIICategoryFmmu([
            SIIFmmu(f.value) for f in ecat._fmmu
        ])

        sm = SIICategorySyncM([
            SIISyncM(
                sm.address,
                sm.length,
                sm.control,
                sm.status,
                sm.enable,
                sm.type.value,
            ) for sm in ecat._sm
        ])

        pdi.write(f)
        strings.write(f)
        general.write(f)
        fmmu.write(f)
        sm.write(f)

        # Fill remainder with 0xFF
        remain = ecat._eeprom_size - f.tell()
        for _ in range(remain):
            f.write(c_ubyte(0xFF))
