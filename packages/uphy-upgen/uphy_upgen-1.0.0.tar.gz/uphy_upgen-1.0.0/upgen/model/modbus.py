from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, validator

HelpText = {
    "ModbusDevice":
    {
        "port": "TCP port.",
    },
}

def hex_uint16(value):
    return f'0x{int(value,0):04x}'
class ModbusDevice(BaseModel):
    port: str = Field(title = "Port", default="502", description=HelpText["ModbusDevice"]["port"])

    @validator('port')
    def hex16(cls, v):
        return hex_uint16(v)

class ModbusRoot(BaseModel):
    pass

