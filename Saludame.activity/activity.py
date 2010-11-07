# -*- coding: utf-8 -*-

from sugar.activity.activity import Activity, ActivityToolbox
from sugargame.canvas import PygameCanvas
import gtk
import gobject

import gettext
gettextold = gettext.gettext
def _(string):
    return unicode(gettextold(string)).upper()
gettext.gettext = _

from gettext import gettext as _

import game
import credits
import content_window

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
        
        self.credits_toolbar = gtk.Toolbar()
        toolbox.add_toolbar(_("Credits"), self.credits_toolbar)
        self.credits_toolbar.show()
        
        self.set_toolbox(toolbox)
        toolbox.show()
                
        # Create the canvas to embbed pygame
        self.pygame_canvas = PygameCanvas(self, False)
        
        # Create Health Library Window
        self.health_library = content_window.ContentWindow()
        
        # Create Credits Window
        self.credits = credits.Credits()
        
        self.items = gtk.HBox()
        self.items.add(self.pygame_canvas)
        self.items.add(self.credits)
        self.items.add(self.health_library)
        
        self.set_canvas(self.items)
        
        # start on the game toolbar, might change this
        # to the create toolbar later
        self.toolbox.connect('current-toolbar-changed', self.change_mode)
        self.toolbox.set_current_toolbar(1)
        
        self.items.show()
        self.show()

        # Start pygame
        self.pygame_canvas.run_pygame(lambda:game.Main().main(True))	# Indico que llame a la función local para iniciar el juego pygame

    def canvas_resize_cb(self):
        pass
  
    def change_mode(self, notebook, index):
        if index == 0:
            game.pause = True
            self.pygame_canvas.hide()
            self.credits.hide()
            self.health_library.hide()
        
        if index == 1:
            game.pause = False
            self.credits.hide()
            self.health_library.hide()
            if game.main_class:
                game.main_class.windows_controller.reload_main = True       # Repaints the whole screen
            self.pygame_canvas.show()
            
        if index == 2:
            game.pause = True
            self.pygame_canvas.hide()
            self.health_library.show()
            self.credits.hide()
            
        if index == 3:
            game.pause = True
            self.pygame_canvas.hide()
            self.health_library.hide()
            self.credits.show()
    
    #Override activity.Activity's can_close method
    def can_close(self):
        game.running = False
        return True
