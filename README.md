# On Massive Antenna Channel Models with Dependent Fading: Theory and Experiments

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/maikwbr/mimo-dependency-measurements/HEAD)
![GitHub](https://img.shields.io/github/license/maikwbr/mimo-dependency-measurements)


This repository is accompanying the paper "On Massive Antenna Channel Models
with Dependent Fading: Theory and Experiments" (E. Jorswieck, M. Weber, P.
Schlegel, and K.-L. Besser, ISWCS 2024, Jul. 2024).

The idea is to give an interactive version of the calculations and presented
concepts to the reader. All measurement data and scripts to reproduce the
results in the paper are provided in this repository.


## File List
The following files are provided in this repository:

- `run.sh`: Bash script that reproduces the figures presented in the paper.
- `util.py`: Python module that contains utility functions, e.g., for saving results.
- `calculate_bounds.py`: Python script to calculate the outage probabilities
  from measurement data.
- `channel_coefficients_abs_squared.npy`: Numpy array data of the measured
  channel gains (square of the absolute values of the channel coefficients).


## Usage
### Running it online
You can use services like [CodeOcean](https://codeocean.com) or
[Binder](https://mybinder.org/v2/gh/maikwbr/mimo-dependency-measurements/HEAD)
to run the scripts online.

### Local Installation
If you want to run it locally on your machine, Python3 and some libraries are needed.
The present code was developed and tested with the following versions:

- Python 3.12
- numpy 2.0
- scipy 1.13
- pandas 2.2
- rearrangement-algorithm 0.1.1
- matplotlib 3.9
- flatdict 4.0

Make sure you have [Python3](https://www.python.org/downloads/) installed on
your computer.
You can then install the required packages by running
```bash
pip3 install -r requirements.txt
```
This will install all the needed packages which are listed in the requirements 
file. 
You can then recreate the figures from the paper by running
```bash
bash run.sh
```


## Acknowledgements
This work is supported in part by the German Research Foundation (DFG) under
grants INST 188/516-1 and BE 8098/1-1.


## License and Referencing
This program is licensed under the GPLv3 license. If you in any way use this
code for research that results in publications, please cite our original
article listed above.

You can use the following BibTeX entry
```bibtex
@inproceedings{Jorswieck2024iswcs,
  author = {Jorswieck, Eduard A. and Weber, Maik and Schlegel, Peter and Besser, Karl-Ludwig},
  title = {On Massive Antenna Channel Models with Dependent Fading: Theory and Experiments},
  booktitle = {19th International Symposium on Wireless Communication Systems (ISWCS)},
  year = {2024},
  month = {7},
  publisher = {IEEE},
  venue = {Rio de Janeiro, Brazil},
}
```
