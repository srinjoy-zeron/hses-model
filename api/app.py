from api.imports import FastAPI, CORSMiddleware, load_dotenv, os, APIRouter, Depends, HTTPException, status, BaseModel

from core.session import Session_Class

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware , 
    allow_origins = [os.getenv("CORS_ALLOWED_ORIGINS")] , 
    allow_credentials = True , 
    allow_methods = ["*"],
    allow_headers = ["*"]
)


class body_model(BaseModel) :
    signals : dict
    time_of_day : str 
    session_length : int
    noise : int
    environmental_factor : str
    access_level : str 
    attacking_skill : str
    user_interaction : str
    company_resources_stake : str 
    company_resources_public : bool 


@app.post("/score")
def get_score(body : body_model) :
    signals_values = body.signals
    if signals_values is None : 
        return {
            success : False , 
            message : "All fields are necessary"
            }
    
    session = Session_Class(
            signals_values , 
            body.time_of_day , 
            body.session_length , 
            body.noise
        )

    session.calculate_weights()
    session.get_dominating_state()
    session.calculate_multipliers(body.environmental_factor)
    session.calculate_exploit_modifier(
            body.access_level , 
            body.attacking_skill , 
            body.user_interaction ,
            body.company_resources_stake ,
            body.company_resources_public
        )
    session.calculate_score()
    session.get_exploit_scenario()
    session.get_exploit_band()

    return {
        "success" : True , 
        "state_weights" : session.state_weights ,
        "signal_weights" : session.signal_weights ,
        "state" : session.state ,
        "base_score" : session.base_score ,
        "total_score" : session.score ,
        "multiplier" : session.multiplier ,
        "exploit_modifier" : session.exploit_modifier ,
        "exploit_scenarios" : session.exploit_scenarios ,
        "exploit_band" : session.exploit_band ,
        }