# -*- coding: utf-8 -*-

import gui
import pygame
import game
import animation

class PersonalWindow(gui.Window):
    def __init__(self, container, rect, frame_rate, windows_controller):
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "personal_window")

        self.active_personal_events = [] # tuple (event, button)
        self.index_personal_event = 0
        
        self.personal_next = gui.ImageButton(self.rect, pygame.Rect(115, 90, 30, 30), 1, "assets/events/go-next.png", self._cb_button_click_personal_next)
        self.personal_back = gui.ImageButton(self.rect, pygame.Rect(10, 90, 30, 30), 1, "assets/events/go-back.png", self._cb_button_click_personal_back)
        
        self.add_button(self.personal_next)
        self.add_button(self.personal_back)
        
        self.count_personal_events = gui.Text(self.rect, 60, 92, 1, "%s/%s" % (self.index_personal_event, len(self.active_personal_events)), 20, pygame.Color("black"))
        self.add_child(self.count_personal_events)
        
        self.b_event_personal = None # Visible event at panel
    
    # Add/remove personal events    
    def add_personal_event(self, event):
        
        if not event in self.active_personal_events:
            b_event_personal = gui.ImageButton(self.rect, pygame.Rect(23, 3, 100, 100), 1, pygame.image.load("assets/events/ill.jpg"))
            b_event_personal.visible = False
            
            event_info = "%s \n" % (event.description)
            
            if event.effect:
                for eff in event.effect.effect_status_list:
                    bar_label = event.effect.bars_controller.get_bar_label(eff[0])
                    if eff[1] > 0:
                        event_info += "+ %s \n" % (bar_label)
                    else:
                        event_info += "- %s \n" % (bar_label)
            
            b_event_personal.set_super_tooltip(event_info)
            
            self.active_personal_events.append((event, b_event_personal))
            
            if self.b_event_personal:
                self.remove_button(self.b_event_personal)
            self.b_event_personal = b_event_personal
            self.add_button(self.b_event_personal)
            self.b_event_personal.set_dirty()
            self.index_personal_event = len(self.active_personal_events) - 1
            
            self.refresh_count_personal_events()
            
            ## Animation
            self.current_animation = animation.ActionAnimation(self.rect, pygame.Rect(0, 0, 0, 0), 3, event.directory_path)
            self.add_child(self.current_animation)
        
    def remove_personal_event(self, event):        
        for e in self.active_personal_events:
            if e[0] == event:
                self.active_personal_events.remove(e)
                
        if self.b_event_personal:
            self.remove_button(self.b_event_personal)
                
        if self.active_personal_events:
            self.index_personal_event = 0
            self.b_event_personal = self.active_personal_events[0][1]
            self.add_button(self.b_event_personal)
        
        self.windows_controller.hide_active_tooltip()
        
        self.refresh_count_personal_events()
        
    def refresh_count_personal_events(self):
        
        if self.active_personal_events:
            self.count_personal_events.text = "%s/%s" % (self.index_personal_event + 1, len(self.active_personal_events))
            self.count_personal_events.refresh()
            
        else:
            self.count_personal_events.text = "0/0"
            self.count_personal_events.refresh()
        
    # Buttons Callbacks
    def _cb_button_click_personal(self, button):
        if game.set_library_function:
            game.set_library_function("99-Eventos.html") #diarrhea")
            
    def _cb_button_click_personal_next(self, button):
        if self.index_personal_event < len (self.active_personal_events) - 1:
            self.remove_button(self.b_event_personal)
            self.index_personal_event += 1
            self.refresh_count_personal_events()
            self.b_event_personal = self.active_personal_events[self.index_personal_event][1]
            self.add_button(self.b_event_personal)
            
    def _cb_button_click_personal_back(self, button):
        if self.index_personal_event > 0:
            self.remove_button(self.b_event_personal)
            self.index_personal_event -= 1
            self.refresh_count_personal_events()
            self.b_event_personal = self.active_personal_events[self.index_personal_event][1]
            self.add_button(self.b_event_personal)
            
