from constants.normalize_metrics import X_MIN , X_MAX

def normalize(signals_values) :
    for signal in signals_values : 
        if signal not in X_MAX or signal not in X_MIN :
            continue
        X_MIN[signal] = min(X_MIN[signal] , signals_values[signal])
        X_MAX[signal] = max(X_MAX[signal] , signals_values[signal])

        signals_values[signal] = (signals_values[signal] - X_MIN[signal]) / (X_MAX[signal] - X_MIN[signal])

    return signals_values
        