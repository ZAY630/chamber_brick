# %%
import numpy as np
from functions.bacnet_point import BACnet_Point
import functions.readWriteProperty as BACpypesAPP
import time

# %%
bacnet_ini_file = '..\\bacpypes\\BACnet_connect.ini'
access_bacnet = BACpypesAPP.Init(bacnet_ini_file)


# %%
import query_ductP_chamber

# %%
control_soo = query_ductP_chamber.control_soo
selected = query_ductP_chamber.selected
selected_ahu = list(selected.keys())[0]
selected_terminal = list(selected[selected_ahu]['terminal'].keys())
result_dict = {}
print(list(control_soo.keys()))
verified = True
# %%
############################################
######### Control sequence markdown ########
############################################

# Pre: prepare for terminal commissioning: enable supply fan (with no fan speed) and open supply damper
# Test_1: run individual commissioning on individual terminal path:
    # Step 1: open terminal damper position to 50% (if there is a damper) and read supply airflow rate for baseline
    # Step 2: increase duct static pressure setpoint
    # Step 3: read supply airflow rate for change
    # Step 4: restore all conditions
# Analysis: analyze measurements 

# %%
import pdb; pdb.set_trace()
result_dict.update({'Pre':{}})

# read supply damper position
supply_damper_position = control_soo.get('check:supply_damper_position').get('brick:Damper_Position_Sensor')
position = BACnet_Point(**supply_damper_position) if bool(supply_damper_position) else supply_damper_position
values = []
for i in range(3):
    value = position.get_point_value(BACpypesAPP)
    values.append(value)
    time.sleep(2)

result_dict.get('Pre').update({'supply_damper_value':values})

# read supply fan status (and enable fan)
supply_fan_status = control_soo.get('check:fan_status').get('brick:Fan_On_Off_Status')
fan_status = BACnet_Point(**supply_fan_status) if bool(supply_fan_status) else supply_fan_status
value = fan_status.get_point_value(BACpypesAPP)
result_dict.get('Pre').update({'fan_status':value})

supply_vfd_enable = control_soo.get('write:vfd_enable').get('brick:Run_Enable_Command')
vfd_enable = BACnet_Point(**supply_vfd_enable) if bool(supply_vfd_enable) else supply_vfd_enable
enable_check = vfd_enable.get_point_value(BACpypesAPP)
if enable_check == 'inactive':
    vfd_enable.write_point_value(BACpypesAPP, "active", 13)

enable_check = vfd_enable.get_point_value(BACpypesAPP)
result_dict.get('Pre').update({'vfd_enable':enable_check})

# open supply damper position to 50% if closed
supply_damper_command = control_soo.get('write:supply_damper_command').get('brick:Damper_Position_Command')

if supply_damper_command != {}:
    command = BACnet_Point(**supply_damper_command) if bool(supply_damper_command) else supply_damper_command
    current_value = command.get_point_value(BACpypesAPP)
    if current_value == 0:
        command.write_point_value(BACpypesAPP, 50, 13)

    values = []
    for i in range(3):
        value = command.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(2)

    result_dict.get('Pre').update({'supply_damper_value':values})

    if values != []:
        verified = verified * True
    else:
        verified = False


if (enable_check == 'active') & verified:
    result_dict.get('Pre').update({'verified':True})
    
import pdb; pdb.set_trace()
# %%
tbcontrolled = [0, 'terminal_path_1']
test = 'Test_1'
if result_dict.get('Pre').get('verified'):
    result_dict.update({test:{'step_1':{}}})

    # open terminal damper position to 50% if closed
    vav_damper_command = control_soo.get('write:vav_damper_command')[tbcontrolled[0]].get(tbcontrolled[1]).get('brick:Damper_Position_Command')
    
    if vav_damper_command != {}:

        command = BACnet_Point(**vav_damper_command) if bool(vav_damper_command) else vav_damper_command
        current_value = command.get_point_value(BACpypesAPP)
        if current_value == 0:
            command.write_point_value(BACpypesAPP, 50, 13)

        values = []
        for i in range(3):
            value = command.get_point_value(BACpypesAPP)
            values.append(value)
            time.sleep(2)

        result_dict.get(test).get('step_1').update({'vav_damper_position':values})

        if values != []:
            verified = verified * True
        else:
            verified = False

    # read terminal supply airflow rate for baseline
    supply_airflow_rate = control_soo.get('check:diffuser_airflow')[tbcontrolled[0]].get(tbcontrolled[1]).get('brick:Supply_Air_Flow_Sensor')
    vav_afr = BACnet_Point(**supply_airflow_rate) if bool(supply_airflow_rate) else supply_airflow_rate
    values = []
    for i in range(15):
        value = vav_afr.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(1)

    if values != []:
        verified = verified * True
    else:
        verified = False

    result_dict.get(test).get('step_1').update({'airflow_rate_value': values, 
                                                'mean_airflow_rate': np.mean(values)})

    if verified:
        result_dict.get(test).get('step_1').update({'verified':True})

