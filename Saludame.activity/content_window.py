# -*- coding: utf-8 -*-

import gtk, os
from gettext import gettext as _

from sugar.activity import activity

#import hulahop
#hulahop.startup( os.path.join(activity.get_activity_root(), 'data/gecko') )

#from hulahop.webview import WebView

import content_parser

ROOT_PATH = "content"

class ContentWindow(gtk.HBox):
    
    def __init__(self):
        gtk.HBox.__init__(self, False)

        self._create_treeview()
        self.add(self.treeview)
        
        health_stuff = gtk.Button("Pretty Health stuff goes here")
        self.add(health_stuff)
        #self.web_view = WebView()
        #self.add(self.web_view)

        self.connect("expose-event", self._exposed)
        self.show_all()
 
    def _create_treeview(self):
        # Provided by Poteland:
        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore(str)
        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)
        # create the TreeViewColumn to display the data
        tvcolumn = gtk.TreeViewColumn("")
        # add tvcolumn to treeview
        self.treeview.append_column(tvcolumn)
        # create a CellRendererText to render the data
        cell = gtk.CellRendererText()
        # add the cell to the tvcolumn and allow it to expand
        tvcolumn.pack_start(cell, True)
        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        tvcolumn.add_attribute(cell, 'text', 0)
        # make it searchable
        self.treeview.set_search_column(0)
        # Allow sorting on the column
        #tvcolumn.set_sort_column_id(0) # Makes the app crash on sugar

        self.treeview_loaded = False
        
    def _exposed(self, widget, event):
        if not self.treeview_loaded:
            self.treeview_loaded = True
            self._load_treeview()

            #self.web_view.load_uri("content/instrucciones.html")
    
    def _load_treeview(self):
        # we'll add some data now - 4 rows with 3 child rows each
        #for parent in range(4):
        #    piter = self.treestore.append(None, ['parent %i' % parent])
        #    for child in range(3):
        #        self.treestore.append(piter, ['child %i of parent %i' % (child, parent)])
        
        _iter = self.treestore.append(None, (_("Library"),))
        iters = {ROOT_PATH: _iter}
        
        for root, dirs, files in os.walk(ROOT_PATH):
            for _file in files:
                self.treestore.append(iters[root], (_file,))
                
            for _dir in dirs:
                _iter = self.treestore.append(iters[root], (_dir,))
                iters[os.path.join(root, _dir)] = _iter

if __name__ == "__main__":
    window = ContentWindow()
    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.add(window)
    main_window.show_all()
    gtk.main()
