import brickschema
from brickschema.namespaces import A, BRICK
from rdflib import Namespace

# Brick:Environment_Box has definition related to Laboratory which also known as climate chamber
# Namespace definition and binding could be found at: https://rdflib.readthedocs.io/en/stable/namespaces_and_bindings.html
# and at: https://www.ibm.com/docs/en/db2/11.5?topic=prolog-namespace-declaration

CHB = Namespace("http://berkeley.edu/climatechamber#")
g = brickschema.Graph()
g.load_file('./Brick.ttl')
g.bind('chamber', CHB)
g.bind('brick', BRICK)


#########################################
#### General Equipment Specification ####
#########################################
# Building site 
g.add((CHB["UCB"], A, BRICK["Site"]))
g.add((CHB['wurster_hall'], A, BRICK["Building"]))
g.add((CHB["chamber_room"], A, BRICK["Environment_Box"]))
g.add((CHB["zone"], A, BRICK["HVAC_Zone"]))


# Air ventilation
g.add((CHB["ahu"], A, BRICK["Air_Handling_Unit"]))
g.add((CHB["OH_diffuser"], A, BRICK["Terminal_Unit"]))
g.add((CHB["UF_diffuse"], A, BRICK["Underfloor_Air_Plenum"]))
g.add((CHB["damper_exhaust"], A, BRICK["Exhaust_Damper"]))
g.add((CHB["damper_return"], A, BRICK["Return_Damper"]))
g.add((CHB["fan_exhaust"], A, BRICK["Exhaust_Fan"]))
g.add((CHB["H_1"], A, BRICK["Humidifier"]))
g.add((CHB["HW_coil"], A, BRICK["Hot_Water_Coil"]))
g.add((CHB["CHW_coil"], A, BRICK["Chilled_Water_Coil"]))
g.add((CHB["damper_supply"], A, BRICK["Damper"]))
g.add((CHB["fan_supply"], A, BRICK["Supply_Fan"]))
g.add((CHB["damper_out"], A, BRICK["Outside_Damper"]))
g.add((CHB["VFD_supply"], A, BRICK["Fan_VFD"]))
g.add((CHB["VFD_exhaust"], A, BRICK["Fan_VFD"]))

# Air-cooled chiller
g.add((CHB["CH_1"], A, BRICK["Chiller"]))
g.add((CHB["CHW_pump_1"], A, BRICK["Chilled_Water_Pump"]))
g.add((CHB["CHW_valve_S1"], A, BRICK["Chilled_Water_Valve"]))
g.add((CHB["CHW_pump_2"], A, BRICK["Chilled_Water_Pump"]))
g.add((CHB["CHW_valve_S2"], A, BRICK["Chilled_Water_Valve"]))
g.add((CHB["CHW_valve_SC"], A, BRICK["Chilled_Water_Valve"]))
g.add((CHB["CHW_valve_A"], A, BRICK["Chilled_Water_Valve"]))
g.add((CHB["RCHWS_valve"], A, BRICK["Chilled_Water_Valve"]))
g.add((CHB["CHW_pump_3"], A, BRICK["Chilled_Water_Pump"]))
g.add((CHB["CHWR_valve"], A, BRICK["Chilled_Water_Valve"]))

# Electric water heater
g.add((CHB["WH_1"], A, BRICK["Water_Heater"]))
g.add((CHB["HW_pump_1"], A, BRICK["Hot_Water_pump"]))
g.add((CHB["HW_valve_S1"], A, BRICK["Hot_Water_Valve"]))
g.add((CHB["HW_valve_A"], A, BRICK["Hot_Water_Valve"]))
g.add((CHB["RHWS_valve"], A, BRICK["Hot_Water_Valve"]))
g.add((CHB["HW_pump_2"], A, BRICK["Hot_Water_Pump"]))
g.add((CHB["HWR_valve"], A, BRICK["Return_Heating_Valve"]))