else:
    print("Preparation verification failed!")

import pdb; pdb.set_trace()

# %%
if result_dict.get(test).get('step_1').get('verified'):
    result_dict.get(test).update({'step_2':{}})

    # increase fan speed to 25 %
    duct_pressure_sensor = control_soo.get('check:duct_pressure').get('brick:Static_Pressure_Sensor')

    sensor = BACnet_Point(**duct_pressure_sensor) if bool(duct_pressure_sensor) else duct_pressure_sensor

    values = []
    for i in range(15):
        value = sensor.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(1)

    if values != []:
        verified = verified * True
    else:
        verified = False

    result_dict.get(test).get('step_2').update({'duct_static_pressure': values, 
                                                'mean_pressure': np.mean(values)})
    

    duct_pressure_command = control_soo.get('write:duct_pressure').get('brick:Supply_Air_Static_Pressure_Setpoint')
    command = BACnet_Point(**duct_pressure_command) if bool(duct_pressure_command) else duct_pressure_command
    current_value = result_dict.get(test).get('step_2').get('mean_pressure')

    command.write_point_value(BACpypesAPP, current_value + 0.1, 13)

    values = []
    for i in range(3):
        value = command.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(2)

    result_dict.get(test).get('step_2').update({'duct_pressure_command':values})

    if values != []:
        verified = verified * True
    else:
        verified = False
    
    if verified:
        result_dict.get(test).get('step_2').update({'verified':True})

else:
    print("Step 1 verification failed!")

import pdb; pdb.set_trace()
# %%
if result_dict.get(test).get('step_2').get('verified'):
    result_dict.get(test).update({'step_3':{}})

    # read supply airflow change
    supply_airflow_rate = control_soo.get('check:diffuser_airflow')[tbcontrolled[0]].get(tbcontrolled[1]).get('brick:Supply_Air_Flow_Sensor')
    vav_afr = BACnet_Point(**supply_airflow_rate) if bool(supply_airflow_rate) else supply_airflow_rate
    values = []
    for i in range(15):
        value = vav_afr.get_point_value(BACpypesAPP)
        values.append(value)
        time.sleep(1)

    result_dict.get(test).get('step_3').update({'airflow_rate_value': value, 
                                                'mean_airflow_rate:': np.mean(values)})

    if result_dict.get(test).get('step_1').get('mean_airflow_rate') < np.mean(values):
        verified = verified * True
    else:
        verified = False

    if verified:
        result_dict.get(test).get('step_3').update({'verified':True})

else:
    print("Step 2 verification failed!")

import pdb; pdb.set_trace()

# %%
if result_dict.get(test).get('step_3').get('verified'):
    result_dict.get(test).update({'step_4':{}})

    # erase: fan speed command 
    command = BACnet_Point(**duct_pressure_command) if bool(duct_pressure_command) else duct_pressure_command
    command.write_point_value(BACpypesAPP, 'null', 13)

    # erase: vav damper command
    command = BACnet_Point(**vav_damper_command) if bool(vav_damper_command) else vav_damper_command
    command.write_point_value(BACpypesAPP, 'null', 13)
    
    # erase supply damper command
    command = BACnet_Point(**supply_damper_command) if bool(supply_damper_command) else supply_damper_command
    command.write_point_value(BACpypesAPP, "null", 13)

else:
    print("Step 3 verification failed!")

# %%
import pdb; pdb.set_trace()
