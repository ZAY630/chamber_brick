# %%
import brickschema
import pandas as pd
import yaml
import rdflib

# %%
g = brickschema.Graph()
g.load_file('chamber_shacl_expanded.ttl')

# %%
def query_ahu_path(loop, brick_point, equipment_type, additional_filter="""""", query_relaxation = False):
    """
    return ahu
    """
    if query_relaxation == False:
        queries = []
        if loop == "cooling":
            for point in brick_point:
                query = g.query(
                    f"""SELECT DISTINCT ?plant ?water_loop ?coil ?ahu ?equipment ?t_type WHERE {{
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
                            {additional_filter}                
                        }}"""
                )
                queries = queries + list(query)
        else:
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
                            ?ahu                    brick:hasPoint              ?point .
                            ?equipment              rdf:type/rdfs:subClassOf?   ?equipment_type .
                            ?equipment              brick:hasPoint              ?point .
                            ?point                  rdf:type/rdfs:subClassOf?   ?t_type .  
                            {additional_filter}                
                        }}"""
                )
                queries = queries + list(query)

    df_result = pd.DataFrame(queries, columns=[str(s) for s in query.vars])
    df_result.drop_duplicates(subset=['equipment', 't_type'], keep='first')

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
            ahu_dict['user_selected'] = False 
            ahus_dict[f"ahu_path_{idx+1}"] = ahu_dict
    else:
        ahus_dict = {}

    return ahus_dict
    

def query_specific_user(upstream, equipment_use_type, brick_point, name, additional_filter="""""", query_relaxation = False):
    """
    return all terminal units for selected equipment
    """
    if query_relaxation == False:
        q_results = []

        for point in brick_point:

            query = f""" SELECT ?equipment ?equipment_type ?t_type WHERE {{
            VALUES ?equipment_type {{ { equipment_use_type } }}
            VALUES ?t_type {{ {point} }} 

                ?upstream   brick:hasPart                 ?equipment .
                ?equipment  rdf:type/rdfs:subClassOf*     ?equipment_type .
                ?equipment  brick:hasPoint                ?point .
                ?point      rdf:type/rdfs:subClassOf*     ?t_type .
                ?point      brick:hasUnit                 ?point_unit .

                ?point      ref:hasExternalReference      ?ref.
                ?ref        bacnet:object-name            ?obj_name .
                ?ref        bacnet:object-identifier      ?obj_identifier .
                ?ref        bacnet:objectOf               ?obj_device .
                ?obj_device bacnet:hasPort                ?ref_port .
                ?ref_port   ref:storedAt                  ?bacnet_address .
                {additional_filter}
            }}"""

            q_result = g.query(query, initBindings={"upstream": upstream})
            q_results = q_results + list(q_result)

    else:
        q_results = []

        for point in brick_point:

            query = f""" SELECT ?equipment ?equipment_type ?t_type WHERE {{
            VALUES ?equipment_type {{ { equipment_use_type } }}
            VALUES ?t_type {{ {point} }} 

                ?equipment  brick:hasPoint                ?point .
                ?point      rdf:type/rdfs:subClassOf*     ?t_type .
                ?point      brick:hasUnit                 ?point_unit .

                ?point      ref:hasExternalReference      ?ref.
                ?ref        bacnet:object-name            ?obj_name .
                ?ref        bacnet:object-identifier      ?obj_identifier .
                ?ref        bacnet:objectOf               ?obj_device .
                ?obj_device bacnet:hasPort                ?ref_port .
                ?ref_port   ref:storedAt                  ?bacnet_address .
                {additional_filter}
            }}"""

            q_result = g.query(query, initBindings={"equipment": upstream})
            q_results = q_results + list(q_result)
    
    df_result = pd.DataFrame(q_results, columns=[str(s) for s in q_result.vars])
    df_result.drop_duplicates(subset=['equipment', 't_type'], keep='last')

    value_counts = df_result['equipment'].value_counts()

    to_remove = value_counts[value_counts < len(seq_name)].index
    df_filtered = df_result[~df_result['equipment'].isin(to_remove)]
    df_filtered = df_filtered.drop_duplicates('equipment')

    if not df_filtered.empty:
        result_dict = df_filtered.to_dict('records')
        equipments_dict = {}
    
        for idx, result in enumerate(result_dict):
            equipment_dict = {'attributes': 
                            {'equipment': str(result['equipment']), 
                            'equipment_type': str(result['equipment_type'])}
                        }  
            equipment_dict['user_selected'] = False 
            equipments_dict[f"{name}_path_{idx+1}"] = equipment_dict
    
    else:
        equipments_dict = {}

    return equipments_dict


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



def query_terminal_user(ahu, terminal_use_type, brick_point, additional_filter=""""""):
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
            {additional_filter}
        }}"""

        q_result = g.query(query, initBindings={"ahu": ahu})
        q_results = q_results + list(q_result)
    
    df_result = pd.DataFrame(q_results, columns=[str(s) for s in q_result.vars])
    df_result.drop_duplicates(subset=['equipment', 't_type'], keep='last')

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
            terminal_dict['user_selected'] = False 
            terminals_dict[f"terminal_path_{idx+1}"] = terminal_dict
    
    else:
        terminals_dict = {}

    return terminals_dict



