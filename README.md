# Beating-Covid

### There are two parts to this project:
#### 1. Minimax Algorithm and Alpha-beta pruning based simulation (beating_covid.py) and 2. SimPy based simulation (run.py)

## The Minimax algorithm is self-explanatory on looking at the code. 
### Dependencies for Minimax based simulation:
1. NetworkX (Latest edition supporting nx.draw)
2. Matplotlib (Latest edition which responds to the nx.draw function)
3. Curiosity to experiment with the code!

## The SimPy based simulation needs an introduction
The simulator is built using simpy. It simulates human mobility along with infectious disease (COVID) spreading in a city, where city has houses, grocery stores, parks, workplaces, and other non-essential establishments.

A basic command is given below on how to run a simulation:
`python run.py sim --n_people 100 --n_stores 100 --n_parks 10 --n_misc 100 --init_percent_sick 0.01 --outfile data`

The numbers above can be tweaked to ones liking. The output file is a pickle format which can be used for data analysis or visualization

`config.py` contains the parameters used for the simulation and can be customized according to the location

Have fun!
