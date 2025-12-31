class Mapping_Class() :
    def __init__(self , _map) :
        self.data = _map
    
    def map(self , state : str) -> float :
        state = state.upper()
        if state not in self.data :
            return 1.0
        
        return self.data[state]

    