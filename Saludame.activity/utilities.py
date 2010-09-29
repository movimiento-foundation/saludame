# -*- coding: utf-8 -*-

# Utilitarios

# Probando branch...

import pygame

class Text:
    def __init__(self, x, y, text, size):
        self.font = pygame.font.SysFont(None, size)
        self.ren = self.font.render(text, 1, (0, 0, 100))
        self.x = x
        self.y = y
    
    def draw(self, screen):
        screen.blit(self.ren, (self.x, self.y))        

class Button:
    
    # Clase abstracta que representa un boton
    
    def __init__(self, rect, x, y, w, h, text):
        # Agregamos los botones con coordenadas "relativas" a la ventana que los cotiene
        self.rect = pygame.Rect(rect.left + x, rect.top + y, w, h)
        self.text = text
        
        self.font = pygame.font.SysFont(None, 16)
        
        self.background_color = (255,0,0)
        self.over = False
          
    def contains_point(self, x, y):
        return self.rect.collidepoint(x, y)
    
    def draw(self, surface):
        ren = self.font.render(self.text, 1, (0, 0, 100))
        surface.fill(self.background_color, self.rect)
        surface.blit(ren, (self.rect.left + 5, self.rect.top + 5))
            
    def set_background_color(self, color):
        self.background_color = color    
    
    # Eventos sobre el boton... seran sobreescritos por los hijos
        
    def on_mouse_click(self):
        None
        
    def on_mouse_over(self):
        None
    
    def on_mouse_out(self):
        None

class ImageButton:
    
    # Clase abstracta que representa un boton con una imagen de fondo
    
    def __init__(self, rect, x, y, image):
        
        if not isinstance(image, pygame.Surface):
            image = pygame.image.load(image).convert_alpha()
        
        self.image = image
        
        # Agregamos los botones con coordenadas "relativas" a la ventana que los cotiene
        self.rect = pygame.Rect(rect.left + x, rect.top + y, image.get_width(), image.get_height())
        
        self.background_color = (0, 0, 0)
        self.over = False
        
    def contains_point(self, x, y):
        return self.rect.collidepoint(x, y)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        return [self.rect]
                
    def set_background_color(self, color):
        self.background_color = color
        
    # Eventos sobre el boton... seran sobreescritos por los hijos
    def on_mouse_click(self):
        None
    
    def on_mouse_over(self):
        None
    
    def on_mouse_out(self):
        None

class CloseButton(Button):
    def __init__(self, rect, x, y, w, h, text):
        Button.__init__(self, rect, x, y, w, h, text)
        self.font = pygame.font.SysFont(None, 30) # Modificamos atributo heredado
        self.background_color = (150, 150, 255) # Modificamos atributo heredado        
    
    def on_mouse_click(self, windows_controller):
        windows_controller.close_active_window()

def change_color(surface, old_color, new_color):
    # No funciona en pygame 1.8.0
    #image_pixel_array = pygame.PixelArray(self.sprite)
    #image_pixel_array.replace(old_color, new_color)
    
    mapped_int = surface.map_rgb(old_color)
    surface.set_palette_at(mapped_int, new_color[0:3])
    
