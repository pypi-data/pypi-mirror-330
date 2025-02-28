from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator

HelpText = {
    "EthernetipRoot": {
        "vendor_id": "Vendor id assigned by ODVA organization"
    },
    "EthernetipDevice": {
        "revision": "Device revision in format major.minor . Increment major revision if device’s logical interface changes. Increment minor revision if behavior on network changes",
        "product_code": "Product code, defined by vendor",
        "device_type": "Type of device. If uncertain, use 43 (Generic Device)",
        "device_type_str": "Type of device. If uncertain, use Generic Device",
        "home_url": "URL for company or product",
        "create_date": "EDS file creation date. If string is empty current date will be used.",
        "create_time": "EDS file creation time. If string is empty current time will be used.",
        "modification_date" : "EDS file modification date. If string is empty current date will be used.",
        "modification_time": "EDS file modification time. If string is empty current time will be used.",
        "min_data_interval": "Fastest datarate supported by device, time in micro seconds",
        "default_data_interval": "Default datarate for device, time in micro seconds"
    }
}

class EthernetipDevice(BaseModel):
    revision: str = Field(title="Revision", default="1.1", description=HelpText['EthernetipDevice']['revision'])
    product_code: str = Field(title="Product Code", description=HelpText['EthernetipDevice']['product_code'])
    device_type: str = Field(title="Device Type", default="43", description=HelpText['EthernetipDevice']['device_type'])
    device_type_str: str = Field(title="Device Type String", default="Generic Device", description=HelpText['EthernetipDevice']['device_type_str'])
    home_url:str = Field(title="Home URL", default="https://rt-labs.com/u-phy/", description=HelpText['EthernetipDevice']['home_url'])
    create_date:Optional[str] = Field(title="EDS File Creation Date", description=HelpText['EthernetipDevice']['create_date'])
    create_time:Optional[str] = Field(title="EDS File Creation Time", description=HelpText['EthernetipDevice']['create_time'])
    modification_date:Optional[str] = Field(title="EDS File Modification Date", description=HelpText['EthernetipDevice']['modification_date'])
    modification_time:Optional[str] = Field(title="EDS File Modification Time", description=HelpText['EthernetipDevice']['modification_time'])
    min_data_interval: str = Field(title="RPI Min - Minimal cyclic data period (in microseconds)", default="4000", description=HelpText['EthernetipDevice']['min_data_interval'])
    default_data_interval: str = Field(title="RPI Default - Default cyclic data period (in microseconds)", default="10000",description=HelpText['EthernetipDevice']['default_data_interval'])

class EthernetipRoot(BaseModel):
    vendor_id: str = Field(title="Vendor Id", default="1772", description=HelpText['EthernetipRoot']['vendor_id'])
