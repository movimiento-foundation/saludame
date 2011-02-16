# -*- coding: utf-8 -*-

import pygame
import os

from gettext import gettext as _

import gui

import animation
import customization
import game

PANEL_BG_PATH = os.path.normpath("assets/layout/panel.png")
WHITE = pygame.Color("white")

BAR_BACK_COLOR = pygame.Color("#106168")
BAR_FILL_COLOR = pygame.Color("#a742bd")

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
        
        # Personal
        self.surf_personal = pygame.Surface((130, 110))
        self.rect_personal = pygame.Rect((410, 652), self.surf_personal.get_rect().size)
        self.active_personal_events = [] # tuple (event, button)
        self.index_personal_event = 0
        
        personal_next = gui.ImageButton(self.rect_personal, pygame.Rect(105, 80, 30, 30), 1, "assets/events/go-next.png", self._cb_button_click_personal_next)
        personal_back = gui.ImageButton(self.rect_personal, pygame.Rect(0, 80, 30, 30), 1, "assets/events/go-back.png", self._cb_button_click_personal_back)
        
        self.add_button(personal_next)
        self.add_button(personal_back)
        
        self.count_personal_events = gui.Text(self.rect_personal, 50, 82, 1, "%s/%s" % (self.index_personal_event, len(self.active_personal_events)), 20, pygame.Color("black"))
        self.add_child(self.count_personal_events)
        
        self.b_event_personal = None # Visible event at panel
        
        # Social
        self.surf_social = pygame.Surface((130, 110))
        self.rect_social = pygame.Rect((579, 652), self.surf_social.get_rect().size)
        self.active_social_events = [] # tuple (event, button)
        self.index_social_event = 0
        
        social_next = gui.ImageButton(self.rect_social, pygame.Rect(105, 80, 30, 30), 1, "assets/events/go-next.png", self._cb_button_click_social_next)
        social_back = gui.ImageButton(self.rect_social, pygame.Rect(0, 80, 30, 30), 1, "assets/events/go-back.png", self._cb_button_click_social_back)
        
        self.add_button(social_next)
        self.add_button(social_back)
        
        self.count_social_events = gui.Text(self.rect_social, 50, 82, 1, "%s/%s" % (self.index_social_event, len(self.active_social_events)), 20, pygame.Color("black"))
        self.add_child(self.count_social_events)
        
        self.b_event_social = None # Visible event at panel
        
        # Customization
        customization_button = gui.ImageButton(self.rect, pygame.Rect(885, 0, 1, 1), 1, "assets/layout/customization.png", self._cb_button_click_customization)
        customization_button.set_tooltip(_("Customization module"))
        self.add_button(customization_button)
        
        # Info
        info_button = gui.ImageButton(self.rect, pygame.Rect(953, 0, 1, 1), 1, "assets/layout/info.png", self._cb_button_click_stop_action)
        self.add_button(info_button)

        # Environment
        self.weather_widget = None
        self.set_weather()
    
    def set_weather(self):
        if self.weather_widget:
            self.remove_child(self.weather_widget)
        
        weather = self.windows_controller.game_man.current_weather
        file_path = "assets/events/weather/" + weather + ".png"
        self.weather_widget = gui.Image(self.rect, pygame.Rect(51, 34, 1, 1), 1, file_path)
        self.add_child(self.weather_widget)
        self.weather_widget.set_dirty()
        
        info = "%s \n" % (weather)
        
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
            self.current_animation = animation.ActionAnimation(self.rect, self.rect_action, 10, action.window_animation_path, action.sound_path)
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
    
    # Events
    def add_personal_event(self, event):
        if not event in self.active_personal_events:
            b_event_personal = gui.ImageButton(self.rect_personal, pygame.Rect(23, 3, 100, 100), 1, pygame.image.load("assets/events/%s" % (event.picture)).convert())
            
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
        
    def add_social_event(self, event):
        if not event in self.active_social_events:
            
            b_event_social = gui.ImageButton(self.rect_social, pygame.Rect(23, 3, 100, 100), 1, pygame.image.load("assets/events/%s" % (event.picture)).convert())
            
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
  
    def refresh_count_personal_events(self):
        
        if self.active_personal_events:
            self.count_personal_events.text = "%s/%s" % (self.index_personal_event + 1, len(self.active_personal_events))
            self.count_personal_events.refresh()
            
        else:
            self.count_personal_events.text = "0/0"
            self.count_personal_events.refresh()
            
    def refresh_count_social_events(self):
        
        if self.active_social_events:
            self.count_social_events.text = "%s/%s" % (self.index_social_event + 1, len(self.active_social_events))
            self.count_social_events.refresh()
            
        else:
            self.count_social_events.text = "0/0"
            self.count_social_events.refresh()
        
    def update(self, frames):
             
        self.timing += 1
        
        # Actions
        if self.on_animation and self.current_animation and self.timing % self.current_animation.frame_rate == 0:
            if self.timing > 12:
                self.timing = 0
    
        gui.Window.update(self, frames)
        
    # Buttons Callbacks
    def _cb_button_click_personal(self, button):
        if game.set_library_function:
            game.set_library_function("99-Eventos.html") #diarrhea")
        
    def _cb_button_click_social(self, button):
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

    def _cb_button_click_customization(self, button):
        self.windows_controller.set_active_window("customization_window")
        
    def _cb_button_click_stop_action(self, nutton):
        self.stop_action_animation()
        
class ActionProgressBar(gui.Widget):
    """
    Shows the progress of the active action
    """
    def __init__(self, container, rect_in_container, frame_rate, action):
        
        self.action = action
        surface = pygame.image.load("assets/layout/main_bar_back.png").convert_alpha()
        
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
