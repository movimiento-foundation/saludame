# -*- coding: utf-8 -*-

# Copyright (C) 2011 ceibalJAM! - ceibaljam.org
# This file is part of Saludame.
#
# Saludame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Saludame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Saludame. If not, see <http://www.gnu.org/licenses/>.

import os
import pygame
from gettext import gettext as _
import status_bars_creator
import utilities
import gui
import game_manager
from gi.repository import GObject

DEFAULT_BARS_VALUES = 50.0
MAX_BARS_VALUE = 100

SECTION_OFFSET_X = 0
SECTION_WIDTH = 220
SECTION_MIN_HEIGHT = 50
SECTION_TOP_PADDING = 18

BAR_OFFSET_X = 30
BAR_WIDTH = 182
BAR_HEIGHT = 24

SCORE_BAR_HEIGHT = 36
SCORE_BAR_WIDTH = 118
SCORE_BAR_X_OFFSET = 82

BAR_BACK_COLOR = pygame.Color("#106168ff")
#ROOT_BAR_COLOR = pygame.Color("#7ee113")
#SUB_BAR_COLOR = pygame.Color("#a742bd")
#SCORE_BAR_COLOR = pygame.Color("#51b8ed")
ROOT_BAR_PARTITIONS = {33: pygame.Color("#cb0e12ff"), 100: pygame.Color("#7ee113ff")}       # Red until 33, Green until hundred
SUB_BAR_PARTITIONS = {100: pygame.Color("#a742bdff")}                                     # Violet until hundred
SCORE_BAR_PARTITIONS = {100: pygame.Color("#51b8edff")}                                   # Skyblue until hundred

TEXT_COLOR = "#0f5e65"
SUB_BAR_TEXT_COLOR = "#ffffff"

NEGATIVE_FACTOR = 0.8   # Applied when decreasing any bar (for gameplay balancing purposes)
POSITIVE_FACTOR = 1.0   # Applied when increasing any bar (for gameplay balancing purposes)

BASEPATH = os.path.dirname(__file__)
# ****************** VISUALES ******************

class BarsWindow(gui.Window):
    """
    Clase que representa la ventana de las barras de estado del juego.
    """
    def __init__(self, container, rect, frame_rate, windows_controller, bars_loader):
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "bars_window")
        
        # rect and surface:
        self.rect.size = (227, 590)
        
        # game bars
        bars = bars_loader.get_second_level_bars()
        
        # sections
        score_section_width = SECTION_WIDTH - 20
        score_section = ScoreSection(bars_loader.get_score_bar(), self.rect, (score_section_width, 40), (SECTION_OFFSET_X + 25, 4), 1)
        
        y = 50
        overall_section = BarSection(windows_controller, self.rect, _(u"TOTAL"), bars_loader.get_overall_bar(), [] , (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, y), os.path.join(BASEPATH, "assets/layout/icon_total.png"))
        
        y = 110
        physica_section = BarSection(windows_controller, self.rect, _(u"ESTADO FÍSICO"), bars[0], bars[0].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, y), os.path.join(BASEPATH, "assets/layout/icon_physica.png"))
        
        y += SECTION_MIN_HEIGHT
        hygiene_section = BarSection(windows_controller, self.rect, _(u"HIGIENE"), bars[1], bars[1].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, y), os.path.join(BASEPATH, "assets/layout/icon_hygiene.png"))
        
        y += SECTION_MIN_HEIGHT
        nutrition_section = BarSection(windows_controller, self.rect, _(u"ALIMENTACIÓN"), bars[2], bars[2].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, y), os.path.join(BASEPATH, "assets/layout/icon_nutrition.png"))
        
        y += SECTION_MIN_HEIGHT
        spare_time_section = BarSection(windows_controller, self.rect, _(u"TIEMPO LIBRE"), bars[3], bars[3].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, y), os.path.join(BASEPATH, "assets/layout/icon_spare_time.png"))
        
        y += SECTION_MIN_HEIGHT
        farm_section = BarSection(windows_controller, self.rect, _(u"RESPONSABILIDAD"), bars[4], bars[4].children_list, (SECTION_WIDTH, SECTION_MIN_HEIGHT), (SECTION_OFFSET_X, y), os.path.join(BASEPATH, "assets/layout/icon_responsability.png"))
        
        self.sections_list = [score_section, overall_section, physica_section, hygiene_section, nutrition_section, spare_time_section, farm_section]
        self.accordeon = Accordeon([physica_section, hygiene_section, nutrition_section, spare_time_section, farm_section])
        
        self.set_bg_image(os.path.join(BASEPATH, "assets/layout/status.png"))
        
        for section in self.sections_list:
            if section != score_section:   # Score section no va porque es Widget
                self.add_window(section)
                
        self.add_child(score_section)
    
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
                pygame.mixer.Sound(os.path.join(BASEPATH, "assets/sound/open_bars.ogg")).play()
                self.set_dirty_background()        # Makes the window repaint its background
                break
    

