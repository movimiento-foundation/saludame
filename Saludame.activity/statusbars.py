# -*- coding: utf-8 -*-
class BarsController:
    """
    Controlador general de las barras, encargado de enviar la señal de decremento o incremento
    a una barra especifica
    """
    def __init__(self):
        self.main_bar = Bar("main_bar", None, [], 100, 50)
        self.second_level_bar = BarsLoader.create_bars()
        self.main_bar.children_list = self.second_level_bar
        third_level_bar = []
        for bar in self.second_level_bar:
            third_level_bar += [child_bar for child_bar in bar.children_list]
            
    def increase_bar(self, id, value):
        return

    def decrease_bar(self, id, value):
        return
        
class Bar:
    """
    Entity that represent the bar
    """
    
    def __init__(self, id, parent_bar, children_list, max_value, init_value):
        self.id = id
        self.max = max_value
        self.value = init_value
        self.parent = parent_bar # Barra padre
        self.children_list = children_list # conjunto de barras hijas
        
    def increase(self, value):
        """
        Incrementa el valor de la barra y repercute en los hijos y la barra padre
        """
        if(len(self.children_list) > 0):
            value = value / len(self.children_list) #para que el incremento de esta barra mantenga relacion con la de sus hijos
        if(self.value + value <= self.max):
            self.value += value
        else:
            self.value += self.max - self.value
        for child in self.children_list:
            child.increase(value)
        if(self.parent != None):
            self.parent.increase(value)
            
    def decrease(self, value):
        """
        Decrementa el valor de la barra y repercute en los hijos y la barra padre
        """
        assert(value > 0)
        if(len(self.children_list) > 0):
            value = value / len(self.children_list) #para que el decremento mantenga relación con el valor de las barras hijas
        if(self.value - value > 0):
            self.value -= value
        else:
            self.value -= value - self.value
        for child in self.children_list:
            child.decrease(value)
        if(self.parent != None):
            self.parent.decrease(value)

class BarsLoader:
    """
    This is just for create the bars, and not full
    of this static code the others class.
    """
    
    def create_bars(self, main_bar):
        
        hard_level = (100, 50) 
        """'hard_level' para plasmar que la idea es que los valores por defecto de las barras
        se carguen según un nivel de dificultad"""
        """ physica """
        physica_children_id = ["energy", "resistencia", "fat"]
        physica = Bar("physica", main_bar, [], hard_level[0], hard_level[1])
        physica_children_bar = [Bar(id, physica, [], hard_level[0], hard_level[1]) for id in physica_children_id]
        physica.children_list = physica_children_bar
        
        """ hygiene """
        hygiene_children_id = ["shower", "w_hands", "b_teeth", "toilet"]
        hygiene = Bar("hygiene", main_bar, [], hard_level[0], hard_level[1])
        hygiene_children_bar = [Bar(id, hygiene, hard_level[0], hard_level[1]) for id in hygiene_children_id]
        hygiene.children_list = hygiene_children_bar

        """ nutrition """
        nutrition_children_id = ["c_leguminosas", "v_frutas", "C_huevos", "dulces", "g_aceites", "l_quesos", "agua"]
        nutrition = Bar("nutrition", main_bar, [], hard_level[0], hard_level[1])
        nutrition_children_bar = [Bar(id, nutrition, hard_level[0], hard_level[1]) for id in nutrition_children_id]
        nutrition.children_list = nutrition_children_bar
        
        """ fun """
        fun_children_id = ["sports", "playing", "relaxing"]
        fun = Bar("fun", main_bar, [], hard_level[0], hard_level[1])
        fun_children_bar = [Bar(id, fun, hard_level[0], hard_level[1]) for id in fun_children_id]
        fun.children_list = fun_children_bar
 
        return [physica, hygiene, nutrition, fun]

        
        
        
        
        
        
