# %%
import brickschema
import pandas as pd
import yaml
import rdflib
import os

# %%
g = brickschema.Graph()
g.load_file('chamber_shacl_expanded.ttl')

# %%
def query_ahu_user(loop, brick_point, equipment_type):
    """
    return ahu
    """
    if loop == "cooling":
        query = g.query(
            f"""SELECT ?plant ?water_loop ?coil ?ahu ?equipment WHERE {{
                VALUES ?t_type {{ {brick_point} }} 
                VALUES ?equipment_type {{ {equipment_type} }}
                    ?plant                  rdf:type/rdfs:subClassOf?   brick:Chiller .
                    ?plant                  brick:feeds+                ?water_loop .
                    ?water_loop             a brick:Chilled_Water_Loop .
                    ?water_loop             brick:feeds                 ?coil .
                    ?coil                   a brick:Chilled_Water_Coil .
                    ?ahu                    brick:hasPart               ?coil .
                    ?ahu                    a brick:Air_Handling_Unit .
                    ?ahu                    brick:hasPart               ?equipment .
                    ?equipment              rdf:type/rdfs:subClassOf?   ?equipment_type .
                    ?equipment              brick:hasPoint              ?point .
                    ?point                  rdf:type/rdfs:subClassOf?   ?t_type .                  
                }}"""
        )

    df_result = pd.DataFrame(query, columns=[str(s) for s in query.vars])

    if not df_result.empty:
        result_dict = df_result.to_dict('records')
        ahus_dict = {}
    
        for idx, result in enumerate(result_dict):
            ahu_dict = {'path': 
                       {'plant': str(result['plant']), 
                       'water_loop': str(result['water_loop']), 
                       'coil': str(result['coil']), 
                       'ahu': str(result['ahu']), 
                       'equipment': str(result['equipment'])}
                       }  
            ahu_dict['selected'] = False 
            ahus_dict[f"ahu_path_{idx+1}"] = ahu_dict
    else:
        ahus_dict = {}

    return ahus_dict
    


def query_bacnet_user(brick_point, equipment):
    """
    return bacnet information for control
    """

    query = f""" SELECT * WHERE {{
            VALUES ?t_type {{ {brick_point} }} 

                ?equipment brick:hasPoint              ?point .
                ?point     rdf:type/rdfs:subClassOf?   ?t_type .
                ?point     brick:hasUnit               ?point_unit .

                ?point     ref:hasExternalReference    ?ref.
                ?ref       bacnet:object-name          ?obj_name .
                ?ref       bacnet:object-identifier    ?obj_identifier .
                ?ref       bacnet:objectOf             ?obj_device .
                ?obj_device bacnet:hasPort             ?ref_port .
                ?ref_port  ref:storedAt                ?bacnet_address .
            }}"""

    q_result = g.query(query, initBindings={"equipment": equipment})
    df_result = pd.DataFrame(q_result, columns=[str(s) for s in q_result.vars])

    if not df_result.empty:
        result_dict = df_result.to_dict('records')[0]
    else:
        result_dict = {}

    return result_dict



def query_terminal_user(ahu, terminal_use_type, brick_point):
    """
    return all terminal units for selected equipment
    """

    query = f""" SELECT ?equipment ?equipment_type ?t_type WHERE {{
    VALUES ?equipment_type {{ { terminal_use_type } }}
    VALUES ?t_type {{ {brick_point} }} 

        ?ahu        brick:feeds                   ?equipment .
        ?equipment  rdf:type/rdfs:subClassOf*     ?equipment_type .
        ?equipment  brick:hasPoint                ?point .
        ?point      rdf:type/rdfs:subClassOf?     ?t_type .
        ?point      brick:hasUnit                 ?point_unit .

        ?point      ref:hasExternalReference      ?ref.
        ?ref        bacnet:object-name            ?obj_name .
        ?ref        bacnet:object-identifier      ?obj_identifier .
        ?ref        bacnet:objectOf               ?obj_device .
        ?obj_device bacnet:hasPort                ?ref_port .
        ?ref_port   ref:storedAt                  ?bacnet_address .

    }}"""

    q_result = g.query(query, initBindings={"ahu": ahu})
    df_result = pd.DataFrame(q_result, columns=[str(s) for s in q_result.vars])

    # get unique equipment
    df_result = df_result.drop_duplicates(['equipment'])

    if not df_result.empty:
        result_dict = df_result.to_dict('records')
        terminals_dict = {}
    
        for idx, result in enumerate(result_dict):
            terminal_dict = {'attributes': 
                            {'equipment': str(result['equipment']), 
                            'equipment_type': str(result['equipment_type']),
                            't_type': str(result['t_type'])}
                        }  
            terminal_dict['selected'] = False 
            terminals_dict[f"terminal_path_{idx+1}"] = terminal_dict
    
    else:
        terminals_dict = {}

    return terminals_dict



