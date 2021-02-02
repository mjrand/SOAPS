import time
from ocs import matched_client

class Amplifier:

    def __init__(self, amplifier_stage, amplifier_number):

        self.amplifier_stage = amplifier_stage
        self.amplifier_number = amplifier_number
        self.vd_channel = None
        self.is_vd_channel_assigned = False
        self.vg_channel = None
        self.is_vg_channel_assigned = False
        self.is_enabled = False
        self.is_biased = False

        if self.amplifier_stage == "4K":

            self.max_warm_vd_voltage = 1.35
            self.max_warm_vg_voltage = 1.1
            self.max_warm_vd_current = 0.030

            self.max_cold_vd_voltage = 0.7
            self.max_cold_vg_voltage = 1.20
            self.max_cold_vd_current = 0.008

        elif self.amplifier_stage == "40K":

            self.max_warm_vd_voltage = 4.0
            self.max_warm_vg_voltage = 0.7
            self.max_warm_vd_current = 0.045

            self.max_cold_vd_voltage = 4.0
            self.max_cold_vg_voltage = 0.7
            self.max_cold_vd_current = 0.015

    def assign_vd_channel(self, channel_to_assign):
        self.vd_channel = channel_to_assign
        self.is_vd_channel_assigned = True
        channel_to_assign.assign_to_amplifier(self)

    def assign_vg_channel(self, channel_to_assign):
        self.vg_channel = channel_to_assign
        self.is_vg_channel_assigned = True
        channel_to_assign.assign_to_amplifier(self)

    def get_warm_parameters(self):
        return [self.max_warm_vd_voltage,
                self.max_warm_vg_voltage,
                self.max_warm_vd_current]

    def get_cold_parameters(self):
        return [self.max_cold_vd_voltage,
                self.max_cold_vg_voltage,
                self.max_cold_vd_current]

    def is_valid_amplifier(self):
        if self.is_enabled:
            if self.is_vd_channel_assigned and self.is_vg_channel_assigned:
                return True

        return False
    
    def enable_amplifier(self):
        self.is_enabled = True
        
    def disable_amplifier(self):
        self.is_enabled = False
        
    def destroy(self):
        if self.is_vd_channel_assigned:
            self.vd_channel.remove_from_amplifier()
        if self.is_vg_channel_assigned:
            self.vg_channel.remove_from_amplifier()

    @property
    def identity(self):
        if self.is_vd_channel_assigned:
            vd_channel_status = self.vd_channel.identity
        else:
            vd_channel_status = "unconnected"

        if self.is_vg_channel_assigned:
            vg_channel_status = self.vg_channel.identity
        else:
            vg_channel_status = "unconnected"

        if self.is_enabled:
            identity = "[ENABLED] "
        else:
            identity = "[DISABLED] "

        identity += "Amplifier #" + str(self.amplifier_number)
        identity += " " + str(self.amplifier_stage)
        identity += " (VD = " + vd_channel_status + ", VG = " + vg_channel_status + ")"

        return identity

    def bias_amplifier(self, is_sat_cold):
        if self.is_enabled:
            print("Biasing amplifier #" + str(self.amplifier_number) + "...\n")
            
            if is_sat_cold:
                max_vd_voltage = self.max_cold_vd_voltage
                max_vg_voltage = self.max_cold_vg_voltage
                max_vd_current = self.max_cold_vd_current

            else:
                max_vd_voltage = self.max_warm_vd_voltage
                max_vg_voltage = self.max_warm_vg_voltage
                max_vd_current = self.max_warm_vd_current
            
            self.vd_channel.enable_output()
            self.vg_channel.enable_output()
            
            self.vd_channel.set_voltage(0)
            self.vg_channel.set_voltage(0)
            
            vd_voltage = self.vd_channel.get_voltage()
            vg_voltage = self.vg_channel.get_voltage()
            vd_current = self.vd_channel.get_current()
            vg_current = self.vg_channel.get_current()

            print("Setting VG channel voltage...\n")
            time.sleep(.05)
            
            vg_voltage_step = max_vg_voltage/5
            vd_voltage_step = max_vd_voltage/10
            
            while vg_voltage < max_vg_voltage:
                new_vg_voltage = vg_voltage + vg_voltage_step 
                print("Setting VG voltage to -> " + str(new_vg_voltage) + "V.")
                self.vg_channel.set_voltage(new_vg_voltage)
                time.sleep(1)
                
                vg_voltage = self.vg_channel.get_voltage()
                print(vg_voltage)
                
                time.sleep(.1)
                vg_current = self.vg_channel.get_current()

                if vg_current > 0.003:
                    print("VG current exceeded safe value.\n")
                    print("All amplifiers will be debiased.\n")
                    return -1

            print("VG channel Voltage set!\n")
            time.sleep(.1)

            print("Setting VD channel Voltage...\n")
            
            while vd_voltage < max_vd_voltage:
                new_vd_voltage = vd_voltage + vd_voltage_step
                print("Setting VD voltage to -> " + str(new_vd_voltage) + "V.")
                self.vd_channel.set_voltage(new_vd_voltage)
                time.sleep(1)
                
                vd_voltage = self.vd_channel.get_voltage()
                time.sleep(.1)
                vd_current = self.vd_channel.get_current()

                if vd_current > max_vd_current + .005:
                    print("VD current exceeded safe value.\n")
                    print("All amplifiers will be debiased.\n")
                    return -1

            print("VD channel Voltage set!\n")
            time.sleep(.1)

            print("Setting VD current...\n")

            while vd_current <= max_vd_current:
                print("Decreasing VG voltage to -> " + str(vg_voltage - .05) + "V.")
                self.vg_channel.set_voltage(vg_voltage - .05)
                time.sleep(.1)
                
                vg_voltage = self.vg_channel.get_voltage()
                time.sleep(.1)
                vd_current = self.vd_channel.get_current()
                
                
                if vd_current > max_vd_current + .005:
                    print("VD current exceeded safe value.\n")
                    print("All amplifiers will be debiased.\n")
                    return -1

            print("VD current set!\n")
            print("Amplifier #" + str(self.amplifier_number) + " successfully biased!\n")
            self.is_biased = True
            return 1
        return 0
    
    def bias_amplifier_best(self, is_sat_cold):
        if self.is_enabled:
            print("Biasing amplifier #" + str(self.amplifier_number) + "...\n")
            
            if is_sat_cold:
                max_vd_voltage = self.max_cold_vd_voltage
                max_vg_voltage = self.max_cold_vg_voltage
                max_vd_current = self.max_cold_vd_current

            else:
                max_vd_voltage = self.max_warm_vd_voltage
                max_vg_voltage = self.max_warm_vg_voltage
                max_vd_current = self.max_warm_vd_current
            
            self.vd_channel.enable_output()
            self.vg_channel.enable_output()
            
            self.vd_channel.set_voltage(0)
            self.vg_channel.set_voltage(0)
            
            time.sleep(2)
            vd_voltage = self.vd_channel.get_voltage()
            vg_voltage = self.vg_channel.get_voltage()
            vd_current = self.vd_channel.get_current()
            vg_current = self.vg_channel.get_current()

            print("Setting VG channel voltage...\n")
            time.sleep(.05)
            
            vg_voltage_step = max_vg_voltage/5
            vd_voltage_step = max_vd_voltage/10
            
            while vg_voltage < max_vg_voltage:
                new_vg_voltage = vg_voltage + vg_voltage_step 
                print("Setting VG voltage to -> " + str(new_vg_voltage) + "V.")
                self.vg_channel.set_voltage(new_vg_voltage)
                time.sleep(2)
                
                vg_voltage = self.vg_channel.get_voltage()
                print(vg_voltage)
                
                time.sleep(.1)
                vg_current = self.vg_channel.get_current()

                if vg_current > 0.003:
                    print("VG current exceeded safe value.\n")
                    print("All amplifiers will be debiased.\n")
                    return -1
            
            self.vg_channel.set_voltage(max_vg_voltage)
            
            print("VG channel Voltage set!\n")
            time.sleep(.1)

            print("Setting VD channel Voltage...\n")
            
            while vd_voltage < max_vd_voltage:
                new_vd_voltage = vd_voltage + vd_voltage_step
                print("Setting VD voltage to -> " + str(new_vd_voltage) + "V.")
                self.vd_channel.set_voltage(new_vd_voltage)
                time.sleep(2)
                
                vd_voltage = self.vd_channel.get_voltage()
                time.sleep(.1)
                vd_current = self.vd_channel.get_current()

                if vd_current > max_vd_current + .005:
                    print("VD current exceeded safe value.\n")
                    print("All amplifiers will be debiased.\n")
                    return -1
            
            self.vd_channel.set_voltage(max_vd_voltage)
            print("VD channel Voltage set!\n")
            time.sleep(2)
            
            vd_voltage = self.vd_channel.get_voltage()
            time.sleep(.5)
            vd_current = self.vd_channel.get_current()
            time.sleep(.5)
            print("Tuning VD channel Current...\n")
            
            vd_voltage_tune_step = max_vd_voltage / 100
            
            while vd_current < max_vd_current:
                new_vd_voltage = vd_voltage + vd_voltage_tune_step
                print("Setting VD voltage to -> " + str(new_vd_voltage) + "V.")
                self.vd_channel.set_voltage(new_vd_voltage)
                time.sleep(2)
                
                vd_voltage = self.vd_channel.get_voltage()
                time.sleep(.1)
                vd_current = self.vd_channel.get_current()

                if vd_current > max_vd_current + .005:
                    print("VD current exceeded safe value.\n")
                    print("All amplifiers will be debiased.\n")
                    return -1
                
            print("VD channel Current tuned!\n")

            return 1
        return 0
    
    
    def debias_amplifier(self):
        print("Debiasing amplifier #" + str(self.amplifier_number) + "...\n")
        print("Setting VD voltage to 0V...\n")
        time.sleep(.1)

        self.vd_channel.set_voltage(0)

        print("Vd channel voltage successfully set to 0V!\n")
        time.sleep(.1)

        print("Setting VG voltage to 0V...\n")
        time.sleep(.1)

        self.vg_channel.set_voltage(0)
        
        print("Amplifier #" + str(self.amplifier_number) + " successfully debiased!\n")
        self.is_biased = False
        
        
    def monitor(self):
        if self.is_biased:
            print("Amplifier #" + str(self.amplifier_number) + ":\n")
            print("VD Voltage: " + str(self.vd_channel.get_voltage()))
            print("VD current: " + str(self.vd_channel.get_current()))
            print("VG Voltage: " + str(self.vg_channel.get_voltage()))
            print("VG current: " + str(self.vg_channel.get_current()) + "\n")
    
            
