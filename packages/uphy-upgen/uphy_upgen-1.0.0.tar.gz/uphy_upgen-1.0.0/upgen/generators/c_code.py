import logging
import re
import json
import importlib.resources
from .. import templates
from jinja2 import Environment, PackageLoader, select_autoescape
from ..model.uphy import *

_logger = logging.getLogger(__name__)


def c_type(value):
    map = {
        DataType.UINT32: 'uint32_t',
        DataType.UINT16: 'uint16_t',
        DataType.UINT8: 'uint8_t',
        DataType.INT32: 'int32_t',
        DataType.INT16: 'int16_t',
        DataType.INT8: 'int8_t',
        DataType.REAL32: 'float',
    }
    return map[value.datatype]

class CNameContext():
    """
    Defines scopes for identifiers:
    - Slots
        - Signals/Parameters (per slot)
    - Modules
    - Alarms
    """
    class Scope(Enum):
        NONE = 0,
        SLOT = 1,
        SIGNAL = 2,
        MODULE = 3,
        ALARM = 4,
        TXPDO = 5,
        RXPDO = 6

    def __init__(self, slot=""):
        self.slot = slot
        self.scope = self.Scope.NONE
        self.ctx = {
            self.Scope.SLOT: {},    # (name, index)
            self.Scope.SIGNAL: {},  # {slot_index: (name, index)}
            self.Scope.MODULE: {},  # (name, index)
            self.Scope.ALARM: {},   # (name, index)
            self.Scope.TXPDO: {},   # (name, index)
            self.Scope.RXPDO: {},   # (name, index)
        }

    def _get_ctx(self):
        assert self.ctx != self.Scope.NONE

        if self.Scope == self.Scope.SIGNAL:
            assert self.slot != ""
            if self.slot not in self.ctx[self.scope]:
                self.ctx[self.scope][self.slot] = {}

            ctx = self.ctx[self.scope][self.slot]
        else:
            ctx = self.ctx[self.scope]

        return ctx

    def name_available(self, name, index):
        ctx = self._get_ctx()

        for other_index, other_name in ctx.items():
            if name == other_name and index != other_index:
                _logger.debug(f"[{self.scope}] name collision: {name}, '{index}' '{other_index}'")
                return False

        return True

    def set_name(self, name, index):
        ctx = self._get_ctx()
        ctx[index] = name

    def get_name(self, index):
        ctx = self._get_ctx()
        return ctx.get(index, None)

    def index_exists(self, index):
        ctx = self._get_ctx()
        return index in ctx

    def new_unique_name(self, name, index):
        if self.index_exists(index):
            name = self.get_name(index)
        else:
            while not self.name_available(name, index):
                name += "_" + str(index)

            # Store name for future calls
            self.set_name(name, index)

            _logger.debug(f"c_name: {name} allocated to index '{index}'")

        return name

def c_name(value, index, ctx, scope):
    """
    Filter for C names. An index should be included to avoid duplicate
    names and ensure consistency across repeated calls. For example:
        {{slot | c_name(loop.index0, ctx, ctx.Scope.SLOT)}}
        {{signal | c_name("in_" ~ loop.index0, ctx, ctx.Scope.SIGNAL)}}

    Valid scopes are defined by the enum ctx.Scope (except NONE):
    - ctx.Scope.SLOT
        - ctx.Scope.SIGNAL (NOTE: requires previous call with scope SLOT)
    - ctx.Scope.MODULE
    - ctx.Scope.ALARM
    - ctx.Scope.TXPDO
    - ctx.Scope.RXPDO

    Note that the SIGNAL scope is shared by inputs, outputs and parameters.
    """
    name = value.name
    if re.search("^[0-9].*", name):           # Escape leading numeral
        name = f"_{name}"

    name = re.sub("[^0-9A-Za-z_]", "_", name) # Replace special chars
    name = re.sub("_+", "_", name)            # Contract repeating underscore
    if name != "_":
        name = re.sub("_$", "", name)         # Strip trailing underscore

    # Set scope
    ctx.scope = scope
    if scope == ctx.Scope.SLOT:
        ctx.slot = index                      # Define signal scope

    name = ctx.new_unique_name(name, index)   # Ensure name is unique

    return name


def c_name_upper(value, index, ctx, scope):
    """Filter for uppercase C names. For example defines."""
    return c_name(value, index, ctx, scope).upper()


def c_hex(value):
    return value.replace('#', '0')

def c_array(signal):
    if not signal.is_array:
        return ""
    else:
        return f"[{signal.array_length}]"

def c_flags(signal):
    if not signal.is_array:
        return "0"
    else:
        return "UP_SIG_FLAG_IS_ARRAY"

def c_bool(value):
    if value:
        return "true"
    else:
        return "false"

# str.__repr__ never escapes double quotes:
# - print(("\"").__repr__())        => '"'
# - print(("\"" + '\'').__repr__()) => '\'"'
# Backslashes also need to appear escaped when output.
def c_string(s):
    if s:
        s = s.replace("\\", "\\\\")
        s = s.replace('"', r'\"')
    return s

# str.__repr__ only escapes single quotes if there is also a
# double quote in the string:
# - print(('\'').__repr__())        => "'"
# - print(("\"" + '\'').__repr__()) => '\'"'
# For C chars an extra backslash therefore needs to be added.
def c_char(s):
    if s:
        s = s.replace("'", r"\'")
    return s

def enip_major_rev(rev_str):
    return rev_str.split('.')[0]

def enip_minor_rev(rev_str):
    return rev_str.split('.')[1]

class CCodeGenerator:
    def __init__(self, model):
        self.model = model
        self.device = None
        self.name_ctx = CNameContext()

        self.env = Environment(
            loader=PackageLoader("upgen"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters['c_type'] = c_type
        self.env.filters['c_name'] = c_name
        self.env.filters['c_hex'] = c_hex
        self.env.filters['c_name_upper'] = c_name_upper
        self.env.filters['c_array'] = c_array
        self.env.filters['c_flags'] = c_flags
        self.env.filters['c_bool'] = c_bool
        self.env.filters['c_string'] = c_string
        self.env.filters['c_char'] = c_char
        self.env.filters['enip_major_rev'] = enip_major_rev
        self.env.filters['enip_minor_rev'] = enip_minor_rev
        self.env.globals['ctx'] = self.name_ctx

    def select_device(self, device_name):
        if device_name == None:
            self.device = self.model.devices[0]
        else:
            self.device = self.model.get_device(device_name)

        if self.device == None:
            raise Exception(f'{device_name} not found in model')

    def export_file(self):
        _logger.info('Generate model.h')
        header = self.generate_header_file()
        _logger.info('Generate model.c')
        source = self.generate_source_file()

        with open('model.h', 'w') as file:
            file.write(header)

        with open('model.c', 'w') as file:
            file.write(source)

    def generate_header_file(self):
        template = self.env.get_template("model_template.h")
        code = template.render(model=self.model, device=self.device)
        _logger.debug(code)
        return code

    def generate_source_file(self):
        template = self.env.get_template("model_template.c")
        code = template.render(model=self.model, device=self.device)
        _logger.debug(code)
        return code
