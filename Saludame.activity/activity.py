# -*- coding: utf-8 -*-

from sugar.activity.activity import Activity, ActivityToolbox
from sugargame.canvas import PygameCanvas
import gtk
import gobject

import gettext
gettextold = gettext.gettext
def _(string):
    string = gettextold(string)
    if isinstance(string, unicode):
        return string.upper()
    else:
        return unicode(string.decode("utf-8")).upper()
gettext.gettext = _
    
from gettext import gettext as _

import startup_window
import game
import credits
import content_window
import guides_window

class SaludameActivity(Activity):
    ''' Clase llamada por sugar cuando se ejecuta la actividad.
        El nombre de esta clase está señalada en el archivo activity/activity.info '''
        
    def __init__(self, handle):
        Activity.__init__(self, handle)
        
        # Crea la barra de herramientas básica de Sugar
        toolbox = ActivityToolbox(self)
        
        activity_toolbar = toolbox.get_activity_toolbar()
        
        self.game_toolbar = gtk.Toolbar()
        toolbox.add_toolbar(_("Game"), self.game_toolbar)
        self.game_toolbar.show()

        self.health_library_toolbar = gtk.Toolbar()
        toolbox.add_toolbar(_("Health Library"), self.health_library_toolbar)
        self.health_library_toolbar.show()

        self.guides_toolbar = gtk.Toolbar()
        toolbox.add_toolbar(_("Guides"), self.guides_toolbar)
        self.guides_toolbar.show()
        
        self.credits_toolbar = gtk.Toolbar()
        toolbox.add_toolbar(_("Credits"), self.credits_toolbar)
        self.credits_toolbar.show()
        
        self.set_toolbox(toolbox)
        toolbox.show()
        
        # Create startup windows
        self.startup_window = startup_window.StartupWindow(self._start_cb)
        
        # Create the canvas to embbed pygame
        self.pygame_canvas = PygameCanvas(self, False)
        
        # Create Health Library Window
        self.health_library = content_window.ContentWindow()
        
        # Create Guides Window
        self.guides = guides_window.GuidesWindow()
        
        # Create Credits Window
        self.credits = credits.Credits()
        
        self.items = gtk.HBox()
        self.items.add(self.startup_window)
        self.items.add(self.pygame_canvas)
        self.items.add(self.credits)
        self.items.add(self.health_library)
        self.items.add(self.guides)
        
        self.set_canvas(self.items)
        
        self.running = False
        
        # start on the game toolbar, might change this
        # to the create toolbar later
        self.toolbox.connect('current-toolbar-changed', self.change_mode)
        self.toolbox.set_current_toolbar(0)     # Start in activity tab
        self.change_mode(None, 0)
        
        self.items.show()
        self.show()
        
        #self.pygame_canvas.run_pygame(lambda:game.Main().main(True))    # Indico que llame a la función local para iniciar el juego pygame
        
    def canvas_resize_cb(self):
        pass
  
    def change_mode(self, notebook, index):
        game.pause = True
        self.startup_window.hide()
        self.pygame_canvas.hide()
        self.health_library.ditch()
        self.guides.ditch()
        self.credits.hide()
        
        if index == 0:
            self.startup_window.show()
        
        if index == 1:
            game.pause = False
            #self.pygame_canvas.show()
            self.show_game()
            
        if index == 2:
            self.health_library.show()
            
        if index == 3:
            self.guides.show()

        if index == 4:
            self.credits.show()

    #Override activity.Activity's can_close method
    def can_close(self):
        game.running = False
        return True
    
    def _start_cb(self):
        game.set_library_function = self.set_library    # Sets the callback to put links in the library
        self.startup_window.set_welcome()
        self.toolbox.set_current_toolbar(1)     # Move to game tab
    
    def show_game(self):
        if game.main_class:
            game.main_class.windows_controller.reload_main = True       # Repaints the whole screen
        
        self.pygame_canvas.show()
        
        if not self.running:
            self.running = True
            # Start pygame
            self.pygame_canvas.run_pygame(lambda:game.Main().main(True))    # Indico que llame a la función local para iniciar el juego pygame

    def set_library(self, link):
        self.toolbox.set_current_toolbar(2)
        self.health_library.set_url(link)
