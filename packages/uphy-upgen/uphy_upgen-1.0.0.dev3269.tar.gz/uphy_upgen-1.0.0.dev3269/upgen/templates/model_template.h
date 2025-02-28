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

#ifndef MODEL_H
#define MODEL_H

#ifdef __cplusplus
extern "C" {
#endif

#include "up_types.h"

{% if model.profinet %}
#define UP_DEVICE_PROFINET_SUPPORTED 1
{% endif %}
{% if model.ethercat %}
#define UP_DEVICE_ETHERCAT_SUPPORTED 1
{% endif %}
{% if model.ethernetip %}
#define UP_DEVICE_ETHERNETIP_SUPPORTED 1
{% endif %}
{% if device.modbus %}
#define UP_DEVICE_MODBUS_SUPPORTED 1
{% endif %}

{% if device.has_alarms(model) %}
/* Alarm error codes */
{% for module in device.get_used_modules(model) %}
   {% set mod_i = prefix_module ~ loop.index0 %}
   {% set module_name = module | c_name_upper(loop.index0, ctx, ctx.Scope.MODULE) %}
   {% for a in module.alarms %}
       {% set a_i = prefix_alarm ~ loop.index0 %}
       {% set alarm_name = a | c_name_upper(loop.index0, ctx, ctx.Scope.ALARM) %}
#define UP_ERROR_CODE_{{module_name}}_{{alarm_name}} {{a.error_code}}
   {% endfor %}
{% endfor %}

{% endif %}
typedef struct up_data
{
{% for slot in device.slots %}
{% set slot_i = prefix_slot ~ loop.index0 %}
{% set module = model.get_module(slot.module) %}
{# Should be run first to give set the scope for the signals #}
{% set slot_name = slot | c_name(loop.index0, ctx, ctx.Scope.SLOT) %}
   struct
   {
   {% for signal in module.inputs %}
      {% set sig_i = prefix_in ~ loop.index0 %}
      {% set signal_name = signal | c_name(suffix_in ~ loop.index0, ctx, ctx.Scope.SIGNAL) %}
      struct
      {
         {{signal | c_type}} value{{signal | c_array}};
         up_signal_status_t status;
      } {{signal_name}};
   {% endfor %}
   {% for signal in module.outputs %}
      {% set sig_i = prefix_out ~ loop.index0 %}
      {% set signal_name = signal | c_name(suffix_out ~ loop.index0, ctx, ctx.Scope.SIGNAL) %}
      struct
      {
         {{signal | c_type}} value{{signal | c_array}};
         up_signal_status_t status;
      } {{signal_name}};
   {% endfor %}
   {% for signal in module.parameters %}
      {% set sig_i = prefix_par ~ loop.index0 %}
      {% set signal_name = signal | c_name(suffix_par ~ loop.index0, ctx, ctx.Scope.SIGNAL) %}
      {{signal | c_type}} {{signal_name}};
   {% endfor %}
   } {{slot_name}};
{% endfor %}
} up_data_t;

extern up_data_t up_data;
extern up_signal_info_t up_vars[];
extern up_device_t up_device;
{% if model.profinet %}
extern up_profinet_config_t up_profinet_config;
{% endif %}
{% if model.ethercat %}
extern up_ecat_device_t up_ethercat_config;
{% endif %}
{% if model.ethernetip %}
extern up_ethernetip_config_t up_ethernetip_config;
{% endif %}
{% if device.modbus %}
extern up_modbus_config_t up_modbus_config;
{% endif %}
extern up_mockadapter_config_t up_mock_config;

#ifdef __cplusplus
}
#endif

#endif /* MODEL_H */
