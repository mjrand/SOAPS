from SOAPS_Drivers import Amplifier
from SOAPS_Drivers import PowerSupply
from SOAPS_Drivers import Channel

def main():
    print("Welcome to SOAP!")
    main_menu()


def main_menu():
    power_supply_list = []
    amplifier_list = []

    main_menu_success = False

    while not main_menu_success:

        print("\nMain Menu")
        print("~~~~~~~~~~~~")
        print("1. Configure Power Supplies")
        print("2. Configure Amplifiers")
        print("3. Assign Power Supply channels to Amplifier")
        print("4. Bias Amplifiers")
        print("5. Monitor Amplifiers")
        print("6. Configure email alerts")
        print("0. Exit\n")

        main_menu_response = input("Choose an operation: ")

        if main_menu_response == "1":
            configure_power_supplies(power_supply_list)

        elif main_menu_response == "2":
            configure_amplifiers(amplifier_list)

        elif main_menu_response == "3":
            assign_power_supply_channels_to_amplifier(power_supply_list, amplifier_list)

        elif main_menu_response == "4":

            if check_for_valid_amplifier(amplifier_list):
                is_sat_cold = get_sat_temperature()

                if is_sat_cold == -1:
                    pass

                else:
                    bias_amplifiers(amplifier_list, is_sat_cold)

            else:
                print("\nThere are no valid amplifiers to bias.")
        
        elif main_menu_response == "5":
            print("\nFeature to be added... sorry... email mrandall@ucsd.edu to finish if this is very required.")
            
        elif main_menu_response == "0":
            print("\nThank you for using SOAPS!")
            return

        else:
            print("\nInvalid response. Please try again.")


def configure_power_supplies(power_supply_list):
    configure_power_supplies_menu_success = False

    while not configure_power_supplies_menu_success:
        print("\n1. Add Power Supply")
        print("2. Remove Power Supply")
        print("0. Cancel\n")

        configure_power_supplies_menu_response = input("Choose an operation: ")

        if configure_power_supplies_menu_response == "1":
            add_power_supply(power_supply_list)

        elif configure_power_supplies_menu_response == "2":
            remove_power_supply(power_supply_list)

        elif configure_power_supplies_menu_response == "0":
            return

        else:
            print("\nInvalid response. Please try again.")


def add_power_supply(power_supply_list):

    new_power_supply = PowerSupply()
    new_power_supply_name = ""
    new_power_supply_menu_success = False
    while not new_power_supply_menu_success:
        print("\n1. Keithley")
        print("2. BK")
        print("0. Cancel\n")
    
        new_power_supply_menu_response = input("Choose a Power Supply: ")
        
        if new_power_supply_menu_response == "1":
            new_power_supply_name = "Keithley"
            new_power_supply_menu_success = True
              
        elif new_power_supply_menu_response == "2":
            new_power_supply_name = "BK"
            new_power_supply_menu_success = True
        
        elif new_power_supply_menu_response == "0":
            return 
       
        else:
            print("\nInvalid response. Please try again.")
            
    new_power_supply.connect_to_power_supply(new_power_supply_name)

    power_supply_list.append(new_power_supply)


def remove_power_supply(power_supply_list):
    if len(power_supply_list) == 0:
        print("\nThere are no power supplies to remove.")
        return power_supply_list

    for i in range(0, len(power_supply_list)):
        if i == 0:
            print("")
        print(str(i + 1) + ". " + power_supply_list[i])

    print("0. Cancel\n")

    remove_power_supply_menu_response = input("Choose a power supply to remove: ")

    try:
        remove_power_supply_menu_response = int(remove_power_supply_menu_response)

        if remove_power_supply_menu_response == 0:
            pass

        else:
            if 0 < remove_power_supply_menu_response <= len(power_supply_list):
                print("\n\"" + power_supply_list.pop(remove_power_supply_menu_response - 1)  # .name
                      + "\" has been removed from power supply list.")
            else:
                print("\nInvalid response. Please try again.")

    except ValueError:
        print("\nInvalid response. Please try again.")


def configure_amplifiers(amplifier_list):
    configure_amplifiers_menu_success = False

    while not configure_amplifiers_menu_success:
        if len(amplifier_list) == 0:
            print("\n-> No amplifiers added.")
        else:
            print("\nList of Amplifiers:\n")

            for amplifier in amplifier_list:
                print("-> " + amplifier.identity)

        print("\n1. Add amplifier")
        print("2. Remove amplifier")
        print("3. Enable/disable amplifier")
        print("0. Cancel\n")

        configure_amplifiers_menu_response = input("Choose an operation: ")

        if configure_amplifiers_menu_response == "1":
            add_amplifier(amplifier_list)

        elif configure_amplifiers_menu_response == "2":
            remove_amplifier(amplifier_list)

        elif configure_amplifiers_menu_response == "3":
            enable_or_disable_amplifier(amplifier_list)

        elif configure_amplifiers_menu_response == "0":
            return

        else:
            print("\nInvalid response. Please try again.")