class Accordeon(GObject.Object):
    """
    Clase encargada de realizar los calculos para expandir y
    contraer las secciones.
    """
    
    def __init__(self, sections_list):
        """
        Las secciones deben estar ordenadas de arriba abajo, según se muestren
        en la pantalla.
        """
        GObject.Object.__init__(self)
        self.sections_list = sections_list # secciones sobre las que se realizarán los cambios
        self.expand_section(None)
    
    def expand_section(self, section):
        """
        Espande la sección 'section' y re calcula la
        posición del resto de las secciones.
        """
        self.compress_sections()
        for i in range(0, len(self.sections_list)):
            
            if self.sections_list[i] == section:
                
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
            section.move_up()
            section.compress()
            section.set_dirty()


class BarSection(gui.Window):
    """
    Clase que contiene un conjunto de BarDisplay, y las
    muestra por pantalla
    """
    
    def __init__(self, windows_controller, container, name, root_bar, children_bar, size, position, icon_path):
        
        rect = pygame.Rect(position, size)
        gui.Window.__init__(self, container, rect, 1, windows_controller, "bar_section_window")
        
        # section attributes
        self.name = name
        self.root_bar = root_bar
        self.children_bar = children_bar
        
        font = utilities.get_font(16, True, True)
        
        #label_render = font.render(self.name, 1, pygame.Color(TEXT_COLOR))
        #label_rect = pygame.Rect((0,0), label_render.get_size())
        #label_rect.right = self.rect.right - 8
        pos = self.rect.right - 8, 0
        label_widget = gui.Text(self.rect, pos[0], pos[1], 1, self.name, 16, pygame.Color(TEXT_COLOR), "normal", gui.Text.ALIGN_RIGHT, True, True)
        
        # visuals
        self.root_bar_display = BarDisplay(BAR_HEIGHT, BAR_WIDTH, (BAR_OFFSET_X, SECTION_TOP_PADDING), self.root_bar, ROOT_BAR_PARTITIONS)
        self.root_bar_display.show_name = False
        
        self.displays_list = self.__get_displays()      # obtengo los displays para cada barra.
        
        self.fixed_widgets = [label_widget, self.root_bar_display]
        
        if icon_path:
            icon = pygame.image.load(icon_path).convert_alpha()
            self.icon = gui.Widget(self.rect, pygame.Rect((0, 0), icon.get_size()), 1, icon)
            self.icon.keep_dirty = True
            self.fixed_widgets.append(self.icon)
        else:
            self.icon = None
        
        # visuals constant
        self.init_top = self.rect[1]
        self.init_height = size[1]
        self.max_expand = len(children_bar) * BAR_HEIGHT
        
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

        self.__calculate()
    
    def move_up(self):
        """
        Desplaza la sección a su posición original.
        """
        offset = self.init_top - self.rect.top
        if offset <> 0:
            self.move((0, offset))
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
        
        self.clear_childs()
        for widget in self.fixed_widgets:
            self.add_child(widget)
        
        if self.expanded:
            y = SECTION_TOP_PADDING
            for display in self.displays_list:
                y += BAR_HEIGHT
                display.container = self.rect
                
                display.rect_in_container.top = y
                display.set_rect_in_container(display.rect_in_container)
                
                self.add_child(display)
        
    def __get_displays(self):
        """
        Crea un BarDisplay para cada barra hija de la sección.
        Y retorna una lista con los mismos.
        """
        display_list = []
        for status_bar in self.children_bar:
            width = BAR_WIDTH
            display = BarDisplay(BAR_HEIGHT, width, (BAR_OFFSET_X, 0), status_bar, SUB_BAR_PARTITIONS)
            display_list.append(display)
        return display_list


