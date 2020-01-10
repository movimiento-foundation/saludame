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
import logging
from hotkeys import HotKeyHandler
from app_init import AppLoader
from sound_manager import SoundManager
from saludame_windows_controller import SaludameWindowsController


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
MAX_FPS = 15            # Max frames per second
SLEEP_TIMEOUT = 30      # Seconds until the PauseScreen if no events show up

D = os.path.join(os.environ["HOME"], ".Saludame")
if not os.path.exists(D):
    os.mkdir(D)
INSTANCE_FILE_PATH = os.path.join(D, "game.save")        # File to save the game in standalone mode



def set_library_function(link, anchor=None):
    if anchor:
        print link + "#" + anchor
    else:
        print link


def set_library_event(anchor):
    set_library_function("90-Eventos-avanzado.html", anchor)


def set_library_full_link(link):
    parts = link.split(u"#")
    link = parts[0]
    anchor = None
    if len(parts) > 1:
        anchor = parts[1]    
    set_library_function(link, anchor)


class Main(GObject.GObject):
    
    def __init__(self, target_size=(800, 600)):

        GObject.GObject.__init__(self)

        self.__target_size = target_size
        
        self.gender = "boy"
        self.name = ""

        self.__screen = None
        self.__clock = None
        self.__game_over_callback = None
        self.__game_man = None
        self.__sound_manager = None

        self.started = False
        self.pause = False
        self.running = True
    
    def set_game_over_callback(self, callback):
        self.__game_over_callback = callback
        
    def main(self, from_sugar, size, loadLast):
        if self.started:
            self.__game_man.reset_game(self.gender)
        else:
            self.__init(size)
            self.__create_game(from_sugar, self.gender, self.name, loadLast)
            self.__run(from_sugar)
        
    def __init(self, size):
        self.__target_size = size
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.init()
        pygame.display.set_mode(self.__target_size, pygame.DOUBLEBUF, 0)
        self.__screen = pygame.display.get_surface()
        self.__screen.blit(pygame.image.load("assets/slides/screen_loading.jpg").convert_alpha(), (0,0))
        pygame.display.flip()
        
    def __create_game(self, from_sugar, gender, name, loadLast):
        self.started = True        
        self.__screen = pygame.display.get_surface()
        self.__clock = pygame.time.Clock()
        self.__sound_manager = SoundManager()        
        app_loader = AppLoader(gender, name)
        bars_loader = app_loader.get_status_bars_loader()
        self.__game_man = app_loader.get_game_manager()
        if loadLast: self.load_game()
        # windows_controller asociado al screen
        self.windows_controller = SaludameWindowsController(self.__screen, self.__game_man)        
        self.windows_controller.create_windows_and_activate_main(app_loader, self.__clock, bars_loader)
        #self.hotkeys_handler = HotKeyHandler()
        self.__game_man.start(self.windows_controller)
    
    def __run(self, from_sugar):               
        if from_sugar:
            import gi
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
        
        # Main loop
        frames = 0
        update = True # The first time the screen need to be updated
        
        pygame.display.update()
        while self.running:
            if from_sugar:
                while Gtk.events_pending():
                    Gtk.main_iteration()
            
            if not self.pause: # FIXME: Está de más
                # Waits for events, if none the game pauses:
                # http://wiki.laptop.org/go/Game_development_HOWTO#Reducing_CPU_Load
                milliseconds = self.__clock.tick(MAX_FPS) # waits if the game is running faster than MAX_FPS
                
                events = pygame.event.get()
                
                if events:
                    for event in events:

                        if event.type == pygame.QUIT:
                            self.running = False
                            if not from_sugar:
                                self.save_game()
                                
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            self.running = False
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
                            #self.__sound_manager.instance.start_playing()
                            self.__sound_manager.start_playing()
                        '''
                        elif event.type == pygame.KEYDOWN:
                            self.hotkeys_handler.handle_keydown(event)
                            
                        elif event.type == pygame.KEYUP:
                            self.hotkeys_handler.handle_keyup(event)
                        '''

                if self.__game_man.game_over:
                    if self.__game_over_callback:
                        self.__game_over_callback()
                    else:
                        self.running = False
                else:
                    self.windows_controller.update(frames)
                    frames += 1
                    self.__game_man.signal()
    
            pygame.display.update()
                
        print "FIXME: Se cuelga todo"
        pygame.quit()

    def save_game(self, path=INSTANCE_FILE_PATH):
        data = self.__game_man.serialize()
        try:
            f = open(path, 'w')
            f.write(data)
        finally:
            f.close()
    
    def load_game(self, path=INSTANCE_FILE_PATH):
        try:
            f = open(path)
            data = f.read()
            if self.__game_man: self.__game_man.parse_game(data)
            f.close()
        except:
            print "Error al cargar la partida"

    def volume_changed(self, range):
        value = range.get_value()
        if value >= 0 and value <= 10:
            value = float(value)/10
            self.__sound_manager.set_volume(value)
        
        
if __name__ == "__main__":
    m = Main((800, 600))
    m.gender = "boy"
    m.name = ""
    m.main(False,(800, 600))
    