def add_amplifier(amplifier_list):
    amplifier_stage = None

    add_amplifier_menu_success = False
    while not add_amplifier_menu_success:
        print("\n1. 4K")
        print("2. 40K")
        print("0. Cancel\n")

        add_amplifier_menu_response = input("Choose amplifier stage: ")

        if add_amplifier_menu_response == "1":
            amplifier_stage = "4K"
            add_amplifier_menu_success = True

        elif add_amplifier_menu_response == "2":
            amplifier_stage = "40K"
            add_amplifier_menu_success = True

        elif add_amplifier_menu_response == "0":
            return

        else:
            print("Invalid response. Please try again.")

    amplifier_number = len(amplifier_list) + 1
    new_amplifier = Amplifier(amplifier_stage, amplifier_number)
    amplifier_list.append(new_amplifier)


def remove_amplifier(amplifier_list):
    remove_amplifier_menu_success = False
    while not remove_amplifier_menu_success:
        if len(amplifier_list) == 0:
            print("\nThere are no amplifiers to remove.")
            return

        print("\nList of Amplifiers:\n")

        menu_number = 1
        for amplifier in amplifier_list:
            print(str(menu_number) + ". " + amplifier.identity)
            menu_number += 1

        print("0. Cancel\n")

        remove_amplifier_menu_response = input("Choose an amplifier to remove: ")

        try:
            remove_amplifier_menu_response = int(remove_amplifier_menu_response)

            if remove_amplifier_menu_response == 0:
                return
            else:
                if 0 < remove_amplifier_menu_response <= len(amplifier_list):
                    amplifier_to_destroy = amplifier_list.pop(remove_amplifier_menu_response - 1)
                    print("\nAmplifier #"
                          + str(amplifier_to_destroy.amplifier_number)
                          + " has been removed from amplifier list.")

                    amplifier_to_destroy.destroy()

                    return

                else:
                    print("\nInvalid response. Please try again.")

        except ValueError:
            print("\nInvalid response. Please try again.")


def enable_or_disable_amplifier(amplifier_list):
    enable_disable_amplifier_menu_success = False
    while not enable_disable_amplifier_menu_success:
        if len(amplifier_list) == 0:
            print("\nThere are no amplifiers to enable/disable.")
            return

        print("\nList of Amplifiers:\n")

        menu_number = 1
        for amplifier in amplifier_list:
            print(str(menu_number) + ". " + amplifier.identity)
            menu_number += 1

        print("0. Cancel\n")

        enable_disable_amplifier_menu_response = input("Choose an amplifier to enable/disable: ")

        try:
            enable_disable_amplifier_menu_response = int(enable_disable_amplifier_menu_response)

            if enable_disable_amplifier_menu_response == 0:
                return
            else:
                if 0 < enable_disable_amplifier_menu_response <= len(amplifier_list):
                    amplifier_to_enable_disable = amplifier_list[enable_disable_amplifier_menu_response - 1]

                    if amplifier_to_enable_disable.is_enabled:
                        print("\nAmplifier #"
                              + str(amplifier_to_enable_disable.amplifier_number)
                              + " has been disabled.")

                    else:
                        print("\nAmplifier #"
                              + str(amplifier_to_enable_disable.amplifier_number)
                              + " has been enabled.")

                    amplifier_to_enable_disable.is_enabled = not amplifier_to_enable_disable.is_enabled
                    return

                else:
                    print("\nInvalid response. Please try again.")

        except ValueError:
            print("\nInvalid response. Please try again.")


def assign_power_supply_channels_to_amplifier(power_supply_list, amplifier_list):
    assign_channel_menu_success = False

    amplifier_to_assign_to = None
    channel_to_be_assigned = None

    while not assign_channel_menu_success:
        if amplifier_to_assign_to is None:
            print("\n-> Amplifier to assign to not chosen.")
        else:
            print("\n-> Amplifier to assign to is: " + amplifier_to_assign_to.identity)

        if channel_to_be_assigned is None:
            print("-> Channel to be assigned not chosen.")
        else:
            print("-> Channel to be assigned is: " + channel_to_be_assigned.identity)

        print("\n1. Choose amplifier to assign to")
        print("2. Choose channel to be assigned")
        print("3. Assign channel")
        print("0. Cancel\n")

        assign_channel_menu_response = input("Choose an operation: ")

        if assign_channel_menu_response == "1":
            if len(amplifier_list) == 0:
                print("\nNo amplifiers available to assign to.")
            else:
                amplifier_to_assign_to = get_amplifier_to_assign_to(amplifier_list, amplifier_to_assign_to)

        elif assign_channel_menu_response == "2":
            if len(power_supply_list) == 0:
                print("\nNo channels available to be assigned.")
            else:
                get_channel_to_be_assigned(power_supply_list, channel_to_be_assigned)

        elif assign_channel_menu_response == "3":
            if amplifier_to_assign_to is None:
                print("\nPlease choose an amplifier to assign to.")

            elif channel_to_be_assigned is None:
                print("\nPlease choose a channel to be assigned.")

            else:
                assign_channel(amplifier_to_assign_to, channel_to_be_assigned)

        elif assign_channel_menu_response == "0":
            return

        else:
            print("\nInvalid response. Please try again.")


