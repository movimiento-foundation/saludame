# -*- coding: utf-8 -*-

import gtk
from gettext import gettext as _

class StartupWindow(gtk.VBox):
    
    def __init__(self, start_cb):
        gtk.VBox.__init__(self, False)
        
        self.start_cb = start_cb
        
        btn_new = gtk.Button(_("New game"))
        btn_new.connect("clicked", self._new_game)
        self.add(btn_new)

        btn_last_game = gtk.Button(_("Load last game"))
        btn_last_game.connect("clicked", self._load_last_game)
        self.add(btn_last_game)
        
        btn_load_game = gtk.Button(_("Load game from journal"))
        btn_load_game.connect("clicked", self._load_game)
        self.add(btn_load_game)
        
        self.show_all()
        
    def _new_game(self, button):
        for child in self.get_children():
            self.remove(child)
        
        self.add(SelectGenderAndName(self._gender_selected))
    
    def _load_last_game(self, button):
        pass
    
    def _load_game(self, button):
        pass
    
    def _gender_selected(self, name, gender, grade = 3):
        for child in self.get_children():
            self.remove(child)
        
        self.add(Introduction(self.start_cb))

class SelectGenderAndName(gtk.VBox):
    
    def __init__(self, callback):
        gtk.VBox.__init__(self, False)
        
        self.callback = callback
        
        hbox = gtk.HBox(False)
        
        label = gtk.Label(_("Name"))
        hbox.pack_start(label, False, False)
        
        self.kid_name = gtk.Entry()
        hbox.pack_start(self.kid_name, True, True)
        
        self.pack_start(hbox, False, False)
        
        btn_boy = gtk.Button(_("Boy"))
        btn_boy.connect("clicked", self._boy)
        self.add(btn_boy)
        
        btn_girl = gtk.Button(_("Girl"))
        btn_girl.connect("clicked", self._girl)
        self.add(btn_girl)
        
        self.show_all()
        
    def _boy(self, button):
        self.callback(self.kid_name.get_text(), "boy")

    def _girl(self, button):
        self.callback(self.kid_name.get_text(), "girl")

class Introduction(gtk.VBox):
    
    def __init__(self, callback):
        gtk.VBox.__init__(self, False)
        
        self.callback = callback
        
        image = gtk.Image()
        image.set_from_file("customization/boy.png")
        self.pack_start(image)
        
        # HBox with buttons
        hbox = gtk.HBox(False)
        btn_back = gtk.Button(_("< Back"))
        btn_back.connect("clicked", self._back)
        hbox.pack_start(btn_back)
        btn_next = gtk.Button(_("Next >"))
        btn_next.connect("clicked", self._next)
        hbox.pack_start(btn_next)
        self.pack_start(hbox)
        
        text_view = gtk.TextView()
        text_buffer = text_view.get_buffer()
        text_buffer.set_text("Hola, Pedrito tiene qué cuidarse para no enfermarse, para eso es muy importante cuidar la alimentación, higiene, actividad física y las actividades que hace en su tiempo libre.")
        text_view.set_wrap_mode(gtk.WRAP_WORD)
        self.pack_start(text_view, False, False)
        self.show_all()
    
    def _next(self, button):
        self.callback()
        
    def _back(self, button):
        pass
    