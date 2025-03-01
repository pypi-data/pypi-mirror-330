import logging
from pathlib import Path
import os
import re

import importlib.resources
from .. import templates
from jinja2 import Environment, PackageLoader, select_autoescape
from ..model.uphy import *
from datetime import date, datetime

_logger = logging.getLogger(__name__)

eip_type = {
    'UINT32': '0xC8',
    'UINT16': '0xC7',
    'UINT8': '0xC6',
    'INT32': '0xC4',
    'INT16': '0xC3',
    'INT8': '0xC2',
    'REAL32':'0xCA',
}

eip_bytelen = {
    'UINT32': 4,
    'UINT16': 2,
    'UINT8': 1,
    'INT32': 4,
    'INT16': 2,
    'INT8': 1,
    'REAL32': 4,
}

class EipAssemblyElement():
    def __init__(self, eds_ref, size_in_bytes : int):
        self.eds_ref = eds_ref
        self.size_in_bytes = size_in_bytes
        self.size_in_bits = size_in_bytes*8

class EipParam():
    id: int = 1
    objects = []

    def get_id():
        id = EipParam.id
        EipParam.id = EipParam.id + 1
        return id

    def reset():
        '''
        Reset class variables. Needed for automatic testing.
        '''
        EipParam.id = 1
        EipParam.objects = []

    def create_params(name = "None", signal = None,
                 data_type = None, value_min = "",
                 value_max = "", value_default = "0", description=""):
        '''
        Prefered method to create parameters.
        To handle array signals a list of parameters is returned.
        An array signal with length n generates n parameters. For scalar signals the length of the list will be 1.
        '''
        params = []

        if signal != None:
            if type(signal) == Signal:
                if signal.is_array:
                    for i in range(0, signal.array_length):
                        array_name = f'{name}[{i}]'
                        p = EipParam(array_name, signal.datatype, help = signal.description, model_ref=signal.id)
                        params.append(p)
                else:
                    p = EipParam(name, signal.datatype, help = signal.description, model_ref=signal.id)
                    params.append(p)
            elif type(signal) == Parameter:
                p = EipParam(name, signal.datatype, help = signal.description, model_ref=signal.id)
                params.append(p)
        else:
            p = EipParam(name, data_type, value_min, value_max, value_default, description)
            params.append(p)
        return params

    def __init__(self, name,
                 data_type = None, value_min = "",
                 value_max = "", value_default = "0", help="", model_ref=None):

        self.id: int = EipParam.get_id()
        self.eds_ref = f'Param{self.id}'
        self.name = name
        self.help = help
        self.model_ref = model_ref
        self.data_type = data_type
        self.value_min = value_min
        self.value_max = value_max
        self.value_default = value_default
        self.size = 0
        self.eds_data_type = eip_type[self.data_type]
        if self.data_type != None:
            self.size = eip_bytelen[self.data_type]
        self.descriptor = 0
        EipParam.objects.append(self)
        _logger.info(f'Create {self.eds_ref:12} {self.name:64} {self.data_type} {self.value_default}')

    def get_size(self):
        return self.size

    def to_eds_assembly_element(self):
        return EipAssemblyElement(self.eds_ref, self.get_size())

