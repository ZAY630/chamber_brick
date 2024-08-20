# %%
import brickschema
import pandas as pd
from functions.bacnet_point import BACnet_Point
import functions.readWriteProperty as BACpypesAPP
import yaml
import rdflib

# %%
g = brickschema.Graph()
g.load_file('chamber_shacl_expanded.ttl')

# %%
# bacnet_ini_file = '..\\bacpypes\\BACnet_connect.ini'
# access_bacnet = BACpypesAPP.Init(bacnet_ini_file)

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
    


def query_specific(brick_point, equipment_type, additional_filter):
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



def query_specific_path(equipment, end_use_type):
    """
    return all endusers for selected equipment
    """

    query = f""" SELECT * WHERE {{
    VALUES ?enduser_type {{ { end_use_type } }}
    VALUES ?t_type {{ {brick_point} }} 
    VALUES ?equipment_type {{ {equipment_type} }}

        ?equipment  brick:hasPart                 ?enduser .
        ?enduser    rdf:type/rdfs:subClassOf*     ?enduser_type .
        ?enduser    brick:hasPoint                ?point .
        ?point      rdf:type/rdfs:subClassOf?     ?t_type .
        ?point      brick:hasUnit                 ?point_unit .

        ?point      ref:hasExternalReference      ?ref.
        ?ref        bacnet:object-name            ?obj_name .
        ?ref        bacnet:object-identifier      ?obj_identifier .
        ?ref        bacnet:objectOf               ?obj_device .
        ?obj_device bacnet:hasPort                ?ref_port .
        ?ref_port   ref:storedAt                  ?bacnet_address .

    }}"""

    q_result = g.query(query, initBindings={"equipment": equipment})
    df_result = pd.DataFrame(q_result, columns=[str(s) for s in q_result.vars])

    # get unique equipment
    df_result = df_result.drop_duplicates(['enduser'])

    if not df_result.empty:
        result_dict = df_result.to_dict('records')
    else:
        result_dict = {}

    return result_dict

    

def write_yaml_config(query_results, filepath):
    """
    Write/Save updated yaml configuration file
    """
    results_dict = {}
    
    for idx, result in enumerate(query_results):
        result_dict = {'attributes': 
                       {'plant': str(result['plant']), 
                       'water_loop': str(result['water_loop']), 
                       'coil': str(result['coil']), 
                       'ahu': str(result['ahu'])}
                       }  
        result_dict['selected'] = False 
        results_dict[f"return_query_{idx+1}"] = result_dict
    
    # Write the results to the YAML file
    with open(filepath, 'w') as file:
        yaml.dump(results_dict, file)



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
brick_point = 'brick:Fan_On_Off_Status'
equipment_type = 'brick:Supply_Fan'
additional_filter = """
?ahu a brick:Air_Handling_Unit . 
?ahu brick:hasPoint ?point .
"""

results = query_specific(brick_point, equipment_type, additional_filter)
if len(results) == 0:
    print("empty return, check query")
elif len(results) > 1:
    print("multiple returns, update config.yaml file")
    results = query_water_loop(water_loop)
    write_yaml_config(results, yaml_path)

# %%
config = load_yaml_config(yaml_path)
for idx, query in enumerate(config):
    plant = rdflib.URIRef(query['attributes']['plant'])
    ahu = rdflib.URIRef(query['attributes']['ahu'])
    coil = rdflib.URIRef(query['attributes']['coil'])
    water_loop = rdflib.URIRef(query['attributes']['water_loop'])

query_specific_path(ahu, equipment_type)


# %%
