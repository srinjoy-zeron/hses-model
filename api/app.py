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
    environmental_factor : str
    access_level : str 
    attacking_skill : str
    user_interaction : str
    company_resources_stake : str 
    company_resources_public : bool 

@app.post("/score")
def get_score(body : body_model) :
    
    session = Session_Class()

    return {success : True}