"""
Classes and methods to facilitate
read and write from/to BACnet network of the building

@author Carlos Duarte <cduarte@berkeley.ed>
"""

import time


class BACnet_Point:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.name = str(self.kwargs.get('obj_name'))
        self.unit = str(self.kwargs.get('point_unit'))
        self.bacnet_address = str(self.kwargs.get('bacnet_address'))
        self.identifier = str(self.kwargs.get('obj_identifier'))
        self.type, self.instance = self.kwargs.get('obj_identifier').split(',')


    def get_point_value(self, bacpypesAPP, sig_fig=4, convert_2_num=False):
        """
        Get current value from sensor in a BACnet network
        """
        read_attr = "presentValue"

        obj_type = self.type
        obj_inst = self.instance
        bacnet_addr = self.bacnet_address

        bacnet_args = [bacnet_addr, obj_type, obj_inst, read_attr]

        val = bacpypesAPP.read_prop(bacnet_args)

        if val is None:
            time.sleep(1)
            val = bacpypesAPP.read_prop(bacnet_args)

        # try to convert to float
        if convert_2_num:
            value = self.convert_to_num(val)
        else:
            try:
                value = float(val)
                value = round(val, sig_fig)
            except ValueError:
                value = val

        return value


    def write_point_value(self, bacpypesAPP, new_value, priority=13):
        """
        Write new value to bacnet point
        """

        write_attr = "presentValue"

        obj_type = self.type
        obj_inst = self.instance
        bacnet_addr = self.bacnet_address

        bacnet_args = [bacnet_addr, obj_type, obj_inst, write_attr, str(new_value), '-', priority]

        bacpypesAPP.write_prop(bacnet_args)


    def get_bacnet_info(self, read_attr=None):
        obj_type = self.type
        obj_inst = self.instance
        bacnet_addr = self.bacnet_address

        if read_attr is None:
            bacnet_args = [bacnet_addr, obj_type, obj_inst]
        else:
            bacnet_args = [bacnet_addr, obj_type, obj_inst, read_attr]

        return bacnet_args


    def print_bacnet_info(self):
        """
        Brick bacnet information for the point
        """
        obj_name = self.name
        obj_type = self.type
        obj_inst = self.instance
        bacnet_addr = self.bacnet_address

        info = f""" ObjectName: {obj_name} \n
                    ObjectType: {obj_type} \n
                    ObjectInstance: {obj_inst} \n
                    BACnetAddress: {bacnet_addr}
                """
        print(info)


    def convert_to_num(self, read_val):
        """
        Convert strings into a numerical value
        """
        if isinstance(read_val, (int, float)):
            return read_val
        else:
            try:
                read_val = float(read_val)
            except ValueError:
                read_val = self.event_2_num(str(read_val).lower())

            return float(read_val)


    def event_2_num(self, dat_val):

        # convert on/off to numbers
        if dat_val.lower() == 'on':
            dat_val = 1
        elif dat_val.lower() == 'off':
            dat_val = 0.0

        # convert true/false to numbers
        if dat_val.lower() == 'true':
            dat_val = 1
        elif dat_val.lower() == 'false':
            dat_val = 0

        # convert open/close to numbers
        elif dat_val.lower() == 'open' or dat_val.lower() == 'opened':
            dat_val = 1
        elif dat_val.lower() == 'close' or dat_val.lower() == 'closed':
            dat_val = 0

        # convert active/inactive to numbers
        elif dat_val.lower() == 'inactive':
            dat_val = 0
        elif dat_val.lower() == 'active':
            dat_val = 1

        # convert OK to numbers
        elif dat_val.lower() == 'ok':
            dat_val = 1

        # convert events of heating/cooling/noflow into numbers
        elif dat_val.lower() == 'heatng' or dat_val.lower() == 'heating':
            dat_val = 1
        elif dat_val.lower() == 'coolng' or dat_val.lower() == 'cooling':
            dat_val = -1
        elif dat_val.lower() == 'noflo'  or dat_val.lower() == 'noflow':
            dat_val = 0.0

        elif dat_val.lower() == 'heat':
            dat_val = 1
        elif dat_val.lower() == 'cool':
            dat_val = -1

        # convert alarms into numbers
        elif dat_val.lower() == 'normal':
            dat_val = 0
        elif dat_val.lower() == 'offnormal':
            dat_val = 1
        elif dat_val.lower() == 'alarm':
            dat_val = 1
        elif dat_val.lower() == 'nofaultdetected':
            dat_val = 0
        elif dat_val.lower() == 'unreliableother':
            dat_val = 1
        elif dat_val.lower() == 'fault':
            dat_val = 1
        elif dat_val.lower() == 'highlimit':
            dat_val = 1
        elif dat_val.lower() == 'lowlimit':
            dat_val = -1

        # convert misc strings
        elif dat_val.lower() == 'nat':
            dat_val = 0
        elif dat_val.lower() == 'other':
            dat_val = 3 # Other data point

        # error codes
        elif dat_val.lower() == 'none':
            dat_val = -999 # No data returned
        elif dat_val.lower() == '[]':
            dat_val = -999 # No data returned
        elif dat_val.lower() == '{}':
            dat_val = -999 # No data returned


        # convert string wind direction into numbers
        elif dat_val.lower() == 'n':
            dat_val = 0.0
        elif dat_val.lower() == 'nne':
            dat_val = 22.5
        elif dat_val.lower() == 'ne':
            dat_val = 45.0
        elif dat_val.lower() == 'ene':
            dat_val = 67.5
        elif dat_val.lower() == 'e':
            dat_val = 90.0
        elif dat_val.lower() == 'ese':
            dat_val = 112.5
        elif dat_val.lower() == 'se':
            dat_val = 135.0
        elif dat_val.lower() == 'sse':
            dat_val = 157.5
        elif dat_val.lower() == 's':
            dat_val = 180.0
        elif dat_val.lower() == 'ssw':
            dat_val = 202.5
        elif dat_val.lower() == 'sw':
            dat_val = 225.0
        elif dat_val.lower() == 'wsw':
            dat_val = 247.5
        elif dat_val.lower() == 'w':
            dat_val = 270.0
        elif dat_val.lower() == 'wnw':
            dat_val = 292.5
        elif dat_val.lower() == 'nw':
            dat_val = 315.0
        elif dat_val.lower() == 'nnw':
            dat_val = 337.5
        else:
            pass

        return dat_val