# Radient System
g.add((CHB["RW_pump"], A, BRICK["Water_Pump"]))
g.add((CHB["RP"], A, BRICK["Radiant_Ceiling_Panel"]))
g.add((CHB["RHWR_valve"], A, BRICK["Return_Heating_Valve"]))
g.add((CHB["RCHWR_valve"], A, BRICK["Chilled_Water_Valve"]))

# Spot cooling
g.add((CHB["damper_SC_supply"], A, BRICK["Damper"]))
g.add((CHB["CHW_SC_coil"], A, BRICK["Chilled_Water_Coil"]))
g.add((CHB["VAV"], A, BRICK["Variable_Air_Volume_Box"]))
g.add((CHB["damper_SC_VAV"], A, BRICK["Damper"]))
g.add((CHB["CHWR_valve_SC"], A, BRICK["Chilled_Water_Valve"]))

# Annular system
g.add((CHB["ahu_A"], A, BRICK["Air_Handling_Unit"]))
g.add((CHB["VFD_A_supply"], A, BRICK["Fan_VFD"]))
g.add((CHB["fan_A_supply"], A, BRICK["Supply_Fan"]))
g.add((CHB["CHW_A_coil"], A, BRICK["Chilled_Water_Coil"]))
g.add((CHB["CHWR_valve_A"], A, BRICK["Chilled_Water_Valve"]))
g.add((CHB["HW_A_coil"], A, BRICK["Hot_Water_Coil"]))
g.add((CHB["HWR_valve_A"], A, BRICK["Hot_Water_Valve"]))
g.add((CHB["A_diffuser"], A, BRICK["Terminal_Unit"]))

######################################
#### General Sensor Specification ####
######################################
# Air ventilation sensor
g.add((CHB["T_out"], A, BRICK["Intake_Air_Temperature_Sensor"]))
g.add((CHB["AF_out"], A, BRICK["Outside_Air_Flow_Sensor"]))
g.add((CHB["RH_out"], A, BRICK["Outside_Air_Humidity_Sensor"]))
g.add((CHB["Pos_DO"], A, BRICK["Damper_Position_Sensor"]))
g.add((CHB["SP_duct"], A, BRICK["Static_Pressure_Sensor"]))
g.add((CHB["T_mix"], A, BRICK["Mixed_Air_Temperature_Sensor"]))
g.add((CHB["Speed_SF"], A, BRICK["Motor_Speed_Sensor"]))
g.add((CHB["Start_SF"], A, BRICK["Fan_On_Off_Status"]))
g.add((CHB["P_DS"], A, BRICK["Damper_Position_Sensor"]))
g.add((CHB["T_CA"], A, BRICK["Preheat_Supply_Air_Temperature_Sensor"]))
g.add((CHB["T_SA"], A, BRICK["Supply_Air_Temperature_Sensor"]))
g.add((CHB["Perc_steam"], A, BRICK["Steam_Usage_Sensor"]))
g.add((CHB["Enable_steam"], A, BRICK["Steam_On_Off_Command"]))
g.add((CHB["RH_SA"], A, BRICK["Supply_Air_Humidity_Sensor"]))
g.add((CHB["T_OHSA"], A, BRICK["Supply_Air_Temperature_Sensor"]))
g.add((CHB["AF_OH"], A, BRICK["Supply_Air_Flow_Sensor"]))
g.add((CHB["T_UFSA"], A, BRICK["Underfloor_Air_Temperature_Sensor"]))
g.add((CHB["AF_UF"], A, BRICK["Supply_Air_Flow_Sensor"]))
g.add((CHB["Pos_DR"], A, BRICK["Damper_Position_Sensor"]))
g.add((CHB["T_RA"], A, BRICK["Return_Air_Temperature_Sensor"]))
g.add((CHB["Pos_DE"], A, BRICK["Damper_Position_Sensor"]))
g.add((CHB["Speed_EF"], A, BRICK["Motor_Speed_Sensor"]))
g.add((CHB["Start_EF"], A, BRICK["Fan_On_Off_Status"]))

