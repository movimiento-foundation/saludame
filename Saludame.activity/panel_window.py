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
import os

from gettext import gettext as _

import gui

import animation
import customization
import game
import sound_manager
from events_windows import *

PANEL_BG_PATH = os.path.normpath("assets/layout/panel.png")
WHITE = pygame.Color("white")

BAR_BACK_COLOR = pygame.Color("#fbfbfbff")
BAR_FILL_COLOR = pygame.Color("#0f5e65ff")


class PanelWindow(gui.Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller):
        
        self.timing = 1 # la idea de timing es llevar una cuenta adentro, de los frames que fueron pasando
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "panel_window")
        
        self.set_bg_image(PANEL_BG_PATH, False)
        
        # Actions
        self.rect_action = pygame.Rect((560, 36), (310, 124))
        
        self.on_animation = False
        self.current_action = None
        self.current_animation = None
        
        self.action_progress_bar = None

        self.info_button_event = None
        self.image_info_blink = "assets/layout/info.png"
        
        TEXT_COLOR = pygame.Color("#0f5e65")
        
        text = gui.Text(self.rect, 145, 22, 1, _("Clima"), 18, TEXT_COLOR, type="normal", alignment=gui.Text.ALIGN_CENTER, bold=True, italic=True)
        self.add_child(text)
        
        text = gui.Text(self.rect, 300, 22, 1, _("Personal"), 18, TEXT_COLOR, type="normal", alignment=gui.Text.ALIGN_CENTER, bold=True, italic=True)
        self.add_child(text)
        
        text = gui.Text(self.rect, 465, 22, 1, _("Social"), 18, TEXT_COLOR, type="normal", alignment=gui.Text.ALIGN_CENTER, bold=True, italic=True)
        self.add_child(text)
        
        text = gui.Text(self.rect, 705, 22, 1, _(u"Acción"), 18, TEXT_COLOR, type="normal", alignment=gui.Text.ALIGN_CENTER, bold=True, italic=True)
        self.add_child(text)
        
        ### Events ###
        # Personal
        self.personal_window = PersonalWindow(self.rect, pygame.Rect((224, 35), (142, 127)), 1, self.windows_controller)
        self.add_window(self.personal_window)
        
        # Social
        self.social_window = SocialWindow(self.rect, pygame.Rect((391, 35), (142, 127)), 1, self.windows_controller)
        self.add_window(self.social_window)
        
        # Customization
        customization_button = gui.ImageButton(self.rect, pygame.Rect(953, 0, 1, 1), 1, "assets/layout/customization.png", self._cb_button_click_customization)
        customization_button.set_tooltip(_("Customization module"))
        self.add_button(customization_button)
        
        # Info
        self.info_button = gui.ImageButton(self.rect, pygame.Rect(885, 0, 1, 1), 1, "assets/layout/info.png", self._cb_button_click_info)
        self.add_button(self.info_button)
        self.info_button.visible = False
        self.info_button_blink_timeout = 0
        
        # Environment
        self.weather_widget = None
        self.set_weather()
    
    def set_weather(self):
        if self.weather_widget:
            self.remove_child(self.weather_widget)

        current_weather = self.windows_controller.game_man.current_weather
        file_path = current_weather[3]
        self.weather_widget = gui.Image(self.rect, pygame.Rect(51, 34, 1, 1), 1, file_path)
        self.add_child(self.weather_widget)
        self.weather_widget.set_dirty()
        
        info = "%s \n" % (current_weather[1])
        
        effect = self.windows_controller.game_man.environment_effect
        if effect:
            for eff in effect.effect_status_list:
                bar_label = effect.bars_controller.get_bar_label(eff[0])
                if eff[1] > 0:
                    info += "+ %s \n" % (bar_label)
                else:
                    info += "- %s \n" % (bar_label)
        
        self.weather_widget.set_super_tooltip(info)
        
    # Actions
    def set_active_action(self, action):
        self.current_action = action
        if action.window_animation_path:
            self.current_animation = animation.ActionAnimation(self.rect, self.rect_action, 10, action.window_animation_path)
            self.add_child(self.current_animation)
        else:
            rect_progress = self.rect_action.move(65, 45)
            rect_progress.size = (182, 26)
            self.action_progress_bar = ActionProgressBar(self.rect, rect_progress, 1, action)
            self.add_child(self.action_progress_bar)
    
    def play_action_animation(self, action):
        self.set_active_action(action)
        self.on_animation = True
        
    def stop_action_animation(self):
        self.on_animation = False
        self.current_action = None
        if self.current_animation:
            self.remove_child(self.current_animation)
            self.current_animation = None
            self.repaint = True
        
        if self.action_progress_bar:
            self.remove_child(self.action_progress_bar)
            self.action_progress_bar = None
            self.repaint = True
    
    ### Events - Delegate to events_windows        
    def add_personal_event(self, event):
        self.personal_window.add_personal_event(event)
        
    def remove_personal_event(self, event):
        self.personal_window.remove_personal_event(event)
        
    def add_social_event(self, event):
        self.social_window.add_social_event(event)
        
    def remove_social_event(self, event):
        self.social_window.remove_social_event(event)

    def add_info_button_event(self, event, action_label):
        self.info_button_event = event
        tooltip = u"La acción %s\nno debe realizarse durante\nel evento %s" % (action_label, event.description)
        self.info_button.set_super_tooltip(tooltip)
        self.info_button_blink_timeout = 6
        sound_manager.instance.play_forbidden_action()
        self.info_button.visible = True
        
    def update(self, frames):
             
        self.timing += 1
        
        self.social_window.set_dirty_background()
        self.personal_window.set_dirty_background()
        
        # Actions
        if self.on_animation and self.current_animation and self.timing % self.current_animation.frame_rate == 0:
            if self.timing > 12:
                self.timing = 0
        
        if frames % 8 == 0:
            if self.info_button_event and self.info_button_blink_timeout:
                # Make the button blink
                if self.image_info_blink == "assets/layout/info.png":
                    self.info_button.switch_image_background("assets/layout/info2.png")
                    self.image_info_blink = "assets/layout/info2.png"
                else:
                    self.info_button.switch_image_background("assets/layout/info.png")
                    self.image_info_blink = "assets/layout/info.png"
                self.info_button.set_dirty()
                
                self.info_button_blink_timeout -= 1
        
        gui.Window.update(self, frames)        
        
    def remove_info_button_event(self, event):
        if self.info_button_event == event:
            self.info_button_event = None
            self.info_button.set_super_tooltip("")
            self.info_button.visible = False
            
    # Buttons Callbacks
    def _cb_button_click_customization(self, button):
        self.windows_controller.set_active_window("customization_window")
        
    def _cb_button_click_info(self, button):
        if self.info_button_event:
            game.set_library_event(self.info_button_event.library_link)

        
