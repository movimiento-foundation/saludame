# -*- coding: utf-8 -*-

# Utilitarios: Text, Button (abstract), ImageButton, TextButton

from widget import *
import pygame
import os
from game_manager import *

class Text(Widget):
    
    ALIGN_LEFT = 0
    ALIGN_RIGHT = 1
    ALIGN_CENTER = 2
    
    def __init__(self, container_rect, x, y, frame_rate, text, size, color, alignment=ALIGN_LEFT, bold=False, italic=False):
        self.font = get_font(size, bold, italic)
        self.text = unicode(text)
        self.color = color
        
        # Render the text and calculate the size
        render = self.font.render(self.text, False, color)
        if alignment == Text.ALIGN_LEFT:
            rect = render.get_rect(topleft=(x, y))
        elif alignment == Text.ALIGN_RIGHT:
            rect = render.get_rect(topright=(x, y))
        else:
            rect = render.get_rect(center=(x, y))
        
        # Make it fit in the container
        if rect.right > container_rect.right:
            rect.right = container_rect.right
        if rect.bottom > container_rect.bottom:
            rect.bottom = container_rect.bottom
        
        Widget.__init__(self, container_rect, rect, frame_rate)
        
        self.refresh()
    
    def refresh(self):
        background = self.get_background_rect().copy()
        self.background = self.font.render(self.text, False, self.color)
    
    def switch_color_text(self, color):
        self.color = color
        self.refresh()
        return (self)
    
class Image(Widget):
    def __init__(self, container, rect, frame_rate, image):
        
        if not isinstance(image, pygame.Surface):
            self.background = pygame.image.load(image).convert_alpha()
        else:
            self.background = image
        Widget.__init__(self, container, rect, frame_rate, self.background)        
        

class Button(Widget):
    
    # Clase abstracta que representa un boton
    
    def __init__(self, container, rect, frame_rate, surface, cb_click=None, cb_over=None, cb_out=None):
        
        Widget.__init__(self, container, rect, frame_rate, surface)
        
        self.function_on_mouse_click = cb_click
        self.function_on_mouse_over = cb_over
        self.function_on_mouse_out = cb_out
        
        self.over = False
        self.enable = True
        
    def contains_point(self, x, y):
        return self.rect_absolute.collidepoint(x, y)
    
    def set_tooltip(self, text):
        self.tooltip = text
        
    def set_super_tooltip(self, text):
        self.super_tooltip = text
    
    def on_mouse_click(self):
        if (self.function_on_mouse_click and self.enable): # if there's a callback setted makes the call
            self.function_on_mouse_click(self)
        
    def on_mouse_over(self):
        if (self.function_on_mouse_over and self.enable): # if there's a callback setted makes the call
            self.function_on_mouse_over(self)
    
    def on_mouse_out(self):
        if (self.function_on_mouse_out and self.enable): # if there's a callback setted makes the call
            self.function_on_mouse_out(self)
            
    def set_on_mouse_click(self, fn):
        self.function_on_mouse_click = fn
   
    def set_on_mouse_over(self, fn):
        self.function_on_mouse_over = fn

    def set_on_mouse_out(self, fn):
        self.function_on_mouse_out = fn   
    

class ImageButton(Button):
    
    def __init__(self, container, rect, frame_rate, image, cb_click=None, cb_over=None, cb_out=None):
        
        self.image = image       
        if not isinstance(image, pygame.Surface):
            self.image = pygame.image.load(image).convert_alpha()
        
        rect.size = self.image.get_rect().size
        Button.__init__(self, container, rect, frame_rate, self.image, cb_click, cb_over, cb_out)
    
    def switch_image_background(self, image):
        if not isinstance(image, pygame.Surface):
            image = pygame.imaself.text_intro.visible = True
        self.text_result.visible = Falsege.load(image).convert_alpha()
        self.background = image
        
class TextButton(ImageButton):     
    def __init__(self, container, rect, frame_rate, text, size, color, cb_click=None, cb_over=None, cb_out=None):
        self.text = Text(container, rect.x, rect.y, frame_rate, text, size, color)
        ImageButton.__init__(self, container, self.text.rect_in_container, frame_rate, self.text.background, cb_click, cb_over, cb_out)
        
    def switch_color_text(self, color):
        self.background = self.text.switch_color_text(color).background
    
