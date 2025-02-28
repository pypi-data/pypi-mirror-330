"""Runtime model representing the plugged state of the device."""

from .uphy import Signal, Parameter
from typing import Optional, List
from pydantic import BaseModel


class Signal(Signal):
    """Signal datatype."""

    description: Optional[str]
    id: Optional[str]


class Parameter(Parameter):
    """Parameter datatype."""

    description: Optional[str]
    id: Optional[str]


class Slot(BaseModel):
    """Slot datatype."""

    name: str
    inputs: List[Signal]
    outputs: List[Signal]
    parameters: List[Parameter]


class Device(BaseModel):
    """Device datatype."""

    name: str
    slots: List[Slot]


class Root(BaseModel):
    """Root datatype."""

    device: Device
