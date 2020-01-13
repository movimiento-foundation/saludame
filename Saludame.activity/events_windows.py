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

import gui
import pygame
import game
import animation
from gettext import gettext as _

TEXT_COLOR = (0,0,0)


class PersonalWindow(gui.Window):
    def __init__(self, container, rect, frame_rate, windows_controller):
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "personal_window")

        self.active_personal_events = [] # tuple (event, animation)
        self.index_personal_event = 0
        
        self.personal_next = gui.ImageButton(self.rect, pygame.Rect(120, 95, 30, 30), 1, "assets/events/go-next.png", self._cb_button_click_personal_next)
        self.personal_back = gui.ImageButton(self.rect, pygame.Rect(5, 95, 30, 30), 1, "assets/events/go-back.png", self._cb_button_click_personal_back)
        
        self.add_button(self.personal_next)
        self.add_button(self.personal_back)
        
        self.personal_next.visible = False
        self.personal_back.visible = False
        
        self.count_personal_events = gui.Text(self.rect, 60, 100, 1, "", 22, TEXT_COLOR, gui.Text.ALIGN_CENTER, True, False)
        self.add_child(self.count_personal_events)
        
        self.current_animation = None # Visible event at panel
    
    # Add/remove personal events    
    def add_personal_event(self, event):
        
        if not event in self.active_personal_events:
            
            event_info = "%s\n%s:\n" % (event.description, _("Affects"))
            if event.effect:
                for eff in event.effect.effect_status_list:
                    bar_label = event.effect.bars_controller.get_bar_label(eff[0])
                    if eff[1] > 0:
                        event_info += "+ %s \n" % (bar_label)
                    else:
                        event_info += "- %s \n" % (bar_label)
            
            ## Animation
            animation_rect = pygame.Rect((0, 0), self.rect.size)
            temp_animation = animation.ActionAnimation(self.rect, animation_rect, 3, event.directory_path)            
            temp_animation.set_on_mouse_click(self._cb_button_click_personal)
            temp_animation.highlight = False
            temp_animation.set_super_tooltip(event_info)
            
            self.active_personal_events.append((event, temp_animation))
            
            if self.current_animation:
                self.remove_button(self.current_animation)
                
            self.current_animation = temp_animation
            self.add_button(self.current_animation, 0)
            
            self.current_animation.set_dirty()
            self.index_personal_event = len(self.active_personal_events) - 1
            
            self.refresh_count_personal_events()       
        
    def remove_personal_event(self, event):        
        for e in self.active_personal_events:
            if e[0] == event:
                self.active_personal_events.remove(e)             
                
        if self.current_animation:
            self.remove_button(self.current_animation)
                
        if self.active_personal_events:
            self.index_personal_event = 0
            self.current_animation = self.active_personal_events[0][1]
            self.add_button(self.current_animation, 0)
        
        self.windows_controller.hide_active_tooltip()
        
        self.parent.set_dirty_background()       
        self.refresh_count_personal_events()        
        
    def refresh_count_personal_events(self):
        if len(self.active_personal_events) > 1:
            self.count_personal_events.text = "%s/%s" % (self.index_personal_event + 1, len(self.active_personal_events))
            self.count_personal_events.refresh()
            
            self.personal_next.visible = True
            self.personal_back.visible = True
        else:
            self.count_personal_events.text = ""
            self.count_personal_events.refresh()
            
            self.personal_next.visible = False
            self.personal_back.visible = False
    
    def get_current_event(self):
        if self.index_personal_event < len(self.active_personal_events):
            return self.active_personal_events[self.index_personal_event][0]

    # Buttons Callbacks
    def _cb_button_click_personal(self, button):
        event = self.get_current_event()
        if event and event.library_link:
            game.set_library_event(event.library_link)
        
    def _cb_button_click_personal_next(self, button):
        if self.index_personal_event < len (self.active_personal_events) - 1:
            self.remove_button(self.current_animation)
            self.index_personal_event += 1
            self.refresh_count_personal_events()
            self.current_animation = self.active_personal_events[self.index_personal_event][1]
            self.add_button(self.current_animation, 0)
            
    def _cb_button_click_personal_back(self, button):
        if self.index_personal_event > 0:
            self.remove_button(self.current_animation)
            self.index_personal_event -= 1
            self.refresh_count_personal_events()
            self.current_animation = self.active_personal_events[self.index_personal_event][1]
            self.add_button(self.current_animation, 0)


