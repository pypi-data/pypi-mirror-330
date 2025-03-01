from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator


HelpText = {
    "ProfinetParameter": {
        "index": "Parameter index used by PLC to address the parameter"
    },
    "ProfinetModule": {
        "module_id": "Module Id. Used by PLC to address the module. ",
        "submodule_id": "Submodule Id. U-Phy implements one submodule per module"
    },
    "ProfinetDevice": {
        "dap_module_id": "Device Access Point module identity number",
        "dap_identity_submodule_id": "No help text available",
        "dap_interface_submodule_id": "No help text available",
        "dap_port_1_submodule_id": "No help text available",
        "dap_port_2_submodule_id": "No help text available",
        "profile_id": "No help text available",
        "profile_specific_type": "No help text available",
        "min_device_interval": "Minimum time interval for sending cyclic IO data. Supported values [32,64,128,256]. Profinet time base is 1/32 ms and 32 gives a send interval of 1ms.",
        "default_stationname": "Name used detect and configure the device using Profinet engineering tools (Discovery and Configuration Protocol)",
        "order_id": "Device order information",
        "hw_revision": "No help text available",
        "sw_revision_prefix": "No help text available",
        "sw_revision_functional_enhancement": "No help text available",
        "sw_revision_bug_fix": "No help text available",
        "sw_revision_internal_change": "No help text available",
        "revision_counter": "No help text available",
        "main_family": "Functional class. For example I/O, Sensor or Gateway",
        "product_family": "Vendor defined product family. Used by engineering tool to generate a catalog hiararchy."
    },
    "ProfinetRoot": {
        "vendor_id": "Vendor identity assigned by PI organization",
        "device_id": "Device identity. Common to all devices in the model. The DAP Module ID is used to identify devices within model."
    }
}


class MainFamilyType(str, Enum):
    """Type of functionaliy. Used by engineering tool to group devices"""
    GENERAL = 'General'
    DRIVES = 'Drives'
    SWITCHING_DEVICES = 'Switching Devices'
    IO = 'I/O'
    VALVES = 'Valves'
    CONTROLLERS = 'Controllers'
    HMI = 'HMI'
    ENCODERS = 'Encoders'
    NC_RC = 'NC/RC'
    GATEWAY = 'Gateway'
    PLCS = 'PLCs'
    IDENT_SYSTEMS = 'Ident Systems'
    PA_PROFILES = 'PA Profiles'
    NETWORK_COMPONENTS = 'Network Components'
    SENSORS = 'Sensors'

    def __str__(self):
        return self.value

def hex_uint32(value):
    return f'0x{int(value,0):08x}'

def hex_uint16(value):
    return f'0x{int(value,0):04x}'

class ProfinetParameter(BaseModel):
    """Profinet specific parameter configuration"""
    index: str = Field(title="Parameter index", default="")

class ProfinetModule(BaseModel):
    """Profinet specific module configuration"""
    module_id: Optional[str] = Field(title="Module ID", default="")
    submodule_id: Optional[str] = Field(title="Submodule ID", default="")

    @validator('module_id', 'submodule_id')
    def hex32(cls, v):
        if not v:
            return ""
        return hex_uint32(v)

    def generate_mapping(self, module, module_ix):
        module_id = (module_ix + 1) * 0x100

        if not self.module_id:
            self.module_id = f"{module_id:#x}"

        if not self.submodule_id:
            self.submodule_id = f"{module_id + 1:#x}"

        for ix, parameter in enumerate(module.parameters):
            if not parameter.profinet:
                parameter.profinet = ProfinetParameter(
                    index = f"{ix + 0x100:#x}"
                )

class ProfinetDevice(BaseModel):
    """Profinet specific device configuration"""
    dap_module_id: str = Field(title="DAP Module ID", default="1", description=HelpText['ProfinetDevice']['dap_module_id'])
    dap_identity_submodule_id: str = Field(title="DAP Identity Submodule ID", default="0x00000001", description=HelpText['ProfinetDevice']['dap_identity_submodule_id'])
    dap_interface_submodule_id: str = Field(title="DAP Interface Submodule ID", default="0x00008000", description=HelpText['ProfinetDevice']['dap_interface_submodule_id'])
    dap_port_1_submodule_id: str = Field(title="DAP Port 1 Submodule ID", default="0x00008001", description=HelpText['ProfinetDevice']['dap_port_1_submodule_id'])
    dap_port_2_submodule_id: str = Field(title="DAP Port 2 Submodule ID", default="0x00008002", description=HelpText['ProfinetDevice']['dap_port_2_submodule_id'])

    @validator('dap_module_id', 'dap_identity_submodule_id', 'dap_interface_submodule_id', 'dap_port_2_submodule_id' )
    def hex32(cls, v):
        return hex_uint32(v)

    @validator('profile_id','profile_specific_type', )
    def hex16(cls, v):
        return hex_uint16(v)

    profile_id: str = Field(title="Profile ID", default="0", description=HelpText['ProfinetDevice']['profile_id'])
    profile_specific_type: str = Field(title="Profile specific type", default="0", description=HelpText['ProfinetDevice']['profile_specific_type'])
    min_device_interval: str = Field(title="Min device interval", default="32", description=HelpText['ProfinetDevice']['min_device_interval'])
    default_stationname: str = Field(title="Default station name", description=HelpText['ProfinetDevice']['default_stationname'])
    order_id: str = Field(title="Order ID", description=HelpText['ProfinetDevice']['order_id'])
    hw_revision: str = Field(title="Hardware revision", default="0", description=HelpText['ProfinetDevice']['hw_revision'])
    sw_revision_prefix: str = Field(title="Software revision prefix", default="V", description=HelpText['ProfinetDevice']['sw_revision_prefix'])
    sw_revision_functional_enhancement: str = Field(title="Software revision functional enhancement", default="0", description=HelpText['ProfinetDevice']['sw_revision_functional_enhancement'])
    sw_revision_bug_fix: str = Field(title="Software revision bug fix", default="0", description=HelpText['ProfinetDevice']['sw_revision_bug_fix'])
    sw_revision_internal_change: str = Field(title="Software revision internal change", default="0", description=HelpText['ProfinetDevice']['sw_revision_internal_change'])
    revision_counter: str = Field(title="Revision counter", default="0", description=HelpText['ProfinetDevice']['revision_counter'])
    main_family: MainFamilyType = Field(title="Main family", default=MainFamilyType.IO, description=HelpText['ProfinetDevice']['main_family'])
    product_family: str = Field(title="Product family", description=HelpText['ProfinetDevice']['product_family'])

class ProfinetRoot(BaseModel):
    """Profinet config"""
    vendor_id: str = Field(title="Vendor ID", description=HelpText['ProfinetRoot']['vendor_id'])
    device_id: str = Field(title="Device Family ID", description=HelpText['ProfinetRoot']['device_id'])

    @validator('vendor_id', 'device_id')
    def hex16(cls, v):
        return hex_uint16(v)
