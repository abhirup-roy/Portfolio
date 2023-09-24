# volatility-forecasting
This project is a FastAPI app that allows users to load ticker data using Alpha Vantage API and predict volatility using a GARCH model. 
The project is an adaptation of a similar project I completed as part of the WorldQuant University Applied Data Science Lab.

## 1. Starting Up
It is essential for the following packages to be installed in Python:
* `pydantic`
* `pandas`
* `arch`
* `joblib`
* `sqlite3`
* `matplotlib`
* `fastapi`

Before running the app, open a terminal in your the location of the workspace and run the following command:
``` python
uvicorn main:app --reload --workers 1 --host localhost --port 8008
```
A `.env` should also be saved in the directory of the project using the following format:
```
ALPHA_API_KEY = "INSERTAPIKEY"
DB_NAME = "stocks.sqlite"
MODEL_DIRECTORY = "models"
```

## 2. App Functions
The app has 2 main functions: fit and predict

### 2.1. fit
The fit function saves the stock data to a SQLite database, fits the data to a GARCH model and saves the model.  
An example of how the function can be run using the following code:
``` python
# URL for connection to application fit function
url = "http://localhost:8008/fit"

# Parameters for data to be fitted in JSON format
json = {
    "ticker": "IBM",
    "use_new_data": True,
    "n_obs": 2000,
    "p":1,
    "q":1
}

# Post request
response = requests.post(url=url, json=json)
print("status code:", response.status_code)
response.json()
```
The JSON component of the function takes the arguments of the function using the following parameters:
* `ticker`: The ticker of a specific stock (**STRING**)
* `use_new_data`: Specifies whether new data is required to be extracted from Alpha Vantage API to SQLite (**BOOL**)
* `n_obs`: Number of observations to be extracted for the ticker (**INT**)
* `p`: The autoregressive order for GARCH model (**INT**)
* `q`: The moving average order for GARCH model (**INT**)

The JSON output of this function includes a boolean success status and a message with:
* The location and name of the saved model
* The AIC and BIC metrics

### 2.2. predict
The predict function loads the saved model and generates predictions for a selected number of days in the future.  
An example of how the function can be run using the following code:
```python
# URL for connection to application predict function
url = "http://localhost:8008/predict"
# Parameters for data to be predicted in JSON format
json = {"ticker": "IBM", "n_days":5}
# Post request
response = requests.post(url=url, json=json)

print("status code:", response.status_code)
response.json()
```
The JSON component of the function takes the arguments of the function using the following parameters:
* `ticker`: Ticker of a specific stock (**STRING**)
* `n_days`: Number of days in future to predict volatility (**INT**)
The JSON output of this function includes a message with the success status (or error) and the forecast in a dictionary.

## 3. Modules and Functions

### 3.1. config
This module takes the parameters from the `.env` file and validates the contents

### 3.2. data
This module contains the `AlphaVantageAPI` and `SQLRepo` classes
#### 3.2.1. AlphaVantageAPI
This class interacts with the AlphaVantage API. The methods it utilises are as follows:
 ```python
 get_daily(self, ticker, output_size="full")
```
Loads price history from AlphaVantage API
* `ticker`: Specifies stock ticker (**STRING**)
* `output_size`: Accepts only "full" or "compact". (**STRING**)
  * Compact returns latest 100 data points
  * Full returns the full-length time series of 20+ years of historical data

#### 3.2.2. SQLRepo
This class interacts with the SQLite repository. The methods are as follows:
```python
insert_table(self, table_name, records, if_exists="fail")
```
Inserts table into SQLite Database
* `table_name`: Specifies table name (**STRING**)
* `records`: Dataframe containing data to add to SQLite Database (**pd.Dataframe**)
* `if_exists`: Determines how to handle if data already exists. Select from "fail", "replace", or "append". (**STRING**)
  *  fail: Raise a ValueError.
  *  replace: Drop the table before inserting new values.
  *  append: Insert new values into the existing table.

 ```python
read_table(self, table_name, limit=None)
```
Reads existing table in repo
* `table_name`: Specifies name of table in repository to read (**STRING**)
* `limit`: Specifies limit on number of rows extracted from table (**INT**)

### 3.3. model
Contains the GARCHModel class which allows interaction with the model

 ```python
def __init__(self, ticker, repo, use_new_data, model_directory=settings.model_directory)
```
* `ticker`: Specifies ticker for which model will be trained on
* `repo`: Name of `SQLRepo` instance (**STRING**)
* `use_new_data`: Specify whether new data is being added to SQL Repo (**BOOL**)
* `model_directory`: Location for models to be saved (**STRING**)

 ```python
def wrangle_data(self, n_obs)
```
Orders and cleans data and computes returns
* `n_obs`: Specifies number of obsevations required (**INT**)

 ```python
fit(self, p, q)
```
Fits model to GARCH model
* `p`: The autoregressive order for GARCH model (**INT**)
* `q` : The moving average order for GARCH model (**INT**)

```python
predict_volatility(self, horizon)
```
Generates predictions using trained model
* `horizon`: Number of days in future for prediction to be generated

```python
dump(self)
```
Saves model as a `.pkl` file in the specified model directory

```python
load(self)
```
Loads model from model directory

## 4. Analysis
When analysing the model's performance the following was done:
1. Comparing model's conditional volatility against model returns
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/5186a16a-f9fc-45e5-9a11-776ae43beb7f)

2. Observed for trends and correlations in model's residuals
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/ec072388-0857-442d-9a4a-1daf7c6c12fd)
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/63699bc0-53ae-43b8-afa3-fb2a2b830991)
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/4ad2f1b0-02d4-4fc1-97fd-551aacdbb7b5)

3.  Carried out walk-forward validation on the latest 30% of available data
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/bf48abb5-f7d1-4a3b-a681-d4d67f4e0b38)

