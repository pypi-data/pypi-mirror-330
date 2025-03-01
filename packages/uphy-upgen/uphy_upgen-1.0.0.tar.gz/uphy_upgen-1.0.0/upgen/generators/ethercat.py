import logging

from pathlib import Path
from xmlschema import XMLSchema, etree_tostring
import xml.etree.ElementTree as ET
from . import SCHEMA_DIR
import os


from ..model import Adapter

xs = XMLSchema(Path(SCHEMA_DIR, 'ESI/EtherCATInfo.xsd'))

_logger = logging.getLogger(__name__)

slot_pdo_increment = 16
slot_index_increment = 0x800

ecat_type = {
    'UINT32': 'UDINT',
    'UINT16': 'UINT',
    'UINT8': 'USINT',
    'INT32': 'DINT',
    'INT16': 'INT',
    'INT8': 'SINT',
    'REAL32':'REAL',
}

ecat_bitlen = {
    'UDINT':32,
    'UINT':16,
    'USINT':8,
    'DINT':32,
    'INT':16,
    'SINT':8,
    'REAL':32,
    'USINT':8
}


default_types = [
    {
        'Name': 'ULINT',
        'BitSize': 64
    },
    {
        'Name': 'UDINT',
        'BitSize': 32
    },
    {
        'Name': 'UINT',
        'BitSize': 16
    },
    {
        'Name': 'USINT',
        'BitSize': 8
    },
    {
        'Name': 'DINT',
        'BitSize': 32
    },
    {
        'Name': 'INT',
        'BitSize': 16
    },
    {
        'Name': 'SINT',
        'BitSize': 8
    },
    {
        'Name': 'REAL',
        'BitSize': 32
    },
    {
        'Name': 'LREAL',
        'BitSize': 64
    },
    {
        'Name': 'BOOL',
        'BitSize': 1
    },
    {
        'Name': 'BYTE',
        'BitSize': 8
    },
    {
        'Name': 'ARRAY [0..15] OF BYTE',
        'BaseType':'BYTE',
        'BitSize': 128,
        'ArrayInfo':{
            'LBound':0,
            'Elements':16
        }
    }
]


def hexify(s):
    return s.replace('0x', '#x')

def dehexify(s):
    return s.replace("#x", "0x")

