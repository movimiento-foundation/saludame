# -*- coding: utf-8 -*-

import pygame
from window import Window
import sys
from utilities import Text, TextBlock

import challenges_creator
import customization
import main_window
import challenges

"""
Clase encargada del control de ventanas
"""
class WindowsController:
    
    def __init__(self, screen, game_manager):
        
        #game manager
        self.game_man = game_manager
        
        internal_size = 1200, 780       # The game is meant to run in this resolution
        self.scaled_game = ScaledGame(screen, internal_size)
        
        self.screen = self.scaled_game.get_internal_screen()
        
        self.windows = {} # Diccionario de ventanas. Aca se encuentran todas las ventanas del programa
        self.windows_stack = [] # Stack de ventanas para el control de venta activa. Aca se enceuntra el stack de ventanas abiertas
        self.reload_main = True
        
        self.next_update_list = []
        
        # Tooltips
        self.showing_tooltip = False
        self.active_tooltip_bg = None
        self.active_tooltip = None
        
    def create_windows_and_activate_main(self, app_loader, clock, bars_loader):
        """
        Creates windows and set the main_window as active window
        """
        # Challenges
        cha_creator = challenges_creator.ChallengesCreator(self.screen.get_rect(), pygame.Rect((250, 30), (934, 567)), 1, self, self.game_man, (40, 40, 200))
        cha_creator.create_challenges()
        self.game_man.challenges_creator = cha_creator
        
        info_master_challenge = challenges.InfoMasterChallenge(self.screen.get_rect(), pygame.Rect((250, 30), (934, 567)), 1, self, cha_creator, u"¡Felicitaciones! \nHas completado el nivel actual. Para pasar de nivel \ndebes contestar bien la siguiente pregunta. \n\n¡¡Suerte!!", u"Felicitaciones, has pasado de nivel. \nSe han desbloqueado nuevas acciones, \n¿te animás a encontrarlas?", u"Contestaste incorrectamente, \ntendrás que intentar pasar de nivel más adelante")
        
        # Customization Window
        customization_window = customization.CustomizationWindow(self.screen.get_rect(), pygame.Rect((250, 30), (934, 567)), 1, self, app_loader.get_character())
        
        # Main Window
        main_win = main_window.MainWindow(self.screen.get_rect(), self.screen.get_rect(), 1, clock, self, cha_creator, bars_loader, self.game_man)
        
        # Activate Main window
        self.set_active_window("main_window")
        self.update(0)
        
        # Activate Customization over main window
        #self.set_active_window("customization_window")
    
    ##### Windows #####    
    def close_active_window(self):
        self.windows_stack[-1].repaint = True
        # Solo puede ser llamado por la ventana activa e implica
        # hacer un pop del stack
        self.windows_stack.pop()  
        
        self.show_window_hierarchy(self.windows_stack[-1])
               
        if (self.windows_stack[-1].get_register_id() == "main_window"):
            self.game_man.continue_game()
            self.reload_main = True 
            for win in self.windows_stack[-1].windows:
                if isinstance(win, Window):
                    win.enable_repaint()
    
    def set_active_window(self, window_key):
        if window_key <> "main_window":
            self.game_man.pause_game()
        
        self.windows_stack.append(self.windows[window_key])        
        self.show_window_hierarchy(self.windows_stack[-1])     
        
    def register_new_window(self, id, window):
        self.windows[id] = window
        
    def show_master_challenge_intro(self):
        self.set_active_window("info_master_challenge")
        self.windows["info_master_challenge"].show_intro()
        
    def show_master_challenge_result_good(self):
        self.set_active_window("info_master_challenge")
        self.windows["info_master_challenge"].show_result_good()
        
    def show_master_challenge_result_bad(self):
        self.set_active_window("info_master_challenge")
        self.windows["info_master_challenge"].show_result_bad()    
        
    def show_window_hierarchy(self, window):
        sys.stdout.write(window.get_register_id())
        W = []
        for win in window.windows:
            W.append(win.register_id)
        print(" (%s)" % (W))    
        
    ##### BACKGROUND #####
    
    def set_environment(self, environment):
        self.windows["kid"].set_environment(environment) 
        
    ##### CLOTHES #####
    
    def update_clothes(self):
        self.windows["kid"].update_clothes() 
    
    ##### Actions #####
    def show_action_animation(self, action):
        """
        Display an action animation at panel and kid window
        """
        self.windows["panel_window"].play_action_animation(action)
        self.windows["kid"].play_action_animation(action)
        
    def stop_actual_action_animation(self):
        self.windows["panel_window"].stop_action_animation() 
        self.windows["kid"].stop_action_animation()
    
    ##### Events #####      
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
    
    ##### Messages at ballon #####
    def show_kid_message(self, message, message_time_span):
        print "mostrar mensaje: ", message, " durante: ", message_time_span
        self.windows["kid"].show_kid_balloon(message, message_time_span)
    
    ##### Moods #####    
    def set_mood(self, mood):
        if self.windows:
            self.windows["kid"].set_mood(mood)               
    
    #### Events handlers ####    
    def handle_mouse_down(self, (x, y)):
        x, y = self.scaled_game.scale_coordinates((x, y))
        self.windows_stack[-1].handle_mouse_down((x, y))
                
    def handle_mouse_over(self, (x, y)):
        x, y = self.scaled_game.scale_coordinates((x, y))
        self.windows_stack[-1].handle_mouse_over((x, y))
    ##########################
    
    #### Tooltips #####    
    def show_tooltip(self, tooltip):
        x, y = self.scaled_game.scale_coordinates(pygame.mouse.get_pos())
        self.active_tooltip = Text(self.screen.get_rect(), x, y, 1, tooltip, 18, pygame.Color('red'))
        
        # Necesitamos guardar lo que esta atras del tooltip para cuando lo querramos esconder
        self.active_tooltip_bg = (self.screen.subsurface(self.active_tooltip.rect_absolute).copy(), self.active_tooltip.rect_absolute) 
        self.showing_tooltip = True
        
    def show_super_tooltip(self, tooltip):
        x, y = self.scaled_game.scale_coordinates(pygame.mouse.get_pos())
        self.active_tooltip = TextBlock(self.screen.get_rect(), x, y, 1, tooltip, 18, pygame.Color('red'))
        
        self.active_tooltip_bg = (self.screen.subsurface(self.active_tooltip.rect_absolute).copy(), self.active_tooltip.rect_absolute) 
        self.showing_tooltip = True
    
    def hide_active_tooltip(self):
        # Solo se ejecuta si se esta mostrando algun tooltip en la pantalla
        if self.showing_tooltip:
            # Hacemos un blit con lo que tenia atras el tooltip
            self.screen.blit(self.active_tooltip_bg[0], self.active_tooltip_bg[1])
            # Lo guardamos en la lista de las proximas actualizaciones 
            self.next_update(self.active_tooltip_bg[1])      
            self.showing_tooltip = False
    ###################
    
    def next_update(self, rect):
        """
        Add a rect that must be updated at next update
        """
        self.next_update_list.append(rect)
    
    def update(self, frames):
        """
        Updates GUI 
        """    
        # Cada vez que "volvamos" a la ventana principal es necesario
        # repintar el fondo para que no queden rastros de la ventana anterior
        if self.reload_main:
            pygame.display.flip() # Actualizamos el screen para hacer visibles los efectos
            self.reload_main = False       
        
        changes = []
        if frames % self.windows_stack[-1].frame_rate == 0:
            changes.extend(self.windows_stack[-1].draw(self.screen, frames))   
        
        if changes:
            if self.next_update_list:
                changes.extend(self.next_update_list)
                self.next_update_list = [] # Vaciamos la lista
        
        # Tooltips        
        if self.showing_tooltip:
            if isinstance(self.active_tooltip, Text):
                self.screen.fill((255, 255, 255), self.active_tooltip.rect_in_container)
            # Le decimos al tooltip (widget) que se dibuje
            self.active_tooltip.draw(self.screen)
            changes.append(self.active_tooltip_bg[1])
        
        self.scaled_game.update_screen(changes)
        #self.scaled_game.flip()


