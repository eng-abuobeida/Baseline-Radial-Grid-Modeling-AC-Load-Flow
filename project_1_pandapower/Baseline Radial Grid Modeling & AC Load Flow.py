import pandapower as pp

def run_basic_grid_analysis():
    # 1. Initialize Network
    net = pp.create_empty_network(name="Radial_Distribution_Grid")

    # 2. Add Buses
    b_hv  = pp.create_bus(net, vn_kv=110.0, name="110kV HV Substation")
    b_mv1 = pp.create_bus(net, vn_kv=20.0,  name="20kV Primary Busbar")
    b_mv2 = pp.create_bus(net, vn_kv=20.0,  name="20kV Feeder End")
    b_lv  = pp.create_bus(net, vn_kv=0.4,   name="0.4kV Commercial Node")

    # Slack Node
    pp.create_ext_grid(net, bus=b_hv, vm_pu=1.00, va_degree=0.0, name="Grid Slack")

    # 3. Add Transformers and Lines
    pp.create_transformer(net, hv_bus=b_hv, lv_bus=b_mv1, std_type="25 MVA 110/20 kV", name="Substation Trafo")
    pp.create_line(net, from_bus=b_mv1, to_bus=b_mv2, length_km=8.5, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="MV Line 1")
    pp.create_transformer(net, hv_bus=b_mv2, lv_bus=b_lv, std_type="0.4 MVA 20/0.4 kV", name="Distribution Trafo")

    # 4. Add Loads
    pp.create_load(net, bus=b_mv2, p_mw=3.5, q_mvar=1.2, name="Industrial Load")
    pp.create_load(net, bus=b_lv, p_mw=0.30, q_mvar=0.1, name="Commercial Load")

    # 5. Execute Power Flow
    pp.runpp(net)

    # 6. Violations Check
    user_input = input("""what do you wanna see?
1. voltage magnitude of each bus.
2. line thermal loading.
3. Output Diagnostic Alerts of low voltages
 """)
    if user_input == "1" :    
        print("=== BUS VOLTAGE MAGNITUDES (p.u.) ===")
        print(net.res_bus[['vm_pu']])
    elif user_input == "2" :    
        print("\n=== LINE THERMAL LOADING (%) ===")
        print(net.res_line[['loading_percent']])
    elif user_input == "3" :    
        # Output Diagnostic Alerts
        low_v = net.res_bus[net.res_bus['vm_pu'] < 0.95]
        if not low_v.empty:
                print(f"\n[ALERT] Undervoltage violation on bus indices: {list(low_v.index)}")
        else : print("no low voltages alert at any bus")
    else: print("wrong output")
while __name__ == "__main__":
    run_basic_grid_analysis()