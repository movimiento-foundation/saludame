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
import signal
import sys

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio

from sugargame.canvas import PygameCanvas

# Configure gettext
import gettext
gettext.bindtextdomain("org.ceibaljam.Saludame", "locale")
gettext.textdomain("org.ceibaljam.Saludame")

# Force "es" locale as it's the only one complete
baseTranslation = gettext.translation("org.ceibaljam.Saludame", "locale", ["es"])
baseTranslation.install(unicode=True)
gettext.gettext = _  # Force the installed locale when imported from gettext

from gettext import gettext as _

from startup_window import StartupWindow
import game
from game import Main
from credits import Credits
from content_window import ContentWindow
from guides_window import GuidesWindow

import logging

D = os.path.join(os.environ["HOME"], ".Saludame")
if not os.path.exists(D):
    os.mkdir(D)
INSTANCE_FILE_PATH = os.path.join(D, "game.save")

BASEPATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(BASEPATH, "Estilos", "Estilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()
context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_SETTINGS)


class SaludameActivity(Gtk.Application):

    def __init__(self):

        Gtk.Application.__init__(self)

        self.set_flags(Gio.ApplicationFlags.NON_UNIQUE | Gio.ApplicationFlags.HANDLES_OPEN)

    def do_activate(self, files=[]):
        self.win = SaludameWindow(self, files)
        self.win.show()

    def do_open(self, files, i, hint):
        self.do_activate(files)

    def do_startup (self):
        Gtk.Application.do_startup(self)


class SaludameWindow(Gtk.ApplicationWindow):
    
    def __init__(self, app, files=[]):
    
        Gtk.Window.__init__(self, title="Saludame", application=app)

        self.__new_game = ''
        self.__data = {}

        self.set_icon_from_file(os.path.join(BASEPATH, "assets/saludame.svg"))
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.maximize()

        self.size = (800, 600)

        self.headerBar = Gtk.HeaderBar()
        self.headerBar.get_style_context().add_class("header")
        self.headerBar.set_show_close_button(True)
        self.headerBar.set_title(_("Saludame"))
        self.set_titlebar(self.headerBar)

        self.startup_window = StartupWindow(self._start_cb, self._load_last_cb)
        self.pygame_canvas = PygameCanvas()
        self.health_library = ContentWindow()
        self.guides = GuidesWindow()
        self.credits = Credits()

        self.notebook = Gtk.Notebook()
        self.notebook.get_style_context().add_class("mynotebook")

        self.notebook.append_page(self.startup_window, Gtk.Label(_("Activity")))
        self.notebook.append_page(self.pygame_canvas, Gtk.Label(_("Game")))
        self.notebook.append_page(self.health_library, Gtk.Label(_("Health Library")))
        self.notebook.append_page(self.guides, Gtk.Label(_("Guides")))
        self.notebook.append_page(self.credits, Gtk.Label(_("Credits")))

        self.add(self.notebook)

        logging.debug("Create main")

        self.game = Main()
        self.game.set_game_over_callback(self.game_over_callback)
        game.set_library_function = self.set_library

        self.healt_toolbar = self.health_library.get_toolbar()
        self.game_toolbar = self.get_game_toolbar()
        self.headerBar.pack_start(self.healt_toolbar)
        self.headerBar.pack_start(self.game_toolbar)

        self.notebook.connect('switch_page', self.__switch_page)
        self.connect("delete-event", self.__salir)
    
        self.connect("realize", self.__realize)

        self.show_all()

        self.notebook.get_children()[1].hide()
        self.healt_toolbar.hide()
        self.game_toolbar.hide()

        self.notebook.set_current_page(0)

    def __realize(self, widget):
        GLib.timeout_add(300, self.__get_allocation)

    def __get_allocation(self):
        a = self.startup_window.get_allocation()
        self.size = (a.width, a.height)
        self.startup_window.set_welcome(self.size)

    def __switch_page(self, widget, widget_child, indice):
        tab = self.notebook.get_tab_label(self.notebook.get_children()[indice])
        item = tab.get_text().decode("utf-8") # convert to unicode because GTK is always utf-8

        if item == _("Game"):
            self.healt_toolbar.hide()
            self.game_toolbar.show_all()

            if self.__new_game == 'new':
                self.game.started = False
                self.game.gender = self.__data.get('gender', '')
                self.game.name = self.__data.get('name', '')
                r = self.startup_window.get_allocation()
                GLib.timeout_add(200, self.game.main, (r.width, r.height), False)

            elif self.__new_game == 'load':
                self.game.started = False
                r = self.startup_window.get_allocation()
                GLib.timeout_add(200, self.game.main, (r.width, r.height), True)

            else:
                self.game.windows_controller.reload_main = True  # Repaints the whole screen

            self.__new_game = ''
            self.__data = {}

        elif item == _("Health Library"):
            self.healt_toolbar.show_all()
            self.game_toolbar.hide()
        else:
            self.healt_toolbar.hide()
            self.game_toolbar.hide()

        if item == _("Credits"):
            self.credits.reload()

    def _start_cb(self, gender, name):
        self.__new_game = 'new'
        self.__data = {'gender': gender, 'name': name}
        self.startup_window.set_welcome()
        self.notebook.get_children()[1].show()
        self.notebook.set_current_page(1)

    def set_library(self, link, anchor=None):
        self.notebook.set_current_page(2)
        self.health_library.set_url(link, anchor)
    
    def _load_last_cb(self, button):
        self.__new_game = 'load'
        self.notebook.get_children()[1].show()
        self.notebook.set_current_page(1)

    def game_over_callback(self):
        self.startup_window.set_welcome()
        self.notebook.get_children()[1].hide()
        self.notebook.set_current_page(0)

    def __salir(self, widget=None, senial=None):
        sys.exit(0)

    def get_game_toolbar(self):        
        toolbar = Gtk.Toolbar()
        
        # Music Volume scale
        min = 0
        max = 10
        step = 1
        default = 3
        
        image = Gtk.Image()
        image.set_from_file(os.path.join(BASEPATH, "assets/music/music_icon.png"))
        image.show()
        
        tool_item = Gtk.ToolItem()
        tool_item.set_expand(False)
        tool_item.add(image)
        tool_item.show()
        toolbar.insert(tool_item, -1)
        
        adj = Gtk.Adjustment(default, min, max, step)
        scale = Gtk.HScale()
        scale.set_adjustment(adj)
        scale.set_size_request(240,15)
        scale.set_draw_value(False)
        scale.connect("value-changed", self.game.volume_changed)
        scale.show()
                
        tool_item = Gtk.ToolItem()
        tool_item.set_expand(False)
        tool_item.add(scale)
        tool_item.show()
        toolbar.insert(tool_item, -1)
        
        toolbar.show()
        return toolbar
    

if __name__=="__main__":
    GLib.threads_init()
    GObject.threads_init()
    Gdk.threads_init()
    app = SaludameActivity()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
    