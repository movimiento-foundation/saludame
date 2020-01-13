# -*- coding: utf-8 -*-
from gi.repository import GObject


class Condition(GObject.Object):
    """ Defines a conditions according to bars values """
    
    def __init__(self, id, operand, bars):
        GObject.Object.__init__(self)
        self.id = id
        self.operand = operand  # all, any
        self.bars = bars        # list of tuples (bar_id, min, max)

    def evaluate(self, bars_value_dic):
        
        condition = False
        
        for bar_con in self.bars:
            bar_id, min_value, max_value = bar_con
            
            value = bars_value_dic[bar_id]
            
            condition = min_value <= value and value <= max_value
            
            if self.operand == "all" and not condition:
                return False
            elif self.operand == "any" and condition:
                return True
            
        return condition
