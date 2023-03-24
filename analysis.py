
import pandas as pd
import numpy



for x in [1, -1, 0]:
    df = pd.read_csv(f"island-data-bottle-round-2/prices_round_2_day_{x}.csv", sep=";")


    pearls = df[df["product"] == "PEARLS"]
    bananas = df[df["product"] == "BANANAS"]
    coconuts = df[df["product"] == "COCONUTS"]
    pinas = df[df["product"] == "PINA_COLADAS"]


    b = bananas["mid_price"].reset_index()["mid_price"]
    p = pearls["mid_price"].reset_index()["mid_price"]
    c = coconuts["mid_price"].reset_index()["mid_price"]
    pc = pinas["mid_price"].reset_index()["mid_price"]

    print("Day ", x)
    print("Pearls mean: ",p.mean())
    print("Bananas mean: ",b.mean())
    print("Coconuts mean: ",c.mean())
    print("Pinas mean: ",pc.mean())
    
    print("Coconuts & Pina Colada correlation: ", pc.corr(c))
    
    