def write_yaml_config(results_dict, filepath):
    """
    Write/Save updated yaml configuration file
    """

    with open(filepath, 'w') as file:
        yaml.dump(results_dict, file)


def load_yaml_config(filepath):
    """
    Load configuration file
    """
    with open(filepath, 'r') as file:
        loaded_dict = yaml.safe_load(file)

    return loaded_dict


def update_yaml_config(section, new_content, filepath):

    config = load_yaml_config(filepath)
    if len(section) > 1:
        section_value = config.get(section[0]).get(section[1])
    else:
        section_value = config.get(section[0])

    section_value.update(new_content)

    write_yaml_config(config, filepath)
    
# %%
control_soo = {}
yaml_path = './readfiles/config.yaml'
water_loop = "cooling"
brick_point = 'brick:Run_Enable_Command'
equipment_type = 'brick:Supply_Fan'
ahu_dict = query_ahu_user(water_loop, brick_point, equipment_type)
write_yaml_config(ahu_dict, yaml_path)

# %%
ahu_path_keys = []
bacnet_update = []
selected = {}
config = load_yaml_config(yaml_path)
for key, value in config.items():
    if value['selected']:

        plant = rdflib.URIRef(value['path']['plant'])
        ahu = rdflib.URIRef(value['path']['ahu'])
        coil = rdflib.URIRef(value['path']['coil'])
        water_loop = rdflib.URIRef(value['path']['water_loop'])
        equipment = rdflib.URIRef(value['path']['equipment'])

        selected.update({key:{'ahu':str(ahu),
                              'equipment':str(equipment)}})

        bacnet_return = query_bacnet_user(brick_point, equipment)
        obj_name = str(rdflib.URIRef(bacnet_return['obj_name']))
        fan_soo = {brick_point: bacnet_return} 
        control_soo[f"{str(equipment)}"] = fan_soo
        bacnet_update.append(obj_name)
        ahu_path_keys.append(key)

# %%
for idx in range(len(ahu_path_keys)):
    update_yaml_config([ahu_path_keys[idx]], {'bacnet_name': bacnet_update[idx]}, yaml_path)

# %%
brick_point = 'brick:Supply_Air_Flow_Sensor'
terminal_use_type = 'brick:VAV'

for idx, ahu in selected.items():
    terminal_dict = query_terminal_user(rdflib.URIRef(ahu['ahu']), terminal_use_type, brick_point)
    update_yaml_config([idx], terminal_dict, yaml_path)

# %%
bacnet_update = []
terminal_path_keys = []
config = load_yaml_config(yaml_path)
for key, value in config.items():
    if value['selected']:
        for terminal_key, terminal_value in value.items():
            if 'terminal' in terminal_key:

                equipment = rdflib.URIRef(terminal_value['attributes']['equipment'])
                t_type = rdflib.URIRef(terminal_value['attributes']['t_type'])

                selected[key].update({terminal_key: {'terminal':terminal_value, 
                                                     'equipment':str(equipment)}})

                terminal_path_keys.append(terminal_key)
                bacnet_return = query_bacnet_user(brick_point, equipment)
                obj_name = str(rdflib.URIRef(bacnet_return['obj_name']))
                terminal_soo = {brick_point: bacnet_return} 
                control_soo[f"{str(equipment)}"] = terminal_soo
                bacnet_update.append(obj_name)


# %%
for idx in range(len(ahu_path_keys)):
    for idx in range(len(terminal_path_keys)):
        update_yaml_config([ahu_path_keys[idx], terminal_path_keys[idx]], {'bacnet_name': bacnet_update[idx]}, yaml_path)

# %%
