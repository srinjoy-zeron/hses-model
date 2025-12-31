from constants.normalize_metrics import X_MIN , X_MAX

def normalize(signals_values) :
    for signal in signal_values : 
        if signal not in X_MAX or signal not in X_MIN :
            continue
        X_MIN[signal] = min(X_MIN , signal_values[signal])
        X_MAX[signal] = max(X_MAX , signal_values[signal])

        signal_values[signal] = (signal_values[signal] - X_MIN[signal]) / (X_MAX[signal] - X_MIN[signal])
        