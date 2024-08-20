import brickschema
from brickschema.namespaces import A, BRICK
from rdflib import Namespace

# Brick:Environment_Box has definition related to Laboratory which also known as climate chamber
# Namespace definition and binding could be found at: https://rdflib.readthedocs.io/en/stable/namespaces_and_bindings.html
# and at: https://www.ibm.com/docs/en/db2/11.5?topic=prolog-namespace-declaration

def make():
    CHB = Namespace("http://berkeley.edu/climatechamber#")
    REC = Namespace("http://example.org/rec#")
    g = brickschema.Graph(load_brick=True, load_brick_nightly=True)
    g.load_file('./readfiles/Brick.ttl')
    g.bind('chamber', CHB)
    g.bind('brick', BRICK)
    g.bind("rec", REC)


    #########################################
    #### General Equipment Specification ####
    #########################################
    # Building site 
    g.add((CHB["UCB"], A, BRICK["Site"]))
    g.add((CHB['wurster_hall'], A, BRICK["Building"]))
    g.add((CHB["chamber_room"], A, BRICK["Environment_Box"]))
    g.add((CHB["Zone"], A, BRICK["HVAC_Zone"]))

    # Meter
    g.add((CHB["Meter_C"], A, BRICK["Meter"]))

    # Air ventilation
    g.add((CHB["AHU_C"], A, BRICK["Air_Handling_Unit"]))
    g.add((CHB["OH_diffuser"], A, BRICK["Terminal_Unit"]))
    g.add((CHB["UF_diffuser"], A, BRICK["Underfloor_Air_Plenum"]))
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
    g.add((CHB["CHW_L"], A, BRICK["Chilled_Water_Loop"]))
    g.add((CHB["PCHW_L"], A, BRICK["Chilled_Water_Loop"]))
    g.add((CHB["SCHW_L"], A, BRICK["Chilled_Water_Loop"]))
    g.add((CHB["CHW_pump_1"], A, BRICK["Chilled_Water_Pump"]))
    g.add((CHB["CHW_valve_mix"], A, BRICK["Chilled_Water_Valve"]))
    g.add((CHB["CHW_pump_2"], A, BRICK["Chilled_Water_Pump"]))
    g.add((CHB["CHW_valve_S2"], A, BRICK["Chilled_Water_Valve"]))
    g.add((CHB["CHW_valve_SC"], A, BRICK["Chilled_Water_Valve"]))
    g.add((CHB["CHW_valve_A"], A, BRICK["Chilled_Water_Valve"]))
    g.add((CHB["RCHWS_valve"], A, BRICK["Chilled_Water_Valve"]))
    g.add((CHB["CHW_pump_3"], A, BRICK["Chilled_Water_Pump"]))
    g.add((CHB["CHW_valve"], A, BRICK["Chilled_Water_Valve"]))

    # Electric water heater
    g.add((CHB["HW_L"], A, BRICK["Hot_Water_Loop"]))
    g.add((CHB["WH_1"], A, BRICK["Boiler"]))
    g.add((CHB["HW_pump_1"], A, BRICK["Hot_Water_Pump"]))
    g.add((CHB["HW_valve_S1"], A, BRICK["Hot_Water_Valve"]))
    g.add((CHB["HW_valve_A"], A, BRICK["Hot_Water_Valve"]))
    g.add((CHB["RHWS_valve"], A, BRICK["Hot_Water_Valve"]))
    g.add((CHB["HW_pump_2"], A, BRICK["Hot_Water_Pump"]))
    g.add((CHB["HW_valve"], A, BRICK["Hot_Water_Valve"]))

    # Radient System
    g.add((CHB["RW_pump"], A, BRICK["Water_Pump"]))
    g.add((CHB["RP"], A, BRICK["Radiant_Ceiling_Panel"]))
    g.add((CHB["RHWR_valve"], A, BRICK["Hot_Water_Valve"]))
    g.add((CHB["RCHWR_valve"], A, BRICK["Chilled_Water_Valve"]))

    # Spot cooling
    g.add((CHB["damper_SC_supply"], A, BRICK["Damper"]))
    g.add((CHB["CHW_SC_coil"], A, BRICK["Chilled_Water_Coil"]))
    g.add((CHB["VAV"], A, BRICK["Variable_Air_Volume_Box"]))
    g.add((CHB["damper_SC_VAV"], A, BRICK["Damper"]))
    g.add((CHB["CHW_valve_SC"], A, BRICK["Chilled_Water_Valve"]))

    # Annular system
    g.add((CHB["AHU_A"], A, BRICK["Air_Handling_Unit"]))
    g.add((CHB["fan_A_supply"], A, BRICK["Supply_Fan"]))
    g.add((CHB["CHW_A_coil"], A, BRICK["Chilled_Water_Coil"]))
    g.add((CHB["CHW_valve_A"], A, BRICK["Chilled_Water_Valve"]))
    g.add((CHB["HW_A_coil"], A, BRICK["Hot_Water_Coil"]))
    g.add((CHB["HW_valve_A"], A, BRICK["Hot_Water_Valve"]))
    g.add((CHB["A_diffuser"], A, BRICK["Terminal_Unit"]))

    ######################################
    #### General Sensor Specification ####
    ######################################
    # Air ventilation sensor
    g.add((CHB["oa_temperature_9"], A, BRICK["Intake_Air_Temperature_Sensor"]))
    g.add((CHB["oa_flow_10"], A, BRICK["Outside_Air_Flow_Sensor"]))
    g.add((CHB["oa_humidity_9"], A, BRICK["Outside_Air_Humidity_Sensor"]))
    g.add((CHB["oa_dmpr_pos_10"], A, BRICK["Damper_Position_Sensor"]))
    g.add((CHB["duct_stat_press_ai_10"], A, BRICK["Static_Pressure_Sensor"]))
    g.add((CHB["ma_temp_10"], A, BRICK["Mixed_Air_Temperature_Sensor"]))
    g.add((CHB["sf_vfd_spd_10"], A, BRICK["Fan_Speed_Command"]))
    g.add((CHB["sf_status_10"], A, BRICK["Fan_On_Off_Status"]))
    g.add((CHB["sf_enable_10"], A, BRICK["Run_Enable_Command"]))
    g.add((CHB["supply_damper_pos_10"], A, BRICK["Damper_Position_Sensor"]))
    g.add((CHB["chamber_cc_temp_10"], A, BRICK["Preheat_Supply_Air_Temperature_Sensor"]))
    g.add((CHB["eff_sa_temp_10"], A, BRICK["Supply_Air_Temperature_Sensor"]))
    g.add((CHB["Perc_steam"], A, BRICK["Steam_Usage_Sensor"]))
    g.add((CHB["RH_SA"], A, BRICK["Supply_Air_Humidity_Sensor"]))
    g.add((CHB["overhead_sa_temp_10"], A, BRICK["Supply_Air_Temperature_Sensor"]))
    g.add((CHB["oh_airflow_10"], A, BRICK["Supply_Air_Flow_Sensor"]))
    g.add((CHB["oh_fpm_10"], A, BRICK["Supply_Air_Velocity_Pressure_Sensor"]))
    g.add((CHB["underfloor_sa_temp_10"], A, BRICK["Underfloor_Air_Temperature_Sensor"]))
    g.add((CHB["uf_airflow_10"], A, BRICK["Supply_Air_Flow_Sensor"]))
    g.add((CHB["uf_fpm_10"], A, BRICK["Supply_Air_Velocity_Pressure_Sensor"]))
    g.add((CHB["ra_dmpr_pos_10"], A, BRICK["Damper_Position_Sensor"]))
    g.add((CHB["ra_temp_10"], A, BRICK["Return_Air_Temperature_Sensor"]))
    g.add((CHB["ea_dmpr_pos_10"], A, BRICK["Damper_Position_Sensor"]))
    g.add((CHB["ef_vfd_spd_10"], A, BRICK["Fan_Speed_Command"]))
    g.add((CHB["ef_ss_10"], A, BRICK["Start_Stop_Command"]))
    g.add((CHB["h_1_enable_10"], A, BRICK["Humidify_Command"]))
    g.add((CHB["chw_valve_10"], A, BRICK["Valve_Position_Sensor"]))
    g.add((CHB["run_stop_8"], A, BRICK["Run_Status"]))
    g.add((CHB["run_enable_8"], A, BRICK["Enable_Status"]))
    g.add((CHB["run_stop_7"], A, BRICK["Run_Status"]))
    g.add((CHB["run_enable_7"], A, BRICK["Enable_Status"]))
    g.add((CHB["power_8"], A, BRICK["Power_Sensor"]))
    g.add((CHB["power_7"], A, BRICK["Power_Sensor"]))

    	

    # Zone sensor
    g.add((CHB["chamber_rh_10"], A, BRICK["Zone_Air_Humidity_Sensor"]))
    g.add((CHB["zone_temp_10"], A, BRICK["Zone_Air_Temperature_Sensor"]))
    g.add((CHB["zone_co2_10"], A, BRICK["CO2_Level_Sensor"]))

    # Air cooled chiller sensor
    g.add((CHB["ch1_ss_1"], A, BRICK["On_Off_Status"]))
    g.add((CHB["chwp1_ss_1"], A, BRICK["Pump_On_Off_Status"]))
    g.add((CHB["mix_vlv_pos_1"], A, BRICK["Valve_Position_Sensor"]))
    g.add((CHB["chwp2_ss_1"], A, BRICK["Pump_On_Off_Status"]))
    g.add((CHB["chwp3_ss_1"], A, BRICK["Pump_On_Off_Status"]))
    g.add((CHB["schws_temp_1"], A, BRICK["Leaving_Chilled_Water_Temperature_Sensor"]))
    g.add((CHB["schwr_temp_1"], A, BRICK["Entering_Chilled_Water_Temperature_Sensor"]))
    g.add((CHB["pchws_temp_1"], A, BRICK["Leaving_Chilled_Water_Temperature_Sensor"]))
    g.add((CHB["pchwr_temp_1"], A, BRICK["Entering_Chilled_Water_Temperature_Sensor"]))

    g.add((CHB["Pos_RCHWS_valve"], A, BRICK["Valve_Position_Sensor"]))

    # Electric water heater sensor
    g.add((CHB["Enable_WH"], A, BRICK["On_Off_Status"]))
    g.add((CHB["RT_HW"], A, BRICK["Entering_Hot_Water_Temperature_Sensor"]))
    g.add((CHB["Start_HW_pump_1"], A, BRICK["Pump_On_Off_Status"]))
    g.add((CHB["ST_HW"], A, BRICK["Leaving_Hot_Water_Temperature_Sensor"]))
    g.add((CHB["hw_valve_10"], A, BRICK["Valve_Position_Sensor"]))
    g.add((CHB["hwp2_ss_2"], A, BRICK["Pump_On_Off_Status"]))
    g.add((CHB["Pos_HWR_valve"], A, BRICK["Valve_Position_Sensor"]))
    g.add((CHB["Pos_RHWS_valve"], A, BRICK["Valve_Position_Sensor"]))

    # Spot cooling sensor
    g.add((CHB["spot_clg_vlv_pos_6"], A, BRICK["Valve_Position_Sensor"]))
    g.add((CHB["spot_clg_dmpr_pos_ao_6"], A, BRICK["Damper_Position_Sensor"]))
    g.add((CHB["spot_cc_temp_6"], A, BRICK["Preheat_Supply_Air_Temperature_Sensor"]))
    g.add((CHB["spot_clg_sa_temp_6"], A, BRICK["Supply_Air_Temperature_Sensor"]))
    g.add((CHB["vav_cfm_6"], A, BRICK["Supply_Air_Flow_Sensor"]))
    g.add((CHB["vav_dmpr_pos_6"], A, BRICK["Damper_Position_Sensor"]))

    # Annular system sensor
    g.add((CHB["sf_enable_1"], A, BRICK["Run_Enable_Command"]))
    g.add((CHB["sf_status_1"], A, BRICK["Fan_On_Off_Status"]))
    g.add((CHB["ra_temp_1"], A, BRICK["Return_Air_Temperature_Sensor"]))
    g.add((CHB["chw_valve_1"], A, BRICK["Valve_Position_Sensor"]))
    g.add((CHB["ann_cc_temp_1"], A, BRICK["Preheat_Supply_Air_Temperature_Sensor"]))
    g.add((CHB["sa_temp_1"], A, BRICK["Supply_Air_Temperature_Sensor"]))
    g.add((CHB["hw_valve_1"], A, BRICK["Valve_Position_Sensor"]))

    # Radiant system sensor
    g.add((CHB["Start_RW_pump"], A, BRICK["Pump_On_Off_Status"]))
    g.add((CHB["Speed_RW_pump"], A, BRICK["Motor_Speed_Sensor"]))
    g.add((CHB["T_RWS"], A, BRICK["Water_Temperature_Sensor"]))
    g.add((CHB["T_RWR"], A, BRICK["Entering_Water_Temperature_Sensor"]))
    g.add((CHB["Pos_RHWR_valve"], A, BRICK["Valve_Position_Sensor"]))
    g.add((CHB["Pos_RCHWR_valve"], A, BRICK["Valve_Position_Sensor"]))

    ##############################################
    #### Equipment Relationship Specification ####
    ##############################################
    # Building site
    g.add((CHB["UCB"], BRICK.hasPart, CHB["wurster_hall"]))
    g.add((CHB["wurster_hall"], BRICK.hasPart, CHB["chamber_room"]))
    g.add((CHB["chamber_room"], BRICK.hasPart, CHB["Zone"]))

    # Air ventilation
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["OH_diffuser"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["UF_diffuser"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["damper_exhaust"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["damper_return"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["fan_exhaust"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["H_1"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["HW_coil"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["CHW_coil"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["damper_supply"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["fan_supply"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["damper_out"]))
    g.add((CHB["fan_exhaust"], BRICK.hasPart, CHB["VFD_exhaust"]))
    g.add((CHB["damper_out"], BRICK.feeds, CHB["fan_supply"]))
    g.add((CHB["fan_supply"], BRICK.feeds, CHB["damper_supply"]))
    g.add((CHB["fan_supply"], BRICK.hasPart, CHB["VFD_supply"]))
    g.add((CHB["damper_supply"], BRICK.feeds, CHB["CHW_coil"]))
    g.add((CHB["CHW_coil"], BRICK.hasPart, CHB["CHW_valve"]))
    g.add((CHB["CHW_coil"], BRICK.feeds, CHB["HW_coil"]))
    g.add((CHB["HW_coil"], BRICK.feeds, CHB["AHU_C"]))
    g.add((CHB["HW_coil"], BRICK.hasPart, CHB["HW_valve"]))
    g.add((CHB["HW_coil"], BRICK.feeds, CHB["H_1"]))
    g.add((CHB["H_1"], BRICK.feeds, CHB["OH_diffuser"]))
    g.add((CHB["H_1"], BRICK.feeds, CHB["UF_diffuser"]))
    g.add((CHB["OH_diffuser"], BRICK.feeds, CHB["Zone"]))
    g.add((CHB["UF_diffuser"], BRICK.feeds, CHB["Zone"]))
    g.add((CHB["Zone"], BRICK.feeds, CHB["damper_return"]))
    g.add((CHB["Zone"], BRICK.feeds, CHB["damper_exhaust"]))
    g.add((CHB["damper_return"], BRICK.feeds, CHB["fan_supply"]))
    g.add((CHB["damper_exahust"], BRICK.feeds, CHB["fan_exahust"]))

    # Air cooled chiller
    g.add((CHB["CHW_L"], BRICK.feeds, CHB["PCHW_L"]))
    g.add((CHB["CHW_L"], BRICK.feeds, CHB["SCHW_L"]))
    g.add((CHB["CH_1"], BRICK.feeds, CHB["PCHW_L"]))
    g.add((CHB["PCHW_L"], BRICK.feeds, CHB["SCHW_L"]))
    g.add((CHB["PCHW_L"], BRICK.hasPart, CHB["CHW_pump_1"]))
    g.add((CHB["SCHW_L"], BRICK.hasPart, CHB["CHW_pump_2"]))
    g.add((CHB["SCHW_L"], BRICK.hasPart, CHB["CHW_pump_3"]))
    g.add((CHB["SCHW_L"], BRICK.feeds, CHB["CHW_coil"]))
    g.add((CHB["SCHW_L"], BRICK.feeds, CHB["CHW_A_coil"]))
    g.add((CHB["SCHW_L"], BRICK.feeds, CHB["CHW_SC_coil"]))
    g.add((CHB["PCHW_L"], BRICK.hasPart, CHB["CHW_valve_mix"]))
    g.add((CHB["SCHW_L"], BRICK.hasPart, CHB["CHW_valve_S2"]))

    g.add((CHB["CH_1"], BRICK.feeds, CHB["CHW_pump_1"]))
    g.add((CHB["CHW_pump_1"], BRICK.feeds, CHB["CHW_pump_2"]))
    g.add((CHB["CHW_pump_2"], BRICK.feeds, CHB["CHW_A_coil"]))
    g.add((CHB["CHW_pump_2"], BRICK.feeds, CHB["CHW_SC_coil"]))
    g.add((CHB["CHW_pump_2"], BRICK.feeds, CHB["CHW_pump_3"]))
    g.add((CHB["CHW_pump_3"], BRICK.feeds, CHB["CHW_coil"]))

    # Electric water heater
    g.add((CHB["WH_1"], BRICK.feeds, CHB["HW_L"]))
    g.add((CHB["HW_L"], BRICK.hasPart, CHB["HW_pump_1"]))
    g.add((CHB["HW_L"], BRICK.hasPart, CHB["HW_pump_2"]))
    g.add((CHB["WH_1"], BRICK.feeds, CHB["HW_pump_1"]))
    g.add((CHB["HW_pump_1"], BRICK.feeds, CHB["HW_A_coil"]))
    g.add((CHB["HW_pump_1"], BRICK.feeds, CHB["HW_pump_2"]))
    g.add((CHB["HW_pump_2"], BRICK.feeds, CHB["HW_coil"]))
    g.add((CHB["HW_L"], BRICK.hasPart, CHB["HW_valve_S1"]))
    
    g.add((CHB["HW_L"], BRICK.feeds, CHB["HW_coil"]))
    g.add((CHB["HW_coil"], BRICK.feeds, CHB["Zone"]))

    # Spot cooling
    g.add((CHB["damper_SC_supply"], BRICK.feeds, CHB["CHW_SC_coil"]))
    g.add((CHB["CHW_SC_coil"], BRICK.feeds, CHB["VAV"]))
    g.add((CHB["CHW_SC_coil"], BRICK.hasPart, CHB["CHW_valve_SC"]))
    g.add((CHB["VAV"], BRICK.hasPart, CHB["damper_SC_VAV"]))
    g.add((CHB["damper_SC_supply"], BRICK.feeds, CHB["Zone"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["damper_SC_supply"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["CHW_SC_coil"]))
    g.add((CHB["AHU_C"], BRICK.hasPart, CHB["VAV"]))

    # Annular system
    g.add((CHB["AHU_A"], BRICK.hasPart, CHB["fan_A_supply"]))
    g.add((CHB["AHU_A"], BRICK.hasPart, CHB["CHW_A_coil"]))
    g.add((CHB["AHU_A"], BRICK.hasPart, CHB["HW_A_coil"]))
    g.add((CHB["AHU_A"], BRICK.hasPart, CHB["A_diffuser"]))
    g.add((CHB["fan_A_supply"], BRICK.feeds, CHB["CHW_A_coil"]))
    g.add((CHB["CHW_A_coil"], BRICK.hasPart, CHB["CHW_valve_A"]))
    g.add((CHB["CHW_valve_A"], BRICK.feeds, CHB["CH_1"]))
    g.add((CHB["CHW_A_coil"], BRICK.feeds, CHB["A_diffuser"]))
    g.add((CHB["HW_A_coil"], BRICK.hasPart, CHB["HW_valve_A"]))
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
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["oa_temperature_9"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["oa_flow_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["oa_humidity_9"]))
    g.add((CHB["damper_out"], BRICK.hasPoint, CHB["oa_dmpr_pos_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["duct_stat_press_ai_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["ma_temp_10"]))
    g.add((CHB["VFD_supply"], BRICK.hasPoint, CHB["sf_vfd_spd_10"]))
    g.add((CHB["VFD_supply"], BRICK.hasPoint, CHB["power_8"]))
    g.add((CHB["VFD_supply"], BRICK.hasPoint, CHB["run_stop_8"]))
    g.add((CHB["VFD_supply"], BRICK.hasPoint, CHB["run_enable_8"]))
    g.add((CHB["fan_supply"], BRICK.hasPoint, CHB["sf_status_10"]))
    g.add((CHB["fan_supply"], BRICK.hasPoint, CHB["sf_enable_10"]))
    g.add((CHB["damper_supply"], BRICK.hasPoint, CHB["supply_damper_pos_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["chamber_cc_temp_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["eff_sa_temp_10"]))
    # No duct heater sensor
    g.add((CHB["H_1"], BRICK.hasPoint, CHB["Perc_steam"]))
    g.add((CHB["H_1"], BRICK.hasPoint, CHB["h_1_enable_10"]))
    g.add((CHB["H_1"], BRICK.hasPoint, CHB["RH_SA"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["overhead_sa_temp_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["oh_airflow_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["underfloor_sa_temp_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["uf_airflow_10"]))
    g.add((CHB["damper_return"], BRICK.hasPoint, CHB["ra_dmpr_pos_10"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["ra_temp_10"]))
    g.add((CHB["damper_exhaust"], BRICK.hasPoint, CHB["ea_dmpr_pos_10"]))
    g.add((CHB["VFD_exhaust"], BRICK.hasPoint, CHB["ef_vfd_spd_10"]))
    g.add((CHB["VFD_exhaust"], BRICK.hasPoint, CHB["power_7"]))
    g.add((CHB["VFD_exhaust"], BRICK.hasPoint, CHB["run_stop_7"]))
    g.add((CHB["VFD_exhaust"], BRICK.hasPoint, CHB["run_enable_7"]))
    g.add((CHB["fan_exhaust"], BRICK.hasPoint, CHB["ef_ss_10"]))
    g.add((CHB["OH_diffuser"], BRICK.hasPoint, CHB["overhead_sa_temp_10"]))
    g.add((CHB["OH_diffuser"], BRICK.hasPoint, CHB["oh_airflow_10"]))
    g.add((CHB["OH_diffuser"], BRICK.hasPoint, CHB["oh_fpm_10"]))
    g.add((CHB["UF_diffuser"], BRICK.hasPoint, CHB["underfloor_sa_temp_10"]))
    g.add((CHB["UF_diffuser"], BRICK.hasPoint, CHB["uf_airflow_10"]))
    g.add((CHB["UF_diffuser"], BRICK.hasPoint, CHB["uf_fpm_10"]))

    # Zone sensor
    g.add((CHB["Zone"], BRICK.hasPoint, CHB["chamber_rh_10"]))
    g.add((CHB["Zone"], BRICK.hasPoint, CHB["zone_temp_10"]))
    g.add((CHB["Zone"], BRICK.hasPoint, CHB["zone_co2_10"]))

    # Spot cooling sensor
    g.add((CHB["damper_SC_supply"], BRICK.hasPoint, CHB["spot_clg_dmpr_pos_ao_6"]))
    g.add((CHB["AHU_C"], BRICK.hasPoint, CHB["spot_cc_temp_6"]))
    g.add((CHB["VAV"], BRICK.hasPoint, CHB["vav_cfm_6"]))
    g.add((CHB["damper_SC_VAV"], BRICK.hasPoint, CHB["vav_dmpr_pos_6"]))

    # Annular system
    g.add((CHB["fan_A_supply"], BRICK.hasPoint, CHB["sf_enable_1"]))
    g.add((CHB["fan_A_supply"], BRICK.hasPoint, CHB["sf_status_1"]))
    g.add((CHB["AHU_A"], BRICK.hasPoint, CHB["ra_temp_1"]))
    g.add((CHB["CHW_valve_A"], BRICK.hasPoint, CHB["chw_valve_1"]))
    g.add((CHB["AHU_A"], BRICK.hasPoint, CHB["ann_cc_temp_1"]))
    g.add((CHB["AHU_A"], BRICK.hasPoint, CHB["sa_temp_1"]))
    g.add((CHB["HW_valve_A"], BRICK.hasPoint, CHB["hw_valve_1"]))

    # Radiant system
    g.add((CHB["RW_pump"], BRICK.hasPoint, CHB["Start_RW_pump"]))
    g.add((CHB["RW_pump"], BRICK.hasPoint, CHB["Speed_RW_pump"]))
    g.add((CHB["RHWR_valve"], BRICK.hasPoint, CHB["Pos_RHWR_valve"]))
    g.add((CHB["RCHWR_valve"], BRICK.hasPoint, CHB["Pos_RCHWR_valve"]))

    # Air cooled chiller
    g.add((CHB["CH_1"], BRICK.hasPoint, CHB["ch1_ss_1"]))
    g.add((CHB["CHW_pump_1"], BRICK.hasPoint, CHB["chwp1_ss_1"]))
    g.add((CHB["CHW_valve_mix"], BRICK.hasPoint, CHB["mix_vlv_pos_1"]))
    g.add((CHB["CHW_pump_2"], BRICK.hasPoint, CHB["chwp2_ss_1"]))
    g.add((CHB["CHW_valve_SC"], BRICK.hasPoint, CHB["spot_clg_vlv_pos_6"]))
    g.add((CHB["CHW_pump_3"], BRICK.hasPoint, CHB["chwp3_ss_1"]))
    g.add((CHB["CH_1"], BRICK.hasPoint, CHB["schws_temp_1"]))
    g.add((CHB["CH_1"], BRICK.hasPoint, CHB["schwr_temp_1"]))
    g.add((CHB["CH_1"], BRICK.hasPoint, CHB["pchws_temp_1"]))
    g.add((CHB["CH_1"], BRICK.hasPoint, CHB["pchwr_temp_1"]))
    g.add((CHB["CHW_valve"], BRICK.hasPoint, CHB["chw_valve_10"]))
    g.add((CHB["RCHWS_valve"], BRICK.hasPoint, CHB["Pos_RCHWS_valve"]))

    # Electric heater
    g.add((CHB["WH_1"], BRICK.hasPoint, CHB["Enable_WH"]))
    g.add((CHB["WH_1"], BRICK.hasPoint, CHB["RT_HW"]))
    g.add((CHB["HW_pump_1"], BRICK.hasPoint, CHB["Start_HW_pump_1"]))
    g.add((CHB["WH_1"], BRICK.hasPoint, CHB["ST_HW"]))
    g.add((CHB["HW_valve_A"], BRICK.hasPoint, CHB["hw_valve_10"]))
    g.add((CHB["HW_pump_2"], BRICK.hasPoint, CHB["hwp2_ss_2"]))
    g.add((CHB["HW_valve"], BRICK.hasPoint, CHB["Pos_HWR_valve"]))
    g.add((CHB["RHWS_valve"], BRICK.hasPoint, CHB["Pos_RHWS_valve"]))

    ################################
    #### Setpoint Specification ####
    ################################

    # Air-Cooled Chilled Water
    g.add((CHB["fixed_chws_temp_stpt_1"], A, BRICK["Leaving_Chilled_Water_Temperature_Setpoint"]))

    # Hot Water Heating Plant
    g.add((CHB["HWST_stp"], A, BRICK["Leaving_Hot_Water_Temperature_Setpoint"]))

    #############################################
    #### Setpoint Relationship Specification ####
    #############################################

    # in csv

    # Air-Cooled Chilled Water
    g.add((CHB["CH_1"], BRICK.hasPoint, CHB["fixed_chws_temp_stpt_1"]))

    # Hot Water Heating Plant
    g.add((CHB["WH_1"], BRICK.hasPoint, CHB["HWST_stp"]))

    print('starting generating ...')
    # g.expand(profile="owlrl")
    g.serialize('./readfiles/chamber_brick.ttl')
    print('brick model exported')