# %%
import brickschema
import pandas as pd
from functions.bacnet_point import BACnet_Point
import functions.readWriteProperty as BACpypesAPP

# %%
g = brickschema.Graph()
g.load_file('chamber_shacl_expanded.ttl')

# %%
# bacnet_ini_file = './readfiles/BACnet_init_controller.ini'
# access_bacnet = BACpypesAPP.Init(bacnet_ini_file)

# %%
brick_point = 'brick:Fan_On_Off_Status'
equipment_type = 'brick:Supply_Fan'
additional_filter = """
?ahu a brick:Air_Handling_Unit . 
?ahu brick:hasPoint ?point .
"""


query = g.query(
    f""" SELECT * WHERE {{
        VALUES ?t_type {{ {brick_point} }} 
        VALUES ?equipment_type {{ {equipment_type} }}
             ?equipment rdf:type/rdfs:subClassOf?   ?equipment_type .
             ?equipment brick:hasPoint              ?point .
             ?point     rdf:type/rdfs:subClassOf?   ?t_type .
             ?point     brick:hasUnit               ?point_unit .

             ?point     ref:hasExternalReference    ?ref.
             ?ref       bacnet:object-name          ?obj_name .
             ?ref       bacnet:object-identifier    ?obj_identifier .
             ?ref       bacnet:objectOf             ?obj_device .
             ?obj_device bacnet:hasPort             ?ref_port .
             ?ref_port  ref:storedAt                ?bacnet_address .
             {additional_filter}
        }}"""
)

df_result = pd.DataFrame(query, columns=[str(s) for s in query.vars])

if not df_result.empty:
    fan_status_dict = df_result.to_dict('records')
else:
    fan_status_dict = {}

fan_status_dict = [result for result in fan_status_dict if result['ahu'].split('#')[-1] != 'AHU_A']

print("returned", len(fan_status_dict), "queries")

# %%
fan_status_dict = fan_status_dict[0]
fan_status = BACnet_Point(**fan_status_dict) if bool(fan_status_dict) else fan_status_dict
fan_status.get_point_value(BACpypesAPP)

# %%
brick_point = 'brick:Run_Enable_Command'
equipment_type = 'brick:Supply_Fan'
additional_filter = """
?ahu a brick:Air_Handling_Unit . 
?ahu brick:hasPoint ?point .
"""


query = g.query(
    f""" SELECT * WHERE {{
        VALUES ?t_type {{ {brick_point} }} 
        VALUES ?equipment_type {{ {equipment_type} }}
             ?equipment rdf:type/rdfs:subClassOf?   ?equipment_type .
             ?equipment brick:hasPoint              ?point .
             ?point     rdf:type/rdfs:subClassOf?   ?t_type .
             ?point     brick:hasUnit               ?point_unit .

             ?point     ref:hasExternalReference    ?ref.
             ?ref       bacnet:object-name          ?obj_name .
             ?ref       bacnet:object-identifier    ?obj_identifier .
             ?ref       bacnet:objectOf             ?obj_device .
             ?obj_device bacnet:hasPort             ?ref_port .
             ?ref_port  ref:storedAt                ?bacnet_address .
             {additional_filter}
        }}"""
)

df_result = pd.DataFrame(query, columns=[str(s) for s in query.vars])

if not df_result.empty:
    fan_enable_dict = df_result.to_dict('records')
else:
    fan_enable_dict = {}

fan_enable_dict = [result for result in fan_enable_dict if result['ahu'].split('#')[-1] != 'AHU_A']

print("returned", len(fan_enable_dict), "queries")

# %%
# Enable command: Enabled/Disabled
fan_enable_dict = fan_enable_dict[0]
fan_enable_cmd = BACnet_Point(**fan_enable_dict) if bool(fan_enable_dict) else fan_enable_dict
fan_enable_cmd.get_point_value(BACpypesAPP)

fan_enable_cmd.write_point_value(BACpypesAPP, "Enabled", 13)
fan_enable_cmd.get_point_value(BACpypesAPP)
fan_status.get_point_value(BACpypesAPP)

# %%
brick_point = 'brick:Damper_Position_Sensor'
equipment_type = 'brick:Damper'
additional_filter = """
?ahu a brick:Air_Handling_Unit . 
?ahu brick:hasPart ?vav .
?vav a brick:VAV .
?vav brick:hasPart ?equipment .
"""


query = g.query(
    f""" SELECT * WHERE {{
        VALUES ?t_type {{ {brick_point} }} 
        VALUES ?equipment_type {{ {equipment_type} }}
             ?equipment rdf:type/rdfs:subClassOf?   ?equipment_type .
             ?equipment brick:hasPoint              ?point .
             ?point     rdf:type/rdfs:subClassOf?   ?t_type .
             ?point     brick:hasUnit               ?point_unit .

             ?point     ref:hasExternalReference    ?ref.
             ?ref       bacnet:object-name          ?obj_name .
             ?ref       bacnet:object-identifier    ?obj_identifier .
             ?ref       bacnet:objectOf             ?obj_device .
             ?obj_device bacnet:hasPort             ?ref_port .
             ?ref_port  ref:storedAt                ?bacnet_address .
             {additional_filter}
        }}"""
)

df_result = pd.DataFrame(query, columns=[str(s) for s in query.vars])

if not df_result.empty:
    vav_damper_dict = df_result.to_dict('records')
else:
    vav_damper_dict = {}

print("returned", len(vav_damper_dict), "queries")

# %%
# damper command: 0 ~ 100
vav_damper_dict = vav_damper_dict[0]
vav_damper_command = BACnet_Point(**vav_damper_dict) if bool(vav_damper_dict) else vav_damper_dict
vav_damper_command.get_point_value(BACpypesAPP)

vav_damper_command.write_point_value(BACpypesAPP, 100, 13)
vav_damper_command.get_point_value(BACpypesAPP)

# %%
brick_point = 'brick:Supply_Air_Flow_Sensor'
equipment_type = 'brick:VAV'
additional_filter = """
"""


query = g.query(
    f""" SELECT * WHERE {{
        VALUES ?t_type {{ {brick_point} }} 
        VALUES ?equipment_type {{ {equipment_type} }}
             ?equipment rdf:type/rdfs:subClassOf?   ?equipment_type .
             ?equipment brick:hasPoint              ?point .
             ?point     rdf:type/rdfs:subClassOf?   ?t_type .
             ?point     brick:hasUnit               ?point_unit .

             ?point     ref:hasExternalReference    ?ref.
             ?ref       bacnet:object-name          ?obj_name .
             ?ref       bacnet:object-identifier    ?obj_identifier .
             ?ref       bacnet:objectOf             ?obj_device .
             ?obj_device bacnet:hasPort             ?ref_port .
             ?ref_port  ref:storedAt                ?bacnet_address .
             {additional_filter}
        }}"""
)

df_result = pd.DataFrame(query, columns=[str(s) for s in query.vars])

if not df_result.empty:
    vav_afr_dict = df_result.to_dict('records')
else:
    vav_afr_dict = {}

print("returned", len(vav_afr_dict), "queries")

# %%
vav_afr_dict = vav_afr_dict[0]
vav_afr = BACnet_Point(**vav_afr_dict) if bool(vav_afr_dict) else vav_afr_dict
vav_afr.get_point_value(BACpypesAPP)