class ActionProgressBar(gui.Widget):
    """
    Shows the progress of the active action
    """
    def __init__(self, container, rect_in_container, frame_rate, action):
        
        self.action = action
        surface = pygame.image.load("assets/layout/progress_bar_back.png").convert_alpha()
        
        gui.Widget.__init__(self, container, rect_in_container, frame_rate)
        
        self.borders = surface       # Borders of the bar
        self.background = surface.copy()   # Actual surface to blit in the screen, _prepare_surface
        self.decrease = action.time_span
        self._prepare_surface()
        
    def _prepare_surface(self):
        rect = pygame.Rect((1, 2), (self.rect_in_container.width - 2, self.rect_in_container.height - 4))
        charged_rect = pygame.Rect(rect)  # create a copy
        
        charged_rect.width = ((float)(self.decrease) / self.action.time_span) * rect.width
        
        self.background.fill(BAR_BACK_COLOR, rect)
        self.background.fill(BAR_FILL_COLOR, charged_rect)
        self.background.blit(self.borders, (0, 0)) # Background blits over the charge, because it has the propper alpha
        
        self.decrease = self.action.time_left
        self.set_dirty()
    
    def update(self, frames):
        """
        Updates the progress bar (if the action is still active)
        """
        if self.decrease > 0:
            self._prepare_surface()