def get_amplifier_to_assign_to(amplifier_list, amplifier_to_assign_to):
    amplifier_choice_menu_success = False
    while not amplifier_choice_menu_success:
        print("\nList of Amplifiers:\n")

        menu_number = 1
        for amplifier in amplifier_list:
            print(str(menu_number) + ". " + amplifier.identity)

            menu_number += 1

        print("0. Cancel\n")

        amplifier_choice_menu_response = input("Choose an amplifier to assign channels to: ")

        try:
            chosen_amplifier_number = int(amplifier_choice_menu_response)

            if 0 < chosen_amplifier_number < len(amplifier_list) + 1:
                return amplifier_list[chosen_amplifier_number - 1]

            elif chosen_amplifier_number == 0:
                return amplifier_to_assign_to

            else:
                print("\nInvalid response. Please try again.")

        except ValueError:
            print("\nInvalid response. Please respond with a number.")


def get_channel_to_be_assigned(power_supply_list, channel_to_be_assigned):
    available_channels_list = []
    for power_supply in power_supply_list:
        for channel in power_supply.channel_list:
            if not channel.is_assigned:
                available_channels_list.append(channel)

    get_channel_menu_success = False

    while not get_channel_menu_success:
        print("\nAvailable power supply channels:")
        for i in range(0, len(available_channels_list)):
            print(str(i) + ". " + available_channels_list[i].identity)

        print("0. Cancel\n")

        get_channel_menu_response = input("Choose a power supply channel: ")

        try:
            chosen_channel_number = int(get_channel_menu_response)

            if 0 < chosen_channel_number < len(available_channels_list):
                return available_channels_list[chosen_channel_number - 1]

            elif chosen_channel_number == 0:
                return channel_to_be_assigned

            else:
                print("\nInvalid response. Please try again.")

        except ValueError:
            print("\nInvalid response. Please respond with a number.")


def assign_channel(amplifier_to_assign_to, channel_to_be_assigned):
    assign_channel_menu_success = False
    while not assign_channel_menu_success:

        print("\n-> Assigning to: " + amplifier_to_assign_to.identity)

        print("\n1. VD")
        print("2. VG")
        print("0. Cancel")

        assign_channel_menu_response = input("Choose an amplifier line to assign channel to: ")

        if assign_channel_menu_response == "1":
            if amplifier_to_assign_to.is_vd_channel_assigned:
                print("\nVD line on Amplifier #" + amplifier_to_assign_to.amplifier_number
                      + " is already assigned.")

            else:
                amplifier_to_assign_to.assign_vd_channel(channel_to_be_assigned)

        elif assign_channel_menu_response == "2":
            if amplifier_to_assign_to.is_vg_channel_assigned:
                print("\nVG line on Amplifier #" + amplifier_to_assign_to.amplifier_number
                      + " is already assigned.")

            else:
                amplifier_to_assign_to.assign_vg_channel(channel_to_be_assigned)

        elif assign_channel_menu_response == "0":
            return

        else:
            print("\nInvalid response. Please try again.")


def check_for_valid_amplifier(amplifier_list):

    for amplifier in amplifier_list:
        if amplifier.is_valid_amplifier():
            return True


def get_sat_temperature():
    get_sat_temperature_menu_success = False

    while not get_sat_temperature_menu_success:
        print("\n1. Cold")
        print("2. Warm")
        print("0. Cancel\n")
        get_sat_temperature_menu_response = input("Choose the correct SAT temperature: ")

        if get_sat_temperature_menu_response == "1":
            sat_is_cold = True
            return sat_is_cold

        elif get_sat_temperature_menu_response == "2":
            sat_is_cold = False
            return sat_is_cold

        elif get_sat_temperature_menu_response == "0":
            return -1

        else:
            print("\nInvalid response. Please try again.")


def bias_amplifiers(amplifier_list, is_sat_cold):
    if is_sat_cold:
        cold_bias_procedure(amplifier_list)

    else:
        warm_bias_procedure(amplifier_list)


def cold_bias_procedure(amplifier_list):
    print("\nCold procedure goes here")


def warm_bias_procedure(amplifier_list):
    print("\neWarm procedure goes here")


main()
