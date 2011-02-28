# -*- coding: utf-8 -*-

import gui
import pygame
import os
import effects

def get_accept_button(container, rect, text, cb_click=None, cb_over=None, cb_out=None):
    background = pygame.image.load("assets/windows/dialog_button.png").convert()
    return gui.TextButton2(container, rect, 1, text, 24, pygame.Color("#397b7e"), background, cb_click, cb_over, cb_out)
    
def change_color(surface, old_color, new_color):
    # No funciona en pygame 1.8.0
    i = 0
    palette = surface.get_palette()
    for color in palette:
       if color == old_color:
           surface.set_palette_at(i, get_color_tuple(new_color))
       i += 1

def get_color_tuple(color):
    if isinstance(color, tuple):
        return color[0:3]
    elif isinstance(color, pygame.Color):
        return (color.r, color.g, color.b)
    else:
        color = pygame.Color(color)
        return get_color_tuple(color)

# Fonts - creates an alias for the get_font function
get_font = gui.get_font

# Paths controls
def check_image(image_path):
    try:
        print image_path
        pygame.image.load(image_path)
        return True
    except:
        return False
    
def verify_path(action, game_manager):
    if isinstance(action.effect, effects.Effect): # If the action has effects on bars
        if action.kid_animation_path: # and has a kid animation path
            return os.path.isdir("%s/%s/%s" % (action.kid_animation_path, game_manager.character.sex, game_manager.character.clothes)) # check animation directory (action_path/sex/clothes)
        else:
            return True
            
    if isinstance(action.effect, effects.ClothesEffect): # If the action has clothes effects
        return os.path.isdir("%s/%s/%s" % (game_manager.character.mood.kid_animation_path, game_manager.character.sex, action.effect.clothes_id))
        
    if isinstance(action.effect, effects.LocationEffect): # If the action has location effects
        return os.path.isfile(game_manager.environments_dictionary[(action.effect.place_id, game_manager.current_weather[0])].background_path)
        
    return True
