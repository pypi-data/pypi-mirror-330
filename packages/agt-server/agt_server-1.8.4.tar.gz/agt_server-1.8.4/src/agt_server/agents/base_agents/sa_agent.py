from agt_server.agents.base_agents.agent import Agent
from agt_server.agents.base_agents.game_report import GameReport
import json
import random
import numpy as np 
import pkg_resources


class SimultaneousAuctionAgent(Agent):
    def __init__(self, name=None, timestamp=None):
        super().__init__(name, timestamp)
        config_path = pkg_resources.resource_filename('agt_server', 'configs/server_configs/sa_config.json')
        with open(config_path) as cfile:
            self.config = json.load(cfile)
        self.response_time = self.config['response_time']

        # To be set by the game
        self.num_goods = None
        self.valuation_type = None
        self.valuations = None
        self._goods_to_index = None
        self.goods = None
        self._index_to_goods = None

    def timeout_handler(self):
        print(f"{self.name} has timed out")
        self.timeout = True

    def handle_permissions(self, resp):
        self.player_type = resp['player_type']
        self.game_report.game_history['my_bid_history'].append(resp['my_bid'])
        self.game_report.game_history['my_utils_history'].append(resp['my_util'])
        self.game_report.game_history['my_payment_history'].append(resp['my_payment'])
        self.game_report.game_history['price_history'].append(resp['prices'])
        self.game_report.game_history['winner_history'].append(resp['winners'])
    
    def handle_postround_data(self, resp):
        self.global_timeout_count = resp['global_timeout_count']
        self.handle_permissions(resp)

    def get_action(self):
        return self.get_bids()
     
    def get_goods(self): 
        """
        Get the set of goods names available in the auction.

        Returns:
        - A set of strings representing the names of the goods.
        """
        return self.goods 

    def get_num_goods(self): 
        """
        Get the total number of goods available.

        Returns:
        - An integer representing the total number of goods.
        """
        return self.num_goods
    
    def get_goods_to_index(self): 
        """
        Get the mapping from goods names to their index in the goods space.

        Returns:
        - A dictionary mapping string names to tuple indices.
        """
        return self._goods_to_index
    
    def calculate_valuation(self, goods):
        """
        Calculate the valuation for a given set of goods.

        Parameters:
        - goods (list): A list of goods for which to calculate the valuation.

        Returns:
        - A float representing the valuation for the given goods.
        """   

        # if goods is a list of strings turn it into indices
        if isinstance(goods, list):
            if all(isinstance(good, str) for good in goods):
                goods = [self._goods_to_index[good] for good in goods]
        
        return np.sum(self.valuations[goods])
    
    def calculate_price(self, goods):
        """
        Calculate the price for a given set of goods.

        Parameters:
        - goods (list): A list of goods for which to calculate the price.

        Returns:
        - A float representing the price for the given goods.
        """   

        # if goods is a list of strings turn it into indices
        if isinstance(goods, list):
            if all(isinstance(good, str) for good in goods):
                goods = [self._goods_to_index[good] for good in goods]
        
        return np.sum(self.current_prices[goods])
    
    def calculate_total_util(self, goods):
        """
        Calculate the utility for a given set of goods.

        Parameters:
        - goods (list): A list of goods for which to calculate the utility.

        Returns:
        - A float representing the utility for the given goods.
        """   
        
        return self.calculate_valuation(goods) - self.calculate_price(goods)
    
    def get_valuation_as_array(self): 
        """
        Retrieves the agent's valuation as a numpy array.
        
        Returns:
        - numpy.ndarray: The valuation array.
        """
        return self.valuations
    
    def get_valuation(self, good): 
        """
        Retrieves the valuation for a specific good.
        
        Parameters:
        - good (str): The name of the good.
        
        Returns:
        - float: The valuation for the specified good.
        """
        return self.valuations[self._goods_to_index[good]]
    
    def get_valuations(self, bundle = None): 
        """
        Retrieves the valuations for a set of goods.
        
        Parameters:
        - bundle (set, optional): A set of goods for which valuations are retrieved. If None, uses all goods.
        
        Returns:
        - dict: A mapping from goods to their valuations.
        """
        if bundle is None: 
            bundle = self.goods
        return {good: self.valuations[self._goods_to_index[good]] for good in bundle}
    
    def get_game_report(self): 
        """
        Retrieves the game report containing the history and outcomes of all the rounds the agent has participated in.

        Returns:
        - GameReport: The game report object.
        """
        return self.game_report
    
    def get_valuation_history(self):
        """
        Retrieves the valuation history for the agent, showing how the agent's valuation has changed over time.

        Returns:
        - list: A list of valuation values, one for each round.
        """
        return self.game_report.get_valuation_history()

    def get_util_history(self):
        """
        Retrieves the utility history for the agent, showing how the agent's utility has changed over time.

        Returns:
        - list: A list of utility values, one for each round.
        """
        return self.game_report.get_util_history()

    def get_bid_history(self): 
        """
        Retrieves the history of bids made [AS A NDARRAY].

        :return: A list of bids (np.ndarrays) if available; otherwise, an empty list.
        """
        return self.game_report.get_bid_history()
    

    def get_payment_history(self):
        """
        Retrieves the history of payments made.

        :return: A list of payments if available; otherwise, an empty list.
        """
        return self.game_report.get_payment_history()
    
    def get_price_history(self):
        """
        Retrieves the history of prices for the goods.

        :return: A list of prices if available; otherwise, an empty list.
        """
        return self.game_report.get_price_history()
    
    def get_winner_history(self): 
        """
        Retrieves the history of winners [AS A NDARRAY of OBJECTS].

        :return: A list of winners (np.ndarrays) if available; otherwise, an empty list.
        """
        return self.game_report.get_winner_history()
    

    

    