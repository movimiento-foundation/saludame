# -*- coding: utf-8 -*-

import pygame
import os
import menuCreator
import animation
import statusBars

BLACK = pygame.Color("black")
BACKGROUND_PATH = os.path.normpath("assets/background/background.png")

class Window:
    
    def __init__(self, rect, frame_rate, background_color):
        self.rect = rect
        self.frame_rate = frame_rate
        self.surface = pygame.Surface((rect.width, rect.height))
        self.background_color = background_color        
        self.surface.fill(self.background_color)
        
    def draw(self, screen):
        self.surface.fill(self.background_color)
        screen.blit(self.surface, self.rect)
        return [self.rect]


class BlinkWindow(Window):
    
    def __init__(self, rect, frame_rate, background_color):
        Window.__init__(self, rect, frame_rate, background_color)
        self.par = True
        
    def draw(self, screen):
        self.par = not self.par
        
        if self.par:
            self.surface.fill(self.background_color)
        else:
            self.surface.fill(BLACK)
            
        screen.blit(self.surface, self.rect)
        
        return [self.rect]


class StatusWindow(Window):
    
    def __init__(self, rect, frame_rate, background_color):
        self.rect = rect
        self.frame_rate = frame_rate
        self.surface = pygame.Surface(rect.size)
        self.background_color = background_color
        
        self.surface.fill(self.background_color)
        
        self.bars = []
        self.bars.append(IdleStatusBar(pygame.Rect(20, 15, 460, 30), pygame.Color("green")))
        self.bars.append(IdleStatusBar(pygame.Rect(20, 55, 460, 30), pygame.Color("blue"), 35))
        self.bars.append(IdleStatusBar(pygame.Rect(20, 95, 460, 30), pygame.Color("yellow"), 65))
        
    def draw(self, screen):
        self.surface.fill(self.background_color)
        
        for bar in self.bars:
            bar.draw(self.surface)
            
            screen.blit(self.surface, self.rect)
            
        return [self.rect]


class StatusBar:
    
    def __init__(self, rect, color, value=0):
        self.rect = rect
        self.color = color
        self.surface = pygame.Surface(rect.size)
        self.value = value


class IdleStatusBar(StatusBar):
    
    def __init__(self, rect, color, value=0):
        StatusBar.__init__(self, rect, color, value)
        
    def draw(self, screen):
        self.value = (self.value + 1) % 101
        factor = self.value / 100.0
        
        rect = pygame.Rect((0, 0), self.rect.size)
        rect.width *= factor
        
        self.surface.fill(BLACK)
        self.surface.fill(self.color, rect)
        screen.blit(self.surface, self.rect)
        
        return [self.rect]

class KidWindow(Window):

    def __init__(self, rect, frame_rate):
        Window.__init__(self, rect, frame_rate, BLACK)
        
        self.first = True
        
        self.background = pygame.image.load(BACKGROUND_PATH).convert()
        
        kid_rect = pygame.Rect((100, 20), (350, 480))
        kid_background = self.background.subsurface(kid_rect)
        
        self.windows = []
        self.windows.append(animation.Kid(kid_rect, kid_background, 1))
    
    def draw(self, screen):
        """    
        if self.first:
            # First time blits the entire background
            self.first = False
            screen.blit(self.background, self.rect)
            return [self.rect]
        else:
            # Next blits only the changed areas
            changes = []
            for win in self.windows:
                changes.extend(win.draw(screen))
                
            return changes #[rect.move(self.rect.left, self.rect.top) for rect in changes]
        """   
        
        # Temporal para que se vea bien el menu principal
        screen.blit(self.background, self.rect)
        changes = [self.rect]
        for win in self.windows:
            changes.extend(win.draw(screen))
        return changes     

class MainWindow():
    
    def __init__(self, clock):
        self.name = "main"   
        self.clock = clock
        self.windows = []   # Lista de ventanas que 'componen' la ventana principal
        #self.windows.append(BlinkWindow(pygame.Rect((700, 0), (500, 140)), 5, pygame.Color("red")))
        #self.windows.append(BlinkWindow(pygame.Rect((700, 150), (500, 140)), 5, pygame.Color("blue")))
        #self.windows.append(StatusWindow(pygame.Rect((700, 300), (500, 140)), 2, pygame.Color("gray")))
        self.windows.append(KidWindow(pygame.Rect((0, 0), (600, 500)), 1))
        self.windows.append(animation.Apple(pygame.Rect((150, 500), (150, 172)), 10))
        self.windows.append(menuCreator.load_menu())
        self.windows.append(animation.FPS(pygame.Rect((650, 80), (50, 20)), 15, self.clock))
        self.windows.append(statusBars.BarsWindow((700, 90), 1, pygame.Color("gray")))
        
    def handle_mouse_down(self, (x, y), windows_controller):
        # Temporal para probar el manejo de ventanas entre 'challenges' y 'main'
        #windows_controller.set_active_window("challenges")
        
        # Temporal para probar BarsWindow
        self.windows[-1].on_mouse_click((x,y))
                
    def handle_mouse_over(self, (x, y)):
        None
    
    def get_windows(self):
        return self.windows

