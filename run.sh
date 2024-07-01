#!/usr/bin/env bash
# Run all script to generate the results presented in the paper "On Massive
# Antenna Channel Models with Dependent Fading: Theory and Experiments" (E.
# Jorswieck, M. Weber, P. Schlegel, K.-L. Besser, ISWCS 2024, July 2024).
#
# License: GPLv3

echo "Figure 1: Outage probabilities for MRC"
python3 calculate_bounds.py channel_coefficients_abs_squared.npy --plot mrc

echo "Figure 2: Outage probabilities for SC"
python3 calculate_bounds.py channel_coefficients_abs_squared.npy --plot sc

echo "Figure 3: Outage probabilities for MRC with two selected antennas"
python3 calculate_bounds.py channel_coefficients_abs_squared.npy --plot mrc_two_antenna
