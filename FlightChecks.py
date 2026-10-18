import sys
import json
A= 0.045
B=38
g= 9.81

def main():
    data= json.loads(sys.stdin.read())
    aircraft= data["aircraft"]
    propulsion= data["propulsion"]
    battery= data["battery"]
    environment= data["environment"]
    mission = data["mission"]
    
    m= aircraft["mass_kg"]
    S= aircraft["wing_area_m2"]
    cl_max=aircraft["cl_max"]
    cg_margin= aircraft["cg_margin"]
    if(m<=0 or S<=0 or cl_max<=0):
        raise AssertionError

    P_max= propulsion["max_power_W"]
    eta= propulsion["efficiency_0to1"]

    if(P_max<=0 or (eta<=0 or eta>1)):
        raise AssertionError
    
    cap= battery["capacity_mAh"]
    vol= battery["voltage_V"]
    if(cap<=0 or vol<=0):
        raise AssertionError

    rho= environment["air_density_kgpm3"]

    E_used= 0
    
    W= m*g
    V_stall= ((2*W)/(rho*S*cl_max))**0.5
    E_tot= (cap/1000)*vol*3600
    E_used=0
    segments= mission["segments"]
    
    if(len(segments)<1):
        raise AssertionError
    
    if(cg_margin<0.05):
        dict=  { "pass": False,
            "reason": "unstable",
            "energy_used_J": E_used,
            "stall_speed_mps": round(V_stall,2)}
        sys.stdout.write(json.dumps(dict))
        sys.exit(0)

    for seg in segments:
        dur= seg["duration_s"]
        V= seg["speed_mps"]

        if(dur<0 or V<=0):
            raise AssertionError
        
        P_mech= A*(V**3)+(B/V)
        P_bat= P_mech/eta
        E_cost= P_bat*dur
        
        if(V_stall>V):
            dict=  { "pass": False,
            "reason": "stall",
            "energy_used_J": round(E_used,2),
            "stall_speed_mps": round(V_stall, 2)}
            sys.stdout.write(json.dumps(dict))
            sys.exit(0)
        
        
        if(P_bat>P_max):
            dict=  { "pass": False,
                "reason": "power",
                "energy_used_J": round(E_used,2),
                "stall_speed_mps": round(V_stall, 2)}
            sys.stdout.write(json.dumps(dict))
            sys.exit(0)
        
        E_used+=E_cost

        if(E_used>E_tot):
            dict=  { "pass": False,
            "reason": "energy",
            "energy_used_J": round(E_used,2),
            "stall_speed_mps": round(V_stall, 2)}
            sys.stdout.write(json.dumps(dict))
            sys.exit(0)

    dict=  { "pass": True,
            "reason": "ok",
            "energy_used_J": round(E_used,2),
            "stall_speed_mps": round(V_stall, 2)}
    
    sys.stdout.write(json.dumps(dict))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.stdout.write("error")
        sys.exit(1)
