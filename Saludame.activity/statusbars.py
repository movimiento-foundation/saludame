# -*- coding: utf-8 -*-

import pygame
import window
from window import StatusBar

"""
 ****************** VISUALES ******************
"""
class BarsWindow(window.Window):
    
    def __init__(self, rect, frame_rate, background_color):
        self.rect = pygame.Rect((0, 0), (400, 450))
        self.frame_rate = frame_rate
        self.surface = pygame.Surface(self.rect.size)
        self.background_color = background_color
        self.surface.fill(self.background_color)
        
        loader = BarsLoader()

        self.bars = loader.create_bars(Bar("main_bar", "overall", None, [], 100, 50))
        
        self.physica_section = BarSection("physica", self.bars[0], self.bars[0].children_list, (398, 68), (1, 39))
        self.fun_section = BarSection("fun", self.bars[3], self.bars[3].children_list, (398, 73), (1, 108))
        self.hygiene_section = BarSection("hygiene", self.bars[1], self.bars[1].children_list, (398, 94), (1, 182))
        self.nutrition_section = BarSection("nutrition", self.bars[2], self.bars[2].children_list, (398, 172), (1, 277))
        self.main_section = BarSection("overall", self.bars[4], [] , (398, 37), (1, 1))
   
    def draw(self, screen):
        self.surface.fill(self.background_color)
        screen.blit(self.surface, self.rect)
        
        changes = []
        changes += self.physica_section.draw(self.surface)
        changes += self.hygiene_section.draw(self.surface)
        changes += self.fun_section.draw(self.surface)
        changes += self.nutrition_section.draw(self.surface)
        changes += self.main_section.draw(self.surface)
        changes += [self.rect]
        
        screen.blit(self.surface, self.rect)
        
        return changes

class BarSection:
    
    def __init__(self, name, root_bar, children_bar, size, position):
        self.name = name
        self.root_bar = root_bar
        self.root_bar_display = BarDisplay(26, (size[0] - 2), (1, (size[1] / 2) - 13), self.root_bar)
        self.children_bar = children_bar
        self.rect = pygame.Rect(position, size)
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill((2, 45, 126))
        self.displays_list = self.__calculate(children_bar)
        self.selected = False #Este flag se activa cuando se están mostrando las sub-barras
        
    def draw(self, screen):
        changes = []
        if (self.selected and len(self.children_bar) > 0):
            for bar_display in self.displays_list:
                changes += bar_display.draw(self.surface)
        else:
            changes += self.root_bar_display.draw(self.surface)
        screen.blit(self.surface, self.rect)
        
        return changes 
        
    def __calculate(self, children_bar):
        qty = len(children_bar)
        if(qty == 0):
            qty = 1
        bar_height = int((self.rect.height / qty) - 2)
        bar_width = int(self.rect.width - 2)
        display_list = []
        print bar_height
        
        y = int(self.rect.height / bar_height) # margen vertical
        for status_bar in children_bar:
            display = BarDisplay(bar_height, bar_width, (1, y), status_bar)
            display_list.append(display)
            y += (bar_height + 1)
        
        return display_list
    
class BarDisplay:
    
    def __init__(self, height, width, position, status_bar):
        self.label = status_bar.label
        self.status_bar = status_bar
        self.rect = pygame.Rect(position, (width, height))
        self.position = position
        self.color = pygame.Color(0, 255, 0, 1)
        self.surface = pygame.Surface(self.rect.size)
        self.font = pygame.font.Font(None, 20)
        
    def draw(self, screen):
        
        charge = pygame.Rect((1, 2), (self.rect.width - 2, self.rect.height - 4))
        charge.width = self.status_bar.value * self.rect.width / self.status_bar.max
        charge_surface = pygame.Surface(charge.size)
        charge_surface.fill(pygame.Color("blue"))
        
        self.surface.fill(pygame.Color("black"))
        self.surface.blit(charge_surface, charge)
        
        self.surface.blit(self.font.render(self.label, 1, (255, 0, 0)), (2, 5))
        
        
        screen.blit(self.surface, self.rect)
        
        return [self.rect]
    
"""
****************** MODELOS ******************
"""    

class BarsController:
    """
    Controlador general de las barras, encargado de enviar la señal de decremento o incremento
    a una barra especifica
    """
    def __init__(self):
        self.main_bar = StatusBar("main_bar", None, [], 100, 50)
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
    
    def __init__(self, id, label, parent_bar, children_list, max_value, init_value):
        self.id = id
        self.label = label
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
            
"""
****************** CREADORES ******************
"""

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
        physica = Bar("physica", "Physica", main_bar, [], hard_level[0], hard_level[1])
        physica_children_bar = [Bar(id, id, physica, [], hard_level[0], hard_level[1]) for id in physica_children_id]
        physica.children_list = physica_children_bar
        
        """ hygiene """
        hygiene_children_id = [("shower", "shower"), ("w_hands", "washing hands"), ("b_teeth", "brushing teeth"), ("toilet", "toilet")]
        hygiene = Bar("hygiene", "Hygiene", main_bar, [], hard_level[0], hard_level[1])
        hygiene_children_bar = [Bar(id[0], id[1], hygiene, [], hard_level[0], hard_level[1]) for id in hygiene_children_id]
        hygiene.children_list = hygiene_children_bar

        """ nutrition """
        nutrition_children_id = [("c_leguminosas", "cereales y leguminosas"), ("v_frutas", "verduras y frutas"), ("C_huevos", "carnes y huevos"), ("dulces", "dulces"), ("g_aceites", "grasas y aceites"), ("l_quesos", "leches y quesos"), ("agua", "agua")]
        nutrition = Bar("nutrition", "Nutrition", main_bar, [], hard_level[0], hard_level[1])
        nutrition_children_bar = [Bar(id[0], id[1], nutrition, [], hard_level[0], hard_level[1]) for id in nutrition_children_id]
        nutrition.children_list = nutrition_children_bar
        
        """ fun """
        fun_children_id = ["sports", "playing", "relaxing"]
        fun = Bar("fun", "Fun", main_bar, [], hard_level[0], hard_level[1])
        fun_children_bar = [Bar(id, id, fun, [], hard_level[0], hard_level[1]) for id in fun_children_id]
        fun.children_list = fun_children_bar
        
        bars_list = [physica, hygiene, nutrition, fun, main_bar]
        
        #displays_list = [BarDisplay(pygame.Rect((0 , 0), (200, 26)), pygame.Color(255, 0, 0, 1), bar) for bar in bars_list]
 
        return bars_list
