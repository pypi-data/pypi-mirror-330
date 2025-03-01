{# Suffixes to resolve signal name collisions #}
{% set suffix_in  = "in_" %}
{% set suffix_out = "out_" %}
{% set suffix_par = "par_" %}
/*********************************************************************
 *        _       _         _
 *  _ __ | |_  _ | |  __ _ | |__   ___
 * | '__|| __|(_)| | / _` || '_ \ / __|
 * | |   | |_  _ | || (_| || |_) |\__ \
 * |_|    \__|(_)|_| \__,_||_.__/ |___/
 *
 * http://www.rt-labs.com
 * Copyright 2022 rt-labs AB, Sweden.
 * See LICENSE file in the project root for full license information.
 ********************************************************************/

#include "model.h"

#ifndef NELEMENTS
#define NELEMENTS(a) (sizeof(a) / sizeof((a)[0]))
#endif

#include <stdint.h>

up_data_t up_data;

up_signal_info_t up_vars[] = {
{% for slot in device.slots %}
   {% set module = model.get_module(slot.module) %}
   {% set slot_name = slot | c_name(loop.index0, ctx, ctx.Scope.SLOT) %}
   {% for signal in module.inputs %}
       {% set signal_name = signal | c_name(suffix_in ~ loop.index0, ctx, ctx.Scope.SIGNAL) %}
   {.value = (void *)&up_data.{{slot_name}}.{{signal_name}}.value,
    .status = &up_data.{{slot_name}}.{{signal_name}}.status},
   {% endfor %}{# end of input signals #}
   {% for signal in module.outputs %}
       {% set signal_name = signal | c_name(suffix_out ~ loop.index0, ctx, ctx.Scope.SIGNAL) %}
   {.value = (void *)&up_data.{{slot_name}}.{{signal_name}}.value,
    .status = &up_data.{{slot_name}}.{{signal_name}}.status},
   {% endfor %}{# end of output signals #}
   {% for signal in module.parameters %}
       {% set signal_name = signal | c_name(suffix_par ~ loop.index0, ctx, ctx.Scope.SIGNAL) %}
   {.value = (void *)&up_data.{{slot_name}}.{{signal_name}},
    .status = NULL},
   {% endfor %}{# end of parameters #}
{% endfor %}{# end of slots #}
};
{% set ns = namespace() %}
{% set ns.ix = 0 %}
{% set ns.inputs = 0 %}
{% set ns.outputs = 0 %}
{% set ns.parameters = 0 %}
{% for slot in device.slots %}
   {% set slot_name = slot | c_name(loop.index0, ctx, ctx.Scope.SLOT) %}
   {% set module = model.get_module(slot.module) %}
   {% if module.inputs | length > 0 %}

static up_signal_t inputs_{{slot_name}}[] = {
      {% for signal in module.inputs %}
   {
      .name = "{{signal.name | c_string}}",
      .ix = {{loop.index0 + ns.ix}},
      .datatype = UP_DTYPE_{{signal.datatype}},
      .bitlength = {{signal.bitlen}},
      .flags = {{ signal | c_flags}},
      .frame_offset = {{((ns.inputs + module.get_offset(module.inputs, signal)) / 8) | int}},
   },
      {% endfor %}{# end of input signals #}
};
   {% endif %}
   {% set ns.ix = ns.ix + module.inputs | length %}
   {% set ns.inputs = ns.inputs + module.inputs_bitlen %}
   {% if module.outputs | length > 0 %}

static up_signal_t outputs_{{slot_name}}[] = {
      {% for signal in module.outputs %}
   {
      .name = "{{signal.name | c_string}}",
      .ix = {{loop.index0 + ns.ix}},
      .datatype = UP_DTYPE_{{signal.datatype}},
      .bitlength = {{signal.bitlen}},
      .flags = {{ signal | c_flags}},
      .frame_offset = {{((ns.outputs + module.get_offset(module.outputs, signal)) / 8) | int}},
   },
      {% endfor %}{# end of output signals #}
};
   {% endif %}
   {% set ns.ix = ns.ix + module.outputs | length %}
   {% set ns.outputs = ns.outputs + module.outputs_bitlen %}
   {% if module.parameters | length > 0 %}

static up_param_t parameters_{{slot_name}}[] = {
      {% for param in module.parameters %}
   {
      .name = "{{param.name | c_string}}",
      .ix = {{loop.index0 + ns.ix}},
      .datatype = UP_DTYPE_{{param.datatype}},
      .bitlength = {{param.bitlen}},
      .frame_offset = {{((ns.parameters + module.get_offset(module.parameters, param)) / 8) | int}},
   },
      {% endfor %}{# end of parameters #}
};
   {% endif %}
   {% set ns.ix = ns.ix + module.parameters | length %}
   {% set ns.parameters = ns.parameters + module.parameters_bitlen %}
{% endfor %}{# end of slots #}

up_slot_t slots[] = {
{% for slot in device.slots %}
   {% set slot_name = slot | c_name(loop.index0, ctx, ctx.Scope.SLOT) %}
   {% set module = model.get_module(slot.module) %}
   {
      .name = "{{slot_name}}",
      .input_bitlength = {{module.inputs_bitlen}},
      .output_bitlength = {{module.outputs_bitlen}},
   {% if module.inputs | length > 0 %}
      .n_inputs = NELEMENTS (inputs_{{slot_name}}),
      .inputs = inputs_{{slot_name}},
   {% endif %}
   {% if module.outputs | length > 0 %}
      .n_outputs = NELEMENTS (outputs_{{slot_name}}),
      .outputs = outputs_{{slot_name}},
   {% endif %}
   {% if module.parameters | length > 0 %}
      .n_params = NELEMENTS (parameters_{{slot_name}}),
      .params = parameters_{{slot_name}},
   {% endif %}
   },
{% endfor %}{# end of slots #}
};

up_device_t up_device = {
   .name = "{{device.name | c_string}}",
   .cfg.serial_number = "{{device.serial | c_string}}",
   .cfg.webgui_enable = {{device.webgui_enable | c_bool}},
   .bustype = UP_BUSTYPE_MOCK,
   .n_slots = NELEMENTS (slots),
   .slots = slots,
};
{% if device.profinet and model.profinet%}
   {% set ns.pn_slots = 0 %}
   {% set ns.pn_ix = 0 %}
   {% for module in device.get_used_modules(model) %}
      {% if module.profinet %}
         {% if module.parameters %}

up_pn_param_t pn_{{module | c_name(loop.index0, ctx, ctx.Scope.MODULE)}}_parameters[] = {
            {% for p in module.parameters %}
   {
      .pn_index = {{p.profinet.index}},
   },
            {% endfor %}{# end of parameters #}
};
         {% endif %}
      {% endif %}
   {% endfor %}{# end of modules #}

up_pn_module_t pn_modules[] = {
   {% for module in device.get_used_modules(model) %}
      {% if module.profinet %}
   {
      .module_id = {{module.profinet.module_id | c_hex}},
      .submodule_id = {{module.profinet.submodule_id | c_hex}},
         {% if module.parameters %}
      .n_params = {{module.parameters | length}},
      .params = pn_{{module | c_name(loop.index0, ctx, ctx.Scope.MODULE)}}_parameters,
         {% endif %}
   },
      {% endif %}
   {% endfor %}{# end of modules #}
};

up_pn_slot_t pn_slots[] = {
   {% for slot in device.slots %}
      {% set module = model.get_module(slot.module) %}
      {% if module.profinet %}
   {
      .module_ix = {{ device.get_used_module_index(slot.module, model) }},
   },
         {% set ns.pn_slots = ns.pn_slots + 1 %}
      {% endif %}
   {% endfor %}{# end of slots #}
};

up_profinet_config_t up_profinet_config = {
   .vendor_id = {{model.profinet.vendor_id}},
   .device_id = {{model.profinet.device_id}},
   .dap_module_id = {{device.profinet.dap_module_id}},
   .dap_identity_submodule_id = {{device.profinet.dap_identity_submodule_id}},
   .dap_interface_submodule_id = {{device.profinet.dap_interface_submodule_id}},
   .dap_port_1_submodule_id = {{device.profinet.dap_port_1_submodule_id}},
   .dap_port_2_submodule_id = {{device.profinet.dap_port_2_submodule_id}},
   .profile_id = {{device.profinet.profile_id}},
   .profile_specific_type = {{device.profinet.profile_specific_type}},
   .min_device_interval = {{device.profinet.min_device_interval}},
   .default_stationname = "{{device.profinet.default_stationname | c_string}}",
   .order_id = "{{device.profinet.order_id | c_string}}",
   .hw_revision = {{device.profinet.hw_revision}},
   .sw_revision_prefix = '{{device.profinet.sw_revision_prefix | c_char}}',
   .sw_revision_functional_enhancement = {{device.profinet.sw_revision_functional_enhancement}},
   .sw_revision_bug_fix = {{device.profinet.sw_revision_bug_fix}},
   .sw_revision_internal_change = {{device.profinet.sw_revision_internal_change}},
   .revision_counter = {{device.profinet.revision_counter}},
   .n_modules = {{device.get_used_modules(model) | length}},
   .n_slots = {{ns.pn_slots}},
   .modules = pn_modules,
   .slots = pn_slots,
};
{% endif %}
{% if model.ethercat and device.ethercat %}
   {% set ns.ecat_ix = 0 %}
   {% for module in device.get_used_modules(model) %}
      {% set module_name = module | c_name(loop.index0, ctx, ctx.Scope.MODULE) %}
      {% if module.ethercat %}
         {% set ecat = module.ethercat %}
         {% set ns.ecat_ix = 0 %}
         {% for txpdo in ecat.txpdo %}

up_ciaobject_t ecat_{{module_name}}_{{txpdo | c_name(loop.index0, ctx, ctx.Scope.TXPDO)}}_txpdo_entries[] = {
            {% for entry in txpdo.entries %}
   {
      .index = {{entry.index | c_hex}},
      .subindex = {{entry.subindex | c_hex}},
      .is_signal = true,
      .signal_or_param_ix = {{ns.ecat_ix}},
   },
               {% set ns.ecat_ix = ns.ecat_ix + 1 %}
            {% endfor %}{# end of txpdo entries #}
};
         {% endfor %}{# end of txpdos #}
         {% if ecat.txpdo %}

up_ciapdo_t ecat_{{module_name}}_txpdos[] = {
            {% for txpdo in ecat.txpdo %}
   {
      .name = "{{txpdo.name | c_string}}",
      .index = {{txpdo.index | c_hex}},
      .n_entries = {{ txpdo.entries | length}},
      .entries = ecat_{{module_name}}_{{txpdo | c_name(loop.index0, ctx, ctx.Scope.TXPDO)}}_txpdo_entries,
   },
            {% endfor %}{# end of txpdos #}
};
         {% endif %}
         {% set ns.ecat_ix = 0 %}
         {% for rxpdo in ecat.rxpdo %}

up_ciaobject_t ecat_{{module_name}}_{{rxpdo | c_name(loop.index0, ctx, ctx.Scope.RXPDO)}}_rxpdo_entries[] = {
            {% for entry in rxpdo.entries %}
   {
      .index = {{entry.index | c_hex}},
      .subindex = {{entry.subindex| c_hex}},
      .is_signal = true,
      .signal_or_param_ix = {{ns.ecat_ix}},
   },
               {% set ns.ecat_ix = ns.ecat_ix + 1 %}
            {% endfor %}{# end of rxpdo entries #}
};
         {% endfor %}{# end of rxpdos #}
         {% if ecat.rxpdo %}

up_ciapdo_t ecat_{{module_name}}_rxpdos[] = {
            {% for rxpdo in ecat.rxpdo %}
   {
      .name = "{{rxpdo.name | c_string}}",
      .index = {{rxpdo.index | c_hex}},
      .n_entries = {{ rxpdo.entries | length}},
      .entries = ecat_{{module_name}}_{{rxpdo | c_name(loop.index0, ctx, ctx.Scope.RXPDO)}}_rxpdo_entries,
   },
            {% endfor %}{# end of rxpdos #}
};
         {% endif %}
         {% if ecat.objects %}
            {% set ns.ecat_ix = 0 %}

up_ciaobject_t ecat_{{module_name}}_objects[] = {
            {% for object in ecat.objects %}
   {
      .index = {{object.index | c_hex}},
      .subindex = {{object.subindex| c_hex}},
      .is_signal = false,
      .signal_or_param_ix = {{ ns.ecat_ix }},
   },
               {% set ns.ecat_ix = ns.ecat_ix + 1 %}
            {% endfor %}{# end of objects #}
};
         {% endif %}
      {% endif %}
   {% endfor %}{# end of modules #}

up_ecat_module_t ecat_modules[] = {
   {% for module in device.get_used_modules(model) %}
      {% set module_name = module | c_name(loop.index0, ctx, ctx.Scope.MODULE) %}
      {% if module.ethercat %}
         {% set ecat = module.ethercat %}
   {
      .profile = {{ecat.profile}},
      .n_rxpdos = {{ ecat.rxpdo | length }},
      .n_txpdos = {{ ecat.txpdo | length }},
      .n_objects = {{ ecat.objects | length }},
         {% if ecat.rxpdo | length > 0 %}
      .rxpdos = ecat_{{module_name}}_rxpdos,
         {% else %}
      .rxpdos = NULL,
         {% endif %}
         {% if ecat.txpdo | length > 0 %}
      .txpdos = ecat_{{module_name}}_txpdos,
         {% else %}
      .txpdos = NULL,
         {% endif %}
         {% if ecat.objects | length > 0 %}
      .objects = ecat_{{module_name}}_objects,
         {% else %}
      .objects = NULL,
         {% endif %}
   },
      {% endif %}
   {% endfor %}{# end of modules #}
};

up_ecat_slot_t ecat_slots[] = {
   {% for slot in device.slots %}
      {% set module = model.get_module(slot.module) %}
      {% if module.ethercat %}
   {
      .module_ix = {{device.get_used_module_index(slot.module, model)}},
   },
      {% endif %}
   {% endfor %}{# end of slots #}
};

up_ecat_device_t up_ethercat_config = {
   .profile = {{device.ethercat.profile | c_hex}},
   .vendor = {{model.ethercat.vendor_id | c_hex}},
   .productcode = {{device.ethercat.product_code | c_hex}},
   .revision = {{device.ethercat.revision | c_hex}},
   .serial = 1,
   .hw_rev = "{{device.ethercat.hw_revision | c_string}}",
   .sw_rev = "{{device.ethercat.hw_revision | c_string}}",
   .pdo_increment = 16,       /* TODO */
   .index_increment = 0x0100, /* TODO */
   .n_modules = {{device.get_used_modules(model) | length}},
   .n_slots = {{device.slots | length}},
   .modules = ecat_modules,
   .slots = ecat_slots,
};

{% endif %}
{% if model.ethernetip and device.ethernetip %}
up_ethernetip_config_t up_ethernetip_config = {
   .vendor_id = {{model.ethernetip.vendor_id}},
   .device_type = {{device.ethernetip.device_type}},
   .product_code = {{device.ethernetip.product_code}},
   .major_revision = {{device.ethernetip.revision | enip_major_rev}},
   .minor_revision = {{device.ethernetip.revision | enip_minor_rev}},
   .min_data_interval = {{device.ethernetip.min_data_interval}},
   .default_data_interval = {{device.ethernetip.default_data_interval}},
   .input_assembly_id = 100,
   .output_assembly_id = 101,
   .config_assembly_id = 102,
   .input_only_heartbeat_assembly_id = 103,
   .listen_only_heartbeat_assembly_id = 104,
};

{% endif %}
{% if device.modbus %}
{% set modbus_port = device.modbus.port | int(base=0) %}
up_modbus_config_t up_modbus_config = {
   .port = {{modbus_port}},
};

{% endif %}
up_mockadapter_config_t up_mock_config = {0};
