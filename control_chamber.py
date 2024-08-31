# %%
import pandas as pd
from functions.bacnet_point import BACnet_Point
import functions.readWriteProperty as BACpypesAPP
import time
# %%
# g = brickschema.Graph()
# g.load_file('chamber_shacl_expanded.ttl')

# %%
bacnet_ini_file = '..\\bacpypes\\BACnet_connect.ini'
access_bacnet = BACpypesAPP.Init(bacnet_ini_file)


# %%
import query_brick_chamber

# %%
control_soo = query_brick_chamber.control_soo
selected = query_brick_chamber.selected
selected_ahu = list(selected.keys())[0]
selected_terminal = list(selected[selected_ahu]['terminal'].keys())
result_dict = {}
print(list(control_soo.keys()))
verified = True
# %%
############################################
######### Control sequence markdown ########
############################################

# Step 1: check and document all baseline measurememts: damper position, fan status, airflow rate
# Step 2: open terminal damper position to 100%, and supply damper position 100%
# Step 3: verify damper position sensor, airflow rate change
# Step 4: (enable fan and) increase fan speed
# Step 5: verify vav airflow sensor change
# Step 6: close terminal damper position 50%
# Step 7: verify vav airflow sensor change
# Step 8: close supply damper position 50%
# Step 9: verify vav airflow sensor change
# Step 10: restore all conditions

# %%
import pdb; pdb.set_trace()
result_dict.update({'step_1':{}})

vav_damper_position = control_soo.get('check:vav_damper_position')[1].get('terminal_path_2').get('brick:Damper_Position_Sensor')
position = BACnet_Point(**vav_damper_position) if bool(vav_damper_position) else vav_damper_position
values = []
for i in range(10):
    value = position.get_point_value(BACpypesAPP)
    values.append(value)
    time.sleep(2)

result_dict.get('step_1').update({'vav_damper_position':values})

if values != []:
    verified = verified * True
else:
    verified = False

supply_damper_position = control_soo.get('check:supply_damper_position').get('brick:Damper_Position_Sensor')
position = BACnet_Point(**supply_damper_position) if bool(supply_damper_position) else supply_damper_position
values = []
for i in range(10):
    value = position.get_point_value(BACpypesAPP)
    values.append(value)
    time.sleep(2)

result_dict.get('step_1').update({'supply_damper_value':values})

supply_airflow_rate = control_soo.get('check:diffuser_airflow')[1].get('terminal_path_2').get('brick:Supply_Air_Flow_Sensor')
vav_afr = BACnet_Point(**supply_airflow_rate) if bool(supply_airflow_rate) else supply_airflow_rate
values = []
for i in range(10):
    value = vav_afr.get_point_value(BACpypesAPP)
    values.append(value)
    time.sleep(5)

if values != []:
    verified = verified * True
else:
    verified = False

result_dict.get('step_1').update({'airflow_rate_value':values})

supply_fan_status = control_soo.get('check:fan_status').get('brick:Fan_On_Off_Status')
fan_status = BACnet_Point(**supply_fan_status) if bool(supply_fan_status) else supply_fan_status
value = fan_status.get_point_value(BACpypesAPP)
result_dict.get('step_1').update({'fan_status':value})

supply_fan_enable = control_soo.get('write:fan_enable').get('brick:Run_Enable_Command')
fan_enable = BACnet_Point(**supply_fan_enable) if bool(supply_fan_enable) else supply_fan_enable
enable_check = fan_enable.get_point_value(BACpypesAPP)
if enable_check == 'inactive':
    fan_enable.write_point_value(BACpypesAPP, "active", 13)

enable_check = fan_enable.get_point_value(BACpypesAPP)
result_dict.get('step_1').update({'fan_enable':enable_check})

if (enable_check == 'active') & verified:
    result_dict.get('step_1').update({'verified':True})

import pdb; pdb.set_trace()
# %%
if result_dict.get('step_1').get('verified'):
    result_dict.update({'step_2':{}})

    vav_damper_command = control_soo.get('write:vav_damper_command')[1].get('terminal_path_2').get('brick:Damper_Position_Command')
    command = BACnet_Point(**vav_damper_command) if bool(vav_damper_command) else vav_damper_command
    command.write_point_value(BACpypesAPP, 100, 13)

    values = []
    for i in range(10):
        value = command.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(2)

    result_dict.get('step_2').update({'vav_damper_position':values})

    if values != []:
        verified = verified * True
    else:
        verified = False

    supply_damper_command = control_soo.get('write:supply_damper_command').get('brick:Damper_Position_Command')
    command = BACnet_Point(**supply_damper_command) if bool(supply_damper_command) else supply_damper_command
    command.write_point_value(BACpypesAPP, 100, 13)

    values = []
    for i in range(10):
        value = command.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(2)

    result_dict.get('step_2').update({'supply_damper_value':values})

    if values != []:
        verified = verified * True
    else:
        verified = False

    if verified:
        result_dict.get('step_2').update({'verified':True})

else:
    print("Step 1 verification failed!")

import pdb; pdb.set_trace()
# %%
if result_dict.get('step_2').get('verified'):
    result_dict.update({'step_3':{}})

    fan_speed_command = control_soo.get('write:fan_speed').get('brick:Fan_Speed_Command')
    command = BACnet_Point(**fan_speed_command) if bool(fan_speed_command) else fan_speed_command
    command.write_point_value(BACpypesAPP, 25, 13)

    values = []
    for i in range(10):
        value = command.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(2)

    result_dict.get('step_3').update({'fan_speed_command':values})

    if values != []:
        verified = verified * True
    else:
        verified = False
    
    if verified:
        result_dict.get('step_3').update({'verified':True})

else:
    print("Step 2 verification failed!")

import pdb; pdb.set_trace()
# %%
if result_dict.get('step_3').get('verified'):
    result_dict.update({'step_4':{}})

    supply_airflow_rate = control_soo.get('check:diffuser_airflow')[1].get('terminal_path_2').get('brick:Supply_Air_Flow_Sensor')
    vav_afr = BACnet_Point(**supply_airflow_rate) if bool(supply_airflow_rate) else supply_airflow_rate
    values = []
    for i in range(10):
        value = vav_afr.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(5)

    if values != []:
        verified = verified * True
    else:
        verified = False

    result_dict.get('step_4').update({'airflow_rate_value':values})

else:
    print("Step 3 verification failed!")

import pdb; pdb.set_trace()