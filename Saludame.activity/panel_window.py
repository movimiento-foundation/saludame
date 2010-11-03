# -*- coding: utf-8 -*-

import pygame
from window import Window
import animation
import os
from widget import Widget
import window

PANEL_BG_PATH = os.path.normpath("assets/layout/panel.png")

class PanelWindow(Window):
    def __init__(self, container, rect, frame_rate, windows_controller, bg_color=(0, 0, 0)):
        
        self.timing = 1 # la idea de timing es llevar una cuenta adentro, de los frames que fueron pasando        
        Window.__init__(self, container, rect, frame_rate, windows_controller, "panel_window")
        
        self.set_bg_image(PANEL_BG_PATH)
        
        # Actions
        self.surf_action = pygame.Surface((260, 110))
        self.surf_action.fill((255, 255, 255))
        
        self.on_animation = False
        self.actual_action = None
        self.actual_animation = None
        
        # Por ahora la barra de progreso se muestra al inicio y una vez que se "consume" no se vuelve a pintar
        action_progress_bar = ActionProgressBar(rect, pygame.Rect((630, 60), (182, 26)), 1, None)
        self.add_child(action_progress_bar)
        
        # Personal
        
        # Environment 
        
        # Social
        
        # Info
        info = Info(rect, pygame.Rect(885, 0, 1, 1), 1)        
        self.add_child(info)
        
    def set_active_action(self, action):
        self.actual_action = action
        self.actual_animation = animation.ActionAnimation(pygame.Rect(20, 5, 100, 100), 10, action.window_animation_path, action.sound_path)
    
    def play_animation(self, action):
        self.set_active_action(action)
        self.on_animation = True
        
    def stop_animation(self, id):
        self.on_animation = False
        
    def pre_draw(self, screen):
                    
        self.timing += 1
        changes = []
        
        # Actions
        if(self.on_animation and self.actual_animation != None and self.timing % self.actual_animation.frame_rate == 0):
            if(self.timing > 12):
                self.timing = 0
            
            #font = pygame.font.SysFont("Dejavu", 25)
            #self.surf_action.blit(font.render(self.actual_animation[1], 1, (0, 0, 255)), (120, 20))
            
            # Draw the animation on action surface
            changes += self.actual_animation.draw(self.surf_action)
        
        # Blit the action surface with screen
        screen.blit(self.surf_action, (780, 652))
        
        # Personal
        
        # Environment 
        
        # Social
        
        # Info
        
        return [self.rect]
    
class Info(Widget):    
    
    def __init__(self, container, rect_in_container, frame_rate):
        surface = pygame.image.load("assets/layout/info.png").convert_alpha()
        rect_in_container.size = surface.get_size()
        Widget.__init__(self, container, rect_in_container, frame_rate, surface)
        
class ActionProgressBar(Widget):
    """
    Shows the progress of the active action
    """
    def __init__(self, container, rect_in_container, frame_rate, action):
        
        self.action = action
        surface = pygame.image.load("assets/layout/main_bar_back.png").convert_alpha()
        
        Widget.__init__(self, container, rect_in_container, frame_rate)
        
        self.background = surface       # Borders of the bar
        self.surface = surface.copy()   # Actual surface to blit in the screen, _prepare_surface
        
        self.decrease = 1 # Porcentaje de tiempo restante de la acción (1 = 100%)
        self._prepare_surface()
        
    def _prepare_surface(self):
        rect = pygame.Rect((1, 2), (self.rect_in_container.width - 2, self.rect_in_container.height - 4))
        charged_rect = pygame.Rect(rect)  # create a copy
        
        charged_rect.width = self.decrease * rect.width
        
        self.surface.fill(pygame.Color("red"), rect)
        self.surface.fill(pygame.Color("blue"), charged_rect)
        self.surface.blit(self.background, (0, 0)) # Background blits over the charge, because it has the propper alpha
        
        self.decrease -= 0.01 # This value should be obtained from the action
        
    def draw(self, screen):
        """
        Draw the progress bar (if the action is still active), override widget draw
        """
        if (self.decrease > 0):        
            self._prepare_surface()            
            screen.blit(self.surface, self.rect_absolute)            
            return self.rect_absolute
