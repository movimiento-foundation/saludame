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

import pygame
from gettext import gettext as _

import gui
from panel_window import PanelWindow
from kid_window import KidWindow
import status_bars
import animation
import utilities


class MainWindow(gui.Window):
    
    def __init__(self, container, rect, frame_rate, clock, windows_controller, cha_loader, bars_loader, game_man):
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "main_window")
        
        self.clock = clock
        self.cha_loader = cha_loader
        
        self.game_manager = game_man
        
        self.windows = []   # Lista de ventanas que 'componen' la ventana principal
        
        self.panel_win = PanelWindow(container, pygame.Rect((180, 609), (1020, 200)), 1, windows_controller)
        self.add_window(self.panel_win)
        
        self.kidW = KidWindow(container, pygame.Rect((227, 0), (973, 609)), 1, windows_controller, cha_loader, game_man)
        self.add_window(self.kidW)
        
        #self.add_child(animation.FPS(container, pygame.Rect((1150, 0), (50, 20)), 15, self.clock))
        
        self.add_window(status_bars.BarsWindow(container, pygame.Rect(0, 0, 227, 590), 5, windows_controller, bars_loader))
        
        self.add_child(Clock(container, pygame.Rect(0, 528, 1, 1), 1, game_man))
        
        #button_image = pygame.image.load("customization/customization_button.png").convert_alpha()
        #btn_reset = gui.TextButton2(self.rect, pygame.Rect((1000, 20), (70, 30)), 1, _("Reset"), 30, (255, 255, 255), button_image, self._cb_reset_game)
        #btn_reset.keep_dirty = True
        #self.add_button(btn_reset)
        
        #btn_change_mood = gui.ImageButton(self.rect, pygame.Rect((1120, 500), (60, 60)), 1, "assets/icons/change.png", self._cb_button_click_change_mood)
        #self.add_button(btn_change_mood)
    
    # Callbacks        
    def _cb_button_click_stop_animation(self, button):
        self.panel_win.stop_animation()
        
    def _cb_button_click_change_mood(self, button):
        self.kidW.change_mood()
    
    #def _cb_reset_game(self, button):
    #    self.game_manager.reset_game()


class Clock(gui.Widget):
    
    def __init__(self, container, rect_in_container, frame_rate, game_manager):
        background = pygame.image.load("assets/layout/clock_background.png").convert_alpha()
        rect_in_container.size = background.get_size()
        gui.Widget.__init__(self, container, rect_in_container, frame_rate)
        
        self.game_manager = game_manager
        self.background = background
        self.frames = 0
        self.frame_index = 0
        self.frame_paths = [
            "assets/layout/clock_D.png",
            "assets/layout/clock_A.png",
            "assets/layout/clock_B.png",
            "assets/layout/clock_C.png",
        ]
        self.set_frame()
    
    def set_frame(self):
        image = pygame.image.load(self.frame_paths[self.frame_index]).convert_alpha()
        rect = pygame.Rect((0,0), image.get_size())
        rect.center = self.rect_absolute.width/2, self.rect_absolute.height/2
        self.background.blit(image, rect)
        
    def update(self, frames):
        if self.game_manager.hour <> self.frame_index:
            self.frame_index = self.game_manager.hour
            self.set_frame()

        self.set_dirty()        # Always dirty because it draws over the panel_window
        