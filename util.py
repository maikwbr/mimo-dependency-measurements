import pandas as pd


def export_results(results: dict, filename):
    df = pd.DataFrame.from_dict(results)
    df.to_csv(filename, sep="\t", index=False)
