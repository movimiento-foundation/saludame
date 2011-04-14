# -*- coding: utf-8 -*-

import pygame

music = {
    "happy": "assets/music/happy.ogg",
    "normal": "assets/music/normal.ogg",
    "sad": "assets/music/sad.ogg",
    "angry": "assets/music/angry.ogg",
    "sick": "assets/music/sick.ogg",
}

instance = None

class SoundManager:
    
    IDLE = 0
    PLAYING = 1
    FADE_OUT = 2
    FADE_IN = 3
    
    def __init__(self):
        global instance
        instance = self
        
        self.current_music_name = ""
        self.next_music_name = ""
        self.state = SoundManager.IDLE
        
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
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play()

    # Sounds
    def play_time_change(self):
        pygame.mixer.Sound("assets/sound/time_change.ogg").play()

    def play_event_solved(self):
        pygame.mixer.Sound("assets/sound/challenge_win.ogg").play()
        