class Mapping_Class() :
    def __init__(self , _map) :
        self.map = _map
    
    def map(self , state : str) -> float :
        state = state.upper()
        if state not in self.map :
            return 1.0
        
        return self.map[state]

    