class BarDisplay(gui.Widget):
    """
    Clase que se encarga de representar visualmente a una barra, manteniéndose
    actualizada según los incrementos o decrementos de la barra representada.
    """
    
    def __init__(self, height, width, position, status_bar, color_partitions):
        
        rect = pygame.Rect(position, (width, height))
        gui.Widget.__init__(self, pygame.Rect(0, 0, width, height), rect, 1)
        
        # attributes
        self.status_bar = status_bar
        self.label = status_bar.label
        self.color_partitions = color_partitions
        self.position = position
        if isinstance(self.status_bar, WeightBar):
            self.background = pygame.image.load(os.path.join(BASEPATH, "assets/layout/weight_bar_back.png")).convert_alpha()
            self.arrow = pygame.image.load(os.path.join(BASEPATH, "assets/layout/weight_bar_arrow.png")).convert_alpha()
        else:
            self.background = pygame.image.load(os.path.join(BASEPATH, "assets/layout/main_bar_back.png")).convert_alpha()
        self.surface = self.background.copy()   # The actual surface to be blitted
        
        # visuals
        self.font = utilities.get_font(13, True, False)
        
        self.last_value = -1    # valor inicial
        
        self.show_name = True
        
    def update(self, frames):
        if self.last_value != int(self.status_bar.value):
            self.last_value = int(self.status_bar.value)
            self.set_dirty()
            
    def draw(self, screen):
        if isinstance(self.status_bar, WeightBar):
            position = (self.status_bar.value * (self.rect_in_container.width) / self.status_bar.max)
            if position < BAR_OFFSET_X:
                position = BAR_OFFSET_X
            elif position > BAR_WIDTH:
                position = BAR_WIDTH
                
            rect = self.arrow.get_rect()         #
            rect.midbottom = position , 23 #para posicionar la imagen de la flecha en el centro del valor de posicion hallado
            
            self.surface.blit(self.background, (0, 0))   # Background blits over the charge, because it has the propper alpha
            self.surface.blit(self.arrow, rect)

        elif isinstance(self.status_bar, StatusBar):
            rect = pygame.Rect((2, 2), (self.rect_absolute.width - 4, self.rect_absolute.height - 4))
            charged_rect = pygame.Rect((2,2), (0, rect.height))  # create a copy
            charged_rect.width = (self.status_bar.value * rect.width / self.status_bar.max)
            color = self.get_color()
            
            self.surface.fill(BAR_BACK_COLOR, rect)
            self.surface.fill(color, charged_rect)
            self.surface.blit(self.background, (0, 0))   # Background blits over the charge, because it has the propper alpha
        
        if self.show_name:
            self.surface.blit(self.font.render(self.label, 1, pygame.Color(SUB_BAR_TEXT_COLOR)), (8, 4))
    
        screen.blit(self.surface, self.rect_absolute)
        
        self.dirty = False
        
        return self.rect_absolute

    def get_color(self):
        for value, color in sorted(self.color_partitions.items()):
            if self.status_bar.value <= value:
                return color
        return sorted(self.color_partitions.values())[-1]
        

class ScoreSection(gui.Widget):
    """
    Sección que muestra la barra de puntaje principal.
    """
    def __init__(self, bar, container, size, position, level):
        rect = pygame.Rect(position, size)
        gui.Widget.__init__(self, container, rect, 1)
        
        # attributes
        self.name = "score section"
        self.score_bar = bar
        self.level = level
        
        # visuals
        score_background = pygame.image.load(os.path.join(BASEPATH, "assets/layout/score_bar_back.png")).convert_alpha()
        self.score_bar_display = BarDisplay(score_background.get_height(), score_background.get_width(), (SCORE_BAR_X_OFFSET, 12), self.score_bar, SCORE_BAR_PARTITIONS)
        self.score_bar_display.background = score_background
        
        self.surface = pygame.Surface(self.rect_in_container.size)
        self.surface.set_alpha(255)
        
        self.font = utilities.get_font(16, True, True)
        
        self.number_font = utilities.get_font(32, True, True)
        
        self.text_color = pygame.Color(TEXT_COLOR)

        self.left_arrow = pygame.image.load(os.path.join(BASEPATH, "assets/events/go-back-s.png")).convert_alpha()
        self.right_arrow = pygame.image.load(os.path.join(BASEPATH, "assets/events/go-next-s.png")).convert_alpha()
        
    def draw(self, screen):
        self.surface.blit(self.get_background().subsurface(self.rect_in_container), (0, 0))
        
        # draw bar:
        self.score_bar_display.draw(self.surface)
        
        # write level:
        level_text = _("LEVEL")
        level_text_surface = self.font.render(level_text, 1, self.text_color)
        
        level_number = str(game_manager.instance.get_level())
        level_number_surface = self.number_font.render(level_number, 1, self.text_color)
        
        self.surface.blit(level_text_surface, (0, 34 - level_text_surface.get_height()))
        self.surface.blit(level_number_surface, (level_text_surface.get_width(), 40 - level_number_surface.get_height()))
        
        # arrows
        l_increase = self.score_bar.last_increase
        if l_increase < 0:
            if l_increase <= -3: # two left arrows:
                 self.surface.blit(self.left_arrow, (125, 0))
                 self.surface.blit(self.left_arrow, (115, 0))
            else: # one left arrow
                 self.surface.blit(self.left_arrow, (125, 0))
        else:
            if l_increase >= 3: # two right arrows:
                self.surface.blit(self.right_arrow, (155, 0))
                self.surface.blit(self.right_arrow, (165, 0))
            elif l_increase > 0: # one right arrow
                self.surface.blit(self.right_arrow, (155, 0))
        
        screen.blit(self.surface, self.rect_absolute)
        return self.rect_absolute

