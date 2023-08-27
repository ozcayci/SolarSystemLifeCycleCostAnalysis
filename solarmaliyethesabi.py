def PV(amount, years, rate):
    return amount / (1 + rate) ** years

def PVA(amount, years, rate):
    return amount * ((1 + rate) ** years - 1) / (rate * (1 + rate) ** years)

def PVI(amount, years, rate):
    return amount * rate / (1 - (1 + rate) ** -years)



def main():
    battery_cnt, battery_reg_cnt, inverter_cnt, cnt = 0, 0, 0, 0
    i, module_life, battery_life, inverter_life, regulator_life = 0, 0, 0, 0, 0
    array_power, module_cost, battery_cost, regulator_cost = 0.0, 0.0, 0.0, 0.0
    inverter_cost, array_inst_cost, oper_cost, d, maint, salvage, electricity = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    cc, omc, rrc, sc, tlcc, alcc, generated, cost = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    battery_rrc, regulator_rrc, inverter_rrc = 0.0, 0.0, 0.0
    
    print("Solar System Life Cycle Cost Analysis:-")
    array_power = float(input("Enter Total Array Power (Watts)...............: "))
    battery_cnt = int(input("Enter Battery Count...........................: "))
    battery_reg_cnt = int(input("Enter Battery Regulator Count.................: "))
    inverter_cnt = int(input("Enter Inverter Count..........................: "))
    print()
    module_cost = float(input("Solar Module Price ($/W)......................: "))
    module_life = int(input("Solar Module Life (Years).....................: "))
    battery_cost = float(input("Battery Price ($ each)........................: "))
    battery_life = int(input("Battery Lifetime (Years)......................: "))
    regulator_cost = float(input("Battery Regulator Cost ($ each)...............: "))
    regulator_life = int(input("Battery Regulator Lifetime (Years)............: "))
    inverter_cost = float(input("Inverter Cost ($ each)........................: "))
    inverter_life = int(input("Inverter Lifetime (Years).....................: "))
    
    array_inst_cost = float(input("Array Installation Cost ($/W).................: "))
    oper_cost = float(input("Op & maint Cost (percent of capital cost).....: "))
    d = float(input("Discount Rate (percent).......................: "))
    maint = float(input("Maintenance Labour ($/year)...................: "))
    salvage = float(input("Salvage Cost (percent of capital cost)........: "))
    electricity = float(input("Daily Electricity Generated (W/day)...........: "))
    
    # END OF USER INPUT
    with open("COST.DAT", "w") as fp:
        fp.write("INPUT DATA\n")
        fp.write("==========\n")
        fp.write(f"Total Array Power\t= {array_power:7.2f}\n")
        fp.write(f"Battery Count\t= {battery_cnt:4d}\n")
        fp.write(f"Battery Reg count\t= {battery_reg_cnt:4d}\n")
        fp.write(f"Inverter Count\t= {inverter_cnt:4d}\n\n")
        
        fp.write(f"Solar Module Price\t= {module_cost:7.2f} $/W\n")
        fp.write(f"Solar Module Life\t= {module_life:4d} Years\n")
        fp.write(f"Battery Price\t= {battery_cost:7.2f} $\n")
        fp.write(f"Battery Lifetime\t= {battery_life:4d} Years\n")
        fp.write(f"Regulator Lifetime\t= {regulator_life:4d} Years\n")
        fp.write(f"Inverter Price\t= {inverter_cost:7.2f} $\n")
        fp.write(f"Inverter Lifetime\t= {inverter_life:4d} Years\n")
        fp.write(f"Array Inst. Cost\t= {array_inst_cost:7.2f} $/W\n")
        fp.write(f"Op & Maint Cost\t= {oper_cost:7.2f} percent of capital cost\n")
        fp.write(f"Discount Rate\t= {d:7.2f} percent\n")
        fp.write(f"Maint. Labour\t= {maint:7.2f} $/year\n")
        fp.write(f"Salvage Cost\t= {salvage:7.2f} percent of capital cost\n")
        fp.write(f"Daily Elec Gen\t= {electricity:7.2f} W/day\n\n")
        fp.write("RESULTS\n")
        fp.write("=======\n")
        
        # START OF CALCULATIONS
        d = d / 100.0
        cc = array_power * (module_cost + array_inst_cost) + battery_cnt * battery_cost + battery_reg_cnt * regulator_cost + inverter_cnt * inverter_cost
        omc = PVA(maint, module_life, d)
        
        battery_rrc = 0
        cnt = module_life // battery_life
        if cnt == 0:
            cnt += 1
        if cnt > 1:
            for i in range(1, cnt + 1):
                battery_rrc += PV(battery_cnt * battery_cost, i * battery_life, d)
        
        regulator_rrc = 0
        cnt = module_life // regulator_life
        if cnt == 0:
            cnt += 1
        if cnt > 1:
            for i in range(1, cnt + 1):
                regulator_rrc += PV(battery_reg_cnt * regulator_cost, i * regulator_life, d)
        
        inverter_rrc = 0
        cnt = module_life // inverter_life
        if cnt == 0:
            cnt += 1
        if cnt > 1:
            for i in range(1, cnt + 1):
                inverter_rrc += PV(inverter_cnt * inverter_cost, i * inverter_life, d)
        
        rrc = battery_rrc + regulator_rrc + inverter_rrc
        sc = PV(cc * salvage / 100.0, module_life, d)
        tlcc = cc + omc + rrc + sc
        alcc = PVI(tlcc, module_life, d)   # ALCC hesabını düzelttim
        generated = 365.0 * electricity / 1000.0
        cost = alcc * 100.0 / generated
        
        # END OF CALCULATIONS
        fp.write(f"Capital Cost\t\t= {cc:7.2f}\n")
        fp.write(f"Operation & Maint Cost\t= {omc:7.2f}\n")
        fp.write(f"Battery replacement Cost\t= {battery_rrc:7.2f}\n")
        fp.write(f"Regulator Replacement Cost\t= {regulator_rrc:7.2f}\n")
        fp.write(f"Inverter Replacement Cost\t= {inverter_rrc:7.2f}\n")
        fp.write(f"Total replacement Cost\t= {rrc:7.2f}\n")
        fp.write(f"Salvage Cost\t\t= {sc:7.2f}\n")
        fp.write(f"Total Life Cycle Cost\t= {tlcc:7.2f}\n")
        fp.write(f"Annualised Life cycle Cost\t= {alcc:.2f}\n")  # Düzeltildi
        fp.write(f"Generated Electricity\t= {generated:7.2f} kWh/year\n")
        fp.write(f"Cost Of Electricity\t\t= {cost:7.2f} cent/kWh\n")

if __name__ == "__main__":
    main()