class EipAssembly():
    id: int = 100
    objects = []

    def get_id():
        id = EipAssembly.id
        EipAssembly.id = EipAssembly.id + 1
        return id

    def reset():
        '''
        Reset class variables. Needed for automatic testing.
        '''
        EipAssembly.id = 100
        EipAssembly.objects = []

    def remove_unused_assemblies():
        '''
        Remove assembly objects with size == 0 from the Assembly objects list
        This should only apply for input, output or config assemblies in the case
        of a device does not have inputs, outputs or configuration parameters
        Note that assemblies are only removes from the list, which is used to
        generate the AssemN objects in [Assembly] section.
        The assembly ids are still kept to create unique connection paths and
        to avoid special cases in the corresponding enip adapter code.
        '''
        EipAssembly.objects = [o for o in EipAssembly.objects if o.get_size() > 0]


    def __init__(self, name:str, signal_list: BaseSignal = None, param_prefix: str = None):
        '''
        Create assembly object. If a list of signal is passed as argument, then parameters
        are created for all signals in the list and the parameters are appended to the assembly.
        The param_prefix is used to create unique parameter names.
        '''
        self.id: int = EipAssembly.get_id()
        self.eds_ref = f'Assem{self.id}'
        EipAssembly.objects.append(self)
        self.name = name
        self.subelements = []

        _logger.info(f'Create {self.eds_ref:12} {self.name} (param prefix {param_prefix})')

        if signal_list != None:
            for signal in signal_list:
                if (param_prefix != None):
                    param_name = f'{param_prefix}.{signal.name}'
                    params = EipParam.create_params(name = param_name, signal=signal)
                else:
                    params = EipParam.create_params(signal=signal)

                for p in params:
                    self.append_element(p.to_eds_assembly_element())

    def get_size(self):
        size = 0
        for e in self.subelements:
            size = size + e.size_in_bytes
        return size

    def append_element(self, element: EipAssemblyElement):
        self.subelements.append(element)

    def to_eds_assembly_element(self):
        return EipAssemblyElement(self.eds_ref, self.get_size())

    def id_hex_str(self):
        return f'{self.id:0>2X}'


def assembly_elements_to_eds(elements):
    txt = '                ,,\n'
    for element in elements:
        txt = f"{txt}                {element.size_in_bits},{element.eds_ref},\n"

    txt = f"{txt[:-2]};" # replace final ',\n' with ';'
    return txt


# Use timestamp if available. If not, use current date
def get_date(date):
    if bool(date):
        return date
    else:
        return datetime.now().strftime("%m-%d-%Y")

# Use timestamp if available. If not, use current time
def get_time(time):
    if bool(time):
        return time
    else:
        return datetime.now().strftime("%H:%M:%S")

def enip_major_rev(rev_str):
    return rev_str.split('.')[0]

def enip_minor_rev(rev_str):
    return rev_str.split('.')[1]