#****************** MODELOS ******************


class BarsController(GObject.Object):
    """
    Controlador general de las barras, encargado de enviar la señal de decremento o incremento
    a una barra especifica
    """
    def __init__(self, bars, score_bar, overall_bar):
        GObject.Object.__init__(self)
        # bars
        self.score_bar = score_bar
        self.overall_bar = overall_bar
        
        self.bars = bars
            
    def increase_bar(self, bar_id, increase_rate):
        for bar in self.bars:
            if bar.id == bar_id:
                if increase_rate < 0:
                    value = increase_rate * NEGATIVE_FACTOR
                else:
                    value = increase_rate * POSITIVE_FACTOR
                bar.increase(value)
                break
    
    def calculate_score(self, score_level_vector):
        """
        Calculates score_bar's score.
        """
        interval = float(self.overall_bar.max) / len(score_level_vector)
        index = int(self.overall_bar.value / interval)
        if index >= len(score_level_vector):
            index = len(score_level_vector) - 1
        self.score_bar.increase(score_level_vector[index])
    
    def get_overall_percent(self):
        percent = self.overall_bar.value / self.overall_bar.max
        
        return percent
    
    def get_bar_label (self, bar_id):
        for bar in self.bars:
            if bar.id == bar_id:
                return bar.label
    
    def get_bars_status(self):
        """
        Generates a dictionary {bar_id : bar_value} and
        returns it.
        """
        return dict([(bar.id, bar.value) for bar in self.bars])
    
    def load_bars_status(self, bars_values):
        """
        Load a previous status for each bar
        """
        for bar in self.bars:
            bar.value = bars_values[bar.id]
            
    def get_lowest_bar(self):
        value = self.bars[0].value
        lowest_bar = None
        for bar in self.bars[0:5]: # bars in second_level (section bars) are self.bars[0:5]
            if bar.value <= value:
                value = bar.value
                lowest_bar = bar
        return lowest_bar
    
    def reset(self):
        """
        Restore the bars value to the default value.
        """
        for bar in self.bars:
            bar.value = DEFAULT_BARS_VALUES
        self.score_bar.value = 0.0
        

class StatusBar(GObject.Object):
    """
    Entity that represents the bar
    """
    
    def __init__(self, id, label, parent_bar, children_list, max_value, init_value):
        GObject.Object.__init__(self)
        # attributes
        self.id = id
        self.label = label
        self.max = max_value
        self.value = init_value
        self.parent = parent_bar # Barra padre
        self.children_list = children_list # conjunto de barras hijas

        self.last_increase = 0.0
        self.ignore = False             # An ingored bar doesn't affect the parent bar
        
    def get_score(self):
        return self.value
    
    def increase(self, increase_rate):
        """
        Incrementa el valor de la barra y repercute en los hijos y la barra padre
        """
        self.last_increase = increase_rate
        if self.children_list:
            # Increments childrens
            for child in self.children_list:
                child.increase_from_parent(increase_rate)
            self.recalculate()
        else:
            # Increments/decrements this bar
            self.value += increase_rate
            
            # Keep the value between self.max and 0
            self.value = min([self.value, self.max])
            self.value = max([self.value, 0])
            
            if self.parent:
                self.parent.recalculate()
    
    def recalculate(self):
        if self.children_list:
            values = [child.get_score() for child in self.children_list if not child.ignore]
            value = float(sum(values)) / len(values)
            if self.value <> value:
                self.value = value
                if self.parent:
                    self.parent.recalculate()

    def increase_from_parent(self, increase_rate):
        """
        Incrementa el valor de la barra y repercute en los hijos.
        """
        self.last_increase = increase_rate
        if len(self.children_list) > 0:
            for child in self.children_list:
                if not child.ignore:
                    child.increase_from_parent(increase_rate)
            self.recalculate()
        else:
            self.value += increase_rate
            
            if self.value > self.max:
                self.value = self.max
            elif self.value < 0:
                self.value = 0


class WeightBar(StatusBar):
    
    def __init__(self, id, label, parent_bar, children_list, max_value, init_value):
        StatusBar.__init__(self, id, label, parent_bar, children_list, max_value, init_value)
    
    def get_score(self):
        return self.max - abs(2 * self.value - self.max)


class IgnoreBar(StatusBar):
    
    def __init__(self, id, label, parent_bar, children_list, max_value, init_value):
        StatusBar.__init__(self, id, label, parent_bar, children_list, max_value, init_value)
        self.ignore = True
        
    def get_score(self):
        return None
