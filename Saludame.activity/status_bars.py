# -*- coding: utf-8 -*-

import pygame
from gettext import gettext as _

import status_bars_creator
from window import *

SECTION_OFFSET_X = 12
SECTION_WIDTH = 182
SECTION_MIN_HEIGHT = 30
BAR_WIDTH = 182
BAR_HEIGHT = 26
ROOT_BAR_COLOR = pygame.Color("blue")
SUB_BAR_COLOR = pygame.Color("green")

"""
 ****************** VISUALES ******************
"""
class BarsWindow(Window):
    """
    Clase que representa la ventana de las barras de estado del juego.
    """
    def __init__(self, container, rect, frame_rate, windows_controller):
        Window.__init__(self, container, rect, frame_rate, windows_controller)
        
        # rect and surface:
        self.rect.size = (227, 590)
       
        # game bars
        loader = status_bars_creator.BarsLoader()
        self.bars = loader.get_second_level_bars()
        
        # sections
        self.score_section = ScoreSection(StatusBar("score_bar", "score", None, loader.get_overall_bar(), 100, 15), (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 0), 1)
        self.overall_section = BarSection(windows_controller, _("Total"), loader.get_overall_bar(), [] , (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 32))
        
        self.physica_section = BarSection(windows_controller, _("physica"), self.bars[0], self.bars[0].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 60))
        self.hygiene_section = BarSection(windows_controller, _("hygiene"), self.bars[1], self.bars[1].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 80))
        self.nutrition_section = BarSection(windows_controller, _("nutrition"), self.bars[2], self.bars[2].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 100))
        self.spare_time_section = BarSection(windows_controller, _("spare time"), self.bars[3], self.bars[3].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 120))
        
        self.sections_list = [self.score_section, self.overall_section, self.physica_section, self.hygiene_section, self.nutrition_section, self.spare_time_section]
        self.accordeon = Accordeon([self.physica_section, self.hygiene_section, self.nutrition_section, self.spare_time_section])
        
        self.set_bg_image("assets/layout/status.png")
        
        #self.score_section,
        self.windows += [section for section in self.sections_list if section != self.score_section]    # Score section no va porque no está convertida a window
        
    def on_mouse_over(self):
        return
    
    def on_mouse_out(self):
        return
    
    def handle_mouse_down(self, (x, y)):
        for section in self.accordeon.sections_list:
            if section.rect.collidepoint((x, y)):
                if section.expanded:
                    self.accordeon.compress_sections()
                else:
                    self.accordeon.expand_section(section)
                break
        self.repaint = True     # Makes the window repaint its background
    
class Accordeon:
    """
    Clase encargada de realizar los calculos para expandir y 
    contraer las secciones.
    """
    
    def __init__(self, sections_list):
        """
        Las secciones deben estar ordenadas de arriba abajo, según se muestren
        en la pantalla.
        """
        self.sections_list = sections_list # secciones sobre las que se realizarán los cambios
        self.expand_section(None)
    
    def expand_section(self, section):
        """
        Espande la sección 'section' y re calcula la
        posición del resto de las secciones.
        """
        self.compress_sections()
        for i in range(0, len(self.sections_list)):
            
            if(self.sections_list[i] == section):
                
                self.sections_list[i].expand()
                offset = self.sections_list[i].max_expand
                
                # The sections under this one must be moved down according to the expanded offset
                for j in range(i + 1, len(self.sections_list)):
                    self.sections_list[j].move_down(offset)
                break
        
    def compress_sections(self):
        """
        Comprime todas las secciones y las localiza en su posición inicial.
        """
        for section in self.sections_list: # move up the sections
            section.compress()
            section.move_up()

