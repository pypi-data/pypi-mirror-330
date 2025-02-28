import logging
from pathlib import Path
from xmlschema import XMLSchema, etree_tostring
import xml.etree.ElementTree as ET
import json
from . import SCHEMA_DIR
import importlib.resources
from .. import templates
from copy import deepcopy
import os

from ..model import Adapter

xs = XMLSchema(Path(SCHEMA_DIR, 'GSDML/GSDML-DeviceProfile-v2.44.xsd'))

_logger = logging.getLogger(__name__)

pn_type = {
    'UINT32': 'Unsigned32',
    'UINT16': 'Unsigned16',
    'UINT8' : 'Unsigned8',
    'INT32' : 'Integer32',
    'INT16' : 'Integer16',
    'INT8'  : 'Integer8',
    'REAL32': 'Float32'
}

class ProfinetGenerator:
    def __init__(self, model):
        self.model = model

    def import_file(self, file):
        raise Exception('Import not supported ')

    def export_file(self):
        '''Generate GSDML file by applying configuration in a U-Phy model to a template file'''

        if Adapter.PROFINET not in self.model.adapters:
            _logger.debug("Profinet is not enabled")
            return

        if not self.model.profinet:
            _logger.warn('Model does not include a valid profinet configuration')
            return

        self.gsdml_template_name = 'GSDML-V2.44-RT-Labs-U-Phy-Template.xml'
        self.gsdml_file_name = 'GSDML-V2.44-VENDOR-DEVICE-YYYYMMDD.xml'

        ET.register_namespace('', 'http://www.profibus.com/GSDML/2003/11/DeviceProfile')

        gsdml_template_xml = importlib.resources.read_text(templates, self.gsdml_template_name, encoding = "iso-8859-1")

        _logger.info('Generate Profinet GSDML ')
        _logger.info(f"Template: {self.gsdml_template_name}")
        _logger.info(f"Model name: {self.model.name}")

        gsdml_template = xs.to_dict(gsdml_template_xml)

        _logger.info('Apply model data to template')
        gsdml = self.model_to_gsdml(gsdml_template, self.model)

        _logger.debug('Generated gsdml in json format')
        _logger.debug(json.dumps(gsdml, indent=3))

        # Tip: When refactoring code it is useful to temporarily check in
        # a 'gsdml.json' file and compare this with the current output.
        # Enable lines below to write the gsdml json dump to file.
        #file = open('gsdml.json', 'w')
        #file.write(json.dumps(gsdml, indent=3))
        #file.close()

        _logger.info('Convert to xml')
        gsdml_xml = xs.encode(gsdml, encoding = 'iso-8859-1')

        _logger.info('Remove unused attributes to pass gsdml checker')
        all_nodes = gsdml_xml.findall('.//*')
        for node in all_nodes:
            node.attrib.pop('F_IO_StructureDescVersion', None)
            node.attrib.pop('F_IO_StructureDescCRC', None)
            node.attrib.pop('PowerBudgetControlSupported', None)
            node.attrib.pop('BitLength', None)

        _logger.info('Remove RequiredSchemaVersion attribute from ModuleItem nodes')
        module_nodes = gsdml_xml.findall('.//{http://www.profibus.com/GSDML/2003/11/DeviceProfile}ModuleItem')
        for node in module_nodes:
            node.attrib.pop('RequiredSchemaVersion')

        _logger.debug(etree_tostring(gsdml_xml))
        _logger.info(f"Save xml: {str(Path(os.getcwd()) / self.gsdml_file_name)}")
        ET.ElementTree(gsdml_xml).write(self.gsdml_file_name, encoding = 'iso-8859-1')

    def gsdml_to_model(self, gsdml):
        return None

    def model_to_gsdml(self, gsdml_template, up_model):
        return GsdmlGenerator(gsdml_template, up_model).run()

