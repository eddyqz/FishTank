# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 00:44:47 2023

@author: eddyz
"""

from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import pandas as pd
import numpy 

class Trader:
    def __init__(self):
        self.bananas_sum = 0
        self.pearls_sum = 0
        self.b_num = 0
        self.p_num = 0
        
        self.coco_ask = self.coco_bid = self.pina_ask = self.pina_bid = 0
        
        self.banana_data = []
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        
        
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
                if len(order_depth.sell_orders) > 0:

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

                # The below code block is similar to the one above,
                # the difference is that it finds the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid] #this will be positive volume
                    
                    
                    if best_bid > acceptable_price and position > -LIMIT:
                        best_bid_volume = min(best_bid_volume, LIMIT + position)
                        print("SELL", str(best_bid_volume) + "x", best_bid, product)
                        orders.append(Order(product, best_bid, -best_bid_volume))

                # Add all the above orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
                
            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'BANANAS':
                
                
                order_depth: OrderDepth = state.order_depths[product]
                
                if(order_depth.sell_orders != {} and order_depth.buy_orders != {}):
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                    self.bananas_sum += mid_price
                    self.b_num += 1
                    
                acceptable_price = 4950
                if(self.b_num > 10): #Start using the average price when have enough data (10 samples?)
                    acceptable_price = self.bananas_sum / self.b_num #comment this line out to go back to old version
                
                
                
                if(order_depth.sell_orders != {} and order_depth.buy_orders != {}):
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                    self.banana_data.append(mid_price)
                    
                if(len(self.banana_data) > 100):
                    mean_price = numpy.mean(self.banana_data)
                    
                    difference = 20
                    buy_volume = LIMIT - position
                    buy_order = Order(product, mean_price - difference, buy_volume//2)
                    buy_order2 = Order(product, mean_price - 2 * difference, buy_volume//2)
                    
                    ask_volume = -LIMIT - position
                    ask_order = Order(product, mean_price + difference, ask_volume//2)
                    ask_order2 = Order(product, mean_price + 2 * difference, ask_volume//2)
                    
                    
                    result[product] = [buy_order, ask_order, buy_order2, ask_order2]
                    
                    
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                # order_depth: OrderDepth = state.order_depths[product]

                # if(order_depth.sell_orders != {} and order_depth.buy_orders != {}):
                #     mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                #     self.bananas_sum += mid_price
                #     self.b_num += 1
                
                
                # # Initialize the list of Orders to be sent as an empty list
                # orders: list[Order] = []

                # # Define a fair value for the PEARLS.
        
                # acceptable_price = 4950
                # if(self.b_num > 10): #Start using the average price when have enough data (10 samples?)
                #     acceptable_price = self.bananas_sum / self.b_num #comment this line out to go back to old version
                
                
                # # If statement checks if there are any SELL orders in the PEARLS market
                # if len(order_depth.sell_orders) > 0:

                #     # Sort all the available sell orders by their price,
                #     # and select only the sell order with the lowest price
                #     best_ask = min(order_depth.sell_orders.keys())
                #     best_ask_volume = order_depth.sell_orders[best_ask] #This will be a negative number

                #     # Check if the lowest ask (sell order) is lower than the above defined fair value
                #     if best_ask < acceptable_price and position < LIMIT:
                #         best_ask_volume = max(best_ask_volume, position - LIMIT)

                #         # In case the lowest ask is lower than our fair value,
                #         # This presents an opportunity for us to buy cheaply
                #         # The code below therefore sends a BUY order at the price level of the ask,
                #         # with the same quantity
                #         # We expect this order to trade with the sell order
                #         print("BUY", str(-best_ask_volume) + "x", best_ask, product)
                #         orders.append(Order(product, best_ask, -best_ask_volume))

                # # The below code block is similar to the one above,
                # # the difference is that it finds the highest bid (buy order)
                # # If the price of the order is higher than the fair value
                # # This is an opportunity to sell at a premium
                # if len(order_depth.buy_orders) != 0:
                #     best_bid = max(order_depth.buy_orders.keys())
                #     best_bid_volume = order_depth.buy_orders[best_bid] #this will be positive volume
                    
                    
                #     if best_bid > acceptable_price and position > -LIMIT:
                #         best_bid_volume = min(best_bid_volume, LIMIT + position)
                        
                #         print("SELL", str(best_bid_volume) + "x", best_bid, product)
                #         orders.append(Order(product, best_bid, -best_bid_volume))

                # # Add all the above orders to the result dict
                # result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for BANANAS
                # Depending on the logic above
                
                
                
                
                
                
        
        #PAIRS TRADING - ROUGH IDEA:
        CUTOFF = 10 #choose some value
        mean_ratio = 15000/8000 #we could use empirical mean instead of given prices
        
        coco_book: OrderDepth = state.order_depths["COCONUTS"]
        pina_book: OrderDepth = state.order_depths["PINA_COLADAS"]
        
        coco_best_ask = min(coco_book.sell_orders.keys())
        pina_best_buy = max(pina_book.buy_orders.keys())
        
        pina_best_ask = min(pina_book.sell_orders.keys())
        coco_best_buy = max(coco_book.buy_orders.keys())
        
        
        if (coco_best_buy * mean_ratio - pina_best_ask) > CUTOFF:
            #buy pinas, sell coconuts
            pina_vol = - pina_book.sell_orders[pina_best_ask]
            coco_vol = coco_book.buy_orders[coco_best_buy]
            trade_vol = min(pina_vol, coco_vol)
            result["PINA_COLADAS"] = [Order("PINA_COLADAS", pina_best_ask, trade_vol)]
            result["COCONUTS"] = [Order("COCONUTS", coco_best_buy, -trade_vol)] #negative trade_vol since its a sell
            #Should do some kind of position-limit checking

        if (pina_best_buy - coco_best_ask * mean_ratio) > CUTOFF:
            #SELL pinas, buy coconuts
            pina_vol = pina_book.buy_orders[pina_best_buy]
            coco_vol = - coco_book.sell_orders[coco_best_ask]
            trade_vol = min(pina_vol, coco_vol)
            result["PINA_COLADAS"] = [Order("PINA_COLADAS", pina_best_buy, -trade_vol)]
            result["COCONUTS"] = [Order("COCONUTS", coco_best_ask, trade_vol)] #negative trade_vol since its a sell
            #Should do some kind of position-limit checking

   
        
                
        return result