class EthernetipGenerator:
    def __init__(self, model):
        self.model = model
        self.eds_file_name = f"{model.name}.eds"
        self.device = None
        self.connections = []               # Connections
        self.module_to_assembly_map = []
        self.rpi_param = None

        self.env = Environment(
            loader=PackageLoader("upgen"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

        self.env.filters['assembly_elements_to_eds'] = assembly_elements_to_eds
        self.env.filters['date'] = get_date
        self.env.filters['time'] = get_time
        self.env.filters['enip_major_rev'] = enip_major_rev
        self.env.filters['enip_minor_rev'] = enip_minor_rev

    def select_device(self, device_name):
        if device_name == None:
            self.device = self.model.devices[0]
        else:
            self.device = self.model.get_device(device_name)
        if self.device == None:
            raise Exception(f'{device_name} not found in model')

        self.eds_file_name = f"{self.device.name}.eds"

    def export_file(self):
        if Adapter.ETHERNETIP not in self.model.adapters:
            _logger.debug("EtherNet/IP is not enabled")
            return

        if not self.model.ethernetip:
            _logger.warn('Model does not include a valid EtherNet/IP configuration')
            return

        _logger.info('Generate eds file')
        eds = self.generate_eds()

        _logger.info(f"Save EDS file: {str(Path(os.getcwd()) / self.eds_file_name)}")
        with open(self.eds_file_name, 'w') as file:
            file.write(eds)

    def create_connection_dict(self, eds_ref, name, trigger_and_transport, connection_parameters, help, rpi_param, input_assembly, output_assembly, config_assembly,path):
        connection = {
            'eds_ref' : eds_ref,
            'name' : name,
            'trigger_and_transport' : trigger_and_transport,
            'connection_parameters' : connection_parameters,
            'help' : help,
            'input_rpi_param' : rpi_param.eds_ref,
            'input_size' : input_assembly.get_size(),
            'input_format' : input_assembly.eds_ref,
            'output_rpi_param' : rpi_param.eds_ref,
            'output_size' : output_assembly.get_size(),
            'output_format' : output_assembly.eds_ref,
            'config_size' : config_assembly.get_size(),
            'config_format' : config_assembly.eds_ref,
            'path': path
        }

        if connection['input_size'] == 0:
            connection['input_format'] = ""
        if connection['output_size'] == 0:
            connection['output_format'] = ""
        if connection['config_size'] == 0:
            connection['config_format'] = ""

        return connection

    def create_connections(self):
        '''
        Generate connection objects from the device properties according to
        the table below:

        Device type         Exclusive Owner     Listen Only     Input Only
        ------------------------------------------------------------------
        inputs + outputs    Yes                 Yes             Yes
        inputs only         No                  Yes             Yes
        outputs only        Yes                 No              No
        '''
        connection_id = 0

        if self.output_assembly.get_size() > 0:
            connection_id = connection_id + 1
            connection = self.create_connection_dict(
                f'Connection{connection_id}',
                'Point to point',
                '0x84010002','0x44640405',
                '',
                self.rpi_param, self.input_assembly, self.output_assembly, self.config_assembly,
                f'20 04 24 {self.config_assembly.id_hex_str()} 2C {self.output_assembly.id_hex_str()} 2C {self.input_assembly.id_hex_str()}')
            self.connections.append(connection)

        if self.input_assembly.get_size() > 0:
            connection_id = connection_id + 1
            connection = self.create_connection_dict(
                f'Connection{connection_id}',
                'Input Only',
                '0x02030002','0x44640305',
                '',
                self.rpi_param, self.input_assembly, self.input_only_hb_assembly, self.config_assembly,
                f'20 04 24 {self.config_assembly.id_hex_str()} 2C {self.input_only_hb_assembly.id_hex_str()} 2C {self.input_assembly.id_hex_str()}')
            self.connections.append(connection)

        if self.input_assembly.get_size() > 0:
            connection_id = connection_id + 1
            connection = self.create_connection_dict(
                f'Connection{connection_id}',
                'Listen Only',
                '0x01030002','0x44640305',
                '',
                self.rpi_param, self.input_assembly, self.listen_only_hb_assembly, self.config_assembly,
                f'20 04 24 {self.config_assembly.id_hex_str()} 2C {self.listen_only_hb_assembly.id_hex_str()} 2C {self.input_assembly.id_hex_str()}')
            self.connections.append(connection)

    def generate_eds_mapping(self):
        EipAssembly.reset()
        EipParam.reset()

        # Generate input, output and config assemblies matching the
        # modules plugged into slots
        self.input_assembly = EipAssembly('Input Assembly')
        self.output_assembly = EipAssembly('Output Assembly')
        self.config_assembly = EipAssembly('Config Assembly')
        self.input_only_hb_assembly = EipAssembly('Input Only Heartbeat Assembly')
        self.listen_only_hb_assembly = EipAssembly('Listen Only Heartbeat Assembly')

        for slot in self.device.slots:
            module = self.model.get_module(slot.module)
            if len(module.inputs) > 0:
                input_asm  = EipAssembly(f'{slot.name} inputs', module.inputs, param_prefix=slot.name)
                self.input_assembly.subelements.append(input_asm.to_eds_assembly_element())
            if len(module.outputs) > 0:
                output_asm = EipAssembly(f'{slot.name} outputs', module.outputs, param_prefix=slot.name)
                self.output_assembly.subelements.append(output_asm.to_eds_assembly_element())
            if len(module.parameters) > 0:
                config_asm = EipAssembly(f'{slot.name} config', module.parameters, param_prefix=slot.name)
                self.config_assembly.subelements.append(config_asm.to_eds_assembly_element())

        # Create RPI parameter, referenced in the connection objects
        self.rpi_param = EipParam.create_params('RPI', data_type='UINT32',
                                  value_min = str(self.device.ethernetip.min_data_interval),
                                  value_default = str(self.device.ethernetip.default_data_interval))[0]

        self.create_connections()

        EipAssembly.remove_unused_assemblies()

    def generate_eds(self):
        template = self.env.get_template("template.eds")
        self.generate_eds_mapping()
        eds = template.render(
            model=self.model,
            device=self.device,
            params=EipParam.objects,
            assemblies=EipAssembly.objects,
            connections=self.connections)

        _logger.debug(eds)
        return eds
