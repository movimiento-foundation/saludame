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
from gi.repository import GObject
from gi.repository import GLib

BASE = os.path.realpath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(BASE, "guides")

HOME_PAGE = os.path.join(ROOT_PATH, u'02-Empezar.html')
ignore_list = ["images", "old", "bak"]


class GuidesWindow(Gtk.HBox):
    
    def __init__(self):

        Gtk.HBox.__init__(self)
        
        self._create_treeview()
        sw = Gtk.ScrolledWindow()
        sw.add(self.treeview)
        self.pack_start(sw, False, False, 0)
        sw.set_size_request(250, -1)
        
        self.path_iter = {}
        self.last_uri = HOME_PAGE

        self._load_treeview()
        self._create_browser()
        
        self.show_all()

    def _create_browser(self):
        self.web_view = WebKit2.WebView()
        self.pack_start(self.web_view, True, True, 0)
        self.web_view.load_uri("file://" + self.last_uri)
        
    def _create_treeview(self):
        # Provided by Poteland:
        # create a TreeStore with one string column to use as the model
        self.treestore = Gtk.TreeStore(str, str)
        
        # create the TreeView using treestore
        self.treeview = Gtk.TreeView(self.treestore)
        
        # create the TreeViewColumn to display the data
        tvcolumn = Gtk.TreeViewColumn("")
        cell = Gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        self.treeview.append_column(tvcolumn)
        
        # set the cell "text" attribute to column 0 - retrieve text
        tvcolumn.add_attribute(cell, 'text', 0)
        
        # make it searchable
        self.treeview.set_search_column(0)
        
        self.treeview.connect("cursor-changed", self.cursor_changed_cb)

    def cursor_changed_cb(self, treeview):
        tree_path, column = self.treeview.get_cursor()
        
        it = self.treestore.get_iter(tree_path)
        path = self.treestore.get_value(it, 1)
        
        if path.endswith(".html"):
            self.last_uri = u"file://" + unicode(path, "utf-8")
            self.web_view.load_uri( self.last_uri )
    
    def _load_treeview(self, directory=ROOT_PATH, parent_iter=None):
        dirList = os.listdir(directory)
        for node in sorted(dirList):
            nodepath = os.path.join(directory, node)
            if os.path.isfile(nodepath):
                if node.endswith(".html"):
                    display_name = self.get_display_name(node)
                    _iter = self.treestore.append(parent_iter, (display_name, nodepath))
                    self.path_iter[nodepath] = _iter
            else:
                if not node in ignore_list:
                    display_name = self.get_display_name(node)
                    _iter = self.treestore.append(parent_iter, (display_name, nodepath))
                    self.path_iter[nodepath] = _iter
                    self._load_treeview(nodepath, _iter)
    
    def get_display_name(self, file_name):
        display_name = file_name.replace(".html", "")
        display_name = display_name.split("-", 1)[-1]
        return display_name
    
        
if __name__ == "__main__":
    window = GuidesWindow()
    main_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
    main_window.add(window)
    main_window.set_size_request(800,600)
    main_window.show_all()
    main_window.connect("delete-event", Gtk.main_quit)
    Gtk.main()
