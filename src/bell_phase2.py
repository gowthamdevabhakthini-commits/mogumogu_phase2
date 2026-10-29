import pandas as pd
from qff_phase2 import bell_experiment, SHOTS

def run_bell_verification(proc_D_cfg):
    pairs = [(0, 1), (0, 8)]  # Near pair (distance 1) & Far pair (distance 4)
    rows = []
    
    for pair in pairs:
        for noisy in (False, True):
            res = bell_experiment(proc_D_cfg, physical_pair=pair, noisy=noisy, shots=SHOTS)
            rows.append({
                'processor': res['processor'],
                'pair': f"[{pair[0]}, {pair[1]}]",
                'noisy': res['noisy'],
                'shots': res['shots'],
                'pair_distance': res['pair_distance'],
                'XX_mean': round(res['XX'], 4),
                'XX_se': round(res['XX_se'], 4),
                'YY_mean': round(res['YY'], 4),
                'YY_se': round(res['YY_se'], 4),
                'ZZ_mean': round(res['ZZ'], 4),
                'ZZ_se': round(res['ZZ_se'], 4),
                'cx_count': res['cx'],
                'fidelity_mean': round(res['fidelity'], 4),
                'fidelity_se': round(res['fidelity_se'], 4)
            })
            
    df_bell = pd.DataFrame(rows)
    df_bell.to_csv("results/tables/bell.csv", index=False)
    print("Saved results/tables/bell.csv")
    return df_bell