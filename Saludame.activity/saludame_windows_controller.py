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

import pygame
import main_window
import challenges_creator
import customization
import challenges
import gui


class SaludameWindowsController(gui.WindowsController):
    
    def __init__(self, screen, game_manager):
        gui.WindowsController.__init__(self, screen)
        self.game_man = game_manager
        
    def create_windows_and_activate_main(self, app_loader, clock, bars_loader):
        """
        Creates windows and set the main_window as active window
        """
        # Challenges
        cha_creator = challenges_creator.ChallengesCreator(self.screen.get_rect(), pygame.Rect((250, 30), (934, 567)), 1, self, self.game_man, (40, 40, 200))
        cha_creator.create_challenges()
        self.game_man.challenges_creator = cha_creator
        
        slide_window = challenges.Slide(self.screen.get_rect(), self.screen.get_rect(), 1, self)
        
        info_master_challenge = challenges.InfoChallenge(self.screen.get_rect(), pygame.Rect((250, 30), (934, 567)), 1, self, cha_creator, u"¡Felicitaciones! \nHas completado el nivel actual. Para pasar de nivel \ndebes contestar bien la siguiente pregunta. \n\n¡¡Suerte!!", u"Felicitaciones, has pasado de nivel. \nSe han desbloqueado nuevas acciones, \n¿te animás a encontrarlas?", u"Contestaste incorrectamente, \ntendrás que intentar pasar de nivel más adelante")
        
        # Customization Window
        customization_window = customization.CustomizationWindow(self.screen.get_rect(), pygame.Rect((250, 30), (934, 567)), 1, self, app_loader.get_character())
        
        # Main Window
        main_win = main_window.MainWindow(self.screen.get_rect(), self.screen.get_rect(), 1, clock, self, cha_creator, bars_loader, self.game_man)
        self.main_window = main_win
        
        # Activate Main window
        self.set_active_window("main_window")
        self.update(0)
        self.reload_main = True
        
        # Activate Customization over main window
        self.set_active_window("customization_window")
    
    # BACKGROUND
    def set_environment(self, environment, time):       
        self.windows["kid"].set_environment(environment, time)
        self.windows["panel_window"].set_weather()
    
    # CLOTHES
    def update_clothes(self):
        self.windows["kid"].update_clothes()
        self.windows["panel_window"].set_weather()
    
    # Actions
    def show_action_animation(self, action):
        """
        Display an action animation at panel and kid window
        """
        self.windows["panel_window"].play_action_animation(action)
        self.windows["kid"].play_action_animation(action)
        
    def stop_current_action_animation(self):
        self.windows["panel_window"].stop_action_animation()
        self.windows["kid"].stop_action_animation()
        
    # Events
    def add_personal_event(self, event):
        self.windows["panel_window"].add_personal_event(event)
        
        if event.kid_message:
            self.show_kid_message(event.kid_message, event.message_time_span)
    
    def remove_personal_event(self, event):
        self.windows["panel_window"].remove_personal_event(event)
        
    def add_social_event(self, event):
        self.windows["panel_window"].add_social_event(event)
        
        if event.person_path:
            self.windows["kid"].add_social_event(event)
        
    def remove_social_event(self, event):
        self.windows["panel_window"].remove_social_event(event)
    
    # Messages at ballon
    def show_kid_message(self, message, message_time_span):
        self.windows["kid"].show_kid_balloon(message, message_time_span)
    
    # Moods
    def set_mood(self, mood):
        if self.windows:
            self.windows["kid"].set_mood(mood)