class EtherCATGenerator:
    def __init__(self, model):
        self.model = model
        self.esi_file_name = f"{self.model.name}.xml"
        self.data_types = {}
        for t in default_types:
            self.add_data_type(t)

    def import_file(self, file):
        _logger.info('Importing model')
        esi = xs.decode(file)
        _logger.debug(esi)
        self.model = self.esi_to_model(esi)

    def export_file(self):
        if Adapter.ETHERCAT not in self.model.adapters:
            _logger.debug("EtherCAT is not enabled")
            return

        if not self.model.ethercat:
            _logger.warn('Model does not include a valid EtherCAT configuration')
            return

        _logger.info('Exporting EtherCAT ESI file')

        esi = self.model_to_esi()
        xml = xs.encode(esi)
        _logger.debug(etree_tostring(xml))
        _logger.info(f"Save xml: {str(Path(os.getcwd()) / self.esi_file_name)}")
        ET.ElementTree(xml).write(self.esi_file_name, encoding='iso-8859-1')

    def esi_to_model(self, esi):
        return None

    def model_to_esi(self):
        config = self.model.ethercat
        esi = {
            'Vendor': {
                'Id': config.vendor_id,
                'Name': self.model.vendor,
            },
            'Descriptions': {
                'Groups': self.model_to_groups(),
                'Devices': self.model_to_devices(),
                'Modules': self.model_to_modules(),
            },
        }
        return esi

    def model_to_groups(self):
        return {
            'Group': [
                {
                    'Type': self.model.ethercat.group,
                    'Name': self.model.ethercat.group
                }
            ]
        }

    def sm_obj(self, cfg):
        sm = {
            '@ControlByte': hexify(f'0x{cfg.control:02x}'),
            '@DefaultSize': str(cfg.length),
            '@Enable': str(cfg.enable),
            '@StartAddress': hexify(f'0x{cfg.address:04x}'),
            '$': cfg.type.name
        }
        return sm

    def model_to_devices(self):
        devices = []
        for d in self.model.devices:
            meta = d.ethercat
            device = {
                '@Physics': 'YY',
                'Type': {
                    '@ProductCode': meta.product_code,
                    '@RevisionNo': meta.revision,
                    '$': d.name
                },
                'Name': d.name,
                'Info': {
                    'StateMachine': {
                        'Timeout': {
                            'PreopTimeout': 1000,
                            'SafeopOpTimeout': 1000,
                            'BackToInitTimeout': 1000,
                            'BackToSafeopTimeout': 200,
                        },
                    },
                },
                'GroupType': self.model.ethercat.group,
                'Profile': {
                    'ProfileNo': int(dehexify(meta.profile), base=0),
                    'AddInfo': 0,
                    'Dictionary': self.model_to_directory(d)
                },
                'Fmmu': [f.name for f in self.model.ethercat._fmmu],
                'Sm': [self.sm_obj(sm) for sm in self.model.ethercat._sm],
                'Mailbox': {
                    '@DataLinkLayer': True,
                    'CoE': {
                        '@CompleteAccess': True,
                        '@PdoUpload': False,
                        '@SdoInfo': True,
                        '@DiagHistory': True
                    },
                    'FoE': {},
                },
                'Slots': {
                    '@SlotPdoIncrement': str(slot_pdo_increment),
                    '@SlotIndexIncrement': hexify(f'0x{slot_index_increment:x}'),
                    'Slot': self.model_to_slots(d)
                }
            }

            if d.has_alarms(self.model):
                device['Profile']['DiagMessages'] = self.model_diag_messages(d)

            devices.append(device)

        return {'Device': devices}

    def model_to_slots(self, device):
        slots = []
        for s in device.slots:
            slot = {
                '@MinInstances': '1',
                '@MaxInstances': '1',
                'Name': s.name,
                'ModuleIdent': {
                    '@Default': '1',
                    '$': str(self.model.get_module_index(s.module) + 1),
                }
            }
            slots.append(slot)

        return slots

    def model_to_modules(self):
        modules = []
        for (ix, m) in enumerate(self.model.modules):
            module = {
                'Type': {
                    '@ModuleIdent': str(ix + 1),
                    '$': m.name
                },
                'Name': m.name,
            }
            rxpdos = self.model_to_module_rxpdo(m)
            if len(rxpdos) > 0:
                module['RxPdo'] = rxpdos
            txpdos = self.model_to_module_txpdo(m)
            if len(txpdos) > 0:
                module['TxPdo'] = txpdos
            modules.append(module)

        return {'Module': modules}

    def model_to_module_rxpdo(self, module):
        pdos = []
        for p in module.ethercat.rxpdo:
            pdo = {
                '@Fixed': True,
                '@Sm': 2,
                'Index': {
                    '@DependOnSlot': True,
                    '$': p.index
                },
                'Name': p.name,
                'Entry': self.model_to_pdo_entries(module, module.outputs, p)
            }
            pdos.append(pdo)
        return pdos

    def model_to_module_txpdo(self, module):
        pdos = []
        for p in module.ethercat.txpdo:
            pdo = {
                '@Fixed': True,
                '@Sm': 3,
                'Index': {
                    '@DependOnSlot': True,
                    '$': p.index
                },
                'Name': p.name,
                'Entry': self.model_to_pdo_entries(module, module.inputs, p)
            }
            pdos.append(pdo)
        return pdos

    def model_to_pdo_entries(self, module, signals, pdo):
        entries = []
        for e in pdo.entries:
            signal = module.get_signal(signals, e.signal)
            if not signal.is_array:
                entry = {
                    'Index': e.index,
                    'SubIndex': e.subindex,
                    'BitLen': signal.bitlen,
                    'Name': signal.name,
                    'DataType': ecat_type[signal.datatype]
                }
                entries.append(entry)
            else:
                for subindex in range (1, signal.array_length + 1):
                    entry = {
                        'Index': e.index,
                        'SubIndex': str(subindex),
                        'BitLen': ecat_bitlen[ecat_type[signal.datatype]],
                        'Name': signal.name,
                        'DataType': ecat_type[signal.datatype]
                    }
                    entries.append(entry)
        return entries

    def model_to_directory(self, device):
        directory = {
            'DataTypes': {
                'DataType': [
                    self.dt1018(),
                    self.dt10f3(),
                    self.dtF000(),
                ]
            },
            'Objects': {
                'Object': [
                    self.x1000_device_type(device),
                    self.x1008_device_name(device),
                    self.x1009_hardware_version(device),
                    self.x100A_software_version(device),
                    self.x1018_identity(device),
                    self.x10F3_diagnosis_history(device),
                    self.x10F8_timestamp_object(device),
                    self.xF000_module_device_profile(device),
                    self.xF010_module_profile_list(device),
                    self.xF050_module_detected_list(device),
                    self.x1C12_sync_manager_2(device),
                    self.x1C13_sync_manager_3(device),
                    self.x1C00_sync_manager_comm_type(device)
                ]
            }
        }

        for name in self.data_types:
            directory['DataTypes']['DataType'].append(self.data_types[name])

        return directory

    def model_diag_messages (self, device):
        diags = {'DiagMessage':[]}

        for slot in device.slots:
            module = self.model.get_module(slot.module)
            for alarm in module.alarms:
                diag = {
                        'TextId': alarm.error_code,
                        'MessageText': alarm.message
                   }
                diags['DiagMessage'].append(diag)
        return diags

    def add_data_type(self, data_type):
        type_name = data_type['Name']
        if type_name not in self.data_types.keys():
            self.data_types[type_name] = data_type
        return type_name

    def add_array_type(self, name, base_type, length):
        type = {
            'Name': name,
            'BaseType': base_type,
            'BitSize': self.data_types[base_type]['BitSize'] * length,
            'ArrayInfo': {
                'LBound': 1,
                'Elements': length
            }
        }
        return self.add_data_type(type)

    def add_string_type(self, string):
        str_type = {
            'Name': f'STRING({len(string)})',
            'BitSize': len(string) * 8
        }
        return self.add_data_type(str_type)

    def add_DT1C00_type(self):
        type = {
            'Name': 'DT1C00',
            'BitSize': 0,
            'SubItem': [
                {
                    'SubIdx': '0',
                    'Name': 'Max SubIndex',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 0,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'Name': 'Elements',
                    'Type': self.add_array_type('DT1C00ARR', 'USINT', 4),
                    'BitSize': self.data_types['DT1C00ARR']['BitSize'],
                    'BitOffs': 16,
                    'Flags': {
                        'Access': 'ro'
                    }
                }
            ]
        }
        type['BitSize'] = self.data_types['DT1C00ARR']['BitSize'] + 16
        return self.add_data_type(type)

    def add_DTF010_type(self, modules):
        type = {
            'Name': 'DTF010',
            'BitSize': 0,
            'SubItem': [
                {
                    'SubIdx': '0',
                    'Name': 'Max SubIndex',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 0,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'Name': 'Elements',
                    'Type': self.add_array_type('DTF010ARR', 'UDINT', len(modules)),
                    'BitSize': self.data_types['DTF010ARR']['BitSize'],
                    'BitOffs': 16,
                    'Flags': {
                        'Access': 'ro'
                    }
                }
            ]
        }
        type['BitSize'] = self.data_types['DTF010ARR']['BitSize'] + 16
        return self.add_data_type(type)

    def add_DTF050_type(self, modules):
        type = {
            'Name': 'DTF050',
            'BitSize': 0,
            'SubItem': [
                {
                    'SubIdx': '0',
                    'Name': 'Max SubIndex',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 0,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'Name': 'Elements',
                    'Type': self.add_array_type('DTF050ARR', 'UDINT', len(modules)),
                    'BitSize': self.data_types['DTF050ARR']['BitSize'],
                    'BitOffs': 16,
                    'Flags': {
                        'Access': 'ro'
                    }
                }
            ]
        }
        type['BitSize'] = self.data_types['DTF050ARR']['BitSize'] + 16
        return self.add_data_type(type)

    def add_DT1C12_type(self, slots):
        n_rxpdos = 0
        for ix, slot in enumerate(slots):
            m = self.model.get_module(slot.module)
            rxpdo = self.model_to_module_rxpdo(m)
            if len(rxpdo) > 0:
                n_rxpdos = n_rxpdos + 1

        type = {
            'Name': 'DT1C12',
            'BitSize': 0,
            'SubItem': [
                {
                    'SubIdx': '0',
                    'Name': 'Max SubIndex',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 0,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'Name': 'Elements',
                    'Type': self.add_array_type('DT1C12ARR', 'UINT', n_rxpdos),
                    'BitSize': self.data_types['DT1C12ARR']['BitSize'],
                    'BitOffs': 16,
                    'Flags': {
                        'Access': 'ro'
                    }
                }
            ]
        }
        type['BitSize'] = self.data_types['DT1C12ARR']['BitSize'] + 16
        return self.add_data_type(type)

    def add_DT1C13_type(self, slots):
        n_txpdos = 0
        for ix, slot in enumerate(slots):
            m = self.model.get_module(slot.module)
            txpdo = self.model_to_module_txpdo(m)
            if len(txpdo) > 0:
                n_txpdos = n_txpdos + 1

        type = {
            'Name': 'DT1C13',
            'BitSize': 0,
            'SubItem': [
                {
                    'SubIdx': '0',
                    'Name': 'Max SubIndex',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 0,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'Name': 'Elements',
                    'Type': self.add_array_type('DT1C13ARR', 'UINT', n_txpdos),
                    'BitSize': self.data_types['DT1C13ARR']['BitSize'],
                    'BitOffs': 16,
                    'Flags': {
                        'Access': 'ro'
                    }
                }
            ]
        }
        type['BitSize'] = self.data_types['DT1C13ARR']['BitSize'] + 16
        return self.add_data_type(type)

    def DTF010_subitems(self, modules):
        subitems = [{
            'Name': 'Max SubIndex',
            'Info': {
                'DefaultValue': str(len(modules))
            }
        }]
        for m in modules:
            subitems.append({
                'Name': m.name,
                'Info': {
                    'DefaultValue': hexify(m.ethercat.profile)
                }
            })
        return subitems

    def DTF050_subitems(self, modules):
        subitems = [{
            'Name': 'Max SubIndex',
            'Info': {
                'DefaultValue': str(len(modules))
            }
        }]
        for ix, m in enumerate(modules):
            subitems.append({
                'Name': m.name,
                'Info': {
                    'DefaultValue': hexify(f'0x{(ix+1):04x}')
                }
            })
        return subitems

    def add_DT1C12_subitems(self, device):
        subitems = []
        pdos = []

        for ix, slot in enumerate(device.slots):
            m = self.model.get_module(slot.module)
            pdo = self.model_to_module_rxpdo(m)
            if len(pdo) > 0:
                pdos.append(0x1600 + slot_pdo_increment * ix)

        max_subindex = {
            'Name': 'Max SubIndex',
            'Info': {
                'DefaultValue': str(len(pdos))
            }
        }

        subitems.append(max_subindex)

        for pdo in pdos:
            subitem = {
                'Name': 'PDO Mapping',
                'Info': {
                    'DefaultValue': hexify(f'0x{pdo:04x}')
                }
            }
            subitems.append(subitem)

        return subitems

    def add_DT1C13_subitems(self, device):
        subitems = []
        pdos = []

        for ix, slot in enumerate(device.slots):
            m = self.model.get_module(slot.module)
            pdo = self.model_to_module_txpdo(m)
            if len(pdo) > 0:
                pdos.append(0x1A00 + slot_pdo_increment * ix)

        max_subindex = {
            'Name': 'Max SubIndex',
            'Info': {
                'DefaultValue': str(len(pdos))
            }
        }

        subitems.append(max_subindex)

        for pdo in pdos:
            subitem = {
                'Name': 'PDO Mapping',
                'Info': {
                    'DefaultValue': hexify(f'0x{pdo:04x}')
                }
            }
            subitems.append(subitem)

        return subitems

    def dt1018(self):
        return {
            'Name': 'DT1018',
            'BitSize': 144,
            'SubItem': [
                {
                    'SubIdx': '0',
                    'Name': 'Max SubIndex',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 0,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '1',
                    'Name': 'Vendor ID',
                    'Type': 'UDINT',
                    'BitSize': 32,
                    'BitOffs': 16,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '2',
                    'Name': 'Product Code',
                    'Type': 'UDINT',
                    'BitSize': 32,
                    'BitOffs': 48,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '3',
                    'Name': 'Revision Number',
                    'Type': 'UDINT',
                    'BitSize': 32,
                    'BitOffs': 80,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '4',
                    'Name': 'Serial Number',
                    'Type': 'UDINT',
                    'BitSize': 32,
                    'BitOffs': 112,
                    'Flags': {
                        'Access': 'ro'
                    }
                }
            ]
        }
    def dt10f3(self):
        dt = {
            'Name': 'DT10F3',
            'BitSize':  64 + 16*128 ,
            'SubItem': [
                {
                    'SubIdx': '0',
                    'Name': 'Max SubIndex',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 0,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '1',
                    'Name': 'Maximum Messages',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 16,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '2',
                    'Name': 'Newest Message',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 24,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '3',
                    'Name': 'Newest Acknowledged Message',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 32,
                    'Flags': {
                        'Access': 'rw'
                    }
                },
                {
                    'SubIdx': '4',
                    'Name': 'New Messages Available',
                    'Type': 'BOOL',
                    'BitSize': 1,
                    'BitOffs': 40,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '5',
                    'Name': 'Flags',
                    'Type': 'UINT',
                    'BitSize': 16,
                    'BitOffs': 48,
                    'Flags': {
                        'Access': 'rw'
                    }
                }
            ]
        }

        for i in range (16):
            msg = {
                    'SubIdx': str(6 + i),
                    'Name': f'Diagnosis Message {1+i}',
                    'Type': 'ARRAY [0..15] OF BYTE',
                    'BitSize': 128,
                    'BitOffs': 64 + i*128,
                    'Flags': {
                        'Access': 'ro'
                    }
            }
            dt['SubItem'].append(msg)

        return dt


    def dtF000(self):
        return {
            'Name': 'DTF000',
            'BitSize': 48,
            'SubItem': [
                {
                    'SubIdx': '0',
                    'Name': 'Max SubIndex',
                    'Type': 'USINT',
                    'BitSize': 8,
                    'BitOffs': 0,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '1',
                    'Name': 'Index distance',
                    'Type': 'UINT',
                    'BitSize': 16,
                    'BitOffs': 16,
                    'Flags': {
                        'Access': 'ro'
                    }
                },
                {
                    'SubIdx': '2',
                    'Name': 'Maximum number of modules',
                    'Type': 'UINT',
                    'BitSize': 16,
                    'BitOffs': 32,
                    'Flags': {
                        'Access': 'ro'
                    }
                }
            ]
        }

    def x1000_device_type(self, device):
        return {
            'Index': '#x1000',
            'Name': 'Device Type',
            'Type': 'UDINT',
            'BitSize': 32,
            'Info': {
                'DefaultValue': hexify(device.ethercat.profile)
            },
            'Flags': {
                'Access': 'ro',
                'Category': 'm'
            }
        }

    def x1008_device_name(self, device):
        return {
            'Index': '#x1008',
            'Name': 'Device Name',
            'Type': self.add_string_type(device.name),
            'BitSize': len(device.name) * 8,
            'Info': {
                'DefaultString': device.name
            },
            'Flags': {
                'Access': 'ro'
            }
        }

    def x1009_hardware_version(self, device):
        return {
            'Index': '#x1009',
            'Name': 'Hardware Version',
            'Type': self.add_string_type(device.hardware_release),
            'BitSize': len(device.hardware_release) * 8,
            'Info': {
                'DefaultString': device.hardware_release
            },
            'Flags': {
                'Access': 'ro',
                'Category': 'o'
            }
        }

    def x100A_software_version(self, device):
        return {
            'Index': '#x100A',
            'Name': 'Software Version',
            'Type': self.add_string_type(device.software_release),
            'BitSize': len(device.software_release) * 8,
            'Info': {
                'DefaultString': device.software_release
            },
            'Flags': {
                'Access': 'ro'
            }
        }

    def x1018_identity(self, device):
        return {
            'Index': '#x1018',
            'Name': 'Identity Object',
            'Type': 'DT1018',
            'BitSize': 144,
            'Info': {
                'SubItem': [
                    {
                        'Name': 'Max SubIndex',
                        'Info': {
                            'DefaultValue': '4'
                        }
                    },
                    {
                        'Name': 'Vendor ID',
                        'Info': {
                            'DefaultValue': hexify(self.model.ethercat.vendor_id)
                        }
                    },
                    {
                        'Name': 'Product Code',
                        'Info': {
                            'DefaultValue': hexify(device.ethercat.product_code)
                        }
                    },
                    {
                        'Name': 'Revision Number',
                        'Info': {
                            'DefaultValue': device.ethercat.revision
                        }
                    },
                    {
                        'Name': 'Serial Number',
                        'Info': {
                            'DefaultValue': '#x00000000'
                        }
                    }
                ]
            },
            'Flags': {
                'Access': 'ro'
            }
        }

    def x10F3_diagnosis_history(self, device):
        return {
            'Index': '#x10F3',
            'Name': 'Diagnosis History',
            'Type': 'DT10F3',
            'BitSize': 64 + 16*128,
            'Info': {
                'SubItem':[
                    {
                        'Name': 'Max SubIndex',
                        'Info': {
                            'DefaultValue': '#x15'
                        }
                    }

                ]
            },
            'Flags': {
                'Access': 'ro'
            }
        }
    def x10F8_timestamp_object(self, device):
        return {
            'Index': '#x10F8',
            'Name': 'Timestamp Object',
            'Type': 'ULINT',
            'BitSize': 64,
            'Info': {
                'Unit': '#xf7030000'
                },
            'Flags': {
                'Access': 'ro'
            }
        }

    def xF000_module_device_profile(self, device):
        return {
            'Index': '#xF000',
            'Name': 'Module Device Profile',
            'Type': 'DTF000',
            'BitSize': 48,
            'Info': {
                'SubItem': [
                    {
                        'Name': 'Max SubIndex',
                        'Info': {
                            'DefaultValue': '2'
                        }
                    },
                    {
                        'Name': 'Index distance',
                        'Info': {
                            'DefaultValue': '#x800'
                        }
                    },
                    {
                        'Name': 'Maximum number of modules',
                        'Info': {
                            'DefaultValue': str(len(self.model.modules))
                        }
                    }
                ]
            },
            'Flags': {
                'Access': 'ro'
            }
        }

    def xF010_module_profile_list(self, device):
        return {
            'Index': '#xF010',
            'Name': 'Module Profile List',
            'Type': self.add_DTF010_type(self.model.modules),
            'BitSize': self.data_types['DTF010']['BitSize'],
            'Info': {
                'SubItem': self.DTF010_subitems(self.model.modules)
            },
            'Flags': {
                'Access': 'ro'
            }
        }

    def xF050_module_detected_list(self, device):
        return {
            'Index': '#xF050',
            'Name': 'Module Detected List',
            'Type': self.add_DTF050_type(self.model.modules),
            'BitSize': self.data_types['DTF050']['BitSize'],
            'Info': {
                'SubItem': self.DTF050_subitems(self.model.modules)
            },
            'Flags': {
                'Access': 'ro'
            }
        }

    def x1C12_sync_manager_2(self, device):
        return {
            'Index': '#x1C12',
            'Name': 'Sync Manager 2 PDO Assignment',
            'Type': self.add_DT1C12_type(device.slots),
            'BitSize': self.data_types['DT1C12']['BitSize'],
            'Info': {
                'SubItem': self.add_DT1C12_subitems(device)
            },
            'Flags': {
                'Access': 'ro'
            }
        }

    def x1C13_sync_manager_3(self, device):
        return {
            'Index': '#x1C13',
            'Name': 'Sync Manager 3 PDO Assignment',
            'Type': self.add_DT1C13_type(device.slots),
            'BitSize': self.data_types['DT1C13']['BitSize'],
            'Info': {
                'SubItem': self.add_DT1C13_subitems(device)
            },
            'Flags': {
                'Access': 'ro'
            }
        }

    def x1C00_sync_manager_comm_type(self, device):
        return {
            'Index': '#x1C00',
            'Name': 'Sync Manager Communication Type',
            'Type': self.add_DT1C00_type(),
            'BitSize': self.data_types['DT1C00']['BitSize'],
            'Info': {
                'SubItem': [
                    {
                        'Name': 'Max SubIndex',
                        'Info': {
                            'DefaultValue': '4'
                        }
                    },
                    {
                        'Name': 'Communications Type SM0',
                        'Info': {
                            'DefaultValue': '1'
                        }
                    },
                    {
                        'Name': 'Communications Type SM1',
                        'Info': {
                            'DefaultValue': '2'
                        }
                    },
                    {
                        'Name': 'Communications Type SM2',
                        'Info': {
                            'DefaultValue': '3'
                        }
                    },
                    {
                        'Name': 'Communications Type SM3',
                        'Info': {
                            'DefaultValue': '4'
                        }
                    }
                ]
            },
            'Flags': {
                'Access': 'ro'
            }
        }
