# -*- coding: utf-8 -*-

# Copyright (C) 2011 ceibalJAM! - ceibaljam.org
# This file is part of Saludame.
#
# Saludame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Saludame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Saludame. If not, see <http://www.gnu.org/licenses/>.

import os
from gi.repository import GObject
import pygame

music = {
    "happy": "assets/music/happy.ogg",
    "normal": "assets/music/normal.ogg",
    "sad": "assets/music/sad.ogg",
    "angry": "assets/music/angry.ogg",
    "sick": "assets/music/sick.ogg",
}

instance = None

class SoundManager(GObject.GObject):
    
    IDLE = 0
    PLAYING = 1
    FADE_OUT = 2
    FADE_IN = 3
    
    def __init__(self):

        GObject.GObject.__init__(self)

        global instance
        instance = self
        
        self.current_music_name = ""
        self.next_music_name = ""
        self.state = SoundManager.IDLE
        
        self.volume = 0.3
    
    def set_volume(self, value):
        self.volume = value
        pygame.mixer.music.set_volume(self.volume)
        
    def set_music(self, name):
        if self.state == SoundManager.IDLE:
            self.current_music_name = name
            self.state = SoundManager.PLAYING
            self.start_playing()
            
        if self.state == SoundManager.PLAYING:
            if name <> self.current_music_name:
                self.state = SoundManager.FADE_OUT
                self.next_music_name = name
                pygame.mixer.music.fadeout(1000)
            
        elif self.state == SoundManager.FADE_OUT:
            if name == self.current_music_name:
                self.state = SoundManager.FADE_IN
                self.next_music_name = ""
            else:
                self.next_music_name = name
            
        elif self.state == SoundManager.FADE_IN:
            if name <> self.current_music_name:
                self.state = SoundManager.FADE_OUT
                self.next_music_name = name

    def start_playing(self):
        global music
        
        if self.next_music_name:
            self.current_music_name = self.next_music_name
            self.next_music_name = None
        
        path = music[self.current_music_name]
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
        
        self.state = SoundManager.PLAYING

    # Sounds
    def play_time_change(self):
        pygame.mixer.Sound("assets/sound/time_change.ogg").play()

    def play_event_solved(self):
        pygame.mixer.Sound("assets/sound/challenge_win.ogg").play()
        
    def play_forbidden_action(self):
        pygame.mixer.Sound("assets/sound/alert.ogg").play(2)
    
    def play_popup(self):
        pygame.mixer.Sound("assets/sound/popup.ogg").play()
        