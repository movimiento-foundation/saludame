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

log = logging.getLogger('saludame')
log.setLevel(logging.DEBUG)

# Variables globales
MAX_FPS = 16            # Max frames per second
SLEEP_TIMEOUT = 30      # Seconds until the PauseScreen if no events show up

INSTANCE_FILE_PATH = "game.save"        # File to save the game in standalone mode

pause = False
running = True

main_class = None

def set_library_function(link, anchor=None):
    if anchor:
        print link + "#" + anchor
    else:
        print link

def set_library_event(anchor):
    set_library_function("90-Eventos-avanzado.html", anchor)

class Main():
    
    def __init__(self, target_size=(1200, 780)):
        self.windows_controller = None
        global main_class
        main_class = self
        self.gender = "boy"
        self.name = ""
        self.started = False
        self.target_size = target_size
        self.loaded_game = None
    
    def main(self, from_sugar):
        self.init(from_sugar)
        self.run(from_sugar, self.gender, self.name)
        
    def init(self, from_sugar):
        # Optimizes sound quality and buffer for quick loading
        pygame.mixer.quit()     # When executting from sugar pygame it's already initialized
        pygame.mixer.pre_init(22050, -16, 1, 512)
        
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        
        # Inits PyGame module
        pygame.init()
        
        if not from_sugar:
            screen = pygame.display.set_mode(self.target_size)
        
        screen = pygame.display.get_surface()
        assert screen, "No screen"
        
        screen.blit(pygame.image.load("assets/slides/screen_loading.jpg"), (0,0))
        pygame.display.flip()
        
    def run(self, from_sugar, gender, name):
        """Main function of the game.
        
        This function initializes the game and enters the PyGame main loop.
        """
        global running, pauses
        
        self.started = True
        
        if from_sugar:
            import gtk

        import app_init
        import customization
        import sound_manager
        import saludame_windows_controller
        
        screen = pygame.display.get_surface()
        
        # This clock is used to keep the game at the desired FPS.
        clock = pygame.time.Clock()
        
        # Initialize sound_manager, game_manager, character, actions and menu.
        sound_manager.SoundManager()
        
        app_loader = app_init.AppLoader(gender, name)
        bars_loader = app_loader.get_status_bars_loader()
        self.game_man = app_loader.get_game_manager()
        if from_sugar:
            if self.loaded_game:
                self.game_man.parse_game(self.loaded_game)
        else:
            self.load_game()
        
        # windows_controller asociado al screen
        self.windows_controller = saludame_windows_controller.SaludameWindowsController(screen, self.game_man)        
        self.windows_controller.create_windows_and_activate_main(app_loader, clock, bars_loader)
        self.hotkeys_handler = hotkeys.HotKeyHandler()
        
        self.game_man.start(self.windows_controller)
        
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
                            if not from_sugar:
                                self.save_game()
                                
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not from_sugar:
                            running = False
                            self.save_game()
                            
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

                self.game_man.signal()
                
        # Una vez que sale del loop manda la senal de quit para que cierre la ventana
        pygame.quit()


    def save_game(self, path=INSTANCE_FILE_PATH):
        """
        Save the game instance
        """
        print "saving game"
        data = self.game_man.serialize()
        
        try:
            f = open(path, 'w')
            f.write(data)
        finally:
            f.close()
        
    def load_game(self, path=INSTANCE_FILE_PATH):
        """ loads the game from a string """
        try:
            f = open(path)
            data = f.read()
            self.game_man.parse_game(data)
            f.close()
        except:
            print "Error al cargar la partida"
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] in ["boy", "girl"]:
        gender = sys.argv[1]
    else:
        gender = "boy"
    
    if len(sys.argv) > 1 and "full" in sys.argv[1:]:
        m = Main()
    else:
        # In regular computers the native resolution is too high (5/6)
        m = Main((1000, 650))
    
    m.gender = gender
    m.name = ""
    m.main(False)
