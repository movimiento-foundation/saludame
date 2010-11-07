# -*- coding: utf-8 -*-

import gtk, gobject
import os
from gettext import gettext as _

hulahop_ok = True
try:
    from sugar.activity import activity
    import hulahop
    hulahop.startup( os.path.join(activity.get_activity_root(), 'data/gecko') )
    from hulahop.webview import WebView
except:
    hulahop_ok = False

import content_parser

gobject.threads_init()

try:
    ROOT_PATH = os.path.join(activity.get_bundle_path(), 'content/')
    HOME_PAGE = os.path.join(activity.get_bundle_path(), u'content/Introducción.html')
except:
    ROOT_PATH = os.path.join('content/')
    HOME_PAGE = os.path.join(u'content/Introducción.html')

class ContentWindow(gtk.HBox):
    
    def __init__(self):
        gtk.HBox.__init__(self, False)
        
        self._create_treeview()
        self.pack_start(self.treeview, False)
        
        if hulahop_ok:
            self.web_view = WebView()
            self.pack_start(self.web_view, True, True)
            self.web_view.load_uri(HOME_PAGE)
        else:
            health_stuff = gtk.Button("Pretty Health stuff goes here")
            self.add(health_stuff)
        
        self.connect("expose-event", self._exposed)
        self.show_all()
 
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
        self.treeview.connect("row-activated", self.selection)
    
    def selection(self, treeview, tree_path, view_column):
        it = self.treestore.get_iter(tree_path)
        path = self.treestore.get_value(it, 1)
        
        real_path = os.path.join(ROOT_PATH, path)
        print real_path
        
        self.web_view.load_uri( unicode(real_path) )
    
    def _exposed(self, widget, event):
        if not self.treeview_loaded:
            self.treeview_loaded = True
            self._load_treeview()
    
    def _load_treeview(self):
        root_iter = self.treestore.append(None, (_("Library"), "/"))
        iters = {ROOT_PATH: root_iter}
        
        for root, dirs, files in os.walk(ROOT_PATH):
            for _file in files:
                if _file.endswith(".html"):
                    display_name = self.get_display_name(_file)
                    fullpath = os.path.join(root, _file)
                    self.treestore.append(iters[root], (display_name, fullpath))
                
            for _dir in dirs:
                _iter = self.treestore.append(iters[root], (_dir, root))
                iters[os.path.join(root, _dir)] = _iter
        
        self.treeview.expand_row((0), False)        # Expand the root path
        
    def get_display_name(self, file_name):
        display_name = file_name.replace(".html", "")
        return display_name
        
if __name__ == "__main__":
    window = ContentWindow()
    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.add(window)
    main_window.show_all()
    gtk.main()
