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

import gtk
import rsvg

class Credits(gtk.Fixed):
    
    def __init__(self):
        gtk.Fixed.__init__(self)
        self.loaded = False
        self.reloaded = False
        
        self.connect("expose-event", self._expose_cb)
                
        self.viewport_initialized = False
        
    def before_show(self):
        if not self.loaded:
            self.pixbuf = gtk.gdk.pixbuf_new_from_file("credits/background.jpg")
            
            self.credits_pixbuf = rsvg.Handle(file="credits/saludame.svg").get_pixbuf()
            
            height = self.credits_pixbuf.get_height()
            self.adj = gtk.Adjustment(value=0, lower=0, upper=height, step_incr=20, page_incr=200, page_size=550)
            scroll = gtk.VScrollbar(self.adj)
            scroll.set_size_request(40, 550)
            scroll.show()
            scroll.connect("value-changed", self.scrolled)
            
            self.put(scroll, 1158, 150)

            self.loaded = True
            
        elif not self.reloaded:
            self.credits_pixbuf = rsvg.Handle(file="credits/saludame.svg").get_pixbuf()
            self.reloaded = True
        
    def ditch(self):
        self.credits_pixbuf = None
        self.reloaded = False
    
    def scrolled(self, gtkrange):
        self.queue_draw()
        
    def _expose_cb(self, widget, event):
        widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], self.pixbuf, 0, 0, 0, 0)
        
        y = int(self.adj.get_value())
        width = self.credits_pixbuf.get_width()
        height = 550
        widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], self.credits_pixbuf, 0, y, 50, 150, width, height)
        
if __name__ == "__main__":
    c = Credits()
    c.before_show()
    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.set_size_request(1200,700)
    main_window.add(c)
    main_window.show_all()
    gtk.main()
    