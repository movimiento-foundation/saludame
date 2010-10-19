# -*- coding: utf-8 -*-

import pygame
import logging
from gettext import gettext as _
import animation
from utilities import *

from windows_controller import *
import window
import main_window
import customization
import app_init
import challenges_loader
import os

log = logging.getLogger('saludame')
log.setLevel(logging.DEBUG)

"""
Variables globales
"""
MAX_FPS = 18            # Max frames per second
SLEEP_TIMEOUT = 30      # Seconds until the PauseScreen if no events show up
pause = False

class Main():
    def __init__(self):
        self.windows_controller = None
    
    def main(self, from_sugar):
        """Main function of the game.
        
        This function initializes the game and enters the PyGame main loop.
        """
        
        if from_sugar:
                import gtk
    
        """
        Initialize game character, actions and menu.
        """
        app_loader = app_init.AppLoader()
        
        character = app_loader.get_character()
        
        
        
        """
        ***********
        """
        # Optimizes sound quality and buffer for quick loading
        pygame.mixer.pre_init(22050, -16, 8, 256)
        
        # Inits PyGame module
        pygame.init()
        
        if not from_sugar:
            target_size = (1000, 650)   # In regular computers the native resolution is too high (5/6)
            screen = pygame.display.set_mode(target_size)
        
        screen = pygame.display.get_surface()
        assert screen, "No screen"
        
        pygame.display.update()  
      
        # This clock is used to keep the game at the desired FPS.
        clock = pygame.time.Clock()
        
        # windows_controller asociado al screen
        self.windows_controller = WindowsController(screen)        

        # Challenges
        cha_loader = challenges_loader.ChallengesLoader(screen.get_rect(), pygame.Rect((200, 150), (800, 400)), 1, self.windows_controller, (100, 40, 200))
        cha_loader.load_challenge("Question 1", ["Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5"], 0, os.path.normpath("assets/challenges/francia.jpg"))
        cha_loader.load_challenge("Question 2", ["Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5", "Answer 6", "Answer 7"], 0, os.path.normpath("assets/challenges/francia.jpg"))
        cha_loader.load_challenge("Question 3", ["Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5"], 0, os.path.normpath("assets/challenges/francia.jpg"))
        cha_loader.load_challenge("Question 4", ["Answer 1", "Answer 2", "Answer 3"], 0, os.path.normpath("assets/challenges/francia.jpg"))

        # Customization Window
        customization_window = customization.CustomizationWindow(screen.get_rect(), pygame.Rect((200, 100), (800, 500)), 1, self.windows_controller, pygame.Color("Gray"))
        self.windows_controller.add_new_window(customization_window, "customization")
        
        # Main Window
        main_win = main_window.MainWindow(screen.get_rect(), screen.get_rect(), 1, clock, self.windows_controller, cha_loader)
        self.windows_controller.add_new_window(main_win, "main")

        # Probando ActionWindow
        main_win.action_win.play_animation('eat_apple')
        
        # Activamos ventana principal
        self.windows_controller.set_active_window("main")  
          
        frames = 0
        
        # Main loop
        update = True # The first time the screen need to be updated
        running = True
        
        while running:
            
            if from_sugar:
                # Pump GTK messages.
                while gtk.events_pending():
                    gtk.main_iteration()
    
            if not pause:
                # Waits for events, if none the game pauses:
                # http://wiki.laptop.org/go/Game_development_HOWTO#Reducing_CPU_Load
                milliseconds = clock.tick(MAX_FPS) # waits if the game is running faster than MAX_FPS
                
                events = pygame.event.get()
                
                if events:
                    for event in events:
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not from_sugar:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.windows_controller.handle_mouse_down(pygame.mouse.get_pos())
                            
                self.windows_controller.handle_mouse_over(pygame.mouse.get_pos())
                
                self.windows_controller.update(frames)
        
                frames += 1
        
        # Una vez que sale del loop manda la senal de quit para que cierre la ventana
        pygame.quit()

if __name__ == "__main__":
    Main().main(False)
