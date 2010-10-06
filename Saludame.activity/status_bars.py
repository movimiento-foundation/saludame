# -*- coding: utf-8 -*-

import pygame
import status_bars_creator

"""
 ****************** VISUALES ******************
"""
class BarsWindow():
    """
    Clase que representa la ventana de las barras de estado del juego.
    """
    def __init__(self, position, frame_rate, background_color):
        self.frame_rate = frame_rate
        """ visual constant """
        self.max_bar_qty = 7
        self.px_per_bar = 26
        self.px_per_section = 50
        self.px_expanded = self.max_bar_qty * self.px_per_bar + 2
        self.qty_section = 50
        """ rect and surface: """
        self.rect = pygame.Rect(position, (400, 484))
        self.surface = pygame.Surface(self.rect.size)
        self.background_color = background_color
        self.surface.fill(self.background_color)
        
        """ game bars """
        loader = status_bars_creator.BarsLoader()
        self.bars = loader.get_second_level_bars()
        
        """ sections """
        self.score_section = ScoreSection(StatusBar("score_bar", "score", None, loader.get_overall_bar(), 100, 15), (398, 50), (1, 1), 1)
        self.overall_section = BarSection("Estado general", loader.get_overall_bar(), [] , (398, 37), (1, 52), self.px_expanded)
        
        self.physica_section = BarSection("physica", self.bars[0], self.bars[0].children_list, (398, self.px_per_section), (1, 90), self.px_expanded)
        self.fun_section = BarSection("fun", self.bars[3], self.bars[3].children_list, (398, self.px_per_section), (1, 142), self.px_expanded)
        self.hygiene_section = BarSection("hygiene", self.bars[1], self.bars[1].children_list, (398, self.px_per_section), (1, 194), self.px_expanded)
        self.nutrition_section = BarSection("nutrition", self.bars[2], self.bars[2].children_list, (398, self.px_per_section), (1, 246), self.px_expanded)
        
        self.sections_list = [self.score_section, self.physica_section, self.fun_section, self.hygiene_section, self.nutrition_section, self.overall_section]
        self.accordeon = Accordeon([self.physica_section, self.fun_section, self.hygiene_section, self.nutrition_section], self.px_per_bar, self.px_per_section, self.px_expanded)
        """  """
        
    def draw(self, screen):
        self.surface.fill(self.background_color)
        changes = []
        for section in self.sections_list:
            changes += section.draw(self.surface)
       
        screen.blit(self.surface, self.rect)
        
        return changes
    
    def on_mouse_over(self):
        return
    
    def on_mouse_out(self):
        return
    
    def on_mouse_click(self, (x, y)):
        
        for section in self.accordeon.sections_list:
            if(section.rect.collidepoint((x, y))):
                if(not section.expanded):
                    self.accordeon.expand_section(section)
    
    def __relative_pos(self, (x, y)):
        return (x + self.rect.left, y + self.rect.top)

class Accordeon:
    """
    Clase encargada de realizar los calculos para expandir y 
    contraer las secciones.
    """
    
    def __init__(self, sections_list, px_per_bar, px_per_section, px_expanded):
        self.sections_list = sections_list #secciones sobre las que se realizarán los cambios
        """
        Las secciones deben estar ordenadas de arriba abajo, según se muestren
        en la pantalla.
        """
        self.px_per_section = px_per_section #cantidad mínima de pixeles por sección
        self.px_expanded = px_expanded #cantidad que se suma a la cantidad mínima de pixeles por sección
        self.expand_section(self.sections_list[-1]) #inicialmente expande la última sección
    
    def expand_section(self, section):
        """
        Espande la sección 'section' y re calcula la
        posición del resto de las secciones.
        """
        self.__compress_sections()
        for i in range(0, len(self.sections_list)):
            if(self.sections_list[i] == section):
                if(i + 1 < len(self.sections_list)):
                    for j in range(i + 1, len(self.sections_list)):
                        self.sections_list[j].move_down()
                self.sections_list[i].expand()
                break
        
    def __compress_sections(self):
        """
        Comprime todas las secciones y las localiza
        en su posición inicial.
        """
        for i in range(0, len(self.sections_list)):
            if(self.sections_list[i].expanded):
                self.sections_list[i].compress()
                if(i + 1 < len(self.sections_list)):
                    for j in range(i + 1, len(self.sections_list)): #move up the displays under the expanded one
                        self.sections_list[j].move_up()
                break

