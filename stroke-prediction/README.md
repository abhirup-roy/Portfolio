# stroke-prediction
This is a classification model developed using the [stroke prediction dataset from Kaggle](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset). The dataset is a CSV file containing anonymised patient data including the following attributes:
* Gender
* Age
* Hypertension
* Heart Disease
* Ever Married?
* Work Type
* Residence Type
* Average Blood Glucose Level
* BMI
This data was used to predict whether the patient in question was likely to experience a stroke.


## Data Preparation
The data was loaded in via Pandas in Python. From explanatory analysis we identified that the data was biased towards: 
* Females
* Individuals not exhibiting hypertension
* Individuals not exhibiting heart disease
* Married individuals
* Individuals working in the private sector
* Non-smokers

![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/8bbb0a6b-4b87-49f9-ad89-449993941ce1)
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/edd00693-7253-4129-a0a1-1d90e4e3b82c)
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/0e3568f3-191f-48ad-bacf-db00c7be2a03)

The data was also heavily biased towards patients with negative stroke diagnoses




## Feature Engineering/ Data Cleaning
First, we converted our categorical data to numerical data using an Ordinal Encoder. We used an ordinal encoder as opposed to a One Hot Encoder as most of the categories seemed to follow a logical order. We also found null values for the BMI column in our data, so we used the Iterative Imputer in sci-kit learn to impute these values. After this, all continuous numerical variables were scaled using a Standard Scaler to keep a consistent range within the data that will be fed to our model. The data was then inspected for intercorrelation and columns that showed correlation >= 0.35 were removed.
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/c5735937-30ce-4936-8d21-e857d473abb9)
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/dfe632bf-9054-41dc-b150-57664c53a3db)


<br>
We then separated the data into training, validation and test splits - the training data was split using stratified sampling to ensure there was a sufficient sample of positive stroke diagnoses to train the model on. To reduce the bias in our data towards patients with negative stroke diagnoses, we oversampled our data using Sklearn's Synthetic Minority Oversampling Technique or SMOTE. 

## Model Selection
Initially, we tested our preprocessed data on a variety of naive classification models, including: 
1. KNeighborsClassifier
2. LinearSVC
3. NuSVC
4. DecisionTreeClassifier
5. RandomForestClassifier
6. AdaBoostClassifier
7. GradientBoostingClassifier
8. GaussianNB
9. LogisticRegression
10. LinearDiscriminantAnalysis
11. QuadraticDiscriminantAnalysis
We only kept the models, which yielded accuracy scores or recall scores greater than 70%:
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/415263aa-c7e4-41fa-8603-f0e043dadcd8)

The models were then hyperparameter-tuned for maximal recall. Recall was prioritised over precision as given the scenario of the project, it is more imperative to reduce false negatives than false positives. The overall results of the model tests are shown below:
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/ed7c3df5-8fc6-410b-b29f-c9d80c8b8988)
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/5abba104-f535-4ddd-8671-5e4e22f74abc)

### Final Model
From the above results, AdaBoost was chosen as the best model to be used in the final model. The parameters of this model included: {'algorithm': 'SAMME', 'learning_rate': 1, 'n_estimators': 100}. Here is the confusion matrix of the results of the test data: <br>
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/c0ca7f6a-6958-4938-9e90-6d665d07a014)
<br>
Here are the performance metrics of the model when used on the test data:
* True Positive Rate: 72.87%
* True Negative Rate: 78.58%
* Accuracy: 74.32%
<br>
From these metrics, our model appears to work very well!

We were also able to extract the feature importances, as shown below:
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/ee435557-ad0e-454f-afc7-1834563985b4)

It was interesting to see residence_type appear in the top 5 features used for our model, but this appears to be corroborated by research - with [rural patients more likely to develop ischemic strokes than urban patients in Northern China](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6571368/#R5). 

