# -*- coding: utf-8 -*-

import gtk
from gettext import gettext as _

class StartupWindow(gtk.VBox):
    
    def __init__(self, start_cb):
        gtk.VBox.__init__(self, False)
        
        self.start_cb = start_cb
        self.set_welcome()

    def set_welcome(self):
        for child in self.get_children():
            self.remove(child)
        
        self.add(Welcome(self.start_cb, self._new_game, self._load_last_game, self._load_game))
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

class Welcome(gtk.VBox):
    
    def __init__(self, start_cb, new_game_cb, load_last_game_cb, load_game_cb):
        gtk.VBox.__init__(self, False)
        
        self.start_cb = start_cb
        
        image = gtk.Image()
        image.set_from_file("credits/welcome.png")
        self.pack_start(image)
        
        buttons = gtk.HBox(False)
        
        btn_new = gtk.Button(_("New game"))
        btn_new.connect("clicked", new_game_cb)
        buttons.add(btn_new)
        
        btn_last_game = gtk.Button(_("Load last game"))
        btn_last_game.connect("clicked", load_last_game_cb)
        buttons.add(btn_last_game)
        
        btn_load_game = gtk.Button(_("Load game from journal"))
        btn_load_game.connect("clicked", load_game_cb)
        buttons.add(btn_load_game)
        
        self.pack_start(buttons)
        
        self.show_all()
    
    
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
        btn_boy.set_size_request(-1, 24)
        self.add(btn_boy)
        
        btn_girl = gtk.Button(_("Girl"))
        btn_girl.connect("clicked", self._girl)
        btn_girl.set_size_request(-1, 24)
        self.add(btn_girl)
        
        self.show_all()
        
    def _boy(self, button):
        self.callback(self.kid_name.get_text(), "boy")

    def _girl(self, button):
        self.callback(self.kid_name.get_text(), "girl")


story = [
    
    #Slide1
    {
        "image": "customization/boy.png",
        "text": "En la escuela los niños están esperando la gran competencia de deportes anual.\nTodos saben que para ganar la competencia es necesario estar sanos."
    },
    
    #Slide2
    {
        "image": "customization/boy.png",
        "text": "Para estar preparados física y mentalmente, deberás mantener altas las barras de Estado físico, Higiene, Alimentación y Tiempo Libre.\nCuanto más altas estén las barras, más puntos ganarás y así podrás avanzar de nivel."
    },

    #Slide3
    {
        "image": "customization/girl.png",
        "text": "Ten cuidado con eventos que aparecerán en el juego, cuando un evento esté activo tus barras bajarán más rápido, por eso es importante investigar y encontrar la forma de solucionarlo."
    },

    #Slide4
    {
        "image": "customization/girl.png",
        "text": "Para estar sano es importante alimentarse correctamente, estar limpios, hacer ejercicio y divertirse! Cuando quieras hacer estas cosas, haz click en el personaje.\n¿Estás listo?"
    }
    
]

class Introduction(gtk.VBox):
    
    def __init__(self, callback):
        gtk.VBox.__init__(self, False)
        
        self.callback = callback
        
        self.index = 0
        
        self.show_slide()
        
    
    def show_slide(self):
        
        for child in self.get_children():
            self.remove(child)
            
        slide = story[self.index]
        
        image = gtk.Image()
        image.set_from_file(slide["image"])
        self.pack_start(image)
        
        # HBox with buttons
        hbox = gtk.HBox(False)
        btn_back = gtk.Button(_("< Back"))
        btn_back.connect("clicked", self._back)
        btn_back.set_size_request(-1, 24)
        hbox.pack_start(btn_back)
        if self.index == 0:
            btn_back.set_sensitive(False)
        
        btn_next = gtk.Button(_("Next >"))
        btn_next.connect("clicked", self._next)
        btn_next.set_size_request(-1, 24)
        hbox.pack_start(btn_next)
        self.pack_start(hbox)
        
        text_view = gtk.TextView()
        text_buffer = text_view.get_buffer()
        text_buffer.set_text(slide["text"])
        text_view.set_wrap_mode(gtk.WRAP_WORD)
        self.pack_start(text_view, False, False)
        self.show_all()
        
    def _next(self, button):
        if self.index + 1 < len(story):
            self.index += 1
            self.show_slide()
        else:
            self.callback()
        
    def _back(self, button):
        if self.index > 0:
            self.index -= 1
            self.show_slide()
        