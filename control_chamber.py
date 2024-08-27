# %%
import pandas as pd
from functions.bacnet_point import BACnet_Point
import functions.readWriteProperty as BACpypesAPP
import time
# %%
# g = brickschema.Graph()
# g.load_file('chamber_shacl_expanded.ttl')

# %%
# bacnet_ini_file = '..\\bacpypes\\BACnet_connect.ini'
# access_bacnet = BACpypesAPP.Init(bacnet_ini_file)


# %%
import query_brick_chamber

# %%
control_soo = query_brick_chamber.control_soo
selected = query_brick_chamber.selected
result_dict = {}
print(list(control_soo.keys()))
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
result_dict.update({'step_1':{'value':{}, 
                              'verified':False}})

vav_damper_position = control_soo.get('check:vav_damper_position').get('brick:Damper_Position_Sensor')
position = BACnet_Point(**vav_damper_position) if bool(vav_damper_position) else vav_damper_position
values = []
for i in range(10):
    value = position.get_point_value(BACpypesAPP)
    value.append(value)
    time.sleep(5)

result_dict.get('step_1').get('value').update(values)
if values != []:
    result_dict.get('step_1').get('verified').update(True)


# %%
