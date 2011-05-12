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

import gtk, gobject
import os
from gettext import gettext as _
import utilities

from sugar.graphics.radiotoolbutton import RadioToolButton

if __name__ == "__main__":
    ROOT_PATH = unicode(os.path.realpath('content/'))
    STARTUP_DIR = os.path.realpath('gecko')
else:
    from sugar.activity import activity
    ROOT_PATH = unicode(os.path.join(activity.get_bundle_path(), 'content/'))
    STARTUP_DIR = os.path.join(activity.get_activity_root(), 'data/gecko')

ignore_list = ["images", "old", "bak", "default.html", "default-avanzado.html", "default-simple.html"]

HOME_PAGE = u"file://" + os.path.join(ROOT_PATH, u'01-Introducción-avanzado.html')

hulahop_ok = True
try:
    import hulahop
    hulahop.startup(STARTUP_DIR)
    from hulahop.webview import WebView
    from progresslistener import ProgressListener
except:
    hulahop_ok = False

gobject.threads_init()

# filesystemencoding should be used, but for some reason its value is ascii instead of utf-8
# the following lines are used to fix that problem, asumming all paths as utf-8
fencoding = 'utf-8'     
uni = lambda s: unicode(s, fencoding)
listdir = lambda x: map(uni, os.listdir(x.encode(fencoding)))
isfile = lambda x: os.path.isfile(x.encode(fencoding))
exists = lambda x: os.path.exists(x.encode(fencoding))
#

class ContentWindow(gtk.HBox):
    
    def __init__(self, toolbar=None):
        gtk.HBox.__init__(self, False)
        
        self._create_treeview()
        sw = gtk.ScrolledWindow()
        sw.add(self.treeview)
        self.pack_start(sw, False)
        self.treeview.set_size_request(300, -1)
        
        self.web_view = None
        self.last_uri = HOME_PAGE
        
        self.connect("expose-event", self._exposed)
        self.show_all()

        self.library_type = "advanced"
        
        # Could be loaded on expose, but the set_url function won't work
        self._load_treeview()
    
    def switch(self, toolbutton, library_type):
        self.library_type = library_type
        self._load_treeview()
    
    def _create_browser(self):
        if hulahop_ok:
            self.web_view = WebView()
            self.pack_start(self.web_view, True, True)
            self.progress_listener = ProgressListener()
            self.progress_listener.setup(self.web_view)
            self.progress_listener.connect('location-changed', self._location_changed_cb)
            
            self.web_view.load_uri(self.last_uri)
            self.web_view.show()
        else:
            self.web_view = gtk.Button()
            self.web_view.load_uri = self.web_view.set_label
            self.web_view.load_uri(self.last_uri)
            self.add(self.web_view)
            self.web_view.show()
    
    def _create_treeview(self):
        # Provided by Poteland:
        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore(str, str)
        
        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)
        
        # create the TreeViewColumn to display the data
        tvcolumn = gtk.TreeViewColumn("")
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        self.treeview.append_column(tvcolumn)
        
        # set the cell "text" attribute to column 0 - retrieve text
        tvcolumn.add_attribute(cell, 'text', 0)
        
        # make it searchable
        self.treeview.set_search_column(0)
        
        self.treeview_loaded = False
        self.treeview.connect("cursor-changed", self.cursor_changed_cb)
        
    def _exposed(self, widget, event):
        if not self.treeview_loaded:
            self.path_iter = {}
            self.treeview_loaded = True
            self._load_treeview()
            
        if not self.web_view:
            # First exposes the widget and then (when idle) creates the browser, so the screen shows up faster
            self.web_view = True # temporary so the conditions doesn't meet
            gobject.idle_add(self._create_browser)
            
    def ditch(self):
        """ Called when we need to ditch the browsing window and hide the whole window """
        if self.web_view:
            self.remove(self.web_view)
            self.web_view = None
            self.progress_listener = None
    
    def _load_treeview(self):
        self.treeview_loaded = True
        self.path_iter = {}
        self.treestore.clear()
        self._load_treeview_recursive(ROOT_PATH, None)
    
    def _load_treeview_recursive(self, directory, parent_iter):
        dirList = listdir(directory)
        for node in sorted(dirList):
            load = self.check_type(node)
            if load:
                nodepath = os.path.join(directory, node)
                if isfile(nodepath):
                    if node.endswith(".html") and not node in ignore_list:
                        display_name = self.get_display_name(node)
                        _iter = self.treestore.append(parent_iter, (display_name, nodepath.encode("utf-8")))
                        self.path_iter[nodepath] = _iter
                else:
                    if not node in ignore_list:
                        display_name = self.get_display_name(node)
                        path = self.check_default_file(nodepath)
                        _iter = self.treestore.append(parent_iter, (display_name, path.encode("utf-8")))
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
        if exists(aux):
            return aux
            
        aux = os.path.join(nodepath, "default-simple.html")
        if exists(aux):
            return aux
            
        aux = os.path.join(nodepath, "default.html")
        if exists(aux):
            return aux
        
        return nodepath

    def get_display_name(self, file_name):
        display_name = file_name.replace(".html", "")
        display_name = display_name.replace("-avanzado", "")
        display_name = display_name.replace("-simple", "")
        display_name = display_name.split("-", 1)[-1]
        return display_name
    
    def cursor_changed_cb(self, treeview):
        tree_path, column = self.treeview.get_cursor()
        
        it = self.treestore.get_iter(tree_path)
        path = self.treestore.get_value(it, 1)
        
        if path.endswith(".html") and self.web_view:
            self.last_uri = u"file://" + unicode(path, "utf-8")
            self.web_view.load_uri(self.last_uri)

    def _location_changed_cb(self, progress_listener, uri):
        path = utilities.unquote(uri.path.encode("utf-8"))
        uri = u"file://" + path
        if self.last_uri <> uri:
            self.last_uri = uri
            self.position_in_filename(path)
        
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
            link.replace("-avanzado", "-simple")
        
        link = os.path.join(ROOT_PATH, link)
        self.position_in_filename(link)
        if anchor:
            self.last_uri = u"file://" + link + u"#" + unicode(anchor)
        else:
            self.last_uri = u"file://" + link
        
        if self.web_view:
            self.web_view.load_uri( self.last_uri )
        
    def get_toolbar(self):
        toolbar = gtk.Toolbar()
        
        radio_adv = RadioToolButton()
        radio_adv.set_active(True)
        radio_adv.set_label("Avanzada")
        radio_adv.set_tooltip("Mostrar biblioteca avanzada")
        radio_adv.connect("clicked", self.switch, "advanced")
        toolbar.insert(radio_adv, -1)
        radio_adv.show()
        
        radio_bas = RadioToolButton(group=radio_adv)
        radio_bas.set_label("Simple")
        radio_bas.set_tooltip("Mostrar biblioteca sencilla")
        radio_bas.connect("clicked", self.switch, "basic")
        toolbar.insert(radio_bas, -1)
        
        toolbar.show_all()
        
        return toolbar

if __name__ == "__main__":
    window = ContentWindow()
    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.add(window)
    main_window.set_size_request(800,600)
    main_window.show_all()
    gtk.main()
    