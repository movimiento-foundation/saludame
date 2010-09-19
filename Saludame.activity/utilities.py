# Utilitarios

import pygame

class Text:
    def __init__(self, x, y, text):
        self.font = pygame.font.SysFont("Verdana", 15)
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
        
        self.font = pygame.font.SysFont("Verdana", 15)
        self.ren = self.font.render(text, 1, (0, 0, 100))
        
        self.background_color = (255, 0, 0)
        self.over = False
          
    def contains_point(self, x, y):
        return self.rect.collidepoint(x, y)
    
    def draw(self, screen):
        screen.fill(self.background_color, self.rect)
        screen.blit(self.ren, (self.rect.left + 5, self.rect.top + 1))
            
    def set_background_color(self, color):
        self.background_color = color    
    
    # Eventos sobre el boton... seran sobreescritos por los hijos
        
    def on_mouse_clik(self):
        None
        
    def on_mouse_over(self):
        None
    
    def on_mouse_out(self):
        None
