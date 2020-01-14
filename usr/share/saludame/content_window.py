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

import utilities

BASE = os.path.realpath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(BASE, "content")
#from sugar.graphics.radiotoolbutton import RadioToolButton

ignore_list = ["images", "old", "bak", "default.html", "default-avanzado.html", "default-simple.html"]
HOME_PAGE = os.path.join(ROOT_PATH, u'01-Introducción-avanzado.html')


class ContentWindow(Gtk.HBox):
    
    def __init__(self):

        Gtk.HBox.__init__(self)
        
        self._create_treeview()
        sw = Gtk.ScrolledWindow()
        sw.add(self.treeview)
        self.pack_start(sw, False, False, 0)
        sw.set_size_request(250, -1)
        
        self.library_type = "advanced"
        self.path_iter = {}
        self.last_uri = HOME_PAGE

        self._load_treeview()
        self._create_browser()

        self.show_all()
    
    def switch(self, toolbutton, library_type):
        self.library_type = library_type
        self._load_treeview()
    
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
        
    def _load_treeview(self):
        self.path_iter = {}
        self.treestore.clear()
        self._load_treeview_recursive(ROOT_PATH, None)
    
    def _load_treeview_recursive(self, directory, parent_iter):
        dirList = os.listdir(directory)
        for node in sorted(dirList):
            load = self.check_type(node)
            if load:
                nodepath = os.path.join(directory, node)
                if os.path.isfile(nodepath):
                    if node.endswith(".html") and not node in ignore_list:
                        display_name = self.get_display_name(node)
                        _iter = self.treestore.append(parent_iter, (display_name, nodepath)) #nodepath.encode("utf-8")))
                        self.path_iter[nodepath] = _iter
                else:
                    if not node in ignore_list:
                        display_name = self.get_display_name(node)
                        path = self.check_default_file(nodepath)
                        _iter = self.treestore.append(parent_iter, (display_name, path)) #.encode("utf-8")))
                        self.path_iter[path] = _iter
                        self._load_treeview_recursive(nodepath, _iter)
    
    def check_type(self, node):
        if self.library_type == "advanced" and "-simple" in node:
            return False
        elif self.library_type == "basic" and "-avanzado" in node:
            return False
        else:
            return True
    
    def check_default_file(self, nodepath):
        aux = os.path.join(nodepath, "default-avanzado.html")
        if os.path.exists(aux):
            return aux
            
        aux = os.path.join(nodepath, "default-simple.html")
        if os.path.exists(aux):
            return aux
            
        aux = os.path.join(nodepath, "default.html")
        if os.path.exists(aux):
            return aux
        
        return nodepath

    def get_display_name(self, file_name):
        display_name = file_name.replace(".html", "")
        display_name = display_name.replace("-avanzado", "")
        display_name = display_name.replace("-simple", "")
        display_name = display_name.split("-", 1)[-1]
        return display_name
    
    def cursor_changed_cb(self, treeview):
        try:
            tree_path, column = self.treeview.get_cursor()
            it = self.treestore.get_iter(tree_path)
            path = self.treestore.get_value(it, 1)
            if path.endswith(".html"):
                uri = u"file://" + unicode(path, "utf-8")
                if not self.last_uri.startswith(uri):           # avoids reloading a page when the cursor is changed by the program
                    self.last_uri = uri
                    self.web_view.load_uri(self.last_uri)
        except:
            pass

    def position_in_filename(self, filepath):
        if filepath in self.path_iter:
            _iter = self.path_iter[filepath]
            if self.treeview.get_selection().get_selected()[1] <> _iter:   # avoids falling in a loop with location_changed
                treepath = self.treestore.get_path(_iter)
                self.treeview.expand_to_path(treepath)
                self.treeview.set_cursor(treepath)
        
    def set_url(self, link, anchor=None):
        # First fix the link in advanced or simple:
        if self.library_type == "basic":
            link = link.replace("-avanzado", "-simple")
        
        # Then add the base path and position in the tree
        link = os.path.join(ROOT_PATH, link)
        self.position_in_filename(link)
        
        # Last add the protocol and the anchor
        if anchor:
            self.last_uri = u"file://" + link + u"#" + unicode(anchor)
        else:
            self.last_uri = u"file://" + link
        
        if self.web_view:
            self.web_view.load_uri( self.last_uri )
     
    def get_toolbar(self):
        toolbar = Gtk.Toolbar()
        
        radio_adv = Gtk.RadioToolButton()
        radio_adv.set_active(True)
        radio_adv.set_label("Avanzada")
        radio_adv.set_tooltip_text("Mostrar biblioteca avanzada")
        radio_adv.connect("clicked", self.switch, "advanced")
        toolbar.insert(radio_adv, -1)
        
        radio_bas = Gtk.RadioToolButton(group=radio_adv)
        radio_bas.set_label("Simple")
        radio_bas.set_tooltip_text("Mostrar biblioteca sencilla")
        radio_bas.connect("clicked", self.switch, "basic")
        toolbar.insert(radio_bas, -1)
        
        toolbar.show_all()
        
        return toolbar


if __name__ == "__main__":
    window = ContentWindow()
    main_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
    main_window.add(window)
    main_window.set_size_request(800,600)
    main_window.show_all()
    main_window.connect("delete-event", Gtk.main_quit)
    Gtk.main()
    