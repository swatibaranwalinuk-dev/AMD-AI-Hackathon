import pandas as pd

def load_assets():

    dataframe = pd.read_csv(
        "data/assets.csv"
    )

    return dataframe
