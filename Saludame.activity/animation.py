# -*- coding: utf-8 -*-

import pygame
import os
import utilities
import gui

COLORS_HAIR = (pygame.Color("#00ffff"), pygame.Color("#009f9f"))
COLORS_SKIN = (pygame.Color("#ffccc7"), pygame.Color("#cba5a0"))
COLORS_SWEATER = (pygame.Color("#00d69f"), pygame.Color("#00b07e"))
COLORS_PANTS = (pygame.Color("#ff9900"), pygame.Color("#d37e00"), pygame.Color("#b06800"), pygame.Color("#d47f00"))
COLORS_SHOES = (pygame.Color("#eeea00"), pygame.Color("#98a600"))

COLORS_TO_MAP = map(utilities.get_color_tuple, COLORS_HAIR + COLORS_SKIN + COLORS_SWEATER + COLORS_PANTS + COLORS_SHOES)
PARENTS_COLORS_TO_MAP = map(utilities.get_color_tuple, COLORS_HAIR + COLORS_SKIN)

GRAY = pygame.Color("gray")
BLACK = pygame.Color("black")
BLUE = pygame.Color("blue")
WHITE = pygame.Color("white")

class Kid(gui.Widget):
    
    def __init__(self, container, rect, frame_rate, windows_controller, game_man, mood):
        gui.Widget.__init__(self, container, rect, frame_rate, windows_controller)
        
        self.character = game_man.character
        
        self.moods = game_man.moods_list
        
        self.mood_index = 9 # Default mood_index (normal)
        self.mood = self.moods[9] # Default mood (normal)
        
        self.action_index = -1 # Default action_index (no-action)
        self.action = None
        
        self.sprite = None
        self.set_animation()
        
        self.visible = True
        
    ##### Moods #####
    def change_mood(self):
        self.mood_index += 1
        if self.mood_index == len(self.moods):
            self.mood_index = 0
        self.mood = self.moods[self.mood_index]
        self.index = 0
        
    def set_mood(self, mood):
        self.mood_index = self.moods.index(mood)
        self.mood = self.moods[self.mood_index]
        self.set_animation()
        
    ##### Clothes ####
    def update_clothes(self):
        self.set_animation()
        
    ##### Actions #####
    def play_action_animation(self, action):
        self.action = action
        self.set_animation()
        
    def stop_action_animation(self):
        self.action = None
        self.set_animation()
    
    def set_animation(self):
        sex = self.character.sex
        clothes = self.character.clothes
        
        self.loops = 0
        self.sound_loops = 0
        self.visible = True
        self.index = 0 # Sequence number of the current animation
        if self.action and self.action.kid_animation_path: # An action with animation is enabled
            directory = "%s/%s/%s" % (self.action.kid_animation_path, sex, clothes)
            self.file_list = get_image_list(directory)
        else:
            directory = "%s/%s/%s" % (self.mood.kid_animation_path, sex, clothes)
            self.file_list = get_image_list(directory)

    ##### update #####
    def update(self, frames):
        filename = self.file_list[self.index]
        self.sprite = load_animation(self.sprite, filename)
        
        self.background = self.sprite.copy()
        maps = self.character.mappings
        self.change_color(COLORS_TO_MAP, maps["hair"] + maps["skin"] + maps["sweater"] + maps["pants"] + maps["shoes"])
        
        self.index += 1
        if self.index >= len(self.file_list):
            self.index = 0
            self.loops += 1
            if self.action and self.action.kid_loop_times > 0 and self.loops == self.action.kid_loop_times:
                self.visible = False
        
        if self.action and self.action.sound_path:
            self.play_sound()

        self.set_dirty()
    
    def play_sound(self):
        if self.sound_loops == self.loops:
            if isinstance(self.action.sound_path, list):
                if len(self.action.sound_path) > self.sound_loops:
                    pygame.mixer.Sound(self.action.sound_path[self.sound_loops]).play()
            else:
                pygame.mixer.Sound(self.action.sound_path).play()
            self.sound_loops += 1
        
    def draw(self, frames):
        if self.visible:
            return gui.Widget.draw(self, frames)
        else:
            return self.rect_absolute
        
    ##### Colors #####
    def change_color(self, old, new):
        index = 0
        for old_color in old:
            new_color = new[index]
            utilities.change_color(self.background, old_color, new_color)
            
            index += 1
            
class ActionAnimation(gui.Button):
    """
    An action animation to show at panel
    """
    def __init__(self, container, rect, frame_rate, animation_path):
        gui.Button.__init__(self, container, rect, frame_rate, None)
        
        self.center_in_rect = True
        
        self.path = animation_path
        self.frame_rate = frame_rate
        
        dirList = os.listdir(animation_path)
        dirList.sort()
        self.file_list = [os.path.join(animation_path, fname) for fname in dirList if '.png' in fname]
        
        self.index = 0
        
    def update(self, frames):
        if frames % self.frame_rate == 0:
            filename = self.file_list[self.index]
            self.background = pygame.image.load(filename)
            self.index = (self.index + 1) % len(self.file_list)
            self.set_dirty()
            
class FPS(gui.Widget):
    def __init__(self, container, rect, frame_rate, clock):
        
        gui.Widget.__init__(self, container, rect, frame_rate)
        
        self.clock = clock
        
        self.font = pygame.font.Font(None, 16)
    
    def draw(self, screen):
        screen.fill(BLACK, self.rect_absolute)
        text = str(round(self.clock.get_fps()))
        text_surf = self.font.render(text, False, (255, 255, 255))
        screen.blit(text_surf, self.rect_absolute)
        return self.rect_absolute

def get_image_list(directory):
    dirList = os.listdir(directory)
    dirList.sort()
    return [os.path.join(directory, fname) for fname in dirList if fname.endswith('.png') or fname.endswith('.diff.gz') or fname.endswith('.diff.zlib')]


import zlib
import imagepatch
def load_animation(last_image, new_filename):
    if new_filename.endswith('.png'):
        new = pygame.image.load(new_filename)
        
    elif new_filename.endswith('.diff.zlib'):
        f = open(new_filename, 'r')
        diff = zlib.decompress(f.read())
        f.close()
        
        new_buffer = imagepatch.patch(last_image.get_buffer().raw, diff)
        
        new = last_image                        # both point to the same surface
        new.get_buffer().write(new_buffer, 0)   # Instead of using a copy modifies the same surface
        
    return new
    