# -*- coding: utf-8 -*-

import gtk, gobject
import os
from gettext import gettext as _

if __name__ == "__main__":
    ROOT_PATH = unicode(os.path.realpath('content/'))
    STARTUP_DIR = os.path.realpath('gecko')
else:
    from sugar.activity import activity
    ROOT_PATH = unicode(os.path.join(activity.get_bundle_path(), 'content/'))
    STARTUP_DIR = os.path.join(activity.get_activity_root(), 'data/gecko')

ignore_list = ["images", "old", "bak"]

HOME_PAGE = os.path.join(ROOT_PATH, u'01-Introducción-avanzado.html')

hulahop_ok = True
try:
    import hulahop
    hulahop.startup(STARTUP_DIR)
    from hulahop.webview import WebView
except:
    hulahop_ok = False

gobject.threads_init()

# filesystemencoding should be used, but for some reason its value is ascii instead of utf-8
# the following lines are used to fix that problem, asumming all paths as unicode
fencoding = 'utf-8'     
uni = lambda s: unicode(s, fencoding)
listdir = lambda x: map(uni, os.listdir(x.encode(fencoding)))
isfile = lambda x: os.path.isfile(x.encode(fencoding))
#

class ContentWindow(gtk.HBox):
    
    def __init__(self):
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

        # Could be loaded on expose, but the set_url function won't work
        self.path_iter = {}
        self.treeview_loaded = True
        self._load_treeview()
        
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
        
        if real_path.endswith(".html"):
            self.web_view.load_uri( unicode(real_path) )

    #def selection(self, treeview, tree_path, view_column):
        #it = self.treestore.get_iter(tree_path)
        #path = self.treestore.get_value(it, 1)

        #real_path = os.path.join(ROOT_PATH, path)
        #print real_path
        
        #self.web_view.load_uri( unicode(real_path) )
    
    def _exposed(self, widget, event):
        if not self.treeview_loaded:
            self.path_iter = {}
            self.treeview_loaded = True
            self._load_treeview()
            
        if not self.web_view:
            self._create_browser()
            
    def ditch(self):
        """ Called when we need to ditch the browsing window and hide the whole window """
        if self.web_view:
            self.remove(self.web_view)
            self.web_view = None
        #self.hide()
        
    def _load_treeview(self, directory=ROOT_PATH, parent_iter=None):
        dirList = listdir(directory)
        for node in sorted(dirList):
            nodepath = os.path.join(directory, node)
            if isfile(nodepath):
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
        display_name = display_name.replace("-avanzado", "")
        display_name = display_name.replace("-simple", "")
        display_name = display_name.split("-", 1)[-1]
        return display_name
    
    def position_in_filename(self, filepath):
        if filepath in self.path_iter:
            _iter = self.path_iter[filepath]
            treepath = self.treestore.get_path(_iter)
            self.treeview.expand_to_path(treepath)
            self.treeview.set_cursor(treepath)
        else:
            print filepath
            print self.path_iter.keys()
            
    def set_url(self, link, anchor=None):
        link = os.path.join(ROOT_PATH, link)
        self.position_in_filename(link)
        if anchor:
            self.last_uri = unicode("file://") + link + unicode("#") + unicode(anchor)
        else:
            self.last_uri = unicode("file://") + link
        
        if self.web_view:
            self.web_view.load_uri( self.last_uri )
        
if __name__ == "__main__":
    window = ContentWindow()
    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.add(window)
    main_window.set_size_request(800,600)
    main_window.show_all()
    gtk.main()
    