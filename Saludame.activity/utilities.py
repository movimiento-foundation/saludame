# -*- coding: utf-8 -*-

# Utilitarios: Text, Button (abstract), ImageButton, TextButton

from widget import *

class Text(Widget):
    def __init__(self, container, x, y, frame_rate, text, size, color):
        self.font = pygame.font.SysFont(None, size)
        self.background = self.font.render(text, True, color)
        
        self.text = text
        Widget.__init__(self, container, self.background.get_rect(topleft=(x, y)), frame_rate, self.background, None)
        
    def switch_color_text(self, color):
        self.background = self.font.render(self.text, True, color)
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
        
    def contains_point(self, x, y):
        return self.rect_absolute.collidepoint(x, y)
    
    def set_tooltip(self, text):
        self.tooltip = text
    
    def on_mouse_click(self):
        if self.function_on_mouse_click: # if there's a callback setted makes the call
            self.function_on_mouse_click(self)
        
    def on_mouse_over(self):
        if self.function_on_mouse_over: # if there's a callback setted makes the call
            self.function_on_mouse_over(self)
    
    def on_mouse_out(self):
        if self.function_on_mouse_out: # if there's a callback setted makes the call
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
            
        Button.__init__(self, container, rect, frame_rate, self.image, cb_click, cb_over, cb_out)
    
    def switch_image_background(self, image):
        if not isinstance(image, pygame.Surface):
            image = pygame.image.load(image).convert_alpha()
        self.background = image
        
class TextButton(ImageButton):     
    def __init__(self, container, rect, frame_rate, text, size, color, cb_click=None, cb_over=None, cb_out=None):
        self.text = Text(rect, 5, 5, frame_rate, text, size, color)
        ImageButton.__init__(self, container, rect, frame_rate, self.text.background, cb_click, cb_over, cb_out)
        
    def switch_color_text(self, color):
        self.background = self.text.switch_color_text(color).background        
        
def change_color(surface, old_color, new_color):
    # No funciona en pygame 1.8.0
    #image_pixel_array = pygame.PixelArray(self.sprite)
    #image_pixel_array.replace(old_color, new_color)
    
    mapped_int = surface.map_rgb(old_color)
    surface.set_palette_at(mapped_int, new_color[0:3])   