class GsdmlGenerator:
    '''
    Generator for converting a U-Phy model to a gsdml file.

    The generation relies on a template that defines most characteristics.
    GSDML template and and U-Phy device model in dict / json format.
    Limitations:
    - Only one device in model is supported
    - Only characteristics defined by model updated, other characteristics needs to be changed in template, for example
      for a device with other port characteristics.
    - TBD - extend model to cover everything?
    '''
    def __init__(self, gsdml_template, model):
        # Do not update the template but create a working copy
        self.gsdml = deepcopy(gsdml_template)
        self.up_model = model

        # List of TextId objects which is extended during generation
        self.text_list = self.gsdml['ProfileBody']['ApplicationProcess']['ExternalTextList']['PrimaryLanguage']

    def run(self):
        self.gsdml['ProfileBody'] = self.profile_body()
        self.cleanup()
        return self.gsdml

    def profile_body(self):
        up_dev = self.up_model.devices[0]
        profile_body = {
            'DeviceIdentity': {
                '@VendorID': self.up_model.profinet.vendor_id,
                '@DeviceID': self.up_model.profinet.device_id,
                'InfoText': { '@TextId' : self.create_text_id('INFO_DEV', up_dev.description) },
                'VendorName': {'@Value': self.up_model.vendor}
            },
            'DeviceFunction': {
                'Family': {
                    '@MainFamily':  up_dev.profinet.main_family,
                    '@ProductFamily': up_dev.profinet.product_family
                }
            },
            'ApplicationProcess': self.application_process()
        }

        return profile_body

    def application_process(self):
        ap = {}
        ap['DeviceAccessPointList'] = self.device_access_point_list()
        ap['ModuleList'] = self.module_list()
        if self.up_model.devices[0].has_alarms(self.up_model):
            ap['ChannelDiagList'] = self.diagnosis_list()
        ap['ExternalTextList'] = { "PrimaryLanguage": self.text_list }
        return ap

    def device_access_point_list(self):
        dap_list = {
            'DeviceAccessPointItem': []
        }
        for up_dev in self.up_model.devices:
            ix = self.up_model.devices.index(up_dev) + 1
            dap_item = deepcopy(self.gsdml['ProfileBody']['ApplicationProcess']['DeviceAccessPointList']['DeviceAccessPointItem'][0])

            dap_item['@ID'] = f'IDD_{ix}'
            dap_item['@DNS_CompatibleName'] = up_dev.profinet.default_stationname
            dap_item['@ModuleIdentNumber'] = up_dev.profinet.dap_module_id
            dap_item['ModuleInfo'] = self.dap_module_info(up_dev, ix)
            dap_item['UseableModules']['ModuleItemRef'] = self.useable_modules_list(up_dev)
            dap_item['VirtualSubmoduleList']['VirtualSubmoduleItem'][0]["@ID"] = f'IDS_{ix}'
            dap_item['VirtualSubmoduleList']['VirtualSubmoduleItem'][0]["@SubmoduleIdentNumber"] = (
                up_dev.profinet.dap_identity_submodule_id)

            dap_item['VirtualSubmoduleList']['VirtualSubmoduleItem'][0]['ModuleInfo'] = {
                'Name': { "@TextId": f'IDT_DAP_{ix}_NAME' },
                'InfoText': { "@TextId": f'IDT_DAP_{ix}_INFO' }
            }
            dap_item['SystemDefinedSubmoduleList']['InterfaceSubmoduleItem']["@ID"] = f'IDS_{ix}_I'
            dap_item['SystemDefinedSubmoduleList']['InterfaceSubmoduleItem']["@SubmoduleIdentNumber"] = (
            up_dev.profinet.dap_interface_submodule_id)
            dap_item['SystemDefinedSubmoduleList']['PortSubmoduleItem'][0]["@ID"] = f'IDS_{ix}_P1'
            dap_item['SystemDefinedSubmoduleList']['PortSubmoduleItem'][0]["@SubmoduleIdentNumber"] = (
                up_dev.profinet.dap_port_1_submodule_id)
            if up_dev.nbr_of_ports == 2:
                dap_item['SystemDefinedSubmoduleList']['PortSubmoduleItem'][1]["@ID"] = f'IDS_{ix}_P2'
                dap_item['SystemDefinedSubmoduleList']['PortSubmoduleItem'][1]["@SubmoduleIdentNumber"] = (
                up_dev.profinet.dap_port_2_submodule_id)
            else:
                self.remove_text_id('IDT_NAME_PS2')
                del dap_item['SystemDefinedSubmoduleList']['PortSubmoduleItem'][1]

            dap_list['DeviceAccessPointItem'].append(dap_item)
        return dap_list

    def useable_modules_list(self, up_dev):
        ul = []
        pn_slot = 1
        plug_type = '@FixedInSlots'

        for slot in up_dev.slots:
            added = False
            module = self.up_model.get_module(slot.module)
            useable_module = self.create_useable_module(module, pn_slot, plug_type)
            for um in ul:
                if um['@ModuleItemTarget'] == useable_module['@ModuleItemTarget']:
                    um[plug_type] += f" {str(pn_slot)}"
                    added = True

            if not added:
                ul.append(useable_module)

            pn_slot = pn_slot + 1
        return ul

    def dap_module_info(self, up_dev, ix):
        module_info = {
            'Name': {'@TextId': self.create_text_id(f'DAP_{ix}_NAME', up_dev.name)},
            'InfoText': {'@TextId': self.create_text_id(f'DAP_{ix}_INFO', up_dev.description)},
            'VendorName': {'@Value': self.up_model.vendor},
            'OrderNumber': {'@Value': up_dev.profinet.order_id},
            'HardwareRelease': {'@Value': up_dev.hardware_release},
            'SoftwareRelease': {'@Value': up_dev.software_release}
        }
        return module_info

    def create_text_id(self, id, value):
        text_item = {
            '@TextId': f"IDT_{id.strip().replace(' ', '_')}",
            '@Value' : value
        }
        self.text_list['Text'].append(text_item)
        return text_item['@TextId']

    def create_useable_module(self, up_module, pn_slot, plug_type):
        module_item_ref = {}
        module_item_ref['@ModuleItemTarget'] = f"IDM_{up_module.profinet.module_id}"
        module_item_ref[plug_type] = str(pn_slot)
        return module_item_ref

    def module_list(self):
        mod_list = {
            'ModuleItem': []
        }
        for module in self.up_model.modules:
            mod_list['ModuleItem'].append(self.create_module_item(module))

        return mod_list

    def create_module_item(self, up_module):
        module_item = {
            '@ID': f"IDM_{up_module.profinet.module_id}",
            '@ModuleIdentNumber': up_module.profinet.module_id,
            'ModuleInfo': {
                'Name': {
                    '@TextId': self.create_text_id(f"MOD_NAME_{up_module.profinet.module_id}", up_module.name)},
                'InfoText': {
                    '@TextId': self.create_text_id(f"MOD_INFO_{up_module.profinet.module_id}", up_module.description)
                }
            },
            'VirtualSubmoduleList': {
                'VirtualSubmoduleItem': [
                    self.create_virtual_sub_module_item(up_module)
                ]
            }
        }

        return module_item

    def diagnosis_list(self):
        diag_list = {
            'ChannelDiagItem': []
        }
        for module in self.up_model.modules:
            for alarm in module.alarms:
                diag_list['ChannelDiagItem'].append(self.create_diag_item(alarm))
        return diag_list

    def create_diag_item(self, alarm):
        diag_item = {
            '@ErrorType': int(alarm.error_code, 0),
            '@MaintenanceAlarmState':"D;MR;MD",
            'Name': { '@TextId': self.create_text_id(f"DIAG_{str(int(alarm.error_code, 0))}", alarm.message) }
        }
        return diag_item

    def create_virtual_sub_module_item(self, up_module):
        item = {
            '@ID': f"IDSM_{up_module.profinet.submodule_id}",
            '@SubmoduleIdentNumber': up_module.profinet.submodule_id,
            '@MayIssueProcessAlarm': False,
            '@API': 0,
            'IOData': self.create_io_data(up_module),
        }

        if len(up_module.parameters) > 0:
            item['RecordDataList'] = self.create_record_data_list(up_module)

        item['ModuleInfo'] = {
            'Name': {'@TextId': self.create_text_id(f"SUBMOD_NAME_{up_module.profinet.submodule_id}", up_module.name) },
            'InfoText': { '@TextId': self.create_text_id(f"SUBMOD_INFO_{up_module.profinet.submodule_id}", up_module.description) }
        }

        return item

    def create_io_data(self, up_module):
        io_data = {}
        if len(up_module.inputs) > 0:
            io_data['Input'] = {}
            io_data['Input']['DataItem'] = []
            for signal in up_module.inputs:
                if not signal.is_array:
                    data_item = {
                        '@DataType': pn_type[signal.datatype],
                        '@TextId': self.create_text_id(f"{up_module.name}_IN_{signal.name}", signal.name),
                        '@UseAsBits': False,
                        '@Subordinate': False
                    }
                    io_data['Input']['DataItem'].append(data_item)
                else:
                    for i in range(0, signal.array_length):
                        data_item = {
                            '@DataType': pn_type[signal.datatype],
                            '@TextId': self.create_text_id(f"{up_module.name}_IN_{signal.name}[{str(i)}]", f"{signal.name} [{str(i)}]"),
                            '@UseAsBits': False,
                            '@Subordinate': False
                        }
                        io_data['Input']['DataItem'].append(data_item)

        if len(up_module.outputs) > 0:
            io_data['Output'] = {}
            io_data['Output']['DataItem'] = []

            for signal in up_module.outputs:
                if not signal.is_array:
                    data_item = {
                        '@DataType': pn_type[signal.datatype],
                        '@TextId': self.create_text_id(f"{up_module.name}_OUT_{signal.name}", signal.name),
                        '@UseAsBits': False,
                        '@Subordinate': False
                    }
                    io_data['Output']['DataItem'].append(data_item)
                else:
                    for i in range(0, signal.array_length):
                        data_item = {
                            '@DataType': pn_type[signal.datatype],
                            '@TextId': self.create_text_id(f"{up_module.name}_OUT_{signal.name}[{str(i)}]", f"{signal.name} [{str(i)}]"),
                            '@UseAsBits': False,
                            '@Subordinate': False
                        }
                        io_data['Output']['DataItem'].append(data_item)


        return io_data

    def create_record_data_list(self, up_module):
        rec_list = []
        for par in up_module.parameters:
            rec_item = {
                '@Index': int(par.profinet.index, 0),
                '@Length': par.bitlen // 8,
                'Name': {
                    '@TextId': self.create_text_id(f"REC_NAME_{par.name}", par.name)
                },
                'Ref': {
                    '@DataType': pn_type[par.datatype],
                    '@DefaultValue': par.default,
                    '@ByteOffset': 0 ,
                    '@TextId': self.create_text_id(f"REC_INFO_{par.name}", par.description)
                }
            }
            if par.min is not None and par.max is not None:
                rec_item['Ref']['@AllowedValues'] = f"{par.min}..{par.max}"
            rec_list.append(rec_item)

        return {'ParameterRecordDataItem': rec_list }


    def cleanup(self):
        ''' Remove unused TextId from original template '''
        self. remove_text_id('IDT_DUMMY')

    def remove_text_id(self, text_id):
        for text in self.text_list['Text']:
            if text['@TextId'] == text_id:
                self.text_list['Text'].remove(text)
