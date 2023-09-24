import sqlite3

from config import settings
from data import SQLRepo
from fastapi import FastAPI
from model import GARCHModel
from pydantic import BaseModel


class FitIn(BaseModel):
    ticker: str
    use_new_data: bool
    n_obs: int
    p: int
    q: int
    
    
class FitOut(FitIn):
    success: bool
    message: str
    

class PredictIn(BaseModel):
    ticker: str
    n_days: int


class PredictOut(PredictIn):
    success: bool
    forecast: dict
    message: str


def build_model(ticker, use_new_data):
    
    # Create sqlite connection
    connection = sqlite3.connect(settings.db_name, check_same_thread=False)
    # Instantiate SQLRepo
    repo = SQLRepo(connection=connection)
    # Instantiate model
    model = GARCHModel(ticker=ticker, repo=repo, use_new_data=use_new_data)
    
    return model


# Instantiate FastAPI object
app = FastAPI()

@app.post("/fit", status_code=200, response_model=FitOut)
def fit_model(request: FitIn):
    # Create dict from request
    response = request.dict()
    
    # Handle exceptions
    try:
        # Build model
        model = build_model(ticker = request.ticker, use_new_data=request.use_new_data)
        # Wrangle data
        model.wrangle_data(request.n_obs)
        # Fit model
        model.fit(p=request.p, q=request.p)
        # Store AIC and BIC metrics
        aic = model.aic
        bic = model.bic
        
        # Save model
        filename = model.dump()
        
        # Create response
        response["success"] = True
        response["message"] = f"Trained and saved '{filename}' - Metrics: AIC {aic}, BIC {bic}"
    
    except Exception as x:
        # create null response
         response["success"] = False
         response["message"] = str(x)
    return response

@app.post("/predict", status_code=200, response_model=PredictOut)
def get_prediction(request: PredictIn):
    
    # Create dict from request
    response = request.dict()
    
    try:
        # Build model
        model = build_model(ticker = request.ticker, use_new_data=False)
        # Load model
        model.load()
        # Generate prediction
        prediction = model.predict_volatility(horizon=request.n_days)
        
         # Create response
        response["success"] = True
        response["forecast"] = prediction
        response["message"] = "Model loaded and prediction generated successfully"
        
    except Exception as x:
        response["success"] = False
        response["forecast"] = {}
        response["message"] = str(x)
    
    return response