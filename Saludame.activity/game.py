# -*- coding: utf-8 -*-

import pygame
import logging
from gettext import gettext as _

import window
import challenges

log = logging.getLogger('saludame')
log.setLevel(logging.DEBUG)

"""
Variables globales
"""
MAX_FPS = 18            # Max frames per second
SLEEP_TIMEOUT = 30      # Seconds until the PauseScreen if no events show up

def main(fromSugar):
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
  
    # Stack de ventanas para el control de venta activa    
    windows_stack = []
    
    # Challenges Window
    windows_stack.append(challenges.MultipleChoice(pygame.Rect((200, 150), (800, 400)), 1))
    # Main Window
    windows_stack.append(window.MainWindow(clock))    
    
    frames = 0
    
    # Main loop
    update = True       # The first time the screen need to be updated
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
        
        if events:
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    windows_stack[-1].handle_mouse_down(pygame.mouse.get_pos()) # Solo le pasamos los eventos a la ventana activa
                    
        windows_stack[-1].handle_mouse_over(pygame.mouse.get_pos()) # Solo le pasamos los eventos a la ventana activa
        
        changes = []
        for win in windows_stack[-1].get_windows(): # Solo actualizamos la ventana activa
            if frames % win.frame_rate == 0:
                changes.extend(win.draw(screen))
          
        if changes:
            pygame.display.update(changes)
            update = False

        frames += 1
        
    # Una vez que sale del loop manda la senal de quit para que cierre la ventana
    pygame.quit()
    
if __name__ == "__main__":
    main(False)
