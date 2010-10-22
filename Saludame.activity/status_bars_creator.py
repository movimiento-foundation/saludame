# -*- coding: utf-8 -*-

import status_bars

class BarsLoader:
    """
    This is just for create the bars, and not full
    of this static code the others class.
    """
    
    def __init__(self):
        self.main_bar = status_bars.StatusBar("main_bar", "overall", None, [], 100, 50)
        
        hard_level = (100, 50) 
        
        #'hard_level' para plasmar que la idea es que los valores por defecto de las barras
        #se carguen segun un nivel de dificultad
        # physica
        physica_children_id = ["Energy", "Resistencia", "Fat"]
        physica = status_bars.StatusBar("physica", "Physica", self.main_bar, [], hard_level[0], hard_level[1])
        physica_children_bar = [status_bars.StatusBar(id, id, physica, [], hard_level[0], hard_level[1]) for id in physica_children_id]
        physica.children_list = physica_children_bar
        
        ### hygiene
        hygiene_children_id = [("shower", "Shower"), ("w_hands", "Washing hands"), ("b_teeth", "Brushing teeth"), ("toilet", "Toilet")]
        hygiene = status_bars.StatusBar("hygiene", "Hygiene", self.main_bar, [], hard_level[0], hard_level[1])
        hygiene_children_bar = [status_bars.StatusBar(id[0], id[1], hygiene, [], hard_level[0], hard_level[1]) for id in hygiene_children_id]
        hygiene.children_list = hygiene_children_bar

        ### nutrition 
        nutrition_children_id = [("c_leguminosas", "Cereales y leguminosas"), ("v_frutas", "Verduras y frutas"), ("C_huevos", "Carnes y huevos"), ("dulces", "Dulces"), ("g_aceites", "Grasas y aceites"), ("l_quesos", "Leches y quesos"), ("agua", "Agua")]
        nutrition = status_bars.StatusBar("nutrition", "Nutrition", self.main_bar, [], hard_level[0], hard_level[1])
        nutrition_children_bar = [status_bars.StatusBar(id[0], id[1], nutrition, [], hard_level[0], hard_level[1]) for id in nutrition_children_id]
        nutrition.children_list = nutrition_children_bar
        
        ### fun 
        fun_children_id = ["Sports", "Playing", "Relaxing"]
        fun = status_bars.StatusBar("fun", "Fun", self.main_bar, [], hard_level[0], hard_level[1])
        fun_children_bar = [status_bars.StatusBar(id, id, fun, [], hard_level[0], hard_level[1]) for id in fun_children_id]
        fun.children_list = fun_children_bar
        
        self.second_level = [physica, hygiene, nutrition, fun]
        self.third_level = physica.children_list + hygiene.children_list + nutrition.children_list + fun.children_list
        
        self.main_bar.children_list = self.second_level
        
        self.bars = self.second_level + self.third_level + [self.main_bar]
        
        self.bars_controller = status_bars.BarsController(self.bars)
        
    def get_bar_controller(self):
        return self.bars_controller
    
    def get_second_level_bars(self):
        return self.second_level
    
    def get_third_level_bars(self):
        return self.third_level
    
    def get_overall_bar(self):
        return self.main_bar
    
    def get_score_bar(self):
        return self.score_bar
    
    
    



