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

from sugar.activity.activity import Activity, ActivityToolbox
from sugar.datastore import datastore
from sugargame.canvas import PygameCanvas

import gc

import gtk
import gobject

import gettext
gettextold = gettext.gettext

def _(string):
    string = gettextold(string)
    if isinstance(string, unicode):
        return string.upper()
    else:
        return unicode(string.decode("utf-8")).upper()
gettext.gettext = _

from gettext import gettext as _

import startup_window
import game
import credits
import content_window
import guides_window
import logging

class SaludameActivity(Activity):
    ''' Clase llamada por sugar cuando se ejecuta la actividad.
        El nombre de esta clase está señalada en el archivo activity/activity.info '''
        
    def __init__(self, handle):
        
        self.game_init = False          # Tells if game engine was initialized
        self.loaded_game = None
        
        Activity.__init__(self, handle)
        
        # Creates the activiy box for toolbars
        self.toolbox = ActivityToolbox(self)
        self.set_toolbox(self.toolbox)
        self.toolbox.show()
        
        # Retrieves the Activity standard toolbar
        self.activity_toolbar = self.toolbox.get_activity_toolbar()

        # Creates other toolbars
        # Game toolbar gets created on demand
        # Library toolbar gets created on demand
        self.guides_toolbar = gtk.Toolbar()
        self.credits_toolbar = gtk.Toolbar()
        
        self.indexes = ["activity"] # right now only activity toolbar

        # Create startup windows
        self.startup_window = startup_window.StartupWindow(self._start_cb, self._load_last_cb)
        
        # Create the canvas to embbed pygame
        self.pygame_canvas = PygameCanvas(self, False)
        
        # Create Health Library Window
        self.health_library = content_window.ContentWindow()
        
        # Create Guides Window
        self.guides = guides_window.GuidesWindow()
        
        # Create Credits Window
        self.credits = credits.Credits()
        
        self.startup_window.show()
        self.pygame_canvas.show()
        self.health_library.show()
        self.guides.show()
        self.credits.show()
        
        self.items = gtk.Notebook()
        self.items.set_show_tabs(False)
        self.items.set_show_border(False)
        self.items.append_page(self.startup_window)
        self.items.append_page(self.pygame_canvas)
        self.items.append_page(self.health_library)
        self.items.append_page(self.guides)
        self.items.append_page(self.credits)
        self.items.show()
        
        self.set_canvas(self.items)

        logging.debug("Create main")
        self.game = game.Main()
        self.game.set_game_over_callback(self.game_over_callback)
        
        self.toolbox.connect('current-toolbar-changed', self.change_mode)
        self.make_toolbox(False)
        self.toolbox.set_current_toolbar(0)     # Start in activity tab
        
        # force the toolbar change
        self.change_mode(None, self.toolbox.get_current_toolbar())
        
        game.set_library_function = self.set_library    # Sets the callback to put links in the library
        
        self.show()
    
    def make_toolbox(self, add_game):
        toolbars = len(self.indexes)
        for i in range(toolbars, 0, -1):
            self.toolbox.remove_toolbar(i)
        
        self.indexes = ["activity"]     # activity toolbar never gets removed
        
        if add_game:
            self.toolbox.add_toolbar(_("Game"), self.get_game_toolbar())
            self.indexes += ["game"]
        
        self.indexes += ["library", "guides", "credits"]
        self.toolbox.add_toolbar(_("Health Library"), self.health_library.get_toolbar())
        self.toolbox.add_toolbar(_("Guides"), self.guides_toolbar)
        self.toolbox.add_toolbar(_("Credits"), self.credits_toolbar)
        
    def change_mode(self, notebook, index):
        game.pause = True
        self.pygame_canvas.translator.unhook_pygame()
        self.health_library.ditch()
        self.guides.ditch()
        self.guides.ditch()
        
        gc.collect()    # Collects garbaje
        
        if self.indexes[index] == "activity":
            self.items.set_current_page(0)
            
        if self.indexes[index] == "game":
            game.pause = False
            self.show_game()
            self.items.set_current_page(1)

        elif self.indexes[index] == "library":
            self.items.set_current_page(2)
            
        elif self.indexes[index] == "guides":
            self.items.set_current_page(3)
            
        elif self.indexes[index] == "credits":
            self.credits.before_show()
            self.items.set_current_page(4)
    
    #Override activity.Activity's can_close method
    def can_close(self):
        game.running = False
        return True
    
    def _start_cb(self, gender, name):
        #self.create_in_journal()
        self.metadata['title'] = _("Saludame") + " " + name
        self.game.gender = gender
        self.game.name = name
        self.startup_window.set_welcome()
        
        if self.game.started:
            self.game.main(True)
        
        self.make_toolbox(True)
        self.toolbox.set_current_toolbar(1)             # Move to game tab
    
    def show_game(self):
        if self.game.started:
            self.game.windows_controller.reload_main = True       # Repaints the whole screen
        
        if self.game_init:
            self.pygame_canvas.translator.hook_pygame()
        else:
            self.game_init = True
            # Start pygame
            self.pygame_canvas.run_pygame(lambda:self.game.main(True))    # Indico que llame a la función local para iniciar el juego pygame

    def set_library(self, link, anchor=None):
        self.toolbox.set_current_toolbar(2)
        self.health_library.set_url(link, anchor)
    
    def _load_last_cb(self, event):
        metadata = self.get_last_game()
        if metadata:
            self.metadata['title'] = metadata['title']
            self.make_toolbox(True)
            self.toolbox.set_current_toolbar(1)
    
    def game_over_callback(self):
        self.make_toolbox(False)
        self.toolbox.set_current_toolbar(0)             # Move to game tab
        
    def write_file(self, file_path):
        if self.game.started:
            try:
                self.game.save_game(file_path)
            except Exception,e:
                print "Error writting to file"
                print e
                raise e
        else:
            raise NotImplementedError
    
    def game_loaded(self):
        self.game.loaded_game = self.loaded_game
        self.make_toolbox(True)
        self.toolbox.set_current_toolbar(1)     # Loading an older game, move to game tab
    
    def read_file(self, file_path):
        logging.debug("Read file")
        # load data from file for this datastore entry in to the data variable
        fd = open(file_path, 'r')
        try:
            data = fd.read()
            self.loaded_game = data
            self.game_loaded()
        except Exception,e:
            print "Error loading data"
            print e
        finally:
            fd.close()
    
    def get_last_game(self):
        """ Make a query in the datastore to load last game """
        
        metadata = None
        
        # This query returns the last activity instance that has a path
        ds_objects, num_objects = datastore.find({'activity': 'org.ceibaljam.Saludame'}, sorting='-mtime', properties=['uid', 'title', 'mtime'])
        for entry in ds_objects:
            filepath = entry.get_file_path()
            if filepath:
                metadata = entry.get_metadata()
                filepath = entry.get_file_path()
                print "Last game is ", metadata['title'], " ", metadata['mtime']
                self.read_file(filepath)
                break
                
        for entry in ds_objects:
            entry.destroy()
            
        return metadata
        
        # This query returns the last activity instance that has a path
        #ds_objects, num_objects = datastore.find({'activity': 'org.ceibaljam.Saludame'}, sorting='mtime', properties=['uid', 'title', 'mtime'])
        
    def get_game_toolbar(self):
        
        toolbar = gtk.Toolbar()
        
        # Music Volume scale
        min = 0
        max = 10
        step = 1
        default = 3
        
        image = gtk.Image()
        image.set_from_file("assets/music/music_icon.png")
        image.show()
        
        tool_item = gtk.ToolItem()
        tool_item.set_expand(False)
        tool_item.add(image)
        tool_item.show()
        toolbar.insert(tool_item, -1)
        
        adj = gtk.Adjustment(default, min, max, step)
        scale = gtk.HScale(adj)
        scale.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
        scale.set_size_request(240,15)
        scale.set_draw_value(False)
        scale.connect("value-changed", self.game.volume_changed)
        scale.show()
                
        tool_item = gtk.ToolItem()
        tool_item.set_expand(False)
        tool_item.add(scale)
        tool_item.show()
        toolbar.insert(tool_item, -1)
        
        toolbar.show()
        return toolbar
        