# FPL team selector

This package selects the best 15 players to choose when playing a wildcard on Fantasy premier league on any given week

  - Selects the best players using linear optimization
  - creates a visualization of the selected players


### Installation

##### Using pip

You can install the package using pip by running the following:

```
pip install FPL_team_selector
```
##### Download from source

Download the source code by cloning the [repository](https://github.com/abdul-gendy/FPL_team_selector). Install by navigating to the proper directory and running
```
python setup.py install
```
### Usage
##### import the package
```
import FPL_team_selector
```
##### call the play_wildcard function
  - This function takes in one argument which is the formation that you want to be displayed during the selection visualization. It should be one of the following: 442, 433, 343, 352
```
FPL_player_selector.play_wildcard(442)
```

