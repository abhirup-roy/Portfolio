# Portfolio
Portfolio of sample work I have engaged in as part of my wider learning and experiences

## Projects
* [shrinkage-tracker](https://github.com/abhirup-roy/Portfolio/tree/main/shrinkage-tracker)
* [stroke-prediction](https://github.com/abhirup-roy/Portfolio/tree/main/stroke-prediction)
* [ipo-algo-trading](https://github.com/abhirup-roy/Portfolio/tree/main/ipo-algo-trading)

## Descriptions

### shrinkage-tracker
This dashboard is an adaptation of a dashboard I developed during a data analytics internship. It is a Power BI dashboard that visualizes workforce shrinkage using a variety of views, enabling managers to plan jobs optimally. Three data sources are used:
* `AbsenceData.csv`
* `PT63.csv`
* `TeamList.csv`

Included in the folder are the CSV files mentioned above, the `.pbix` file (for dynamic viewing), and the `.pdf` file for static viewing.

### stroke-prediction
In this project, I developed a classification model to predict whether a patient will suffer a stroke, using the [stroke prediction dataset from Kaggle](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset). In the `.ipynb` file, I cover the data extraction, cleaning, feature engineering, and model development. Eleven models were tested and cross-validated, and of these, the best-performing six were hyper-parameter tuned. The best model was the `AdaBoostClassifier`, which returned the following metrics:
* `Accuracy`: 74%
* `Recall`: 76%
* `True Positive Rate`: 73%
* `True Negative Rate`: 79%

This folder includes the data source as a `.csv` file and the Jupyter Notebook (`.ipynb` file) with the data extraction, cleaning, feature engineering, and model development, as well as the results.

### ipo-algo-trading
This project aimed to test several reinforcement learning models in trading stocks in the first 100 days after its IPO. For the initial test, the Deliveroo (`ROO.L`) stock was used, particularly due to the [negative news coverage around this IPO](https://www.ft.com/content/bdf6ac6b-46b5-4f7a-90db-291d7fd2898d). To do this, OpenAI's `gymnasium` was used in conjunction with the `gym_anytrading` environment. The models that were tested in this environment alongside the `gym_anytrading` base model, obtained from OpenAI's `stable-baselines3`, were:

1. `A2C` (Advantage Actor-Critic)
2. `PPO` (Proximal Policy Optimization)
3. `DQN` (Deep Q-Network)

Summary of performance:
* `gym_anytrading` base model: Returned a **15.69% loss**
* `A2C`: Returned a **12.19% loss**
* `PPO`: Returned a **2.49% profit** (this was the best model)
* `DQN`: Returned a **55.16% profit** - this value is misleading as the algorithm only took long positions after an initial short position (this was the worst model)

Files in this folder include: `.ipynb` file with testing and comparison of models and `renders` folder with visualizations of renders of long and short positions taken by algorithms.

N.B: In further commits, the following will be added:
* Hyperparameter tuning for models
* Testing of models on other IPO stocks
* Adding extra features for prediction


  
