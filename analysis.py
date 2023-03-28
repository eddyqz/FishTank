
import pandas as pd
import numpy
from typing import Dict, List
from matplotlib import pyplot

SYMBOLS = ["BANANAS", "PEARLS", "COCONUTS", "PINA_COLADAS", "DIVING_GEAR", "DOLPHIN_SIGHTINGS", "BERRIES", "PICNIC_BASKET","DIP","UKULELE","BAGUETTE"]

for x in [1, 2, 3]:
    print("\n\nDay", x ,": \n")
    df = pd.read_csv(f"island-data-bottle-round-4/prices_round_4_day_{x}.csv", sep=";")
    #df = pd.read_csv("example.csv", sep=";")

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
    
    #print(product_mid_prices["DOLPHIN_SIGHTINGS"].shift(500).corr(product_mid_prices["DIVING_GEAR"]))
    
    
    
    combined = 4 * product_mid_prices["DIP"] + 2 * product_mid_prices["BAGUETTE"] + product_mid_prices["UKULELE"]
    print(combined.corr(product_mid_prices["PICNIC_BASKET"])) #Generally around .85, hopefully low enough to extract some profit
    
    
    #Checking to see if pina colada leads coconuts or vice versa
    #Seems like no
    # for k in range(-50,50,5):
    #     print("Shift by",k,"ticks")
    #     c1 = c.shift(periods=k)
    #     print(c1.corr(pc))
        
    b = product_mid_prices["BANANAS"]
    # bt = pd.DataFrame(b)
    
    # k = 100
    # bt["group1"] = b.rolling(window=k).mean()
    # bt["group2"] = b.shift(k).rolling(window=k).mean()
    # bt["group3"] = b.shift(k * 2).rolling(window=k).mean()
    # bt["d1"] = bt["group1"] - bt["group2"]
    # bt["d2"] = bt["group2"] - bt["group3"]
        
    # #print(bt)
    # print(bt.corr())
    # #print(d1.corr(d2))

    
    
    # bl = b.to_list()
    # sma = bt["group1"].to_list()
    # # for i in range(10, len(bl) - 10):
    # #     if bl[i] == max(bl[i-10:i+10]):
    # #         print(i)
    
  
  #BANANA GRAPHING
  
    # k = 50
    # output = pd.DataFrame(b)
    # output["sma2"] = b.rolling(k).mean()
    # output["prev"] = b.shift(k).rolling(k).mean()
    # diff = output["sma2"] - output["prev"]
    # pyplot.plot(output)
    # pyplot.show()
    # pyplot.plot(diff)
    # pyplot.show()
    
    output = pd.DataFrame(product_mid_prices["DOLPHIN_SIGHTINGS"]/ product_mid_prices["DOLPHIN_SIGHTINGS"].mean() )
    output["DIVING_GEAR"] = product_mid_prices["DIVING_GEAR"] / product_mid_prices["DIVING_GEAR"].mean()
    pyplot.plot(output, label=output.columns)
    pyplot.legend()
    pyplot.show()


    
