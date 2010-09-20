# -*- coding: utf-8 -*-

import pygame
import os

BLACK = pygame.Color("black")

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
        self.bars.append(IdleStatusBar(pygame.Rect(20, 15, 260, 30), pygame.Color("green")))
        self.bars.append(IdleStatusBar(pygame.Rect(20, 55, 260, 30), pygame.Color("blue"), 35))
        self.bars.append(IdleStatusBar(pygame.Rect(20, 95, 260, 30), pygame.Color("yellow"), 65))
        
    def draw(self, screen):
        self.surface.fill(self.background_color)
        
        for bar in self.bars:
            bar.draw(self.surface)
            
            screen.blit(self.surface, self.rect)
            
        return [self.rect]


class StatusBar:
    
    def __init__(self, rect, color, value = 0):
        self.rect = rect
        self.color = color
        self.surface = pygame.Surface(rect.size)
        self.value = value


class IdleStatusBar(StatusBar):
    
    def __init__(self, rect, color, value = 0):
        StatusBar.__init__(self, rect, color, value)
        
    def draw(self, screen):
        self.value = (self.value + 1) % 101
        factor = self.value / 100.0
        
        rect = pygame.Rect((0,0), self.rect.size)
        rect.width *= factor
        
        self.surface.fill(BLACK)
        self.surface.fill(self.color, rect)
        screen.blit(self.surface, self.rect)
        
        return [self.rect]

import animation

BACKGROUND_PATH = os.path.normpath("assets/background/background.png")

class MainWindow(Window):

    def __init__(self, rect, frame_rate):
        Window.__init__(self, rect, frame_rate, BLACK)
        
        self.first = True
        
        self.background = pygame.image.load(BACKGROUND_PATH).convert()
        
        kid_rect = pygame.Rect((100, 20),(350,480))
        kid_background = self.background.subsurface(kid_rect)
        
        self.windows = []
        self.windows.append(animation.Kid(kid_rect, kid_background, 1))
    
    def draw(self, screen):
        
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