def write_yaml_config(results_dict, filepath):
    """
    Write/Save updated yaml configuration file
    """

    with open(filepath, 'w') as file:
        yaml.dump(results_dict, file, sort_keys=False)


def load_yaml_config(filepath):
    """
    Load configuration file
    """
    with open(filepath, 'r') as file:
        loaded_dict = yaml.safe_load(file)

    return loaded_dict


def update_yaml_config(section, new_content, filepath):

    config = load_yaml_config(filepath)
    if len(section) == 2:
        section_value = config.get(section[0]).get(section[1])
    elif len(section) == 3:
        section_value = config.get(section[0]).get(section[1]).get(section[2])
    elif len(section) == 4:
        section_value = config.get(section[0]).get(section[1]).get(section[2]).get(section[3])
    else:
        section_value = config.get(section[0])

    section_value.update(new_content)

    write_yaml_config(config, filepath)
    
# %%
control_soo = {}
yaml_path = './readfiles/config.yaml'
water_loop = "cooling"

seq_name = ['check:fan_status']
brick_point = ['brick:Fan_On_Off_Status']
equipment_type = 'brick:Supply_Fan'

ahu_dict = query_ahu_path(water_loop, brick_point, equipment_type)
if ahu_dict == {}:
    print("no air handling units found, please modify query")
else:
    print("query returned, check config.yaml file")
    write_yaml_config(ahu_dict, yaml_path)

# %%
import pdb; pdb.set_trace()

selected = {}
config = load_yaml_config(yaml_path)
for key, value in config.items():

    if value['user_selected']:

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
            soo = {brick_point[idx]: bacnet_return[idx]} 
            control_soo[seq_name[idx]] = soo
            bacnet.update({f'operation_{idx+1}': {seq_name[idx]:obj_name}})

        ahu_path_key = key
        ahu_selected = str(ahu)

# %%
update_yaml_config([ahu_path_key], bacnet, yaml_path)

# %%
brick_point = ['brick:Run_Enable_Command', 'brick:Fan_Speed_Command']
specific_user_type = 'brick:Fan_VFD'
seq_name = ['write:vfd_enable', 'write:fan_speed']
name = 'VFD'

specific_user_dict = query_specific_user(rdflib.URIRef(ahu_selected), specific_user_type, brick_point, name, query_relaxation = False)
if specific_user_dict == {}:
    print("no equipment found, tying query relaxation ...")
    specific_user_dict = query_specific_user(rdflib.URIRef(ahu_selected), specific_user_type, brick_point, name, query_relaxation = True)
    if specific_user_dict == {}:
        print("no equipment found")
    else:
        print("query returned, check config.yaml file")
        update_yaml_config([ahu_path_key], specific_user_dict, yaml_path)
else:
    print("query returned, check config.yaml file")
    update_yaml_config([ahu_path_key], specific_user_dict, yaml_path)

# %%
import pdb; pdb.set_trace()
config = load_yaml_config(yaml_path)
ahu_path = config[ahu_path_key]
for key, value in ahu_path.items():
    if (f'{name}_path' in key):
        if value['user_selected']:
            equipment = rdflib.URIRef(value['attributes']['equipment'])

            selected[ahu_path_key].update({key: {'specific_user':value, 
                                                'equipment':str(equipment)}})

            specific_user_path_key = key
            bacnet_return = query_bacnet_user(brick_point, equipment)
            bacnet = {}
            for idx in range(len(seq_name)):
                obj_name = str(rdflib.URIRef(bacnet_return[idx]['obj_name']))
                soo = {brick_point[idx]: bacnet_return[idx]} 
                control_soo[seq_name[idx]] = soo
                bacnet.update({f'operation_{idx+1}': {seq_name[idx]:obj_name}})