class BarSection:
    """
    Clase que contiene un conjunto de BarDisplay, y las
    muestra por pantalla
    """
    
    def __init__(self, name, root_bar, children_bar, size, position, max_expand):
        """ section attributes """
        self.name = name
        self.root_bar = root_bar
        self.children_bar = children_bar
        self.rect = pygame.Rect(position, size)
        
        """ visuals """
        self.surface = pygame.Surface(self.rect.size)
        self.root_bar_display = BarDisplay(26, (size[0] - 2), (1, (size[1] / 2) - 13), self.root_bar, pygame.Color("blue"))
        self.displays_list = self.__get_displays() #obtengo los displays para cada barra.
        self.surface.fill((2, 45, 126)) #back ground color
        
        """ visuals constant """
        self.init_top = position[1]
        self.init_height = size[1]
        self.max_expand = max_expand
        """   """
        self.expanded = False #Este flag se activa cuando se están mostrando las sub-barras
        self.__calculate() #calculo la posición de cada barra en la sección
    
    def expand(self):
        """
        Expande la sección, y calcula la posición de las barras
        """
        self.expanded = True
        self.rect.height = self.init_height + self.max_expand
        self.__set_surface(self.rect.size)
        self.__calculate()
                
    def compress(self):
        """
        Comprime la sección, y re calcula la posición de las barras
        """
        self.expanded = False
        self.rect.height = self.init_height #vuelve al tamaño inicial
        self.rect.top = self.init_top
        self.__set_surface(self.rect.size)
        self.__calculate()
    
    def move_up(self):
        """
        Desplaza la sección a su posición original.
        """
        self.rect.top = self.init_top
        self.__calculate()
    
    def move_down(self):
        """
        Desplaza la sección desde su posición original a
        la posición original más el número de expanción
        máxima de una sección.
        """
        self.rect.top = self.init_top + self.max_expand
        self.__calculate()
        
    def draw(self, screen):
        changes = []
        if (self.expanded and len(self.children_bar) > 0):
            changes += self.root_bar_display.draw(self.surface)
            for bar_display in self.displays_list:
                changes += bar_display.draw(self.surface)
        else:
            changes += self.root_bar_display.draw(self.surface)
        screen.blit(self.surface, self.rect)
        
        return changes
        
    def __calculate(self):
        """
        Calcula la posición de cada barra
        dependiendo de si está expandida o no la sección.
        """
        qty = len(self.displays_list)
        if(self.expanded):
            if(qty == 0):
                qty = 1
            bar_height = 26
        
            y = 50
            for display in self.displays_list:
                display.rect.top = y
                y += (bar_height + 1)
        else:
            for display in self.displays_list:
                display.rect.top = 1 
                
    def __get_displays(self):
        """
        Crea un BarDisplay para cada barra hija de la sección.
        Y retorna una lista con los mismos.
        """
        display_list = []
        bar_height = 26
        color = pygame.Color(25, 255, 25, 1) #carga las barras hijas con el color verde por defecto.
        for status_bar in self.children_bar:
            display = BarDisplay(bar_height, 393, (1, 1), status_bar, color)
            display_list.append(display)
        return display_list
    
    def __set_surface(self, size):
        self.surface = pygame.Surface(size)
        self.surface.fill((2, 45, 126))
    
                   
    def __relative_pos(self, (x, y)):
        return (x + self.rect.left, y + self.rect.top)
    
class BarDisplay:
    """
    Clase que se encarga de representar visualmente a una barra, manteniéndose
    actualizada según los incrementos o decrementos de la barra representada.
    """
    
    def __init__(self, height, width, position, status_bar, color):
        """ attributes """
        self.status_bar = status_bar
        self.label = status_bar.label
        self.color = color
        self.rect = pygame.Rect(position, (width, height))
        self.position = position
        """ visuals """
        self.surface = pygame.Surface(self.rect.size)
        self.font = pygame.font.Font(None, 20)
        """ """
        self.last_value = self.status_bar.value #valor inicial
        self.charge = pygame.Rect((1, 2), (((self.rect.width - 2) * self.last_value / self.status_bar.max, self.rect.height - 4)))
        
    def draw(self, screen):
        if(self.last_value != self.status_bar.value):
            self.charge = pygame.Rect((1, 2), (self.rect.width - 2, self.rect.height - 4))
            self.charge.width = self.status_bar.value * self.rect.width / self.status_bar.max
         
        charge_surface = pygame.Surface(self.charge.size)
        charge_surface.fill(self.color)
        
        self.surface.fill(pygame.Color("black"))
        self.surface.blit(charge_surface, self.charge)
        
        self.surface.blit(self.font.render(self.label, 1, (0, 0, 0)), (2, 5))
        
        screen.blit(self.surface, self.rect)
        
        return [self.rect]
    
    def __relative_pos(self, (x, y)):
        #(x + self.rect.left, y + self.rect.top)
        return (x + self.rect.left, y + self.rect.top)
    
        