class Channel:

    def __init__(self, parent_power_supply, channel_number):
        self.parent_power_supply = parent_power_supply
        self.parent_session = parent_power_supply.session
        self.channel_number = channel_number
        self.output_enabled = True
        self.is_assigned_to_amplifier = False
        self.parent_amplifier = None

    def assign_to_amplifier(self, parent_amplifier):
        self.parent_amplifier = parent_amplifier
        self.is_assigned_to_amplifier = True

    def remove_from_amplifier(self):
        self.is_assigned_to_amplifier = False
        self.parent_amplifier = None

    def enable_output(self):
        self.output_enabled = True

        self.parent_session.set_output.start(channel=self.channel_number, state=True)
        self.parent_session.set_output.wait()

    def disable_output(self):
        self.output_enabled = False

        self.parent_session.set_output.start(channel=self.channel_number, state=False)
        self.parent_session.set_output.wait()

    def set_voltage(self, new_voltage):
 
        self.parent_session.set_voltage.start(channel=self.channel_number, volts=new_voltage)
        self.parent_session.set_voltage.wait()

    def get_voltage(self):
        self.parent_session.monitor_output.start()
        time.sleep(.1)

        get_voltage_success = False
        while not get_voltage_success:
            status, message, session = self.parent_session.monitor_output.status()

            try:
                channel_voltage = session['data']['data']['Voltage_' + str(self.channel_number)]
                get_voltage_success = True
                
            except:
                time.sleep(.1)

        time.sleep(.1)
        self.parent_session.monitor_output.stop()

        return channel_voltage

    def get_current(self):
        self.parent_session.monitor_output.start()
        time.sleep(.1)

        get_current_success = False
        while not get_current_success:
            status, message, session = self.parent_session.monitor_output.status()

            try:
                channel_current = session['data']['data']['Current_' + str(self.channel_number)]
                get_current_success = True

            except:
                time.sleep(.1)

        time.sleep(.1)
        self.parent_session.monitor_output.stop()

        return channel_current
    
    def get_output(self):
        if self.output_enabled:
            print("Channel #" + str(self.channel_number) + " voltage = " + str(self.get_voltage()))
            print("Channel #" + str(self.channel_number) + " current = " + str(self.get_current()))
                  
        else:
            print("Channel #" + str(self.channel_number) + " is output is disabled.")
                  
    @property
    def identity(self):
        identity = self.parent_power_supply.name
        identity += " channel #" + str(self.channel_number)

        return identity

class PowerSupply:

    def __init__(self):
        self.session = None
        self.number_of_channels = 0
        self.channel_list = []
        self.name = "Power supply not connected!"

    def connect_to_power_supply(self, power_supply_name):

        if power_supply_name == "Keithley":
            new_session = matched_client.MatchedClient('psuK', args=[])
            self.name = "Keithley"
            self.number_of_channels = 3

        if power_supply_name == "BK":
            new_session = matched_client.MatchedClient('psuBK', args=[])
            self.name = "BK"
            self.number_of_channels = 3

        self.session = new_session

        self.session.init.start()
        self.session.init.wait()

        self.populate_channel_list(self.number_of_channels)

    def populate_channel_list(self, number_of_channels):
        for i in range(1, number_of_channels + 1):
            new_channel = Channel(self, i)
            self.channel_list.append(new_channel)
            
    
    def get_output(self):
        if self.session is not None:
            for channel in self.channel_list:
                channel.get_output()
                print("")
            