class SocialWindow(gui.Window):
    def __init__(self, container, rect, frame_rate, windows_controller):
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "social_window")   
        
        self.active_social_events = [] # tuple (event, button)
        self.index_social_event = 0
        
        self.social_next = gui.ImageButton(self.rect, pygame.Rect(115, 90, 30, 30), 1, "assets/events/go-next.png", self._cb_button_click_social_next)
        self.social_back = gui.ImageButton(self.rect, pygame.Rect(10, 90, 30, 30), 1, "assets/events/go-back.png", self._cb_button_click_social_back)
        
        self.add_button(self.social_next)
        self.add_button(self.social_back)
        
        self.count_social_events = gui.Text(self.rect, 60, 92, 1, "%s/%s" % (self.index_social_event, len(self.active_social_events)), 20, pygame.Color("black"))
        self.add_child(self.count_social_events)
        
        self.b_event_social = None # Visible event at panel
        
    # Add/Remove social events    
    def add_social_event(self, event):
        
        if not event in self.active_social_events:
            
            b_event_social = gui.ImageButton(self.rect, pygame.Rect(23, 3, 100, 100), 1, pygame.image.load("assets/events/ill.jpg"))
            b_event_social.visible = False
            
            event_info = "%s \n" % (event.description)
            
            if event.effect:
                for eff in event.effect.effect_status_list:
                    bar_label = event.effect.bars_controller.get_bar_label(eff[0])
                    if eff[1] > 0:
                        event_info += "+ %s \n" % (bar_label)
                    else:
                        event_info += "- %s \n" % (bar_label)
            
            b_event_social.set_super_tooltip(event_info)
            
            self.active_social_events.append((event, b_event_social))
            
            if self.b_event_social:
                self.remove_button(self.b_event_social)
            self.b_event_social = b_event_social
            self.add_button(self.b_event_social)
            self.b_event_social.set_dirty()
            self.index_social_event = len(self.active_social_events) - 1
            
            self.refresh_count_social_events()
            
            self.current_animation = animation.ActionAnimation(self.rect, pygame.Rect(0, 0, 0, 0), 3, "assets/events/personal/stomach_ache")
            self.add_child(self.current_animation)
        
    def remove_social_event(self, event):
        
        for e in self.active_social_events:
            if e[0] == event:
                self.active_social_events.remove(e)
                
        if self.b_event_social:
            self.remove_button(self.b_event_social)
                
        if self.active_social_events:
            self.index_social_event = 0
            self.b_event_social = self.active_social_events[0][1]
            self.add_button(self.b_event_social)
            
        self.windows_controller.hide_active_tooltip()
        self.refresh_count_social_events()
            
    def refresh_count_social_events(self):
        
        if self.active_social_events:
            self.count_social_events.text = "%s/%s" % (self.index_social_event + 1, len(self.active_social_events))
            self.count_social_events.refresh()
            
        else:
            self.count_social_events.text = "0/0"
            self.count_social_events.refresh()
            
    ## Buttons callbacks
    def _cb_button_click_social(self, button):
        if game.set_library_function:
            game.set_library_function("99-Eventos.html") #diarrhea")
            
    def _cb_button_click_social_next(self, button):
        if self.index_social_event < len (self.active_social_events) - 1:
            self.remove_button(self.b_event_social)
            self.index_social_event += 1
            self.refresh_count_social_events()
            self.b_event_social = self.active_social_events[self.index_social_event][1]
            self.add_button(self.b_event_social)
            
    def _cb_button_click_social_back(self, button):
        if self.index_social_event > 0:
            self.remove_button(self.b_event_social)
            self.index_social_event -= 1
            self.refresh_count_social_events()
            self.b_event_social = self.active_social_events[self.index_social_event][1]
            self.add_button(self.b_event_social)
        