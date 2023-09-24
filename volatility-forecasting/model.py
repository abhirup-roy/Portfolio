import os
from glob import glob

import joblib
import pandas as pd
from arch import arch_model
from config import settings
from data import AlphaVantageAPI, SQLRepo

class GARCHModel:
    
    def __init__(
        self, ticker, repo, use_new_data, model_directory=settings.model_directory
    ):
    
        self.ticker = ticker
        self.repo = repo
        self.use_new_data = use_new_data
        self.model_directory = model_directory
    
    
    
    def wrangle_data(self, n_obs):
        
        # If specified, insert new data
        if self.use_new_data:
            api = AlphaVantageAPI()
            ticker = self.ticker
            new_data = api.get_daily(ticker=ticker)
            self.repo.insert_table(
                table_name=self.ticker, records=new_data, if_exists="replace"
                )
        
        # Query data from SQL database
        df = self.repo.read_table(table_name=self.ticker, limit=n_obs+1)
        
        #Clean data
        df.sort_index(ascending=True, inplace=True)
        df["return"] = df["close"].pct_change() * 100
        self.data = df["return"].dropna()
        
        
    def fit(self, p, q):
        
        # Instantiate model and train
        self.model = arch_model(self.data, p=p, q=q, rescale=False).fit(disp=0)
        
        # Define AIC and BIC metrics
        self.aic = self.model.aic
        self.bic = self.model.bic
        
        
    def __clean_prediction(self, prediction):
        
        # Find first day of forecast
        start = prediction.index[0] + pd.DateOffset(days=1)
        # Create date range
        prediction_dates = pd.bdate_range(start=start, periods=prediction.shape[1])
        #create ISO format index labels
        prediction_idx = [d.isoformat() for d in prediction_dates]
        # Extract standard deviations from predictions df
        data = prediction.values.flatten() ** 0.5
        # Create Series for std
        predictions_formatted = pd.Series(data, index=prediction_idx)
        
        return predictions_formatted.to_dict()
        
        
    def predict_volatility(self, horizon):
        
        # Forecast variance from model
        prediction = self.model.forecast(horizon=horizon, reindex=False).variance
        # Format predictions
        predictions_formatted = self.__clean_prediction(prediction)
        
        return predictions_formatted
    
    
    def dump(self):
        
        # Create ISO format timestamp
        timestamp = pd.Timestamp.now().isoformat().replace(":", "_")

        # Create filepath for model
        filepath = os.path.join(
            self.model_directory, rf"{timestamp}_{self.ticker}.pkl"
        )
        #save model
        joblib.dump(self.model, filepath)
        
        return filepath
    
    def load(self):
        # Create pattern for glob search
        pattern = os.path.join(self.model_directory, f"*{self.ticker}.pkl")
        
        # Use glob to get most recent model / Handle errors
        try:
            model_path = sorted(glob(pattern))[-1]
        except IndexError:
            raise Exception(f"No model trained for '{self.ticker}")
        
        # Load model
        self.model = joblib.load(model_path)