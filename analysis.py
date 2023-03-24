
import pandas as pd
import numpy
from typing import Dict, List

SYMBOLS = ["BANANAS", "PEARLS", "COCONUTS", "PINA_COLADAS"]

for x in [-1, 0, 1]:
    print("\n\nDay", x ,": \n")
    df = pd.read_csv(f"island-data-bottle-round-2/prices_round_2_day_{x}.csv", sep=";")

    product_dfs: Dict[str,pd.DataFrame] = {}
    product_mid_prices: Dict[str,pd.Series] = {}
    
    for symbol in SYMBOLS:
        product_dfs[symbol] = df[df["product"] == symbol]
        product_mid_prices[symbol] = product_dfs[symbol]["mid_price"].reset_index()["mid_price"]

        print(symbol, " mean price: ", product_mid_prices[symbol].mean())
    
    mid_prices = pd.DataFrame(product_mid_prices)
    print("\nMEAN PRICES:\n")
    print(mid_prices.mean())
    print("\nSTD DEVATIONS:\n")
    print(mid_prices.std())
    print("\nCORRELATIONS:\n")
    print(mid_prices.corr())
    
    

    #pairs trading:
    pc = product_mid_prices["PINA_COLADAS"]
    c = product_mid_prices["COCONUTS"]
    mean_ratio = pc.mean()/c.mean()
    diff = pc - c * mean_ratio #difference between adjusted pina colada and coconut mid prices
    
    #print(diff.mean()) # mathematically should be zero
    print("standard dev of difference between pinas and coconuts:", diff.std()) #tells us how far this difference spreads
    
    print()
    
    
    
    #Checking to see if pina colada leads coconuts or vice versa
    #Seems like no
    for k in range(-50,50,5):
        print("Shift by",k,"ticks")
        c1 = c.shift(periods=k)
        print(c1.corr(pc))
        
        
        
    