# %%
update_yaml_config([ahu_path_key, specific_user_path_key], bacnet, yaml_path)

# %%
seq_name = ['check:duct_pressure', 'write:duct_pressure']
brick_point = ['brick:Static_Pressure_Sensor', 'brick:Supply_Air_Static_Pressure_Setpoint']
specific_user_type = 'brick:Air_Handling_Unit'
name = 'Duct'

specific_user_dict = query_specific_user(rdflib.URIRef(ahu_selected), specific_user_type, brick_point, name, query_relaxation = False)
if specific_user_dict == {}:
    print("no equipment found, tying query relaxation ...")
    specific_user_dict = query_specific_user(rdflib.URIRef(ahu_selected), specific_user_type, brick_point, name, query_relaxation = True)
    if specific_user_dict == {}:
        print("no equipment found")
    else:
        print("query returned, check config.yaml file")
        update_yaml_config([ahu_path_key], specific_user_dict, yaml_path)
else:
    print("query returned, check config.yaml file")
    update_yaml_config([ahu_path_key], specific_user_dict, yaml_path)

# %%
import pdb; pdb.set_trace()
config = load_yaml_config(yaml_path)
ahu_path = config[ahu_path_key]
for key, value in ahu_path.items():
    if (f'{name}_path' in key):
        if value['user_selected']:
            equipment = rdflib.URIRef(value['attributes']['equipment'])

            selected[ahu_path_key].update({key: {'specific_user':value, 
                                                'equipment':str(equipment)}})

            specific_user_path_key = key
            bacnet_return = query_bacnet_user(brick_point, equipment)
            bacnet = {}
            for idx in range(len(seq_name)):
                obj_name = str(rdflib.URIRef(bacnet_return[idx]['obj_name']))
                soo = {brick_point[idx]: bacnet_return[idx]} 
                control_soo[seq_name[idx]] = soo
                bacnet.update({f'operation_{idx+1}': {seq_name[idx]:obj_name}})
# %%
update_yaml_config([ahu_path_key, specific_user_path_key], bacnet, yaml_path)
# %%
brick_point = ['brick:Damper_Position_Sensor', 'brick:Damper_Position_Command']
specific_user_type = 'brick:Damper'
additional_filter = """
?equipment brick:feeds+ ?vav .
?vav a brick:VAV .
"""
seq_name = ['check:supply_damper_position', 'write:supply_damper_command']
name = 'Damper'

specific_user_dict = query_specific_user(rdflib.URIRef(ahu_selected), specific_user_type, brick_point, name, additional_filter, query_relaxation = False)
if specific_user_dict == {}:
    print("no downstream terminal found, trying query relaxation ...")
    specific_user_dict = query_specific_user(rdflib.URIRef(ahu_selected), specific_user_type, brick_point, name, additional_filter, query_relaxation = True)
    if specific_user_dict == {}:
        print("no equipment found")
    else:
        print("query returned, check config.yaml file")
        update_yaml_config([ahu_path_key], specific_user_dict, yaml_path)
else:
    print("query returned, check config.yaml file")
    update_yaml_config([ahu_path_key], specific_user_dict, yaml_path)

# %%
import pdb; pdb.set_trace()
config = load_yaml_config(yaml_path)
ahu_path = config[ahu_path_key]
for key, value in ahu_path.items():
    if (f'{name}_path' in key):
        if value['user_selected']:
            equipment = rdflib.URIRef(value['attributes']['equipment'])

            selected[ahu_path_key].update({key: {'specific_user':value, 
                                                'equipment':str(equipment)}})

            specific_user_path_key = key
            bacnet_return = query_bacnet_user(brick_point, equipment)
            bacnet = {}
            for idx in range(len(seq_name)):
                obj_name = str(rdflib.URIRef(bacnet_return[idx]['obj_name']))
                soo = {brick_point[idx]: bacnet_return[idx]} 
                control_soo[seq_name[idx]] = soo
                bacnet.update({f'operation_{idx+1}': {seq_name[idx]:obj_name}})

# %%
update_yaml_config([ahu_path_key, specific_user_path_key], bacnet, yaml_path)