class ScoreSection:
    """
    Sección que muestra la barra de puntaje principal.
    """
    def __init__(self, bar, size, position, level):
        """ attributes """
        self.name = "score section"
        self.score_bar = bar
        self.level = level
        self.rect = pygame.Rect(position, size)
        """ visuals """
        self.score_bar_display = BarDisplay(26, (size[0] - 2), (1, (size[1] / 2) - 3), self.score_bar, pygame.Color("blue"))
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill((2, 45, 126))
        self.font = pygame.font.Font(None, 20)
        
        
        
    def draw(self, screen):
        #draw bar:
        self.score_bar_display.draw(self.surface)
        
        #write actual level:
        level_text = "Nivel: " + str(self.level)
        
        self.surface.blit(self.font.render(level_text, 1, (255, 255, 255)), (2, 5))
        
        screen.blit(self.surface, self.rect)
        return [self.rect]
    
    def __relative_pos(self, (x, y)):
        #(x + self.rect.left, y + self.rect.top)
        return (x + self.rect.left, y + self.rect.top)
    
"""
****************** MODELOS ******************
"""    

class BarsController:
    """
    Controlador general de las barras, encargado de enviar la señal de decremento o incremento
    a una barra especifica
    """
    def __init__(self):
        self.loader = status_bars_creator.BarsLoader()
        """ bars """
        self.overall_bar = self.loader.get_overall_bar()
        self.second_level = self.loader.get_second_level_bars()
        self.third_level = self.loader.get_third_level_bars()
        self.bars = [self.overall_bar] + self.second_level + self.third_level
        """      """
            
    def increase_bar(self, bar_id, increase_rate):
        
        for bar in self.bars:
            if(bar.id == bar_id):
                bar.increase(increase_rate)
                break
        
class StatusBar:
    """
    Entity that represent the bar
    """
    
    def __init__(self, id, label, parent_bar, children_list, max_value, init_value):
        """ attributes """
        self.id = id
        self.label = label
        self.max = max_value
        self.value = init_value
        self.parent = parent_bar # Barra padre
        self.children_list = children_list # conjunto de barras hijas
        
    def increase(self, increase_rate):
        """
        Incrementa el valor de la barra y repercute en los hijos y la barra padre
        """
        if(len(self.children_list) > 0):
            value = increase_rate / len(self.children_list) #para que el incremento de esta barra mantenga relacion con la de sus hijos
            self.value += value
            for child in self.children_list:
                child.increase(value)
        else:
            self.value += increase_rate

        if(self.parent != None):
            self.parent.increase_from_child(value)
    
    def increase_from_child(self, increase_rate):
        """
        Incrementa el valor de la barra.
        """
        if(len(self.children_list) > 0):
            value = increase_rate / len(self.children_list) #para que el incremento de esta barra mantenga relacion con la de sus hijos
            self.value += value
        else:
            self.value += increase_rate
        
        if(self.parent != None):
            self.parent.increase_from_child(value)
        
        if(self.value > self.max):
            self.value = self.max
        elif(self.value < 0):
            self.value = 0
        
    def increase_from_parent(self, increase_rate):
        """
        Incrementa el valor de la barra y repercute en los hijos.
        """
        if(len(self.children_list) > 0):
            value = increase_rate / len(self.children_list) #para que el incremento de esta barra mantenga relacion con la de sus hijos
            self.value += value
            for child in self.children_list:
                child.increase(value)
        else:
            self.value += increase_rate
        
        if(self.value > self.max):
            self.value = self.max
        elif(self.value < 0):
            self.value = 0
        
    def child_decrease(self, value):
        """
        Decremento recibido de un hijo, no repercute en los hijos del nodo que lo recibe. Solo en el
        actual y el padre.
        """
        assert(value > 0)
        if(len(self.children_list) > 0):
            value = value / len(self.children_list) #para que el decremento mantenga relación con el valor de las barras hijas
        if(self.value - value > 0):
            self.value -= value
        else:
            self.value -= value - self.value
        if(self.parent != None):
            self.parent.child_decrease(value)
    
    def child_increase(self, value):
        """
        Incremento recibido de un hijo. No repercute en los hijos, del nodo que recibió el incremento.
        Solo en el actual y en el padre.
        """
        if(len(self.children_list) > 0):
            value = value / len(self.children_list) #para que el incremento de esta barra mantenga relacion con la de sus hijos
        if(self.value + value <= self.max):
            self.value += value
        else:
            self.value += self.max - self.value
        if(self.parent != None):
            self.parent.child_increase(value)



