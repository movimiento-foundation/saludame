# -*- coding: utf-8 -*-
import os
import pygame

import gui
import menu_creator
import animation
import utilities
from character import *
from gettext import gettext as _

BACKGROUND_PATH = os.path.normpath("assets/background/schoolyard_normal.png")

class KidWindow(gui.Window):

    def __init__(self, container, rect, frame_rate, windows_controller, cha_loader, game_man):
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "kid")
        self.set_bg_image(pygame.image.load(BACKGROUND_PATH).convert())
        
        kid_rect = pygame.Rect((280, 70), (400, 500))
        self.mood = "normal"
        
        self.game_man = game_man
        
        self.cha_loader = cha_loader
            
        self.kid = animation.Kid(rect, kid_rect, 1, windows_controller, game_man, self.mood)
        self.add_child(self.kid)
        
        self.balloon = None
        
        ### Events ###
        
        # Socials
        self.social_event = None
        self.external_character = None
        
        # Menu
        self.menu = menu_creator.load_menu(game_man, (480, 250), self.rect, windows_controller)
        self.add_window(self.menu)
        
        # Challenges
        challenges_button = gui.ImageButton(self.rect, pygame.Rect((900, 400), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_mc_challenges)
        challenges_button.set_tooltip(_("Multiple choice"))
        challenges_button.keep_dirty = True
        self.add_button(challenges_button)
        
        challenges_button2 = gui.ImageButton(self.rect, pygame.Rect((900, 500), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_tf_challenges)
        challenges_button2.set_tooltip(_("True or false"))
        challenges_button2.keep_dirty = True
        self.add_button(challenges_button2)
        
        challenges_button3 = gui.ImageButton(self.rect, pygame.Rect((900, 300), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_master_challenge)
        challenges_button3.set_tooltip(_("Master challenge"))
        challenges_button3.keep_dirty = True
        self.add_button(challenges_button3)
        
        challenges_button4 = gui.ImageButton(self.rect, pygame.Rect((900, 200), (60, 60)), 1, "challenges/trophy.png", self._cb_button_click_cooking_challenge)
        challenges_button4.set_tooltip(_("Cooking"))
        challenges_button4.keep_dirty = True
        self.add_button(challenges_button4)
        
        self.last_repaint = False
        
    ##### Callbacks #####
    def _cb_button_click_mc_challenges(self, button):
        self.cha_loader.get_challenge("mc")
        self.windows_controller.set_active_window("mc_challenge_window")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Múltiple Opción: %s" %(self.cha_loader.game_man.get_lowest_bar().label),  u"Tu barra de %s está baja. \nPara ganar puntos tienes que acertar \nla respuesta correcta. \n\n¡Suerte!" %(self.cha_loader.game_man.get_lowest_bar().label))
        self.windows_controller.set_active_window("info_challenge_window")
        
    def _cb_button_click_tf_challenges(self, button):
        self.cha_loader.get_challenge("tf")
        self.windows_controller.set_active_window("tf_challenge_window")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Verdadero o Falso: %s" %(self.cha_loader.game_man.get_lowest_bar().label), u"Tu barra de %s está baja. \nPara ganar puntos tienes que acertar \nlas preguntas de verdero o falso. \n\n¡Suerte!" %(self.cha_loader.game_man.get_lowest_bar().label))
        self.windows_controller.set_active_window("info_challenge_window")
        
    def _cb_button_click_master_challenge(self, button):
        self.cha_loader.get_challenge("master")
        self.windows_controller.set_active_window("tf_challenge_window")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Super Desafío",  u"¡Estas por pasar de nivel! \nPara superarlo tienes que responder \ncorrecto a 3 de las 5 preguntas \nque siguen \n\n¡Suerte!")
        self.windows_controller.set_active_window("info_challenge_window")
        
    def _cb_button_click_cooking_challenge(self, button):
        self.windows_controller.set_active_window("cooking_challenge_window")
        
    ##### Environment #####
    def set_environment(self, environment, time):
        sky = pygame.image.load("assets/background/sky/" + time + ".png").convert_alpha()
        
        image = pygame.image.load(environment.background_path).convert_alpha()
        if time == "night":
            #image = image.convert(24)
            _filter = pygame.Surface(image.get_size())
            _filter.fill((30, 30, 100))
            _filter.set_alpha(50)
            image.blit(_filter, (0,0))
        sky.blit(image, (0,0))
        self.set_bg_image(sky.convert())
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
        self.remove_social_event()
        self.social_event = event
        self.external_character = ExternalCharacter(self.rect, (30, 609), 1, self.windows_controller, event, self.game_man.character)
        self.add_window(self.external_character)
                
    def remove_social_event(self):
        self.social_event = None
        if self.external_character:
            self.remove_window(self.external_character)
        self.external_character = None
    
    ##### Kid ballon #####
    def show_kid_balloon(self, message, time_span):
        self.remove_kid_balloon()
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
    
    def __init__(self, container, left_bottom, frame_rate, windows_controller, event, character):

        rect = pygame.Rect((0,0), (300, 559))
        rect.bottomleft = left_bottom
        
        self.visible = True
        
        gui.Window.__init__(self, container, rect, frame_rate, windows_controller, "external_character")
        
        self.time_span = event.message_time_span
                
        self.character = character # Main character (Kid)        
        self.mappings = DEFAULT_MAPPINGS.copy()
        
        self.external_character = gui.Image(self.rect, pygame.Rect((13, 179), (273, 380)), 1, event.person_path)
        
        if (event.person_path == "assets/characters/mother.png" or event.person_path == "assets/characters/father.png"):
            #new_colors = [pygame.Color(color) for color in ("#000000", "#191919")]
            #self.set_mapping("hair", new_colors)
            pass
        
        self.external_character.keep_dirty = True
        self.add_child(self.external_character)
        
        message_balloon = MessageBalloon(self.rect, pygame.Rect(0, 0, 1, 1), 1, self.windows_controller, 'B')
        message_balloon.set_text(event.person_message)
        self.add_window(message_balloon)
      
    ###########################################   
    
    def set_mapping(self, key, colors):
        self.mappings[key] = tuple(colors)
        self.apply_mappings()
        
    def apply_mappings(self):
        self.external_character.background = self.external_character.background.copy()
        self.external_character.background = self.background.convert(8)
        maps = self.mappings
        self.change_color(animation.COLORS_TO_MAP, maps["hair"] + maps["skin"] + maps["socks"] + maps["shoes"])
        self.set_dirty()
        
    def change_color(self, old, new):
        index = 0
        for old_color in old:
            new_color = new[index]
            utilities.change_color(self.external_character.background, old_color, new_color)
            index += 1
            
    ###########################################
    
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
        if self.visible:
            self.hide()
            self.dispose()
            return True
        else:
            return False
        
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
        self.time_span -= 1
        if self.time_span == 0:
            self.hide()
            self.dispose()
        
        if self.visible:
            self.set_dirty_background()    # Always draws it because it collides with the character rectangle
    