# Zone sensor
g.add((CHB["RH_zone"], A, BRICK["Zone_Air_Humidity_Sensor"]))
g.add((CHB["T_zone"], A, BRICK["Zone_Air_Temperature_Sensor"]))
g.add((CHB["CO2_zone"], A, BRICK["CO2_Level_Sensor"]))

# Air cooled chiller sensor
g.add((CHB["Enable_CH"], A, BRICK["On_Off_Status"]))
g.add((CHB["RT_PCHW"], A, BRICK["Chilled_Water_Return_Temperature_Sensor"]))
g.add((CHB["Start_CHW_pump_1"], A, BRICK["Pump_On_Off_Status"]))
g.add((CHB["ST_PCHW"], A, BRICK["Chilled_Water_Supply_Temperature_Sensor"]))
g.add((CHB["Pos_CHW_valve_S1"], A, BRICK["Valve_Position_Sensor"]))
g.add((CHB["Start_CHW_pump_2"], A, BRICK["Pump_On_Off_Status"]))
g.add((CHB["Pos_CHW_valve_SC"], A, BRICK["Valve_Position_Sensor"]))
g.add((CHB["Start_CHW_pump_3"], A, BRICK["Pump_On_Off_Status"]))
g.add((CHB["ST_SCHW"], A, BRICK["Chilled_Water_Supply_Temperature_Sensor"]))
g.add((CHB["RT_SCHW"], A, BRICK["Chilled_Water_Return_Temperature_Sensor"]))
g.add((CHB["Pos_CHWR_valve"], A, BRICK["Valve_Position_Sensor"]))
g.add((CHB["Pos_RCHWS_valve"], A, BRICK["Valve_Position_Sensor"]))

# Electric water heater sensor
g.add((CHB["Enable_WH"], A, BRICK["On_Off_Status"]))
g.add((CHB["RT_HW"], A, BRICK["Hot_Water_Return_Temperature_Sensor"]))
g.add((CHB["Start_HW_pump_1"], A, BRICK["Pump_On_Off_Status"]))
g.add((CHB["ST_HW"], A, BRICK["Hot_Water_Supply_Temperature_Sensor"]))
g.add((CHB["Pos_HW_valve_A"], A, BRICK["Valve_Position_Sensor"]))
g.add((CHB["Start_HW_pump_2"], A, BRICK["Pump_On_Off_Status"]))
g.add((CHB["Pos_HWR_valve"], A, BRICK["Valve_Position_Sensor"]))
g.add((CHB["Pos_RHWS_valve"], A, BRICK["Valve_Position_Sensor"]))

# Spot cooling sensor
g.add((CHB["Pos_SC_DS"], A, BRICK["Damper_Position_Sensor"]))
g.add((CHB["T_SC_CA"], A, BRICK["Preheat_Supply_Air_Temperature_Sensor"]))
g.add((CHB["T_SC_SA"], A, BRICK["Supply_Air_Temperature_Sensor"]))
g.add((CHB["AF_SC"], A, BRICK["Supply_Air_Flow_Sensor"]))
g.add((CHB["Pos_SC_VAV_DS"], A, BRICK["Damper_Position_Sensor"]))

# Annular system sensor
g.add((CHB["Speed_A_SF"], A, BRICK["Motor_Speed_Sensor"]))
g.add((CHB["Start_A_SF"], A, BRICK["Fan_On_Off_Status"]))
g.add((CHB["T_A_RA"], A, BRICK["Return_Air_Temperature_Sensor"]))
g.add((CHB["Pos_CHWR_valve_A"], A, BRICK["Valve_Position_Sensor"]))
g.add((CHB["T_A_CA"], A, BRICK["Preheat_Supply_Air_Temperature_Sensor"]))
g.add((CHB["T_A_SA"], A, BRICK["Supply_Air_Temperature_Sensor"]))
g.add((CHB["Pos_HWR_valve_A"], A, BRICK["Valve_Position_Sensor"]))

