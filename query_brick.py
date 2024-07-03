import brickschema

g = brickschema.Graph()
g.load_file('chamber_brick.ttl')

# Query test 1
query1 = g.query(
    """SELECT ?ahu ?sat ?damper WHERE {
    ?ahu a brick:Air_Handling_Unit .
    ?ahu brick:hasPoint ?sat .
    ?sat a brick:Supply_Air_Temperature_Sensor .
    ?ahu brick:hasPart ?damper .
    ?damper a brick:Damper
}"""
)
print("\nQuery test 1 results:")
for row in query1:
    print(row)

# Query test 2
query2 = g.query(
    """SELECT * WHERE{ 
    ?sensor rdf:type/rdfs:subClassOf* brick:Water_Temperature_Sensor
}"""
)
print("\nQuery test 2 results:")
for row in query2:
    print(row)

# Query test 3
query3 = g.query(
    """SELECT ?position WHERE{
    ?ahu a brick:Air_Handling_Unit .
    ?position a brick:Damper_Position_Sensor .
    ?damper a brick:Damper .
    ?zone a brick:HVAC_Zone .
    ?ahu brick:hasPart ?damper .
    ?damper brick:hasPoint ?position .
    ?damper brick:feeds ?zone
    }
    """
)
print("\nQuery test 3 results:")
for row in query3:
    print(row)

# Query test 4
query4 = g.query(
    """SELECT ?sat WHERE{
        ?ahu a brick:Air_Handling_Unit .
        ?sat a brick:Supply_Air_Temperature_Sensor .
        ?ahu brick:hasPoint ?sat
    }
    """
)
print("\nQuery test 4 results:")
for row in query4:
    print(row)

# Query test 5
query5 = g.query(
    """SELECT ?sat WHERE{
        ?ahu a brick:Air_Handling_Unit .
        ?sat a brick:Supply_Air_Temperature_Sensor .
        ?sat brick:isPointOf ?ahu
    }
    """
)
print("\nQuery test 5 results:")
for row in query5:
    print(row)