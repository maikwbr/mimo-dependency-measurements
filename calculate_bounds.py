import flatdict
import matplotlib.pyplot as plt
import numpy as np
import rearrangement_algorithm as ra
from scipy import stats

from util import export_results

# plt.rcParams["text.usetex"] = True


def find_antenna_pair(corr_coeffs, arg_function):
    corr_coeffs_copy = np.copy(corr_coeffs)
    np.fill_diagonal(corr_coeffs_copy, np.nan)

    return np.unravel_index(
        arg_function(corr_coeffs_copy, axis=None), corr_coeffs_copy.shape
    )


def find_nearest_to_zero(array, axis):
    idx = np.nanargmin((np.abs(array)), axis=axis)
    return idx


def calculate_rates(data, capacity_functions: dict, use_ra: bool = False):
    rates = {}
    for _label, _capacity_function in capacity_functions.items():
        if use_ra:
            data = ra.basic_rearrange(
                data.T,
                optim_func=max,
                is_sorted=False,
                cost_func=capacity_functions[_label],
            ).T
        rates[_label] = _capacity_function(data)

    return rates


def calculate_rates_for_two_antennas(
    data, corr_coeffs: np.ndarray, arg_functions: dict, capacity_functions: dict
):
    rates = {}
    for _label, _arg_function in arg_functions.items():
        _ant1, _ant2 = find_antenna_pair(corr_coeffs, _arg_function)
        _mean_ant1 = np.mean(data[_ant1])
        _mean_ant2 = np.mean(data[_ant2])
        rates[_label] = calculate_rates(
            [data[_ant1] / _mean_ant1, data[_ant2] / _mean_ant2], capacity_functions
        )
    return rates


def swap_dict_hierarchies(in_dict: dict):
    inner_keys = set([key for value in in_dict.values() for key in value.keys()])
    outer_keys = set(in_dict.keys())
    out_dict = {
        inner_key: {
            outer_key: in_dict[outer_key][inner_key] for outer_key in outer_keys
        }
        for inner_key in inner_keys
    }
    return out_dict


def create_cdf_from_data(data: dict, rates, num_bins: int = 70):
    cdf = {}
    for _label, _data in data.items():
        _hist = np.histogram(_data, bins=num_bins, density=True)
        _rv_hist = stats.rv_histogram(_hist, density=True)
        _cdf = _rv_hist.cdf(rates)
        cdf[_label] = _cdf
    return cdf


def plot_cdfs(rates, cdfs):
    fig, axs = plt.subplots()
    for _label, _cdf in cdfs.items():
        axs.semilogy(rates, np.maximum(_cdf, np.finfo(_cdf.dtype).eps), label=_label)
    axs.set_ylim(1e-5, 1)
    axs.legend()
    plt.show()


def main(data_path, plot: str = None, export: bool = False):
    data = np.load(data_path)

    corr_coeffs = np.corrcoef(data)

    capacity_functions = {
        "mrc": lambda gains, axis=0: np.log2(1 + np.sum(gains, axis=axis)),
        "sc": lambda gains, axis=0: np.log2(1 + np.max(gains, axis=axis)),
    }

    arg_functions = {
        "best_case": np.nanargmin,
        "iid": find_nearest_to_zero,
        "worst_case": np.nanargmax,
    }

    rates_two_antenna = swap_dict_hierarchies(
        calculate_rates_for_two_antennas(
            data, corr_coeffs, arg_functions, capacity_functions
        )
    )

    # Theory
    rng = np.random.default_rng()

    permuted_data = rng.permuted(data, axis=1)
    sorted_data = np.fliplr(np.sort(data, axis=1))

    rates = {}
    _config = [
        ("measured", data, False),
        ("iid", permuted_data, False),
        ("worst_case", sorted_data, False),
        ("best_case", data, True),
    ]
    for _label, _data, _use_ra in _config:
        rates[_label] = calculate_rates(_data, capacity_functions, _use_ra)

    rates_all_antenna = swap_dict_hierarchies(rates)

    rates = {"two_antennas": rates_two_antenna, "all_antennas": rates_all_antenna}

    num_bins = 70
    _rates = np.linspace(0, 3, 250)

    _cdf_data = {}
    for _label, _rate in rates.items():
        _cdf_data[_label] = create_cdf_from_data(
            dict(flatdict.FlatDict(_rate)), _rates, num_bins=num_bins
        )

    if plot:
        cdfs = {
            "mrc": {
                "Pos.dep. - MRC": _cdf_data["all_antennas"]["mrc:worst_case"],
                "Measured - MRC": _cdf_data["all_antennas"]["mrc:measured"],
                "IID - MRC": _cdf_data["all_antennas"]["mrc:iid"],
                "Neg.dep. - MRC": _cdf_data["all_antennas"]["mrc:best_case"],
            },
            "sc": {
                "Pos.dep. - SC": _cdf_data["all_antennas"]["sc:worst_case"],
                "Measured - SC": _cdf_data["all_antennas"]["sc:measured"],
                "IID - SC": _cdf_data["all_antennas"]["sc:iid"],
                "Neg.dep. - SC": _cdf_data["all_antennas"]["sc:best_case"],
            },
            "mrc_two_antenna": {
                "Pos.dep. - MRC": _cdf_data["two_antennas"]["mrc:worst_case"],
                "IID - MRC": _cdf_data["two_antennas"]["mrc:iid"],
                "Neg.dep. - MRC": _cdf_data["two_antennas"]["mrc:best_case"],
            },
            "sc_two_antenna": {
                "Pos.dep. - SC": _cdf_data["two_antennas"]["sc:worst_case"],
                "IID - SC": _cdf_data["two_antennas"]["sc:iid"],
                "Neg.dep. - SC": _cdf_data["two_antennas"]["sc:best_case"],
            },
        }

        plot_cdfs(_rates, cdfs[plot])

    if export:
        for _label, _cdfs in _cdf_data.items():
            _cdfs["rates"] = _rates
            export_results(_cdfs, f"outage_probabilities_{_label}.dat")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("data_path", help="Path to the numpy input file")
    parser.add_argument(
        "--plot",
        default=None,
        choices=["mrc", "sc", "mrc_two_antenna", "sc_two_antenna"],
        help="Selects, which plot to display",
    )
    parser.add_argument(
        "--export", action="store_true", help="Exports calculated data to .dat files"
    )

    args = vars(parser.parse_args())

    main(**args)
