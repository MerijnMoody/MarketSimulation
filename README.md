# MarketSimulation
Project Computational Science Market Simulation Code
The code consists of two files: Simulation.py and Plot.py. They do the following:
Simulation.py:
  - runs the main market simulation for a specified number of iterations and p-values
  - saves the raw data in the "data.csv" file
  - plots the final state of the buyers and sellers in a bar plot
Plot.py:
  - plots a graph of the average buyer and seller prices and their difference with a shaded standard deviation
  - plots a graph of the average buy and sell price difference for different p-values
  
To reproduce the figures used in the report, run Plot.py which uses the data.csv file, which is the data file that we used for the report.
Data.csv was generated using the generate_data() function in Simulation.py with the following parameters:
Global parameters:
  - n_buyers = 10000
  - n_sellers = 500
  - starting_stock = 20
  - price_var = 0.05
  - max_hunger = 20
Function parameters:
  - p_list = [0.5, 0.1, 0.05, 0.02, 0.01, 0.005, 0.004, 0.003, 0.002, 0.001, 0.0025, 0.0015, 0.005]
  - n_iter = 100
  - n_days = 500
Generating this data took a long time (>10hrs) so to get a more manageable simulation the following parameters can be used:
Global parameters:
  - n_buyers = 1000
  - n_sellers = 50
  - starting_stock = 20
  - price_var = 0.05
  - max_hunger = 20
Function parameters:
  - p_list = [0.5, 0.002, 0.0025, 0.001, 0.0015]
  - n_iter = 10
  - n_days = 300
