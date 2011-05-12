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

import gtk
import pango
from gettext import gettext as _
    
def get_button(path):
    img = gtk.Image()
    img.set_from_file(path)
    btn = gtk.Button()
    btn.set_image(img)
    return btn

class StartupWindow(gtk.VBox):
    
    def __init__(self, start_cb, load_last_game_cb):
        gtk.VBox.__init__(self, False)
        
        self.start_cb = start_cb
        self.load_last_game_cb = load_last_game_cb
        
        self.set_welcome()

    def set_welcome(self):
        for child in self.get_children():
            self.remove(child)
        
        self.add(Welcome(self.start_cb, self._new_game, self.load_last_game_cb))
        self.show_all()
        
    def _new_game(self, button):
        for child in self.get_children():
            self.remove(child)
        
        self.add(SelectGenderAndName(self._gender_selected))
    
    def _gender_selected(self, name, gender):
        for child in self.get_children():
            self.remove(child)
        
        callback = lambda: self.start_cb(gender, name)
        self.add(Introduction(callback))

class Welcome(gtk.Fixed):
    
    def __init__(self, start_cb, new_game_cb, load_last_game_cb):
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
        
        self.show_all()

class SelectGenderAndName(gtk.Fixed):
    
    def __init__(self, callback):
        gtk.Fixed.__init__(self)
        
        self.callback = callback
        
        image = gtk.Image()
        image.set_from_file("assets/slides/screen_name_and_gender.jpg")
        self.put(image, 0, 0)

        self.kid_name = PlaceholderEntry(_('Escribe un nombre'))
        font = 'dejavu 24'
        font_desc = pango.FontDescription(font)
        self.kid_name.modify_font(font_desc)
        self.kid_name.set_has_frame(False)
        self.kid_name.set_size_request(776, 98)
        self.put(self.kid_name, 213, 127)
        
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


class PlaceholderEntry(gtk.Entry):

    _default = True

    def __init__(self, placeholder):
        gtk.Entry.__init__(self)
        self.placeholder = placeholder
        self._focus_out_event(self, None)
        self.connect('focus-in-event', self._focus_in_event)
        self.connect('focus-out-event', self._focus_out_event)

    def _focus_in_event(self, widget, event):
        if self._default:
            self.set_text('')
            self.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))

    def _focus_out_event(self, widget, event):
        if gtk.Entry.get_text(self) == '':
            self.set_text(self.placeholder)
            self.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('gray'))
            self._default = True
        else:
            self._default = False

    def get_text(self):
        if self._default:
            return ''
        return gtk.Entry.get_text(self)

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
        self.put(btn_next, 1087, 604)
        
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
        
if __name__ == "__main__":
    sw = StartupWindow(None)
    main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    main_window.set_size_request(1200,700)
    main_window.add(sw)
    main_window.show_all()
    gtk.main()
