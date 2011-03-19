# -*- coding: utf-8 -*-

import gtk
from gettext import gettext as _

def get_button(path):
    img = gtk.Image()
    img.set_from_file(path)
    btn = gtk.Button()
    btn.set_image(img)
    return btn

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
    
    def _gender_selected(self, name, gender):
        for child in self.get_children():
            self.remove(child)
        
        callback = lambda: self.start_cb(gender, name)
        self.add(Introduction(callback))

class Welcome(gtk.Fixed):
    
    def __init__(self, start_cb, new_game_cb, load_last_game_cb, load_game_cb):
        gtk.Fixed.__init__(self)

        self.start_cb = start_cb
        
        image = gtk.Image()
        image.set_from_file("assets/slides/screen_mainmenu.jpg")
        self.put(image, 0, 0)
        
        btn_new = get_button("assets/layout/btn_new_game.png")
        btn_new.connect("clicked", new_game_cb)
        self.put(btn_new, 490, 386)
        
        btn_last_game = get_button("assets/layout/btn_load_last.png")
        btn_last_game.connect("clicked", load_last_game_cb)
        self.put(btn_last_game, 490, 500)
        
        btn_load_game = get_button("assets/layout/btn_from_journal.png")
        btn_load_game.connect("clicked", load_game_cb)
        self.put(btn_load_game, 490, 620)

        self.show_all()

class SelectGenderAndName(gtk.Fixed):
    
    def __init__(self, callback):
        gtk.Fixed.__init__(self)
        
        self.callback = callback
        
        image = gtk.Image()
        image.set_from_file("assets/slides/screen_name_and_gender.jpg")
        self.put(image, 0, 0)

        self.kid_name = gtk.Entry()
        self.put(self.kid_name, 225, 150)
        
        btn_boy = get_button("assets/layout/btn_boy.png")
        btn_boy.connect("clicked", self._boy)
        self.put(btn_boy, 210, 260)
        
        btn_girl = get_button("assets/layout/btn_girl.png")
        btn_girl.connect("clicked", self._girl)
        self.put(btn_girl, 750, 260)
        
        self.show_all()
        
    def _boy(self, button):
        self.callback(self.kid_name.get_text(), "boy")

    def _girl(self, button):
        self.callback(self.kid_name.get_text(), "girl")


story = [
    
    #Slide1
    {
        "image": "assets/slides/history1.jpg",
        "text": None
    },
    
    #Slide2
    {
        "image": "assets/slides/history2.jpg",
        "text": None
    },

    #Slide3
    {
        "image": "assets/slides/help.png",
        "text": None
    },
    
]

class Introduction(gtk.Fixed):
    
    def __init__(self, callback):
        gtk.Fixed.__init__(self)
        
        self.callback = callback
        
        self.index = 0
        
        self.show_slide()
        
    
    def show_slide(self):
        
        for child in self.get_children():
            self.remove(child)
            
        slide = story[self.index]
        
        # Image
        image = gtk.Image()
        image.set_from_file(slide["image"])
        self.put(image, 0, 0)
        
        # Text
        if slide["text"]:
            text_view = gtk.TextView()
            text_buffer = text_view.get_buffer()
            text_buffer.set_text(slide["text"])
            text_view.set_wrap_mode(gtk.WRAP_WORD)
            self.pack_start(text_view, False, False)
        
        btn_back = get_button("assets/layout/btn_back.png")
        btn_back.connect("clicked", self._back)
        self.put(btn_back, 0, 604)
        if self.index == 0:
            btn_back.set_sensitive(False)
        
        btn_next = get_button("assets/layout/btn_next.png")
        btn_next.connect("clicked", self._next)
        self.put(btn_next, 192, 604)
        
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
        