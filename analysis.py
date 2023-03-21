
import pandas as pd
import numpy



for x in [-2, -1, 0]:
    df = pd.read_csv(f"island-data-bottle-round-1/prices_round_1_day_{x}.csv", sep=";")


    pearls = df[df["product"] == "PEARLS"]
    bananas = df[df["product"] == "BANANAS"]


    b = bananas["mid_price"].reset_index()["mid_price"]
    p = pearls["mid_price"].reset_index()["mid_price"]

    print("Day ", x)
    print("Pearls mean: ",p.mean())
    print("Bananas mean: ",b.mean())
    print("Correlation: ", p.corr(b))

