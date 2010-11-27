# -*- coding: utf-8 -*-
import os
import pygame

from window import Window
import utilities
import menu_creator
import animation

BACKGROUND_PATH = os.path.normpath("assets/background/schoolyard_sunny.png")

class KidWindow(Window):

    def __init__(self, container, rect, frame_rate, windows_controller, game_man):
        
        Window.__init__(self, container, rect, frame_rate, windows_controller, "kid")
        self.set_bg_image(pygame.image.load(BACKGROUND_PATH).convert())   
        
        self.kid_rect = pygame.Rect((280, 70), (350, 480))  
        self.mood = "normal" 
            
        self.kid = animation.Kid(rect, self.kid_rect, 1, windows_controller, game_man, self.mood)
        
        self.add_window(self.kid)
        self.kid.set_bg_image(self.bg_image.subsurface(self.kid_rect))          

        self.balloon = None
        
        ### Events ###
    
        # Socials
        self.social_event = None
        self.external_character = None
        
        # Menu
        self.menu = menu_creator.load_menu(game_man, (480, 250), self.rect, windows_controller)
        self.add_window(self.menu)
        
        self.last_repaint = False
        
    ##### Environment #####
    def set_environment(self, environment):
        self.set_bg_image(pygame.image.load(environment.background_path).convert())  
        self.kid.set_bg_image(self.bg_image.subsurface(self.kid_rect))
        
    ##### Moods #####    
    def change_mood(self):
        self.kid.change_mood()
        
    def set_mood(self, mood):
        self.kid.set_mood(mood)
        
    ##### Actions #####
    def play_action_animation(self, action):
        self.kid.play_action_animation(action)
    
    def stop_action_animation(self):
        self.kid.stop_action_animation()
        
    ##### Events #####
    def add_social_event(self, event):
        self.social_event = event
        self.external_character = ExternalCharacter(self.rect, pygame.Rect(700, 170, 1, 1), 1, self.windows_controller)
        self.add_window(self.external_character)
                
    def remove_social_event(self):
        self.social_event = None
        self.windows.remove(self.external_character)
        self.external_character = None
    
    ##### Kid ballon #####
    def show_kid_balloon(self, message, time_span):
        self.balloon = MessageBalloon(self.rect, pygame.Rect(580, 80, 1, 1), 1, self.windows_controller)
        self.balloon.set_text(message)
        self.balloon.set_time_span(time_span)
        self.add_window(self.balloon)
        
    def remove_kid_balloon(self):
        self.windows.remove(self.balloon)
        self.balloon = None

    def draw(self, screen, frames):
        
        changes = []
        
        if self.last_repaint:
            self.repaint = True
            self.last_repaint = False
            
        # If the menu is showing repaint the whole window
        if self.menu.show:
            self.last_repaint = True
            self.repaint = True         
        
        changes += Window.draw(self, screen, frames)
    
        if self.balloon:    
            if not self.balloon.visible:
                self.remove_kid_balloon()
                
        if self.external_character:    
            if not self.external_character.visible:
                self.remove_social_event()
        
        # Characters at social events        
        if self.external_character:
            changes += self.external_character.draw(screen, frames)
                
        return changes
    
class ExternalCharacter(Window):
    def __init__(self, container, rect, frame_rate, windows_controller):
        
        self.character = pygame.image.load("assets/characters/teacher.png").convert_alpha()
        rect.size = self.character.get_size()
        
        Window.__init__(self, container, rect, frame_rate, windows_controller, "external_character")
        
        self.set_bg_image(self.character)
        
        self.visible = True
        self.time_span = 100 # Hardcoded 
        
        self.message_balloon = MessageBalloon(self.container, pygame.Rect(580, 80, 1, 1), 1, self.windows_controller)  
        self.message_balloon.set_text(u"Deberías ir al dentista....") # Hardcoded
        self.message_balloon.set_time_span(self.time_span) # Mismo time_span que el character
        
        self.bg1 = (self.windows_controller.screen.subsurface(self.rect).copy())
        self.bg2 = (self.windows_controller.screen.subsurface(self.message_balloon.rect).copy())
        
    # Override handle_mouse_down    
    def handle_mouse_down(self, (x, y)):
        self.visible = False
        
    def draw(self, screen, frames):
        if (not self.time_span):
            self.visible = False
        if (self.visible):
            changes = []
            self.time_span -= 1
            self.repaint = True
            changes += Window.draw(self, screen, frames)
            changes += self.message_balloon.draw(screen, frames)
            return changes
        else:
            screen.blit(self.bg1, self.rect)
            screen.blit(self.bg2, self.message_balloon.rect)
            return [self.rect, self.message_balloon.rect]
         
        
class MessageBalloon(Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller):
        
        background = pygame.image.load("assets/events/balloon.png").convert_alpha()
        rect.size = background.get_size()
        
        Window.__init__(self, container, rect, frame_rate, windows_controller, "balloon")
        
        self.bg = (self.windows_controller.screen.subsurface(self.rect).copy())
        
        self.set_bg_image(background)
        self.text = None
        self.time_span = None
        
        self.visible = True
    
    # Override handle_mouse_down    
    def handle_mouse_down(self, (x, y)):
        self.visible = False
        
    def set_text(self, text):
        self.text = utilities.TextBlock(self.rect, 140, 40, 1, text, 18, pygame.Color("black"))
        self.add_child(self.text)
        
    def set_time_span(self, time_span):
        self.time_span = time_span
    
    def draw(self, screen, frames):
        if (not self.time_span):
            self.visible = False
        if (self.visible):
            self.time_span -= 1
            self.repaint = True
            return Window.draw(self, screen, frames)
        else:
            screen.blit(self.bg, self.rect)
            return [self.rect]