class TextButton2(ImageButton):
    
    def __init__(self, container, rect, frame_rate, text, size, color, background, cb_click=None, cb_over=None, cb_out=None):
        self.back = background
        self.text = text
        self.size = size
        self.color = color
        
        rect.size = self.back.get_size()
        surface = self.get_surface()
        ImageButton.__init__(self, container, rect, frame_rate, surface, cb_click, cb_over, cb_out)
        
    def switch_color_text(self, color):
        self.color = color
        self.background = self.get_surface()
    
    def get_surface(self):
        font = get_font(self.size)
        render = font.render(self.text, True, self.color)
        
        surface = self.back.copy()
        surface.blit(render, render.get_rect(center=surface.get_rect().center))
        return surface

def get_accept_button(container, rect, text, cb_click=None, cb_over=None, cb_out=None):
    background = pygame.image.load("assets/windows/dialog_button.png").convert_alpha()
    return TextButton2(container, rect, 1, text, 24, pygame.Color("#397b7e"), background, cb_click, cb_over, cb_out)
    
def change_color(surface, old_color, new_color):
    # No funciona en pygame 1.8.0
    i = 0
    indexes = []
    palette = surface.get_palette()
    for color in palette:
        if get_color_tuple(color) == get_color_tuple(old_color):
            indexes += [i]
        i += 1
    
    for i in indexes:
        surface.set_palette_at(i, get_color_tuple(new_color))

def get_color_tuple(color):
    if isinstance(color, tuple):
        return color[0:3]
    elif isinstance(color, pygame.Color):
        return (color.r, color.g, color.b, color.a)[0:3]
    else:
        color = pygame.Color(color)
        return get_color_tuple(color)
    
class TextBlock(Widget):
    def __init__(self, container, x, y, frame_rate, text, size, color):    
            
        Widget.__init__(self, container, pygame.Rect(x, y, 0, 0), frame_rate)
        
        self.lines = []
        self.font = get_font(size)
        self.color = color
        self.parse_lines(text)
        self.size = size
        self.prepare_text_block()
        
    def parse_lines(self, text):
        if isinstance(text, unicode):
            eol = u"\n"
        else:
            eol = "\n"
            
        (b, _, a) = text.partition(eol)
        self.lines.append(b)
        while(a != ''):
            (b, _, a) = a.partition(eol)
            self.lines.append(b)

    def prepare_text_block(self):
        number_of_lines = 0
        for l in self.lines:
            number_of_lines += 1           
            r = self.font.render(l, False, self.color)
            if (r.get_rect().width > self.rect_absolute.width):
                self.rect_absolute.width = r.get_rect().width
            self.rect_absolute.height += r.get_rect().height 
            
        # Make it fit in the container
        if self.rect_absolute.right > self.container.right:
            self.rect_absolute.right = self.container.right
        if self.rect_absolute.bottom > self.container.bottom:
            self.rect_absolute.bottom = self.container.bottom                  
        
    def draw(self, screen):
        if self.visible:
            number_of_lines = 0
            screen.fill((255, 255, 255), (self.rect_absolute))
            for l in self.lines:          
                r = self.font.render(l, False, self.color)
                screen.blit(r, (self.rect_absolute.left, self.rect_absolute.top + r.get_rect().height * number_of_lines))
                number_of_lines += 1

font_dict = {}  # Chaches created font instances
def get_font(size, bold=False, italic=False):
    key = (size, bold, italic)
    if key in font_dict:
        return font_dict[key]
    
    if bold:
        font = pygame.font.Font("assets/fonts/DroidSans-Bold.ttf", size)
    else:
        font = pygame.font.Font("assets/fonts/DroidSans.ttf", size)
    
    if italic:
        font.set_italic(True)
    
    font_dict[key] = font
    
    return font

#### Paths controls ####
def check_directory(directory):
    try:
        print directory
        os.listdir(directory)
        return True
    except OSError:
        return False
    
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
            return check_directory("%s/%s/%s" % (action.kid_animation_path, game_manager.character.sex, game_manager.character.clothes)) # check animation directory (action_path/sex/clothes)
        else:
            return True
            
    if isinstance(action.effect, effects.ClothesEffect): # If the action has clothes effects
        return check_directory("%s/%s/%s" % (game_manager.character.mood.kid_animation_path, game_manager.character.sex, action.effect.clothes_id))
        
    if isinstance(action.effect, effects.LocationEffect): # If the action has location effects
        return check_image(game_manager.environments_dictionary[action.effect.place_id + "_" + game_manager.current_weather].background_path)        
        
    return True
