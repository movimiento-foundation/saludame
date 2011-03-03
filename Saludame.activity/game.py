# -*- coding: utf-8 -*-

from game_manager import GameManager
import pygame
import logging
import hotkeys


if __name__ == "__main__":
    import gettext
    gettext.textdomain("org.ceibaljam.Saludame")
    gettext.bindtextdomain("org.ceibaljam.Saludame", "locale/")
    
    gettextold = gettext.gettext
    def _(string):
        string = gettextold(string)
        if isinstance(string, unicode):
            return string.upper()
        else:
            return unicode(string.decode("utf-8")).upper()
    gettext.gettext = _

from gettext import gettext as _
import os

log = logging.getLogger('saludame')
log.setLevel(logging.DEBUG)

# Variables globales
MAX_FPS = 16            # Max frames per second
SLEEP_TIMEOUT = 30      # Seconds until the PauseScreen if no events show up
pause = False
running = True

main_class = None

def set_library_function(link):
    print library

class Main():
    def __init__(self):
        self.windows_controller = None
        global main_class
        main_class = self
    
    def main(self, from_sugar):
        """Main function of the game.
        
        This function initializes the game and enters the PyGame main loop.
        """
        global running, pauses
        
        if from_sugar:
            import gtk

        import app_init
        import challenges_creator
        import customization
        import sound_manager
        import saludame_windows_controller
        
        # Optimizes sound quality and buffer for quick loading
        pygame.mixer.quit()     # When executting from sugar pygame it's already initialized
        pygame.mixer.pre_init(22050, -16, 1, 512)
        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        # Inits PyGame module
        pygame.init()
        
        if not from_sugar:
            target_size = (1000, 650) #(1200, 800)  # In regular computers the native resolution is too high (5/6)
            screen = pygame.display.set_mode(target_size)
        
        screen = pygame.display.get_surface()
        assert screen, "No screen"
        
        pygame.display.update()
        
        # This clock is used to keep the game at the desired FPS.
        clock = pygame.time.Clock()
        
        # windows_controller asociado al screen
        self.windows_controller = saludame_windows_controller.SaludameWindowsController(screen, None)
        
        # Initialize sound_manager, game_manager, character, actions and menu.
        sound_manager.SoundManager()
        
        app_loader = app_init.AppLoader(self.windows_controller)
        bars_loader = app_loader.get_status_bars_loader()
        game_man = app_loader.get_game_manager()
        
        self.hotkeys_handler = hotkeys.HotKeyHandler()
        self.windows_controller.game_man = game_man
        self.windows_controller.create_windows_and_activate_main(app_loader, clock, bars_loader)

        game_man.load_game()
          
        frames = 0
        
        # Main loop
        update = True # The first time the screen need to be updated
        
        while running:
            
            if from_sugar:
                # Pump GTK messages.
                while gtk.events_pending():
                    block = pause
                    gtk.main_iteration(block)
            
            if not pause:
                # Waits for events, if none the game pauses:
                # http://wiki.laptop.org/go/Game_development_HOWTO#Reducing_CPU_Load
                milliseconds = clock.tick(MAX_FPS) # waits if the game is running faster than MAX_FPS
                
                events = pygame.event.get()
                
                if events:
                    for event in events:
                        if event.type == pygame.QUIT:
                            running = False
                            game_man.save_game()
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not from_sugar:
                            running = False
                            game_man.save_game()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.windows_controller.handle_mouse_down(pygame.mouse.get_pos())
                        elif event.type == pygame.MOUSEBUTTONUP:
                            self.windows_controller.handle_mouse_up(event.pos)
                        elif event.type == pygame.MOUSEMOTION:
                            self.windows_controller.handle_mouse_motion(event.pos)
                        elif event.type == pygame.VIDEOEXPOSE:
                            self.windows_controller.reload_main = True
                        elif event.type == pygame.USEREVENT and event.code == 0: # Music ended
                            sound_manager.instance.start_playing()
                        elif event.type == pygame.KEYDOWN:
                            self.hotkeys_handler.handle_keydown(event)
                        elif event.type == pygame.KEYUP:
                            self.hotkeys_handler.handle_keyup(event)
                            
                            
                self.windows_controller.handle_mouse_over(pygame.mouse.get_pos())
                
                self.windows_controller.update(frames)
        
                frames += 1

                game_man.signal()
                
        # Una vez que sale del loop manda la senal de quit para que cierre la ventana
        pygame.quit()

if __name__ == "__main__":
    Main().main(False)
