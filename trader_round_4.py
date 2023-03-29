# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 00:44:47 2023

@author: eddyz
"""

from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd
import numpy 
import queue

class Trader:
    
    
    def __init__(self):
        self.bananas_sum = 0
        self.pearls_sum = 0
        self.b_num = 0
        self.p_num = 0
        
        self.coco_ask = self.coco_bid = self.pina_ask = self.pina_bid = 0
        
        self.bd = []
        self.bl = []
        self.last_buy = 0
        
        
        self.last_berries = 1000000

    
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        
        def get_best_orders(book: OrderDepth):
            return (max(book.buy_orders.keys()), min(book.sell_orders.keys()))
        
        def dict_sum(dict: Dict):
            sum = 0
            for key in dict.keys():
               sum += dict[key]
            return abs(sum) #in case it's sell dict with all negative 
                
        
        k = 20
        
        print(state.position)
        

        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}
        LIMIT = 20

        # Iterate over all the keys (the available products) contained in the order depths
        for product in state.order_depths.keys():
            position = state.position.get(product, 0)


            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':
                
                    
                

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                if(order_depth.sell_orders != {} and order_depth.buy_orders != {}):
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                    self.pearls_sum += mid_price
                    self.p_num += 1
                    
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                
                acceptable_price = 10000
                if(self.p_num > 10):  #Start using the average price when have enough data (10 samples?)
                    acceptable_price = self.pearls_sum / self.p_num #comment this line out to go back to old version

                # If statement checks if there are any SELL orders in the PEARLS market
                while len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask] #This will be a negative number

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask < acceptable_price and position < LIMIT:
                        best_ask_volume = max(best_ask_volume, position - LIMIT)

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print("BUY", str(-best_ask_volume) + "x", best_ask, product)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        del order_depth.sell_orders[best_ask]
                    else:
    
                        break
                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                while len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid] #this will be positive volume
                    
                    
                    if best_bid > acceptable_price and position > -LIMIT:
                        best_bid_volume = min(best_bid_volume, LIMIT + position)
                        print("SELL", str(best_bid_volume) + "x", best_bid, product)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        
                        del order_depth.buy_orders[best_bid]
                    else:
                        break
                # Add all the above orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
                
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'BANANAS':
                
                k = 50
                
                # for trade in state.own_trades.get(product,[]):
                #     print("Trade for bananas of", trade.quantity ,"units for price", trade.price)
                    
                order_depth: OrderDepth = state.order_depths[product]
                
                if(order_depth.sell_orders != {} and order_depth.buy_orders != {}):
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                    
                    self.bd.insert(0,mid_price)
                    if(len(self.bd) > 2 * k):
                        self.bd = self.bd[0: 2*k ]
                        
                    self.bl.append(mid_price)
                
                
                if(len(self.bd) > 2 * k):
                    current = numpy.mean(self.bd[0:k])
                    prev = numpy.mean(self.bd[k: 2*k])
                    diff = current - prev
                    
                    
                    # b = pd.Series(self.bl)
                    # diff_list = b.rolling(200).mean() - b.shift(200).rolling(200).mean()
                    # diff = diff_list
                    THRESHOLD = 1.8
                    if(diff > THRESHOLD and position < LIMIT):
                        #increasing, so buy
                        volume = LIMIT - position
                        best_price = min(order_depth.sell_orders.keys())
                        
                        #Only buy when short-term vlatitlity is in favor
                        if(best_price < prev):
                            result[product] = [Order(product, best_price, volume)]
                        
                    elif(diff < -THRESHOLD and position > -LIMIT):
                        
                        #decreasing, so sell
                        volume = -LIMIT - position
                        best_price = max(order_depth.buy_orders.keys())
                        
                        #Only sell when short-term vlatitlity is in favor
                        if(best_price > prev):
                            result[product] = [Order(product, best_price, volume)]
                    
                
                
        #PAIRS TRADING - ROUGH IDEA:
        CUTOFF = 2 #choose some value
        mean_ratio = 15000/8000 #we could use empirical mean instead of given prices
        
        coco_book: OrderDepth = state.order_depths["COCONUTS"]
        pina_book: OrderDepth = state.order_depths["PINA_COLADAS"]
        
        coco_best_ask = min(coco_book.sell_orders.keys())
        pina_best_buy = max(pina_book.buy_orders.keys())
        
        pina_best_ask = min(pina_book.sell_orders.keys())
        coco_best_buy = max(coco_book.buy_orders.keys())
        
        cutoff_1 = cutoff_2 = CUTOFF
        coco_pos = state.position.get("COCONUTS",0)
        pina_pos = state.position.get("PINA_COLADAS",0)
        if(pina_pos > 0 and coco_pos < 0):
            cutoff_1 *= 5 #harder to buy pinas sell coconuts
        if(pina_pos < 0 and coco_pos > 0):
            cutoff_2 *= 5 #harder to sell pinas buy coconuts
        
        diff1 = coco_best_buy * mean_ratio - pina_best_ask
        if (diff1) > cutoff_1:
            #buy pinas, sell coconuts
            pina_vol = - pina_book.sell_orders[pina_best_ask]
            coco_vol = coco_book.buy_orders[coco_best_buy]
            trade_vol = min(pina_vol, coco_vol//2, diff1//cutoff_1)
            result["PINA_COLADAS"] = [Order("PINA_COLADAS", pina_best_ask, trade_vol)]
            result["COCONUTS"] = [Order("COCONUTS", coco_best_buy, -trade_vol * 2)] #negative trade_vol since its a sell
            #Should do some kind of position-limit checking

        diff2 = pina_best_buy - coco_best_ask * mean_ratio
        if (diff2) > cutoff_2:
            #SELL pinas, buy coconuts
            pina_vol = pina_book.buy_orders[pina_best_buy]
            coco_vol = - coco_book.sell_orders[coco_best_ask]
            trade_vol = min(pina_vol, coco_vol//2, diff2//cutoff_2)
            result["PINA_COLADAS"] = [Order("PINA_COLADAS", pina_best_buy, -trade_vol)]
            result["COCONUTS"] = [Order("COCONUTS", coco_best_ask, trade_vol * 2)] #negative trade_vol since its a sell
            #Should do some kind of position-limit checking


        
        
        
        #ETF ARBITRAGE
        picnic_book: OrderDepth = state.order_depths["PICNIC_BASKET"]
        dip_book: OrderDepth = state.order_depths["DIP"]
        bread_book: OrderDepth = state.order_depths["BAGUETTE"]
        uk_book: OrderDepth = state.order_depths["UKULELE"]
        
        result["DIP"] = []
        result["BAGUETTE"] = []
        result["UKULELE"] = []
        result["PICNIC_BASKET"] = []
        
        
        #get buy and sell prices of the picnic basket
        picnic_bid, picnic_ask = get_best_orders(picnic_book)
        
        bp = state.position.get("PICNIC_BASKET",0)
        
        #if(dict_sum(dip_book.sell_orders) >= 4 and dict_sum(bread_book.sell_orders) >= 2 and dict_sum(uk_book.sell_orders) >= 1):
        while(True):
            try: 
                #calculate buy cost of combined basket items
                buy_cost = 0
                
                dips = 0
                breads = 0
                
                temp_orders = {"BAGUETTE":[], "DIP":[], "UKULELE":[]}
                
                while(dips < 4):
                    #find best sell order that we will use to buy
                    dip_sell = get_best_orders(dip_book)[1]
                    qty = min(4-dips, -dip_book.sell_orders[dip_sell]) 
                    dips += qty
                    
                    #remove listing from order book
                    del dip_book.sell_orders[dip_sell] 
                    
                    buy_cost += dip_sell * qty
                    temp_orders["DIP"].append(Order("DIP", dip_sell, qty)) #buy
                
                while(breads < 2):
                    #find best sell order that we will use to buy
                    bread_sell = get_best_orders(bread_book)[1]
                    qty = min(2-breads, -bread_book.sell_orders[bread_sell]) 
                    breads += qty
                    
                    #remove listing from order book
                    del bread_book.sell_orders[bread_sell] 
                    
                    buy_cost += bread_sell * qty
                    temp_orders["BAGUETTE"].append(Order("BAGUETTE", bread_sell, qty)) #buy
                    
                    
                uk_sell = get_best_orders(uk_book)[1]
                qty = 1
                #uk_book.sell_orders[uk_sell] -= qty
            
                buy_cost += uk_sell * qty
                temp_orders["UKULELE"].append(Order("UKULELE", uk_sell, qty)) #buy
            
                print("sell basket for", picnic_bid, "buy items for", buy_cost)
                
                if(buy_cost < picnic_bid + bp):
                    result["PICNIC_BASKET"].append(Order("PICNIC_BASKET", picnic_bid, -1)) #sell basket
                    result["DIP"].extend(temp_orders["DIP"]) #buy the rest
                    result["UKULELE"].extend(temp_orders["UKULELE"])
                    result["BAGUETTE"].extend(temp_orders["BAGUETTE"])
                else:
                    
                    break
            except:
                break        
                
            #if(dict_sum(dip_book.buy_orders) >= 4 and dict_sum(bread_book.buy_orders) >= 2 and dict_sum(uk_book.buy_orders) >= 1):
            
        
        while(True):
            try:  
                #calculate sell cost
                sell_cost = 0
                
                
                dips = 0
                breads = 0
                
                temp_orders = {"BAGUETTE":[], "DIP":[], "UKULELE":[]}
                
                while(dips < 4):
                    #find best sell order that we will use to buy
                    dip_buy = get_best_orders(dip_book)[0]
                    qty = min(4-dips, dip_book.buy_orders[dip_buy]) 
                    dips += qty
                    
                    #remove listing from order book
                    del dip_book.buy_orders[dip_buy] 
                    
                    sell_cost += dip_buy * qty
                    temp_orders["DIP"].append(Order("DIP", dip_buy, -qty)) #sell
                
                while(breads < 2):
                    #find best sell order that we will use to buy
                    bread_buy = get_best_orders(bread_book)[0]
                    qty = min(2-breads, bread_book.buy_orders[bread_buy]) 
                    breads += qty
                    
                    #remove listing from order book
                    del bread_book.buy_orders[bread_buy] 
                    
                    sell_cost += bread_buy * qty
                    temp_orders["BAGUETTE"].append(Order("BAGUETTE", bread_buy, -qty)) #sell
                    
                    
                uk_buy = get_best_orders(uk_book)[0]
                qty = 1
                #uk_book.buy_orders[uk_buy] -= qty
            
                sell_cost += uk_buy * qty
                temp_orders["UKULELE"].append(Order("UKULELE", uk_buy, -qty)) #sell
                
                print("buy basket for", picnic_ask, "sell items for", sell_cost)
                if(sell_cost > picnic_ask + bp):
                    result["PICNIC_BASKET"].append(Order("PICNIC_BASKET", picnic_ask, 1)) #buy basket
                    result["DIP"].extend(temp_orders["DIP"]) #sell the rest
                    result["UKULELE"].extend(temp_orders["UKULELE"])
                    result["BAGUETTE"].extend(temp_orders["BAGUETTE"])
                else:
                    break
            except:
                break     
            
        
        
        
        berries_book = state.order_depths["BERRIES"]
        
        #buy berries at start
        
        if state.timestamp < 5000:
            bid, ask = get_best_orders(berries_book)
            
            qty = -berries_book.sell_orders[ask]
            result["BERRIES"] = [Order("BERRIES", ask, qty)]


        
        #Sell berries midday
        
        if state.timestamp > 45000 and state.timestamp < 55000:
            
            bid, ask = get_best_orders(berries_book)
            
            qty = berries_book.buy_orders[bid]
            result["BERRIES"] = [Order("BERRIES", bid, -qty)]
        
        
        
        return result