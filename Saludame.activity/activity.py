# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

from sugar.activity.activity import Activity, ActivityToolbox
from sugargame.canvas import PygameCanvas
import gtk
import gobject

from gettext import gettext as _

import game
import credits

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
        
        self.credits_toolbar = gtk.Toolbar()
        toolbox.add_toolbar(_("Credits"), self.credits_toolbar)
        self.credits_toolbar.show()
        
        self.set_toolbox(toolbox)
        toolbox.show()
        
        # start on the game toolbar, might change this
        # to the create toolbar later
        self.toolbox.connect('current-toolbar-changed', self.change_mode)
        self.toolbox.set_current_toolbar(1)
        
        # Create the canvas to embbed pygame
        self.pygame_canvas = PygameCanvas(self, False)
        self.credits = credits.Credits()
        
        self.items = gtk.HBox()
        self.items.add(self.pygame_canvas)
        self.items.add(self.credits)
        
        self.set_canvas(self.items)
        self.pygame_canvas.show()
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
        
        if index == 1:
            game.pause = False
            self.credits.hide()
            self.pygame_canvas.show()
            
        if index == 2:
            game.pause = True
            self.pygame_canvas.hide()
            self.credits.show()
    