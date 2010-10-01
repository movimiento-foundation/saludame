# -*- coding: utf-8 -*-

import pygame
import logging
from gettext import gettext as _

from utilities import *

from windows_controller import *
import window
import challenges
import customization

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
        self.windows_controller = WindowsController()
    
    def main(self, fromSugar):
        """Main function of the game.
        
        This function initializes the game and enters the PyGame main loop.
        """
        
        if fromSugar:
                import gtk
    
        # Optimizes sound quality and buffer for quick loading
        pygame.mixer.pre_init(22050, -16, 8, 256)
        
        # Inits PyGame module
        pygame.init()
        
        target_size = (1200, 780)
        
        if not fromSugar:
            screen = pygame.display.set_mode(target_size)
        
        screen = pygame.display.get_surface()
        assert screen, "No screen"
        
        pygame.display.update()  
      
        # This clock is used to keep the game at the desired FPS.
        clock = pygame.time.Clock()
        

        # Challenges Window
        challenges_window = challenges.MultipleChoice(pygame.Rect((200, 150), (800, 400)), 1, (100,45,255), screen, self.windows_controller)
        self.windows_controller.add_new_window(challenges_window, "challenges")

        """
        # Customization Window
        customization_window = customization.CustomizationWindow(pygame.Rect((200, 100), (800, 500)), 1, pygame.Color("Gray"), screen)
        self.windows_controller.add_new_window(customization_window, "customization")
        """
        
        # Main Window
        main_window = (window.MainWindow(screen.get_rect(), 1, clock, screen, self.windows_controller))
        self.windows_controller.add_new_window(main_window, "main")  
        
        # Activamos ventana principal
        self.windows_controller.set_active_window("main")    
          
        frames = 0
        
        # Main loop
        update = True # The first time the screen need to be updated
        running = True
        
        while running:
            
            if fromSugar:
                # Pump GTK messages.
                while gtk.events_pending():
                    gtk.main_iteration()
    
            # Waits for events, if none the game pauses:
            # http://wiki.laptop.org/go/Game_development_HOWTO#Reducing_CPU_Load
            milliseconds = clock.tick(MAX_FPS) # waits if the game is running faster than MAX_FPS
            
            events = pygame.event.get()        
            
            if not pause:
                
                if events:
                    for event in events:
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.windows_controller.handle_mouse_down(pygame.mouse.get_pos())
                            
                self.windows_controller.handle_mouse_over(pygame.mouse.get_pos())
                
                self.windows_controller.update(frames, screen)
        
                frames += 1
        
        # Una vez que sale del loop manda la senal de quit para que cierre la ventana
        pygame.quit()

if __name__ == "__main__":
    Main().main(False)
