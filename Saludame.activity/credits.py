# -*- coding: utf-8 -*-

import gtk
import rsvg

class Credits(gtk.DrawingArea):
    
    def __init__(self):
        self.loaded = False
        gtk.DrawingArea.__init__(self)
        self.connect('expose-event', self._expose_cb)

    
    def _expose_cb(self, widget, event):
        if not self.loaded:
            icon_file = open("credits/saludame.svg", 'r')
            data = icon_file.read()
            icon_file.close()
            
            pixbuf = rsvg.Handle(data=data).get_pixbuf()
            self.window.draw_pixbuf(None, pixbuf, 0, 0, 0, 0)
            self.loaded = True
