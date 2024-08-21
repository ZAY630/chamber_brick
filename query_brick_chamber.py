# %%
import brickschema
import pandas as pd
from functions.bacnet_point import BACnet_Point
import functions.readWriteProperty as BACpypesAPP
import yaml
import rdflib
import os

# %%
g = brickschema.Graph()
g.load_file('chamber_shacl_expanded.ttl')

# %%
def query_water_loop(loop):
    """
    return relavent water loop
    """
    if loop == "cooling":
        query = g.query(
            f"""SELECT ?plant ?water_loop ?coil ?ahu WHERE {{
                VALUES ?t_type {{ {brick_point} }} 
                VALUES ?equipment_type {{ {equipment_type} }}
                    ?plant                  rdf:type/rdfs:subClassOf?   brick:Chiller .
                    ?plant                  brick:feeds+                ?water_loop .
                    ?water_loop             a brick:Chilled_Water_Loop .
                    ?water_loop             brick:feeds                 ?coil .
                    ?coil                   a brick:Chilled_Water_Coil .
                    ?coil                   brick:feeds+                ?terminal .
                    ?terminal               rdf:type/rdfs:subClassOf?   brick:Terminal_Unit .
                    ?terminal               brick:isPartOf              ?ahu .
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
    else:
        result_dict = {}

    return result_dict
    


def make_query(brick_point, equipment_type, additional_filter):
    """
    return specific queries on a brick point
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
        result_dict = df_result.to_dict('records')
    else:
        result_dict = {}

    return result_dict



def query_end_user(ahu, end_use_type):
    """
    return all endusers for selected equipment
    """

    query = f""" SELECT * WHERE {{
    VALUES ?equipment_type {{ { end_use_type } }}
    VALUES ?t_type {{ {brick_point} }} 

        ?ahu        brick:hasPart                 ?enduser .
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

    q_result = g.query(query, initBindings={"equipment": ahu})
    df_result = pd.DataFrame(q_result, columns=[str(s) for s in q_result.vars])

    # get unique equipment
    df_result = df_result.drop_duplicates(['enduser'])

    if not df_result.empty:
        result_dict = df_result.to_dict('records')
    else:
        result_dict = {}

    return result_dict

    

def write_yaml_config(results_dict, filepath):
    """
    Write/Save updated yaml configuration file
    """
    
    # Write the results to the YAML file
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            existing_config = yaml.safe_load(file)
        
        existing_config.update(results_dict)
        with open(filepath, 'w') as file:
            yaml.dump(existing_config, file)
    else:
        with open(filepath, 'w') as file:
            yaml.dump(results_dict, file)


def get_path_dict(query_results):
    """
    Write/Save queried path results
    """
    results_dict = {}
    
    for idx, result in enumerate(query_results):
        result_dict = {'path': 
                       {'plant': str(result['plant']), 
                       'water_loop': str(result['water_loop']), 
                       'coil': str(result['coil']), 
                       'ahu': str(result['ahu'])}
                       }  
        result_dict['selected'] = False 
        results_dict[f"path_{idx+1}"] = result_dict
    
    return results_dict

def get_end_user_dict(query_results):
    """
    Write/Save queried end user results
    """
    results_dict = {}
    
    for idx, result in enumerate(query_results):
        result_dict = {'attributes': 
                       {'equipment': str(result['equipment']), 
                        'equipment_type': str(result['equipment_type']),
                        't_type': str(result['t_type']),
                        'obj_name': str(result['obj_name'])}
                       }  
        result_dict['selected'] = False 
        results_dict[f"end_user_{idx+1}"] = result_dict
    
    return results_dict


def load_yaml_config(filepath):
    """
    Load configuration file
    """
    with open(filepath, 'r') as file:
        updated_dict = yaml.safe_load(file)
    
    selected_results = []
    
    for key, query in updated_dict.items():
        if query['selected']:
            selected_results.append(query)
    
    return selected_results


# %%
water_loop = "cooling"
yaml_path = './readfiles/config.yaml'
brick_point = 'brick:Damper_Position_Sensor'
equipment_type = 'brick:Damper'
additional_filter = """
?ahu a brick:Air_Handling_Unit . 
?ahu brick:hasPart ?vav .
?vav a brick:VAV .
?vav brick:hasPart ?equipment .
"""

results = make_query(brick_point, equipment_type, additional_filter)
if len(results) == 0:
    print("empty return, check query")
elif len(results) > 1:
    print("multiple returns, update config.yaml file")
    results = query_water_loop(water_loop)
    results_dict = get_path_dict(results)
    write_yaml_config(results_dict, yaml_path)

    config = load_yaml_config(yaml_path)
    for idx, query in enumerate(config):
        plant = rdflib.URIRef(query['path']['plant'])
        ahu = rdflib.URIRef(query['path']['ahu'])
        coil = rdflib.URIRef(query['path']['coil'])
        water_loop = rdflib.URIRef(query['path']['water_loop'])
        
        end_user_results = query_end_user(ahu, equipment_type)
        end_user_dict = get_end_user_dict(end_user_results)
        write_yaml_config(end_user_dict, yaml_path)
        
else:
    print("query returned, check config.yaml")
    end_user_dict = get_end_user_dict(results)
    write_yaml_config(end_user_dict, yaml_path)


# %%
end_user_selected = []
config = load_yaml_config(yaml_path)
for idx, query in enumerate(config):
    if 'attributes' in query.keys():
        end_user_selected.append(end_user_results[idx])
# %%
