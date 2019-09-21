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

import gi
import os
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2
from gi.repository import Gtk

BASE = os.path.realpath(os.path.dirname(__file__))


class Credits(WebKit2.WebView):
    
    def __init__(self):
        
        WebKit2.WebView.__init__(self)

        self.load_uri("file://" + os.path.join(BASE, "credits", "credits.html"))
        self.show_all()

    def reload(self):
        self.load_uri("file://" + os.path.join(BASE, "credits", "credits.html"))

        
if __name__ == "__main__":
    c = Credits()
    main_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
    main_window.maximize()
    main_window.add(c)
    main_window.show_all()
    main_window.connect("delete-event", Gtk.main_quit)
    Gtk.main()
    