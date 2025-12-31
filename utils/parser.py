from api.imports import pandas as pd, Path, re
from constants.normalize_metrics import X_MIN, X_MAX


def parse_mappings() :
    base_dir = Path(__file__).resolve().parent
    path_to_csv = base_dir / "../constants/signals_mapping.csv"
    df = pd.read_csv(path_to_csv)
    weights_map = {}
    thresholds_map = {}

    for _, row in df.iterrows() :
        key1 = str(row["State"])
        key2 = str(row["Signal"])
        key3 = str(row["Evidence_Type"])
        val = float(row["Final_Weight"])
        
        if key3 == "NEGATIVE" :
            if key1 not in thresholds_map :
                thresholds_map[key1] = {}
            thresholds_map[key1][key2] = str(row["Activation_Condition"])
        if key1 not in weights_map :
            weights_map[key1] = {}
        if key2 not in weights_map[key1] :
            weights_map[key1][key2] = {}
        weights_map[key1][key2][key3] = val

    return weights_map , thresholds_map

def parse_threshold(text : str , signal : str) :
    tokens = text.split(" ")
    if len(tokens) < 3 :
        return None , None
    
    if signal not in X_MIN or signal not in X_MAX : 
        return None , None

    operator = tokens[1]
    threshold_value = float("".join(re.findall(r'[-+]?\d*\.?\d+', tokens[2])))
    threshold_value = max(0 , threshold_value - X_MIN[signal]) / (X_MAX[signal] - X_MIN[signal])
    threshold_value = max(0, min(1, threshold_value))

    return operator , threshold_value