# %%
brick_point = ['brick:Supply_Air_Flow_Sensor']
terminal_use_type = 'brick:Terminal_Unit'
seq_name = ['check:diffuser_airflow']
name = 'terminal'
terminal_dict = query_terminal_user(rdflib.URIRef(ahu_selected), terminal_use_type, brick_point)
if terminal_dict == {}:
    print("no downstream terminal found")
else:
    print("query returned, check config.yaml file")
    update_yaml_config([ahu_path_key], {'terminal':{}}, yaml_path)
    update_yaml_config([ahu_path_key, 'terminal'], terminal_dict, yaml_path)

# %%
terminal_path_keys = []

config = load_yaml_config(yaml_path)
terminal_path = config[ahu_path_key]['terminal']
terminal_unit = {}
soo = [[] for _ in range(len(seq_name))]

for terminal_key, terminal_value in terminal_path.items():
    if (f'{name}_path' in terminal_key):
        equipment = rdflib.URIRef(terminal_value['attributes']['equipment'])
        terminal_unit.update({terminal_key:{'tu':str(equipment)}})
        terminal_path_keys.append(terminal_key)
        bacnet_return = query_bacnet_user(brick_point, equipment)
        bacnet = {}

        for idx in range(len(seq_name)):
            obj_name = str(rdflib.URIRef(bacnet_return[idx]['obj_name']))
            soo[idx].append({terminal_key:{brick_point[idx]:bacnet_return[idx]}})
            bacnet.update({f'operation_{idx+1}': {seq_name[idx]:obj_name}})
        update_yaml_config([ahu_path_key, 'terminal', terminal_key], bacnet, yaml_path)


for idx in range(len(seq_name)):
    control_soo.update({seq_name[idx]:soo[idx]})

selected[ahu_path_key]['terminal'] = terminal_unit

# %%
brick_point = ['brick:Damper_Position_Sensor', 'brick:Damper_Position_Command']
specific_user_type = 'brick:Damper'
seq_name = ['check:vav_damper_position', 'write:vav_damper_command']
name = 'VAV_Damper'

for terminal in terminal_path_keys:
    specific_user_dict = query_specific_user(rdflib.URIRef(selected[ahu_path_key]['terminal'][terminal]['tu']), specific_user_type, brick_point, name, query_relaxation = False)
    if specific_user_dict == {}:
        print("no downstream terminal found, trying query relaxation ...")
        specific_user_dict = query_specific_user(rdflib.URIRef(selected[ahu_path_key]['terminal'][terminal]['tu']), specific_user_type, brick_point, name, query_relaxation = True)
        if specific_user_dict == {}:
            print("no downstream terminal found")
        else:
            print("query returned, check config.yaml file")
            update_yaml_config([ahu_path_key, 'terminal', terminal], specific_user_dict, yaml_path)
    else:
        print("query returned, check config.yaml file")
        update_yaml_config([ahu_path_key, 'terminal', terminal], specific_user_dict, yaml_path)

# %%
config = load_yaml_config(yaml_path)
terminal_path = config[ahu_path_key]['terminal']
soo = [[] for _ in range(len(seq_name))]
for terminal_key, terminal_value in terminal_path.items():
    found = False
    for key, value in terminal_value.items():
        if (f'{name}_path' in key):
            found = True
            equipment = rdflib.URIRef(value['attributes']['equipment'])

            selected[ahu_path_key]['terminal'][terminal_key].update({key: {'specific_user':value, 
                                                'equipment':str(equipment)}})

            specific_user_path_key = key
            bacnet_return = query_bacnet_user(brick_point, equipment)
            bacnet = {}
            for idx in range(len(seq_name)):
                obj_name = str(rdflib.URIRef(bacnet_return[idx]['obj_name']))
                soo[idx].append({terminal_key:{brick_point[idx]:bacnet_return[idx]}})
                bacnet.update({f'operation_{idx+1}': {seq_name[idx]:obj_name}})
            update_yaml_config([ahu_path_key, 'terminal', terminal_key, key], bacnet, yaml_path)

    if not found:
        for idx in range(len(seq_name)):
            soo[idx].append({terminal_key:{}})

for idx in range(len(seq_name)):
    control_soo.update({seq_name[idx]:soo[idx]})

# %%
if __name__ == "__main__":
    print("Finished querying")
# %%