# %%
import brickschema
import pandas as pd
import yaml
import rdflib

# %%
g = brickschema.Graph()
g.load_file('chamber_shacl_expanded.ttl')

# %%
def query_ahu_user(loop, brick_point, equipment_type):
    """
    return ahu
    """
    queries = []
    if loop == "cooling":
        for point in brick_point:
            query = g.query(
                f"""SELECT ?plant ?water_loop ?coil ?ahu ?equipment ?t_type WHERE {{
                    VALUES ?t_type {{ {point} }} 
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
            queries = queries + list(query)

    df_result = pd.DataFrame(queries, columns=[str(s) for s in query.vars])

    value_counts = df_result['equipment'].value_counts()

    to_remove = value_counts[value_counts < len(seq_name)].index
    df_filtered = df_result[~df_result['equipment'].isin(to_remove)]
    df_filtered = df_filtered.drop_duplicates('equipment')

    if not df_filtered.empty:
        result_dict = df_filtered.to_dict('records')
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
    q_results = []
    for point in brick_point:

        query = f""" SELECT * WHERE {{
                VALUES ?t_type {{ {point} }} 

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

        q_results = q_results + list(q_result)
        

    df_result = pd.DataFrame(q_results, columns=[str(s) for s in q_result.vars])
    
    if not df_result.empty:
        result_dict = df_result.to_dict('records')
    else:
        result_dict = {}

    return result_dict



def query_terminal_user(ahu, terminal_use_type, brick_point):
    """
    return all terminal units for selected equipment
    """
    q_results = []

    for point in brick_point:

        query = f""" SELECT ?equipment ?equipment_type ?t_type WHERE {{
        VALUES ?equipment_type {{ { terminal_use_type } }}
        VALUES ?t_type {{ {point} }} 

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
        q_results = q_results + list(q_result)
    
    df_result = pd.DataFrame(q_results, columns=[str(s) for s in q_result.vars])
    value_counts = df_result['equipment'].value_counts()

    to_remove = value_counts[value_counts < len(seq_name)].index
    df_filtered = df_result[~df_result['equipment'].isin(to_remove)]
    df_filtered = df_filtered.drop_duplicates('equipment')

    if not df_filtered.empty:
        result_dict = df_filtered.to_dict('records')
        terminals_dict = {}
    
        for idx, result in enumerate(result_dict):
            terminal_dict = {'attributes': 
                            {'equipment': str(result['equipment']), 
                            'equipment_type': str(result['equipment_type'])}
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

seq_name = ['run:fan_enable', 'check:fan_status']
brick_point = ['brick:Run_Enable_Command', 'brick:Fan_On_Off_Status']
equipment_type = 'brick:Supply_Fan'
ahu_dict = query_ahu_user(water_loop, brick_point, equipment_type)
if ahu_dict == {}:
    print("no air handling units found, please modify query")
else:
    print("query returned, check config.yaml file")
    write_yaml_config(ahu_dict, yaml_path)

# %%
import pdb; pdb.set_trace()
ahu_path_keys = []
bacnet_update_ahu = []
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
        bacnet = {}
        for idx in range(len(seq_name)):
            obj_name = str(rdflib.URIRef(bacnet_return[idx]['obj_name']))
            fan_soo = {brick_point[idx]: bacnet_return[idx]} 
            control_soo[seq_name[idx]] = fan_soo
            bacnet.update({seq_name[idx]:obj_name})
        bacnet_update_ahu.append(bacnet)
        ahu_path_keys.append(key)

# %%
for idx in range(len(ahu_path_keys)):
    update_yaml_config([ahu_path_keys[idx]], bacnet_update_ahu[idx], yaml_path)

# %%
brick_point = ['brick:Supply_Air_Flow_Sensor', 'brick:Supply_Air_Temperature_Sensor']
terminal_use_type = 'brick:Terminal_Unit'
seq_name = ['check:diffuser_airflow', 'check:diffuser_airtemp']
for idx, ahu in selected.items():
    terminal_dict = query_terminal_user(rdflib.URIRef(ahu['ahu']), terminal_use_type, brick_point)
    if terminal_dict == {}:
        print("no downstream terminal found")
    else:
        print("query returned, check config.yaml file")
        update_yaml_config([idx], terminal_dict, yaml_path)

# %%
import pdb; pdb.set_trace()
bacnet_update_ahu = []
terminal_path_keys = []
config = load_yaml_config(yaml_path)
for key, value in config.items():
    if value['selected']:
        bacnet_update_terminal = []
        for terminal_key, terminal_value in value.items():
            if ('terminal' in terminal_key):
                if terminal_value['selected']:
                    equipment = rdflib.URIRef(terminal_value['attributes']['equipment'])

                    selected[key].update({terminal_key: {'terminal':terminal_value, 
                                                        'equipment':str(equipment)}})

                    terminal_path_keys.append(terminal_key)
                    bacnet_return = query_bacnet_user(brick_point, equipment)
                    bacnet = {}
                    for idx in range(len(seq_name)):
                        obj_name = str(rdflib.URIRef(bacnet_return[idx]['obj_name']))
                        fan_soo = {brick_point[idx]: bacnet_return[idx]} 
                        control_soo[seq_name[idx]] = fan_soo
                        bacnet.update({seq_name[idx]:obj_name})

                    bacnet_update_terminal.append(bacnet)
        bacnet_update_ahu.append(bacnet_update_terminal)


# %%
for idx in range(len(ahu_path_keys)):
    for jdx in range(len(terminal_path_keys)):
        update_yaml_config([ahu_path_keys[idx], terminal_path_keys[jdx]], bacnet_update_ahu[idx][jdx], yaml_path)

# %%
if __name__ == "__main__":
    print("running queries ......")