#tester

import pandas as pd
import numpy
import sys
from trader_round_1 import Trader
from datamodel import TradingState, Order, Observation, OrderDepth, Trade
from typing import Dict, List

Time = int
Symbol = str
Product = str
Position = int
UserId = str
Observation = int

if __name__ == "__main__":
    
    if(len(sys.argv) != 2):
        print("Needs 2 arguments: tester.py [market data]")
        exit(1)
            
    file = sys.argv[1]
    
    
    df = pd.read_csv(file, sep=";")
    
    pearls = df[df["product"] == "PEARLS"]
    bananas = df[df["product"] == "BANANAS"]
    
    bananas = bananas.reset_index()
    pearls = pearls.reset_index()
    
    
    symbols = ["PEARLS", "BANANAS"]
    POSITION_LIMITS = {"PEARLS":20, "BANANAS":20}
    
    trader = Trader()
    
    own_trades: Dict[Symbol, List[Trade]] = {}
    
    position: Dict[Product, Position] = {}
    
    profit = 0
    net_profit = 0
    
    f = open("profit.txt", 'w')
    e = open("error.txt", 'w')
    
    for symbol in symbols:
        position[symbol] = 0
    
    for iteration in range(0, len(bananas)):
        b_row = bananas.iloc[iteration]
        p_row = pearls.iloc[iteration]
        
        print()
        print()
        timestamp = b_row["timestamp"]
        print(timestamp)
        
        
        order_depths: Dict[Symbol, OrderDepth] = {}
        
        #bananas orderbook
        b_book = OrderDepth()
        for x in [1,2,3]:
            if pd.notna(b_row[f"bid_price_{x}"]):
                b_book.buy_orders[b_row[f"bid_price_{x}"]] = b_row[f"bid_volume_{x}"]
            if pd.notna(b_row[f"ask_price_{x}"]):
                b_book.sell_orders[b_row[f"ask_price_{x}"]] = - b_row[f"ask_volume_{x}"]
        
        #pearls orderbook
        p_book = OrderDepth()
        for x in [1,2,3]:
            if pd.notna(p_row[f"bid_price_{x}"]):
                p_book.buy_orders[p_row[f"bid_price_{x}"]] = p_row[f"bid_volume_{x}"]
            if pd.notna(b_row[f"ask_price_{x}"]):
                p_book.sell_orders[p_row[f"ask_price_{x}"]] = - p_row[f"ask_volume_{x}"]

        order_depths["PEARLS"] = p_book
        order_depths["BANANAS"] = b_book
        
        #print(b_row)
        #print(order_depths["BANANAS"].sell_orders)
        
        #Need to implement own_trades and rest of stuff
        state: TradingState = TradingState(timestamp, None, order_depths, own_trades, None, position, None)
        output: Dict[str, List[Order]] = trader.run(state)
        
        
        #resolve the new orders made
        for symbol in output:
            new_orders = output[symbol]
            book = order_depths[symbol]
            print("initial order book for", symbol + ": ", book.buy_orders, book.sell_orders)

            for order in new_orders:
                if order.quantity > 0:
                    #Buy order
                    while(order.quantity != 0):
                        if(book.sell_orders == {}):
                            break
                        best_price = min(book.sell_orders) #cheapest ask on market
                        if(best_price > order.price):
                            break #could not find a cheap enough order
                        
                        volume_traded = min(order.quantity, -book.sell_orders[best_price])
                        order.quantity -= volume_traded
                        book.sell_orders[best_price] += volume_traded
                        if book.sell_orders[best_price] == 0:
                            del book.sell_orders[best_price]
                        
                        position[symbol] += volume_traded
                        profit -= volume_traded * best_price
                        print("\tnew status:", book.buy_orders, book.sell_orders)
                        
                    
                elif order.quantity < 0:
                    #Ask order
                    order.quantity = -order.quantity
                    while(order.quantity != 0):
                        if(book.buy_orders == {}):
                            break
                        best_price = max(book.buy_orders) #highest bid on market
                        if(best_price < order.price):
                            break #could not find a bid high enough 
                        
                        volume_traded = min(order.quantity, book.buy_orders[best_price])
                        order.quantity -= volume_traded
                        book.buy_orders[best_price] -= volume_traded
                        if book.buy_orders[best_price] == 0:
                            del book.buy_orders[best_price]
                        
                        position[symbol] -= volume_traded
                        profit += volume_traded * best_price
                        print("\tnew status:", book.buy_orders, book.sell_orders)

        
            print("POSITION FOR", symbol + ":", position[symbol])
            if(abs(position[symbol]) > POSITION_LIMITS[symbol]):
                e.write(f"POSITION LIMIT EXCEEDED FOR {symbol}, with position {position[symbol]} \n")
        
        print(profit)
        net_profit = profit
        net_profit += b_row["mid_price"] * position["BANANAS"]
        net_profit += p_row["mid_price"] * position["PEARLS"]
        
        print(net_profit)
        
        f.write(str(net_profit))
        f.write("\n")
            
        
   
    #print(bananas.set_index("tick"))
    #print(bananas)
    #print(pearls)
    
    





