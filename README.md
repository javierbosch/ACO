# DISSERTATION TITLE

## Abstract

Hello, this is the repository for my dissertation. This repository contains all the code used to run the experiments and generate the results. If you are interested in the dissertation itself, you can read it on `dissertation.pdf`. Here you might find some useful information about the code.


## Creating TSP maps from real bins in Edinburgh

On the `real-maps` directory there is a Python script named `bins_to_TSP.py`. This script takes two optinal arugments `--bin_type` and `--ward`, which are the type of bin and the ward to use, if left blank, the script will use all bins in the city. This script outputs two files in the `ACO/maps` directory. Using both and euclidean and a nonplanar heuristic for the values of the adjecency matrix. 

## Running ACO

The `ACO` directory contatins all the code for the ACO algorithm. To run an experiment, run `./run.sh` with the name of the test file. Test files are located in the `ACO/test` directory. They are format as follwos:
```
nCopies,1
maxIterations,100
nAnts,20
alphas,0,1,101
betas,0,1,101
Qs,1
rhos,0.8
sigmas,1
map_file,normal_att48.txt
output_file,sample.csv
```
In this example, we are running one copy of the ACO algorithm with 100 iterations, 20 ants, 101 values of alpha between 0 and 1, 101 values of beta between 0 and 1, Q=1, rho=0.8, sigma=1, and the map file is `normal_att48.txt`. The output will be written to `sample.csv`.

Maps live in the `ACO/maps` directory. The `normal_` prefix indicates that the map is a normalized map. The `att48` suffix indicates that the map is the 48-city map from the TSPLIB. The fomat of the map file is a line for each city with x and y coordinates between comas and `.txt` extentsion, or a adjacency matrix with the extension `.csv`.

The results of the experiments are in the `ACO/results` directory, these are very self explanatory csv files.

## Plotting results

The `plots` directory contains a jupyter notebook that can be used to plot the results of the experiments. Results files are too large to be included in the repo, sorry.

## Thank you

Thank you for your interest in my dissertation. If you have any questions, please feel free to contact me at `javier.bosch@outlook.com`.