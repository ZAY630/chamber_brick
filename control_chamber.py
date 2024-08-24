# %%
import pandas as pd
from functions.bacnet_point import BACnet_Point
import functions.readWriteProperty as BACpypesAPP
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
# %%
