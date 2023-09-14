# ipo-algo-trader

This project is aimed at testing algorithmic trading using reinforcement learning models via OpenAI's gymnasium toolkit, utilising the gym_anytrading environment. We will examine the effectiveness of these trades using the initial 100 days of trading after an IPO, specifically on the London Stock Exchange. IPOs are often very volatile in the first months of trading, making this an interesting test of the algorithms' abilities to produce results in these volatile times.  For this project, we utilised the Deliveroo stock, which was labelled by FT as the [worst IPO in London's history](https://www.ft.com/content/bdf6ac6b-46b5-4f7a-90db-291d7fd2898d). 
<br>
4 models were tested:
* gym_anytrading base RL model
* A2C (from OpenAI's stable-baslines3)
* PPO (from OpenAI's stable-baslines3)
* DQN (from from OpenAI's stable-baslines3)

Via ACF analysis on the adjusted close prices, it appeared that 7 days was the optimal window size to be used for our models:
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/9128828b-9eb9-4128-b6b6-524c477e8bb5)

The results for each model are summarised below:

|   Model      |    Returns |
|    ---       |     ---    |
|   `Base`     |  -15.69%   |
|    `A2C`     |  -12.18%   |
|    `PPO`     |    2.49%   |
|    `DQN`     |    55.16%  |

![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/27902d64-9de4-4592-8cac-aa5245683986)


## A2C 
The A2C model has 2 main components: an actor (carrying out the act of shorting or buying stock), and the critic provides feedback on each action (in this case based on each buy or short). This creates a 'dialogue' improving performances at each timestep. Due to the variable nature of the data being used, the stochastic version of the model was opted for instead of the deterministic model. The performance for 10 runs is displayed below:<br>
![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/caa74ea6-234b-466d-8b99-42a3208a22de) <br>
A2C, despite providing a 12.18% loss on average, performed better than the base model and appeared to improve its returns towards the latter stages of each run. Hence this model may produce better results over a longer period. However, for the 100-day period we were looking at, this model was ineffective.

## PPO 
PPO stands for Proximal Policy Optimization. In PPO there is an actor and critic as in A2C, but the actor has policies (almost like a rulebook), which they follow. PPO makes small changes to the actor's policy to prevent large, aggressive changes, which in turn could cause instability. <br>

![image](https://github.com/abhirup-roy/Portfolio/assets/66738639/0225d50d-2ce8-4a19-8bfd-ce4604a6ff63)

<br>
This strategy appeared to work, producing an average profit of 2.49% across 10 runs. In runs where losses were made, these were often small losses. 

## DQN
Deep Q-Network uses a deep neural network to approximate Q-Values. Q-values are a metric that estimates the potential reward of taking an action. This model appears to work through only taking long positions in the stock (see [DQN Renders](https://github.com/abhirup-roy/Portfolio/tree/main/ipo-algo-trading/renders/dqn ). This could potentially have negative consequences for both the trader and the issuer. With large long positions, there are increased liquidity risks, particularly with newly placed stocks. Large long positions could also affect the price of the stock and potentially raise regulatory actions. This makes this model unviable

# Conclusion and Next Steps
From our tests, we have found that PPO is the best model to use to algorithmically trade in the first 100 days of trading of a newly placed stock. To improve the quality of this research, in further commits, the following will be added:
* Hyperparameter tuning for models
* Testing of models on other IPO stocks
* Adding extra features for prediction
