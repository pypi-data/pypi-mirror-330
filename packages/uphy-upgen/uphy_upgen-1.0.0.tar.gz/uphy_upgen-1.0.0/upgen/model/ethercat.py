from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, UUID4, PrivateAttr


class MBox(BaseModel):
    offset: int
    size: int


class Fmmu(Enum):
    Unused = 0
    Outputs = 1
    Inputs = 2
    MBoxState = 3


class SMType(Enum):
    MBoxOut = 1
    MBoxIn = 2
    Outputs = 3
    Inputs = 4


class SM(BaseModel):
    address: int
    length: int
    control: int
    status: int
    enable: int
    type: SMType


class CoE(Enum):
    Sdo = 1 << 0
    SdoInfo = 1 << 1
    PdoAssign = 1 << 2
    PdoConfiguration = 1 << 3
    PdoUpload = 1 << 4
    CompleteAccess = 1 << 5

class FoE(Enum):
    Enable = 1 << 0

class MBoxProtocol(Enum):
    EoE = 1 << 1
    CoE = 1 << 2
    FoE = 1 << 3
    SoE = 1 << 4
    VoE = 1 << 5


class CiAObject(BaseModel):
    """EtherCAT process data"""
    index: str = Field(title="Index")
    subindex: str = Field(title="Subindex")
    signal: UUID4 = Field(title="Signal")


class CiAPDO(BaseModel):
    """An EtherCAT Rx or Tx PDO. An Rx PDO is an output signal, a Tx PDO is an input signal."""
    name: str = Field(title="PDO name")
    index: str = Field(title="Index")
    entries: List[CiAObject] = Field(title="PDO entries", default=[])


class EtherCATModule(BaseModel):
    """EtherCAT specific module configuration. Maps signals to Rx or Tx PDO:s"""
    rxpdo: List[CiAPDO] = Field(title="Rx PDO", default=[])
    txpdo: List[CiAPDO] = Field(title="Tx PDO", default=[])
    objects: List[CiAObject] = Field(title="SDO", default=[])
    profile: str = Field(title="EtherCAT profile", default="5001")

    def generate_mapping(self, module, module_ix):
        if len(module.outputs) > 0 and len(self.rxpdo) == 0:
            pdo = CiAPDO(
                name = "Outputs",
                index = "#x1600",
            )
            for ix, signal in enumerate(module.outputs):
                entry = CiAObject(
                    index = f"#x{0x6000 + ix:x}",
                    subindex = 0,
                    signal = signal.id
                )
                pdo.entries.append(entry)
            self.rxpdo.append(pdo)

        if len(module.inputs) > 0 and len(self.txpdo) == 0:
            pdo = CiAPDO(
                name = "Inputs",
                index = "#x1A00",
            )
            for ix, signal in enumerate(module.inputs):
                entry = CiAObject(
                    index = f"#x{0x7000 + ix:x}",
                    subindex = 0,
                    signal = signal.id
                )
                pdo.entries.append(entry)
            self.txpdo.append(pdo)

        if len(module.parameters) > 0 and len(self.objects) == 0:
            for ix, parameter in enumerate(module.parameters):
                entry = CiAObject(
                    index = f"#x{0x8000 + ix:x}",
                    subindex = 0,
                    signal = parameter.id
                )
                self.objects.append(entry)

class EtherCATDevice(BaseModel):
    """EtherCAT specific device configuration"""
    product_code: str = Field(title="Product code", default="0")
    revision: str = Field(title="Revision", default="0")
    profile: str = Field(title="EtherCAT profile", default="5001")


class EtherCATRoot(BaseModel):
    """EtherCAT config"""
    vendor_id: str = Field(title="Vendor ID")
    group: str = Field(title="Group", default="U-Phy")

    _pdi_control: int = PrivateAttr(default=0x0e82)  # SPI EtherCAT Direct Mapped Mode
    _pdi_configuration: int = PrivateAttr(default=0x0681)
    _asic_config: int = PrivateAttr(default=0x4000)  # ERRLED enable
    _coe: int = PrivateAttr(default=(CoE.Sdo.value | CoE.SdoInfo.value))
    _foe: int = PrivateAttr(default=FoE.Enable.value)
    _mbox_control: int = PrivateAttr(default=(
        MBoxProtocol.CoE.value |
        MBoxProtocol.FoE.value
    ))
    _eeprom_size: int = PrivateAttr(512)  # bytes
    _boot_recv_mbox: MBox = PrivateAttr(default=MBox(
        offset=0x1000,
        size=512
    ))
    _boot_send_mbox: MBox = PrivateAttr(default=MBox(
        offset=0x1200,
        size=512
    ))
    _standard_recv_mbox: MBox = PrivateAttr(default=MBox(
        offset=0x1000,
        size=512
    ))
    _standard_send_mbox: MBox = PrivateAttr(default=MBox(
        offset=0x1200,
        size=512
    ))
    _fmmu: List[Fmmu] = PrivateAttr(default=[
        Fmmu.Outputs,
        Fmmu.Inputs,
        Fmmu.MBoxState,
    ])
    _sm: List[SM] = PrivateAttr(default=[
        SM(
            address=0x1000,
            length=512,
            control=0x26,
            status=0,
            enable=1,
            type=SMType.MBoxOut,
        ),
        SM(
            address=0x1200,
            length=512,
            control=0x22,
            status=0,
            enable=1,
            type=SMType.MBoxIn,
        ),
        SM(
            address=0x1400,
            length=0,
            control=0x64,
            status=0,
            enable=1,
            type=SMType.Outputs,
        ),
        SM(
            address=0x1A00,
            length=0,
            control=0x20,
            status=0,
            enable=1,
            type=SMType.Inputs,
        ),
    ])
