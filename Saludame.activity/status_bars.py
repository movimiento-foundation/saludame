# -*- coding: utf-8 -*-

import pygame
from gettext import gettext as _

import status_bars_creator
from window import *

SECTION_OFFSET_X = 0
SECTION_WIDTH = 182
SECTION_MIN_HEIGHT = 40
SECTION_TOP_PADDING = 12
BAR_OFFSET_X = 30
BAR_WIDTH = 182
BAR_HEIGHT = 26
BAR_BACK_COLOR = pygame.Color("#106168")
ROOT_BAR_COLOR = pygame.Color("blue")
SUB_BAR_COLOR = pygame.Color("green")


# ****************** VISUALES ******************

class BarsWindow(Window):
    """
    Clase que representa la ventana de las barras de estado del juego.
    """
    def __init__(self, container, rect, frame_rate, windows_controller, bars_loader):
        Window.__init__(self, container, rect, frame_rate, windows_controller)
        
        # rect and surface:
        self.rect.size = (227, 590)
       
        # game bars
        self.bars = bars_loader.get_second_level_bars()
        
        # sections
        self.score_section = ScoreSection(StatusBar("score_bar", "score", None, bars_loader.get_overall_bar(), 100, 15), self.rect, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X + 25, 4), 1)
        self.overall_section = BarSection(windows_controller, _("Total"), bars_loader.get_overall_bar(), [] , (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 27), "assets/layout/icon_total.png")
        
        self.physica_section = BarSection(windows_controller, _("physica"), self.bars[0], self.bars[0].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 60), "assets/layout/icon_physica.png")
        self.hygiene_section = BarSection(windows_controller, _("hygiene"), self.bars[1], self.bars[1].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 90), "assets/layout/icon_hygiene.png")
        self.nutrition_section = BarSection(windows_controller, _("nutrition"), self.bars[2], self.bars[2].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 120), "assets/layout/icon_nutrition.png")
        self.spare_time_section = BarSection(windows_controller, _("spare time"), self.bars[3], self.bars[3].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, 150), "assets/layout/icon_spare_time.png")
        
        self.sections_list = [self.score_section, self.overall_section, self.physica_section, self.hygiene_section, self.nutrition_section, self.spare_time_section]
        self.accordeon = Accordeon([self.physica_section, self.hygiene_section, self.nutrition_section, self.spare_time_section])
        
        self.set_bg_image("assets/layout/status.png")
        
        self.windows += [section for section in self.sections_list if section != self.score_section]    # Score section no va porque no está convertida a window
        self.add_child(self.score_section)
    
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
    
    def __init__(self, windows_controller, name, root_bar, children_bar, size, position, icon_path):
        
        rect = pygame.Rect(position, size)
        Window.__init__(self, rect, rect, 1, windows_controller)
        
        # section attributes
        self.name = name
        self.root_bar = root_bar
        self.children_bar = children_bar
        
        # visuals
        self.root_bar_display = BarDisplay(BAR_HEIGHT, (size[0] - 2), (BAR_OFFSET_X, SECTION_TOP_PADDING), self.root_bar, ROOT_BAR_COLOR)
        self.displays_list = self.__get_displays()      # obtengo los displays para cada barra.
        
        self.fixed_widgets = []
        
        if icon_path:
            icon = pygame.image.load(icon_path).convert_alpha()
            self.icon = Widget(self.rect, pygame.Rect((0, 0), icon.get_size()), 1, icon)
            self.fixed_widgets.append(self.icon)
        else:
            self.icon = None
        
        
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
        self.icon.rect_absolute.top = self.init_top
        
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
    
    def draw(self, screen, frames):
        changes = Window.draw(self, screen, frames)
        return [self.rect]      # Drops individual changes and returns the whole section
    
    def __calculate(self):
        """
        Calcula la posición de cada barra
        dependiendo de si está expandida o no la sección.
        """
        
        # Refresh the absolute position of the root bar
        self.root_bar_display.container = self.rect
        self.root_bar_display.set_rect_in_container(self.root_bar_display.rect_in_container)
        
        self.widgets = [self.root_bar_display]
        
        if self.expanded:
            y = SECTION_TOP_PADDING
            for display in self.displays_list:
                y += (BAR_HEIGHT + 1)
                display.container = self.rect
                
                display.rect_in_container.top = y
                display.set_rect_in_container(display.rect_in_container)
                
                self.widgets.append(display)
        self.widgets.extend(self.fixed_widgets)
        
    def __get_displays(self):
        """
        Crea un BarDisplay para cada barra hija de la sección.
        Y retorna una lista con los mismos.
        """
        display_list = []
        for status_bar in self.children_bar:
            display = BarDisplay(BAR_HEIGHT, BAR_WIDTH, (BAR_OFFSET_X, 1), status_bar, SUB_BAR_COLOR)
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
        self.font = pygame.font.Font(None, 20)
        
        self._prepare_surface()

    def _prepare_surface(self):
        rect = pygame.Rect((1, 2), (self.rect_in_container.width - 2, self.rect_in_container.height - 4))
        charged_rect = pygame.Rect(rect)  # create a copy
        charged_rect.width = self.status_bar.value * rect.width / self.status_bar.max
        
        self.surface.fill(BAR_BACK_COLOR, rect)
        self.surface.fill(self.color, charged_rect)
        self.surface.blit(self.background, (0, 0))   # Background blits over the charge, because it has the propper alpha
        
        self.surface.blit(self.font.render(self.label, 1, (0, 0, 0)), (15, 5))
        self.last_value = self.status_bar.value
        
    def draw(self, screen):
        if self.last_value != self.status_bar.value:
            self._prepare_surface()
        
        screen.blit(self.surface, self.rect_absolute)
        
        return self.rect_absolute
    