class SocialWindow(gui.Window):
    def __init__(self, container, rect, frame_rate, windows_controller):
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "social_window")   
        
        self.active_social_events = [] # tuple (event, animation)
        self.index_social_event = 0
        
        self.social_next = gui.ImageButton(self.rect, pygame.Rect(120, 95, 30, 30), 1, "assets/events/go-next.png", self._cb_button_click_social_next)
        self.social_back = gui.ImageButton(self.rect, pygame.Rect(5, 95, 30, 30), 1, "assets/events/go-back.png", self._cb_button_click_social_back)
        
        self.add_button(self.social_next)
        self.add_button(self.social_back)
        self.social_next.visible = False
        self.social_back.visible = False
        
        self.count_social_events = gui.Text(self.rect, 60, 100, 1, "", 22, TEXT_COLOR, gui.Text.ALIGN_CENTER, True, False)
        self.add_child(self.count_social_events)
        
        self.current_animation = None # Visible event at panel
        
    # Add/Remove social events    
    def add_social_event(self, event):
        
        if not event in self.active_social_events:
                       
            event_info = "%s\n%s:\n" % (event.description, _("Affects"))
            if event.effect:
                for eff in event.effect.effect_status_list:
                    bar_label = event.effect.bars_controller.get_bar_label(eff[0])
                    if eff[1] > 0:
                        event_info += "+ %s \n" % (bar_label)
                    else:
                        event_info += "- %s \n" % (bar_label)
            
            animation_rect = pygame.Rect((0, 0), self.rect.size)
            temp_animation = animation.ActionAnimation(self.rect, animation_rect, 3, event.directory_path)
            temp_animation.set_on_mouse_click(self._cb_button_click_social)
            temp_animation.highlight = False
            temp_animation.set_super_tooltip(event_info)
            
            self.active_social_events.append((event, temp_animation))
            
            if self.current_animation:
                self.remove_button(self.current_animation)
            self.current_animation = temp_animation
            self.add_button(self.current_animation, 0)
            
            self.current_animation.set_dirty()
            self.index_social_event = len(self.active_social_events) - 1
            
            self.refresh_count_social_events()
    
    def remove_social_event(self, event):
        
        for e in self.active_social_events:
            if e[0] == event:
                self.active_social_events.remove(e)
                
        if self.current_animation:
            self.remove_button(self.current_animation)
                
        if self.active_social_events:
            self.index_social_event = 0
            self.current_animation = self.active_social_events[0][1]
            self.add_button(self.current_animation, 0)
            
        self.windows_controller.hide_active_tooltip()
        
        self.parent.set_dirty_background()          
        self.refresh_count_social_events()
            
    def refresh_count_social_events(self):
        if len(self.active_social_events) > 1:
            self.count_social_events.text = "%s/%s" % (self.index_social_event + 1, len(self.active_social_events))
            self.count_social_events.refresh()
            
            self.social_next.visible = True
            self.social_back.visible = True
        else:
            self.count_social_events.text = ""
            self.count_social_events.refresh()
            
            self.social_next.visible = False
            self.social_back.visible = False

    def get_current_event(self):
        if self.index_social_event < len(self.active_social_events):
            return self.active_social_events[self.index_social_event][0]
    
    ## Buttons callbacks
    def _cb_button_click_social(self, button):
        event = self.get_current_event()
        if event and event.library_link:
            game.set_library_event(event.library_link)
    
    def _cb_button_click_social_next(self, button):
        if self.index_social_event < len (self.active_social_events) - 1:
            self.remove_button(self.current_animation)
            self.index_social_event += 1
            self.refresh_count_social_events()
            self.current_animation = self.active_social_events[self.index_social_event][1]
            self.add_button(self.current_animation, 0)

    def _cb_button_click_social_back(self, button):
        if self.index_social_event > 0:
            self.remove_button(self.current_animation)
            self.index_social_event -= 1
            self.refresh_count_social_events()
            self.current_animation = self.active_social_events[self.index_social_event][1]
            self.add_button(self.current_animation, 0)
