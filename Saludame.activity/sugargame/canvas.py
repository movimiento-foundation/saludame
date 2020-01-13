# -*- coding: utf-8 -*-
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GdkX11
import pygame
from event import Translator


class PygameCanvas(Gtk.DrawingArea):

    def __init__(self):
    
        Gtk.DrawingArea.__init__(self)
        
        self.set_can_focus(True)
        self._screen = None
        self.connect('realize', self._realize_cb)
        self.show_all()
        self.translator = Translator(self)

    def _realize_cb(self, widget):
        os.environ['SDL_WINDOWID'] = str(self.get_property('window').get_xid())
        pygame.init()
        widget.props.window.set_cursor(None)
        r = self.get_allocation()
        self._screen = pygame.display.set_mode((r.width, r.height), pygame.RESIZABLE)
        self.translator.hook_pygame()