class ScoreSection(Widget):
    """
    Sección que muestra la barra de puntaje principal.
    """
    def __init__(self, bar, container, size, position, level):
        rect = pygame.Rect(position, size)
        Widget.__init__(self, container, rect, 1, pygame.Color("black"))
        
        # attributes
        self.name = "score section"
        self.score_bar = bar
        self.level = level
        
        # visuals
        self.score_bar_display = BarDisplay(BAR_HEIGHT, (size[0] - 2), (1, (size[1] / 2) - 3), self.score_bar, pygame.Color("blue"))
        self.surface = pygame.Surface(self.rect_in_container.size)
        self.surface.fill((2, 45, 126))
        self.font = pygame.font.Font(None, 20)
        
    def draw(self, screen):
        #draw bar:
        self.score_bar_display.draw(self.surface)
        
        #write actual level:
        level_text = _("Level") + ": " + str(self.level)
        
        self.surface.blit(self.font.render(level_text, 1, (255, 255, 255)), (2, 5))
        
        screen.blit(self.surface, self.rect_absolute)
        return self.rect_absolute

#****************** MODELOS ******************

class BarsController:
    """
    Controlador general de las barras, encargado de enviar la señal de decremento o incremento
    a una barra especifica
    """
    def __init__(self, bars):
        # bars
        self.bars = bars
            
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
        if(self.value < self.max and self.value > 0):
            if(len(self.children_list) > 0):
                value = increase_rate / len(self.children_list) #para que el incremento de esta barra mantenga relacion con la de sus hijos
                self.value += value
                for child in self.children_list:
                    child.increase_from_parent(value)
            else:
                self.value += increase_rate
    
            if(self.parent != None):
                self.parent.increase_from_child(increase_rate)
    
    def increase_from_child(self, increase_rate):
        """
        Incrementa el valor de la barra.
        """
        value = increase_rate / len(self.children_list) #para que el incremento de esta barra mantenga relacion con la de sus hijos
        self.value += value
        
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
        
        if(self.value < max and self.value > 0):
            if(len(self.children_list) > 0):
                value = increase_rate / len(self.children_list) #para que el incremento de esta barra mantenga relacion con la de sus hijos
                self.value += increase_rate
                for child in self.children_list:
                    child.increase_from_parent(increase_rate)
            else:
                self.value += increase_rate
            
            if(self.value > self.max):
                self.value = self.max
            elif(self.value < 0):
                self.value = 0