# Radiant system sensor
g.add((CHB["Start_RW_pump"], A, BRICK["Pump_On_Off_Status"]))
g.add((CHB["Speed_RW_pump"], A, BRICK["Motor_Speed_Sensor"]))
g.add((CHB["T_RWS"], A, BRICK["Water_Temperature_Sensor"]))
g.add((CHB["Meter_WF"], A, BRICK["Building_Water_Meter"]))
g.add((CHB["T_RWR"], A, BRICK["Return_Water_Temperature_Sensor"]))
g.add((CHB["Pos_RHWR_valve"], A, BRICK["Valve_Position_Sensor"]))
g.add((CHB["Pos_RCHWR_valve"], A, BRICK["Valve_Position_Sensor"]))

##############################################
#### Equipment Relationship Specification ####
##############################################
# Building site
g.add((CHB["site"], BRICK.hasPart, CHB["building"]))
g.add((CHB["building"], BRICK.hasPart, CHB["chamber_room"]))
g.add((CHB["zone"], BRICK.hasPart, CHB["chamber_room"]))

# Air ventilation
g.add((CHB["ahu"], BRICK.hasPart, CHB["OH_diffuser"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["UF_diffuser"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["damper_exhaust"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["damper_return"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["fan_exhaust"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["H_1"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["HW_coil"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["CHW_coil"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["damper_supply"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["fan_supply"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["damper_out"]))
g.add((CHB["fan_exhaust"], BRICK.hasPart, CHB["VFD_exhaust"]))
g.add((CHB["damper_out"], BRICK.feeds, CHB["fan_supply"]))
g.add((CHB["fan_supply"], BRICK.feeds, CHB["damper_supply"]))
g.add((CHB["damper_supply"], BRICK.feeds, CHB["CHW_coil"]))
g.add((CHB["CHW_coil"], BRICK.feeds, CHB["HW_coil"]))
g.add((CHB["HW_coil"], BRICK.feeds, CHB["H_1"]))
g.add((CHB["H_1"], BRICK.feeds, CHB["OH_diffuser"]))
g.add((CHB["H_1"], BRICK.feeds, CHB["UF_diffuser"]))
g.add((CHB["OH_diffuser"], BRICK.feeds, CHB["zone"]))
g.add((CHB["UF_diffuser"], BRICK.feeds, CHB["zone"]))
g.add((CHB["zone"], BRICK.feeds, CHB["damper_return"]))
g.add((CHB["zone"], BRICK.feeds, CHB["damper_exhaust"]))
g.add((CHB["damper_return"], BRICK.feeds, CHB["fan_supply"]))
g.add((CHB["damper_exahust"], BRICK.feeds, CHB["fan_exahust"]))

# Air cooled chiller
g.add((CHB["CH_1"], BRICK.feeds, CHB["CHW_pump_1"]))
g.add((CHB["CHW_pump_1"], BRICK.feeds, CHB["CHW_valve_1"]))
g.add((CHB["CHW_valve_1"], BRICK.feeds, CHB["CHW_pump_2"]))
g.add((CHB["CHW_pump_2"], BRICK.feeds, CHB["CHW_valve_2"]))
g.add((CHB["CHW_valve_2"], BRICK.feeds, CHB["CHW_pump_3"]))
g.add((CHB["CHW_pump_3"], BRICK.feeds, CHB["CHW_coil"]))
g.add((CHB["CHW_coil"], BRICK.feeds, CHB["CHWR_valve"]))

# Electric water heater
g.add((CHB["WH_1"], BRICK.feeds, CHB["HW_pump_1"]))
g.add((CHB["HW_pump_1"], BRICK.feeds, CHB["HW_valve_1"]))
g.add((CHB["HW_valve_1"], BRICK.feeds, CHB["HW_pump_2"]))
g.add((CHB["HW_pump_2"], BRICK.feeds, CHB["HW_coil"]))
g.add((CHB["HW_coil"], BRICK.feeds, CHB["HWR_valve"]))

# Spot cooling
g.add((CHB["damper_SC_supply"], BRICK.feeds, CHB["CHW_SC_coil"]))
g.add((CHB["CHW_SC_coil"], BRICK.feeds, CHB["VAV"]))
g.add((CHB["CHW_SC_coil"], BRICK.feeds, CHB["CHWR_valve_SC"]))
g.add((CHB["CHWR_valve_SC"], BRICK.feeds, CHB["CH_1"]))
g.add((CHB["VAV"], BRICK.hasPart, CHB["damper_SC_VAV"]))
g.add((CHB["VAV"], BRICK.feeds, CHB["damper_SC_VAV"]))
g.add((CHB["damper_SC_supply"], BRICK.feeds, CHB["zone"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["damper_SC_supply"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["CHW_SC_coil"]))
g.add((CHB["ahu"], BRICK.hasPart, CHB["VAV"]))

# Annular system
g.add((CHB["ahu_A"], BRICK.hasPart, CHB["fan_A_supply"]))
g.add((CHB["ahu_A"], BRICK.hasPart, CHB["CHW_A_coil"]))
g.add((CHB["ahu_A"], BRICK.hasPart, CHB["HW_A_coil"]))
g.add((CHB["ahu_A"], BRICK.hasPart, CHB["A_diffuser"]))
g.add((CHB["fan_A_supply"], BRICK.hasPart, CHB["VFD_A_supply"]))
g.add((CHB["fan_A_supply"], BRICK.feeds, CHB["CHW_A_coil"]))
g.add((CHB["CHW_A_coil"], BRICK.feeds, CHB["CHWR_valve_A"]))
g.add((CHB["CHWR_valve_A"], BRICK.feeds, CHB["CH_1"]))
g.add((CHB["CHW_A_coil"], BRICK.feeds, CHB["HW_A_coil"]))
g.add((CHB["HW_A_coil"], BRICK.feeds, CHB["HWR_valve_A"]))
g.add((CHB["HWR_valve_A"], BRICK.feeds, CHB["WH_1"]))
g.add((CHB["HW_A_coil"], BRICK.feeds, CHB["A_diffuser"]))

# Radiant system
g.add((CHB["RW_pump"], BRICK.feeds, CHB["RP"]))
g.add((CHB["RP"], BRICK.feeds, CHB["RHWR_valve"]))
g.add((CHB["RP"], BRICK.feeds, CHB["WH_1"]))
g.add((CHB["RP"], BRICK.feeds, CHB["RCHWR_valve"]))
g.add((CHB["RCHWR_valve"], BRICK.feeds, CHB["CH_1"]))

####################################################################################
#### Sensor Relationship Specification (without upstream or downstream details) ####
####################################################################################
# Air ventilation system
g.add((CHB["ahu"], BRICK.hasPoint, CHB["T_out"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["AF_out"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["RH_out"]))
g.add((CHB["damper_out"], BRICK.hasPoint, CHB["Pos_DO"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["SP_duct"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["T_mix"]))
g.add((CHB["VFD_supply"], BRICK.hasPoint, CHB["Speed_SF"]))
g.add((CHB["VFD_supply"], BRICK.hasPoint, CHB["Start_SF"]))
g.add((CHB["damper_supply"], BRICK.hasPoint, CHB["Pos_DS"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["T_CA"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["T_SA"]))
# No duct heater sensor
g.add((CHB["H_1"], BRICK.hasPoint, CHB["Perc_steam"]))
g.add((CHB["H_1"], BRICK.hasPoint, CHB["Enable_steam"]))
g.add((CHB["H_1"], BRICK.hasPoint, CHB["RH_SA"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["T_OHSA"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["AF_OH"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["T_UFSA"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["AF_UF"]))
g.add((CHB["damper_return"], BRICK.hasPoint, CHB["Pos_DR"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["T_RA"]))
g.add((CHB["damper_exhaust"], BRICK.hasPoint, CHB["Pos_DE"]))
g.add((CHB["VFD_exhaust"], BRICK.hasPoint, CHB["Speed_EF"]))
g.add((CHB["VFD_exhaust"], BRICK.hasPoint, CHB["Start_EF"]))

# Zone sensor
g.add((CHB["zone"], BRICK.hasPoint, CHB["RH_zone"]))
g.add((CHB["zone"], BRICK.hasPoint, CHB["T_zone"]))
g.add((CHB["zone"], BRICK.hasPoint, CHB["CO2_zone"]))

# Spot cooling sensor
g.add((CHB["damper_SC_supply"], BRICK.hasPoint, CHB["Pos_SC_DS"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["T_SC_CA"]))
g.add((CHB["VAV"], BRICK.hasPoint, CHB["T_SC_SA"]))
g.add((CHB["VAV"], BRICK.hasPoint, CHB["AF_SC"]))
g.add((CHB["damper_SC_VAV"], BRICK.hasPoint, CHB["Pos_SC_VAV"]))

# Annular system
g.add((CHB["VFD_A_supply"], BRICK.hasPoint, CHB["Speed_A_SF"]))
g.add((CHB["VFD_A_supply"], BRICK.hasPoint, CHB["Start_A-SF"]))
g.add((CHB["ahu_A"], BRICK.hasPoint, CHB["T_A_RA"]))
g.add((CHB["CHWR_valve_A"], BRICK.hasPoint, CHB["Pos_CHWR_valve_A"]))
g.add((CHB["ahu_A"], BRICK.hasPoint, CHB["T_A_CA"]))
g.add((CHB["ahu_A"], BRICK.hasPoint, CHB["T_A_SA"]))
g.add((CHB["HWR_valve_A"], BRICK.hasPoint, CHB["Pos_HWR_valve_A"]))

# Radiant system
g.add((CHB["RW_pump"], BRICK.hasPoint, CHB["Start_RW_pump"]))
g.add((CHB["RW_pump"], BRICK.hasPoint, CHB["Speed_RW_pump"]))
g.add((CHB["RHWR_valve"], BRICK.hasPoint, CHB["Pos_RHWR_valve"]))
g.add((CHB["RCHWR_valve"], BRICK.hasPoint, CHB["Pos_RCHWR_valve"]))

# Air cooled chiller
g.add((CHB["CH_1"], BRICK.hasPoint, CHB["Enable_CH"]))
g.add((CHB["CH_1"], BRICK.hasPoint, CHB["RT_PCHW"]))
g.add((CHB["CHW_pump_1"], BRICK.hasPoint, CHB["Start_CHW_pump_1"]))
g.add((CHB["CH_1"], BRICK.hasPoint, CHB["ST_PCHW"]))
g.add((CHB["CHW_valve_S1"], BRICK.hasPoint, CHB["Pos_CHW_valve_S1"]))
g.add((CHB["CHW_pump_2"], BRICK.hasPoint, CHB["Start_CHW_pump_2"]))
g.add((CHB["CHW_valve_SC"], BRICK.hasPoint, CHB["Pos_CHW_valve_SC"]))
g.add((CHB["CHW_pump_3"], BRICK.hasPoint, CHB["Start_CHW_pump_3"]))
g.add((CHB["CH_1"], BRICK.hasPoint, CHB["ST_SCHW"]))
g.add((CHB["CH_1"], BRICK.hasPoint, CHB["RT_SCHW"]))
g.add((CHB["CHWR_valve"], BRICK.hasPoint, CHB["Pos_CHWR_valve"]))
g.add((CHB["RCHWS_valve"], BRICK.hasPoint, CHB["Pos_RCHWS_valve"]))

# Electric heater
g.add((CHB["WH_1"], BRICK.hasPoint, CHB["Enable_WH"]))
g.add((CHB["WH_1"], BRICK.hasPoint, CHB["RT_HW"]))
g.add((CHB["HW_pump_1"], BRICK.hasPoint, CHB["Start_HW_pump_1"]))
g.add((CHB["WH_1"], BRICK.hasPoint, CHB["ST_HW"]))
g.add((CHB["HW_valve_A"], BRICK.hasPoint, CHB["Pos_HW_valve_A"]))
g.add((CHB["HW_pump_2"], BRICK.hasPoint, CHB["Start_HW_pump_2"]))
g.add((CHB["HWR_valve"], BRICK.hasPoint, CHB["Pos_HWR_valve"]))
g.add((CHB["RHWS_valve"], BRICK.hasPoint, CHB["Pos_RHWS_valve"]))

################################
#### Setpoint Specification ####
################################
# Zone State
g.add((CHB["ZAHT_stp"], A, BRICK["Zone_Air_Heating_Temperature_Setpoint"]))
g.add((CHB["ZACT_stp"], A, BRICK["Zone_Air_Cooling_Temperature_Setpoint"]))
g.add((CHB["ZAH_stp"], A, BRICK["Zone_Air_Humidity_Setpoint"]))

# Chamber Air System
g.add((CHB["SAT_stp"], A, BRICK["Supply_Air_Temperature_Setpoint"]))
g.add((CHB["DAT_stp"], A, BRICK["Discharge_Air_Temperature_Setpoint"]))
g.add((CHB["min_OAF_stp"], A, BRICK["Min_Outside_Air_Flow_Setpoint_Limit"]))

# Annular System
g.add((CHB["SAT_A_stp"], A, BRICK["Supply_Air_Temperature_Setpoint"]))

# Spot Conditioning System
g.add((CHB["SAT_SC_stp"], A, BRICK["Supply_Air_Temperature_Setpoint"]))
g.add((CHB["AF_SC_stp"], A, BRICK["Cooling_Supply_Air_Flow_Setpoint"]))
g.add((CHB["AF_VAV_stp"], A, BRICK["Supply_Air_Flow_Setpoint"]))

# Radiant System
g.add((CHB["RPT_stp"], A, BRICK["Radiant_Panel_Temperature_Setpoint"]))
g.add((CHB["SWT_stp"], A, BRICK["Supply_Water_Temperature_Setpoint"]))
g.add((CHB["WF_stp"], A, BRICK["Water_Flow_Setpoint"]))

# Air-Cooled Chilled Water
g.add((CHB["CHWST_stp"], A, BRICK["Chilled_Water_Supply_Temperature_Setpoint"]))

# Hot Water Heating Plant
g.add((CHB["HWST_stp"], A, BRICK["Hot_Water_Supply_Temperature_Setpoint"]))

#############################################
#### Setpoint Relationship Specification ####
#############################################
# Zone State
g.add((CHB["zone"], BRICK.hasPoint, CHB["ZAHT_stp"]))
g.add((CHB["zone"], BRICK.hasPoint, CHB["ZACT_stp"]))
g.add((CHB["zone"], BRICK.hasPoint, CHB["ZAH_stp"]))

# Chamber Air System
g.add((CHB["ahu"], BRICK.hasPoint, CHB["SAT_stp"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["DAT_stp"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["min_OAF_stp"]))

# Annular System
g.add((CHB["ahu_A"], BRICK.hasPoint, CHB["SAT_A_stp"]))

# Spot Conditioning System
g.add((CHB["ahu"], BRICK.hasPoint, CHB["SAT_SC_stp"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["AF_SC_stp"]))
g.add((CHB["ahu"], BRICK.hasPoint, CHB["AF_VAV_stp"]))

# Radiant System
g.add((CHB["RP"], BRICK.hasPoint, CHB["RPT_stp"]))
g.add((CHB["RP"], BRICK.hasPoint, CHB["WF_stp"]))

# Air-Cooled Chilled Water
g.add((CHB["CH_1"], BRICK.hasPoint, CHB["CHWST_stp"]))

# Hot Water Heating Plant
g.add((CHB["WH_1"], BRICK.hasPoint, CHB["HWST_stp"]))

print('starting generating ...')
g.expand(profile="owlrl")
g.serialize('./chamber_brick.ttl')
print('brick model exported')