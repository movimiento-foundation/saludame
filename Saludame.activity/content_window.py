# -*- coding: utf-8 -*-

import gtk, gobject
import os
from gettext import gettext as _

if __name__ == "__main__":
    ROOT_PATH = os.path.realpath('content/')
    STARTUP_DIR = os.path.realpath('gecko')
else:
    from sugar.activity import activity
    ROOT_PATH = os.path.join(activity.get_bundle_path(), 'content/')
    STARTUP_DIR = os.path.join(activity.get_activity_root(), 'data/gecko')

HOME_PAGE = os.path.join(ROOT_PATH, u'01-Introducción.html')

hulahop_ok = True
try:
    import hulahop
    hulahop.startup( STARTUP_DIR )
    from hulahop.webview import WebView
except:
    hulahop_ok = False

import content_parser

gobject.threads_init()

class ContentWindow(gtk.HBox):
    
    def __init__(self):
        gtk.HBox.__init__(self, False)
        
        self._create_treeview()
        self.pack_start(self.treeview, False)
        
        self.web_view = None
        self.last_uri = HOME_PAGE
        
        self.connect("expose-event", self._exposed)
        self.show_all()

    def _create_browser(self):
        if hulahop_ok:
            self.web_view = WebView()
            self.pack_start(self.web_view, True, True)
            
            print HOME_PAGE
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

    def cursor_changed_cb(self, treeview):
        tree_path, column = self.treeview.get_cursor()
        
        it = self.treestore.get_iter(tree_path)
        path = self.treestore.get_value(it, 1)

        real_path = os.path.join(ROOT_PATH, path)
        #print real_path
        
        self.web_view.load_uri( unicode(real_path) )

    #def selection(self, treeview, tree_path, view_column):
        #it = self.treestore.get_iter(tree_path)
        #path = self.treestore.get_value(it, 1)

        #real_path = os.path.join(ROOT_PATH, path)
        #print real_path
        
        #self.web_view.load_uri( unicode(real_path) )
    
    def _exposed(self, widget, event):
        if not self.treeview_loaded:
            self.treeview_loaded = True
            self._load_treeview()
            self.treeview.expand_row((0), False)        # Expand the root path
        
        if not self.web_view:
            self._create_browser()
            
    def ditch(self):
        """ Called when we need to ditch the browsing window and hide the whole window """
        if self.web_view:
            self.remove(self.web_view)
            self.web_view = None
        self.hide()
        
    def _load_treeview(self):
        root_iter = self.treestore.append(None, (_("Library"), "ROOT"))
        iters = {ROOT_PATH: root_iter}
        
        for root, dirs, files in os.walk(ROOT_PATH):
            all = []
            all += [(file, 'f') for file in files]
            all += [(dir, 'd') for dir in dirs]
            all = sorted(all)
            
            for node_name, node_type in all:
                if node_type == 'f':
                    if node_name.endswith(".html"):
                        display_name = self.get_display_name(node_name)
                        fullpath = os.path.join(root, node_name)
                        self.treestore.append(iters[root], (display_name, fullpath))
                else:
                    display_name = self.get_display_name(node_name)
                    _iter = self.treestore.append(iters[root], (display_name, root))
                    iters[os.path.join(root, node_name)] = _iter
        
    def get_display_name(self, file_name):
        display_name = file_name.replace(".html", "")
        display_name = display_name.split("-", 1)[-1]
        return display_name
    
    def set_url(self, link):
        link = ROOT_PATH + link
        self.last_uri = unicode(link)
        if self.web_view:
            self.web_view.load_uri( self.last_uri )
        
if __name__ == "__main__":
    window = ContentWindow()
    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.add(window)
    main_window.show_all()
    gtk.main()
