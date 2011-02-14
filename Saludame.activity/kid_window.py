# -*- coding: utf-8 -*-
import os
import pygame

import gui
import menu_creator
import animation

BACKGROUND_PATH = os.path.normpath("assets/background/schoolyard_sunny.png")

class KidWindow(gui.Window):

    def __init__(self, container, rect, frame_rate, windows_controller, game_man):
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "kid")
        self.set_bg_image(pygame.image.load(BACKGROUND_PATH).convert())
        
        self.kid_rect = pygame.Rect((280, 70), (350, 480))
        self.mood = "normal"
            
        self.kid = animation.Kid(rect, self.kid_rect, 1, windows_controller, game_man, self.mood)
        self.add_child(self.kid)
        
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
    def set_environment(self, environment, time):
        image = pygame.image.load(environment.background_path).convert(24)
        if time == "night":
            _filter = pygame.Surface(image.get_size())
            _filter.fill((30, 30, 100))
            _filter.set_alpha(50)
            image.blit(_filter, (0,0))
        self.set_bg_image(image.convert())
        self.set_dirty_background()
        
    ##### Clothes #####
    def update_clothes(self):
        self.kid.update_clothes()
        
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
        self.external_character = ExternalCharacter(self.rect, (30, 609), 1, self.windows_controller, event)
        self.add_window(self.external_character)
                
    def remove_social_event(self):
        self.social_event = None
        if self.external_character:
            self.remove_window(self.external_character)
        self.external_character = None
        self.set_dirty_background()
    
    ##### Kid ballon #####
    def show_kid_balloon(self, message, time_span):
        self.balloon = MessageBalloon(self.rect, pygame.Rect(580, 80, 1, 1), 1, self.windows_controller, 'A')
        self.balloon.set_text(message)
        self.balloon.set_time_span(time_span)
        self.add_window(self.balloon)
        
    def remove_kid_balloon(self):
        if self.balloon:
            self.remove_window(self.balloon)
        self.balloon = None

    def update(self, frames):
        
        gui.Window.update(self, frames)
        
        if self.balloon:
            if not self.balloon.visible:
                self.remove_kid_balloon()
                
        if self.external_character:
            if not self.external_character.visible:
                self.remove_social_event()


class ExternalCharacter(gui.Window):
    
    def __init__(self, container, left_bottom, frame_rate, windows_controller, event):

        rect = pygame.Rect((0,0), (300, 559))
        rect.bottomleft = left_bottom
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "external_character")
        
        self.time_span = event.message_time_span
                
        character = gui.Image(self.rect, pygame.Rect((13, 179), (273, 380)), 1, event.person_path)
        character.keep_dirty = True
        self.add_child(character)
        
        message_balloon = MessageBalloon(self.rect, pygame.Rect(0, 0, 1, 1), 1, self.windows_controller, 'B')
        message_balloon.set_text(event.person_message)
        self.add_window(message_balloon)
    
    # Override handle_mouse_down
    def handle_mouse_down(self, (x, y)):
        self.hide()
        
    def update(self, frames):
        self.time_span -= 1
        if self.time_span == 0:
            self.hide()
            self.dispose()
        
        if self.visible:
            # This shouldn't be neccesary but it's not working without it.
            self.set_dirty_background()    # Always draws it because it collides with the character rectangle
    
class MessageBalloon(gui.Window):
    
    def __init__(self, container, rect, frame_rate, windows_controller, b_type):
        
        self.b_type = b_type
        
        if b_type == 'A':
            # Thinking balloon
            background = pygame.image.load("assets/events/balloon.png").convert()
        else:
            # Saying balloon
            background = pygame.image.load("assets/events/balloonB.png").convert()
            
        rect.size = background.get_size()
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "balloon")        
        
        self.set_bg_image(background)
        self.text = None
        self.time_span = None
        
        self.visible = True
    
    # Override handle_mouse_down
    def handle_mouse_down(self, (x, y)):
        self.hide()
        
    def set_text(self, text):
        if self.b_type == 'A':
            self.text = gui.TextBlock(self.rect, 135, 40, 1, text, 18, pygame.Color("black"))
        else:
            self.text = gui.TextBlock(self.rect, 40, 40, 1, text, 18, pygame.Color("black"))
        self.text.keep_dirty = True
        self.add_child(self.text)
        
    def set_time_span(self, time_span):
        self.time_span = time_span
    
    def update(self, frames):
        if self.time_span == 0:
            self.hide()
            self.dispose()
        
        if self.visible:
            self.set_dirty_background()    # Always draws it because it collides with the character rectangle
    