class BarSection(Window):
    """
    Clase que contiene un conjunto de BarDisplay, y las
    muestra por pantalla
    """
    
    def __init__(self, windows_controller, name, root_bar, children_bar, size, position):
        
        rect = pygame.Rect(position, size)
        Window.__init__(self, rect, rect, 1, windows_controller)
        
        # section attributes
        self.name = name
        self.root_bar = root_bar
        self.children_bar = children_bar
        
        # visuals
        self.root_bar_display = BarDisplay(BAR_HEIGHT, (size[0] - 2), (1, (size[1] / 2) - 13), self.root_bar, ROOT_BAR_COLOR)
        self.displays_list = self.__get_displays()      # obtengo los displays para cada barra.
        
        # visuals constant
        self.init_top = self.rect[1]
        self.init_height = size[1]
        self.max_expand = len(children_bar) * (BAR_HEIGHT + 1)
        
        self.expanded = False   # Este flag se activa cuando se están mostrando las sub-barras
        self.__calculate()      # calculo la posición de cada barra en la sección
    
    def expand(self):
        """
        Expande la sección, y calcula la posición de las barras
        """
        self.expanded = True
        self.rect.height = self.init_height + self.max_expand
        self.__calculate()
                
    def compress(self):
        """
        Comprime la sección, y re calcula la posición de las barras
        """
        self.expanded = False
        self.rect.height = self.init_height #vuelve al tamaño inicial
        self.rect.top = self.init_top
        self.__calculate()
    
    def move_up(self):
        """
        Desplaza la sección a su posición original.
        """
        self.rect.top = self.init_top
        self.__calculate()
    
    def move_down(self, offset):
        """
        Desplaza la sección desde su posición original a la posición original
        más el desplazamiento que provocó la sección expandida.
        """
        self.move((0, offset))
        
    def __calculate(self):
        """
        Calcula la posición de cada barra
        dependiendo de si está expandida o no la sección.
        """
        
        # Refresh the absolute position of the root bar
        self.root_bar_display.container = self.rect
        self.root_bar_display.set_rect_in_container(self.root_bar_display.rect_in_container)
        
        self.widgets = [self.root_bar_display]
        
        if(self.expanded):
            y = 0
            for display in self.displays_list:
                y += (BAR_HEIGHT + 1)
                display.container = self.rect
                
                display.rect_in_container.top = y
                display.set_rect_in_container(display.rect_in_container)
                
                self.widgets.append(display)
        
    def __get_displays(self):
        """
        Crea un BarDisplay para cada barra hija de la sección.
        Y retorna una lista con los mismos.
        """
        display_list = []
        for status_bar in self.children_bar:
            display = BarDisplay(BAR_HEIGHT, BAR_WIDTH, (1, 1), status_bar, SUB_BAR_COLOR)
            display_list.append(display)
        return display_list

class BarDisplay(Widget):
    """
    Clase que se encarga de representar visualmente a una barra, manteniéndose
    actualizada según los incrementos o decrementos de la barra representada.
    """
    
    def __init__(self, height, width, position, status_bar, color):
        
        rect = pygame.Rect(position, (width, height))
        surface = pygame.image.load("assets/layout/main_bar_back.png").convert_alpha()
        Widget.__init__(self, pygame.Rect(0, 0, height, width), rect, 1, surface)
        
        # attributes
        self.status_bar = status_bar
        self.label = status_bar.label
        self.color = color
        self.position = position
        self.surface = surface.copy()
        
        # visuals
        self.surface = pygame.Surface(self.rect_in_container.size)
        self.font = pygame.font.Font(None, 20)
        
        self.last_value = self.status_bar.value #valor inicial
        self.charge = pygame.Rect((1, 2), (((self.rect_in_container.width - 2) * self.last_value / self.status_bar.max, self.rect_in_container.height - 4)))
        
    def draw(self, screen):
        if(self.last_value != self.status_bar.value):
            self.charge = pygame.Rect((1, 2), (self.rect_in_container.width - 2, self.rect_in_container.height - 4))
            self.charge.width = self.status_bar.value * self.rect.width / self.status_bar.max
         
        charge_surface = pygame.Surface(self.charge.size)
        charge_surface.fill(self.color)
        
        self.surface.blit(charge_surface, self.charge)
        self.surface.blit(self.background, (0, 0))   # Background blits over the charge, because it has the propper alpha
        
        self.surface.blit(self.font.render(self.label, 1, (0, 0, 0)), (2, 5))
        
        screen.blit(self.surface, self.rect_absolute)
        
        return self.rect_absolute
    

class ScoreSection:
    """
    Sección que muestra la barra de puntaje principal.
    """
    def __init__(self, bar, size, position, level):
        # attributes
        self.name = "score section"
        self.score_bar = bar
        self.level = level
        self.rect = pygame.Rect(position, size)
        
        # visuals
        self.score_bar_display = BarDisplay(BAR_HEIGHT, (size[0] - 2), (1, (size[1] / 2) - 3), self.score_bar, pygame.Color("blue"))
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
        # bars
        self.overall_bar = self.loader.get_overall_bar()
        self.second_level = self.loader.get_second_level_bars()
        self.third_level = self.loader.get_third_level_bars()
        self.bars = [self.overall_bar] + self.second_level + self.third_level
            
    def increase_bar(self, bar_id, increase_rate):
        
        for bar in self.bars:
            if(bar.id == bar_id):
                bar.increase(increase_rate)
                break
        
class StatusBar:
    """
    Entity that represents the bar
    """
    
    def __init__(self, id, label, parent_bar, children_list, max_value, init_value):
        # attributes
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
