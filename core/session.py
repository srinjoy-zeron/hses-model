from utils.parser import parse_mappings, parse_threshold
from utils.mappings import Mapping_Class
from utils.normalize import normalize
from utils.multiplier import time_of_day_multiplier , session_length_multiplier , noise_environment_multiplier

from constants.state_modifiers import STATE_MODIFIERS_MAPPINGS
from constants.exploit_modifiers import ACCESS_LEVEL_MAPPINGS , ATTACKING_SKILL_MAPPINGS , USER_INTERACTION_MAPPINGS , PUBLIC_CTC_MAPPINGS , PRIVATE_CTC_MAPPINGS
from constants.exploit_scenarios import EXPLOIT_SCENARIOS

class Session_Class():
    def __init__(self , _signals : dict , _time : str , _session_length : int , _noise_score : int) :
        self.signals_values = normalize(_signals)
        self.time_of_day = _time
        self.session_length = _session_length
        self.noise_score = _noise_score
        self.weights_map , self.thresholds_map = parse_mappings()

        self.state_weights = {}
        self.signal_weights = {}
        self.state = None
        self.base_score = 0.0
        self.score = 0.0
        self.multiplier = 1.0
        self.exploit_modifier = 1.0
        self.exploit_scenarios = []
        self.exploit_band = None

        self.SIGNALS_SCALING_FACTOR = 10/7

    

    def check_threshold(self , state: str , signal: str , signal_value: float) :
        if state not in self.thresholds_map :
            return False
        if signal not in self.thresholds_map[state] :
            return False

        operator , threshold_value = parse_threshold(self.thresholds_map[state][signal] , signal)

        if operator is None or threshold_value is None :
            return False

        match operator:
            case "<":
                return signal_value < threshold_value
            case ">":
                return signal_value > threshold_value
            case "<=":
                return signal_value <= threshold_value
            case ">=":
                return signal_value >= threshold_value
            case "==":
                return signal_value == threshold_value
            case _:
                return False



    # first run this
    def calculate_weights(self) :
        for state in self.weights_map :
            total_weight = 0
            for signal in self.weights_map[state] :
                if signal not in self.signals_values or self.signals_values[signal] is None :
                    continue

                if signal not in self.signal_weights : 
                    self.signal_weights[signal] = 0

                EVIDENCE_POSITIVE = "POSITIVE"
                EVIDENCE_NEGATIVE = "NEGATIVE"

                threshold_verdict = self.check_threshold(state , signal , self.signals_values[signal])

                if EVIDENCE_NEGATIVE in self.weights_map[state][signal] and threshold_verdict :
                    total_weight += self.weights_map[state][signal][EVIDENCE_NEGATIVE] * self.signals_values[signal]
                    self.signal_weights[signal] += self.weights_map[state][signal][EVIDENCE_NEGATIVE] * self.signals_values[signal]

                elif EVIDENCE_POSITIVE in self.weights_map[state][signal] :
                    total_weight += self.weights_map[state][signal][EVIDENCE_POSITIVE] * self.signals_values[signal]
                    self.signal_weights[signal] += self.weights_map[state][signal][EVIDENCE_POSITIVE] * self.signals_values[signal]


                #threshold_verdict = EVIDENCE_NEGATIVE in self.weights_map[state][signal] and self.check_threshold(state , signal , self.signals_values[signal])
                #threshold_verdict = EVIDENCE_NEGATIVE if threshold_verdict else EVIDENCE_POSITIVE

                #total_weight += self.weights_map[state][signal][threshold_verdict] * self.signals_values[signal]
                #self.signal_weights[signal] += self.weights_map[state][signal][threshold_verdict] * self.signals_values[signal]

            self.state_weights[state] = total_weight



    # 2nd run this
    def get_dominating_state(self) :
        mx_weight = -1e9

        for state in self.state_weights :
            if self.state_weights[state] > mx_weight : 
                mx_weight = self.state_weights[state]
                self.state = state



    # 3rd run this
    def calculate_multipliers(self , environmental_factor : str) :
        self.t_factor = max(1e-2 , time_of_day_multiplier(self.time_of_day))
        self.sl_factor = max(1e-2 , session_length_multiplier(self.session_length))
        self.nev_factor = max(1e-2 , noise_environment_multiplier(self.noise_score , environmental_factor))

        self.multiplier = (self.t_factor * self.sl_factor * self.nev_factor) ** (1/3)



    # 4th run run this
    def calculate_exploit_modifier(self , access_level : str , attacking_skill : str , user_interaction : str , company_resources_stake : str , company_resources_public : bool ) :
        access_level_mapping_obj = Mapping_Class(ACCESS_LEVEL_MAPPINGS)
        self.al_factor = access_level_mapping_obj.map(access_level)

        attacking_skill_mappping_obj = Mapping_Class(ATTACKING_SKILL_MAPPINGS)
        self.as_factor = attacking_skill_mappping_obj.map(attacking_skill)

        user_interaction_mapping_obj = Mapping_Class(USER_INTERACTION_MAPPINGS)
        self.ui_factor = user_interaction_mapping_obj.map(user_interaction)

        if company_resources_public :
            ctc_mapping_obj = Mapping_Class(PUBLIC_CTC_MAPPINGS)
        else :
            ctc_mapping_obj = Mapping_Class(PRIVATE_CTC_MAPPINGS)
        self.ctc_factor = ctc_mapping_obj.map(company_resources_stake)

        self.exploit_modifier = (self.al_factor * self.as_factor * self.ui_factor * self.ctc_factor) ** (0.25)


        
    # 5th run this
    def calculate_score(self) :
        state_mapping_obj = Mapping_Class(STATE_MODIFIERS_MAPPINGS)

        _base_score = 0
        for state in self.state_weights :
            _base_score += state_mapping_obj.map(state) * self.state_weights[state]
        
        self.base_score = _base_score * self.SIGNALS_SCALING_FACTOR
        self.score = self.base_score * self.multiplier * self.exploit_modifier


    # 6th run this
    def get_exploit_scenario(self) :
        if self.state not in EXPLOIT_SCENARIOS or self.score < 30:
            return 

        severity_col = ""

        if 30 <= self.score < 60:
            severity_col = "high"
        elif 60 <= self.score < 80:
            severity_col = "very_high"
        else:
            severity_col = "critical"

        for code in EXPLOIT_SCENARIOS[self.state] :
            curr_scenario = EXPLOIT_SCENARIOS[self.state][code]
            if curr_scenario["severity"] == severity_col :
                self.exploit_scenarios.append(curr_scenario["name"])

    # 7th run this
    def get_exploit_band(self) :
        if self.score < 15 :
            self.exploit_band = "LOW" 
        elif 15 <= self.score < 30 :
            self.exploit_band = "MEDIUM" 
        elif 30 <= self.score < 60 :
            self.exploit_band = "HIGH" 
        elif 60 <=  self.score < 80 :
            self.exploit_band = "VERY_HIGH"
        else :
            self.exploit_band = "CRITICAL" 


        


        


        

                




            
                
