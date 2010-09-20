# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

from sugar.activity.activity import Activity, ActivityToolbox
from sugargame.canvas import PygameCanvas
import gtk
import gobject

from gettext import gettext as _

import game

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
        
        self.set_toolbox(toolbox)
        toolbox.show()
        
        # Create the canvas to embbed pygame
        self.pygame_canvas = PygameCanvas(self, False)
        self.set_canvas(self.pygame_canvas)
        self.show_all()

        # Start pygame
        self.pygame_canvas.run_pygame(lambda:game.main(True))	# Indico que llame a la función local para iniciar el juego pygame

    def canvas_resize_cb(self):
      pass
