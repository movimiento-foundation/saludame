import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib
import pygame
import sugargame.event as event


class PygameCanvas(Gtk.EventBox):

    def __init__(self):
    
        Gtk.EventBox.__init__(self)

        # Initialize Events translator before widget gets "realized".
        self.translator = event.Translator(self)
        self.set_can_focus(True)

        self._socket = Gtk.Socket()
        self._socket.connect('realize', self._realize_cb)
        self.add(self._socket)

        self.show_all()

    def _realize_cb(self, widget):
        # Preinitialize Pygame with the X window ID.
        os.environ['SDL_WINDOWID'] = str(widget.get_id())
        pygame.init()

        # Restore the default cursor.
        widget.props.window.set_cursor(None)

        # Confine the Pygame surface to the canvas size
        r = self.get_allocation()
        self._screen = pygame.display.set_mode((r.width, r.height), pygame.RESIZABLE)

        # Hook certain Pygame functions with GTK equivalents.
        self.translator.hook_pygame()

    def get_pygame_widget(self):
        return self._socket
