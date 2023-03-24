# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 00:44:47 2023

@author: eddyz
"""

from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:
    def __init__(self):
        self.bananas_sum = 0
        self.pearls_sum = 0
        self.b_num = 0
        self.p_num = 0
    
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
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
                if(self.p_num > 10):
                    acceptable_price = self.pearls_sum / self.p_num

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
                
                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                if(order_depth.sell_orders != {} and order_depth.buy_orders != {}):
                    mid_price = (min(order_depth.sell_orders.keys()) + max(order_depth.buy_orders.keys()))/2
                    self.bananas_sum += mid_price
                    self.b_num += 1
                
                
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!
                acceptable_price = 4950
                if(self.b_num > 10):
                    acceptable_price = self.bananas_sum / self.b_num
                
                
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
                # These possibly contain buy or sell orders for BANANAS
                # Depending on the logic above
        return result