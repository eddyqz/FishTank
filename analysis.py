
import pandas as pd
import numpy


df = pd.read_csv("island-data-bottle-round-1/prices_round_1_day_0.csv", sep=";")




pearls = df[df["product"] == "PEARLS"]
bananas = df[df["product"] == "BANANAS"]
print(pearls)

print(pearls["mid_price"].mean())
print(bananas["mid_price"].mean())



# for row in df.iterrows():
#     print(row[1].)