class ScaledGame:
    
    def __init__(self, pygame_screen, internal_size):
        self.screen = pygame_screen

        pygame_screen_size = pygame_screen.get_size()
        self.scale_factor = pygame_screen_size[0] / float(internal_size[0]), pygame_screen_size[1] / float(internal_size[1])
        
        if self.scale_factor == (1, 1):
            self.internal_screen = self.screen
        else:
            self.internal_screen = pygame.Surface(internal_size)
        
        
    def get_internal_screen(self):
        """ Returns the screen where everything should be drawn.
        If using scalation its a virtual surface if not is the real display surface.
        """
        return self.internal_screen
    
    def flip(self):
        if self.scale_factor == (1, 1):
            pygame.display.flip()
        else:
            pygame.transform.scale(self.internal_screen, self.screen.get_size(), self.screen)
            pygame.display.flip()
        
    def update_screen(self, rect_list):
        if self.scale_factor == (1, 1):
            pygame.display.update(rect_list)
        else:
            pygame.transform.scale(self.internal_screen, self.screen.get_size(), self.screen)
            pygame.display.update(self.scale_rect_list(rect_list))
    
    def scale_rect_list(self, rect_list):
        return [self.scale_rect(rect) for rect in rect_list if rect]
    
    def scale_rect(self, rect):
        if rect:
            left = int(rect.left * self.scale_factor[0])
            top = int(rect.top * self.scale_factor[1])
            width = int(rect.width * self.scale_factor[0])
            height = int(rect.height * self.scale_factor[1])
            return pygame.Rect(left, top, width, height)
        else:
            return None
    
    def scale_coordinates(self, display_coordinates):
        """ Retruns the internal coordinates corresponding to the display coordinates """
        if self.scale_factor == (1, 1):
            return display_coordinates
        else:
            x = int(display_coordinates[0] / self.scale_factor[0])
            y = int(display_coordinates[1] / self.scale_factor[0])
            return x, y

