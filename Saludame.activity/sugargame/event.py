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
import gobject
import pygame
import pygame.event
import logging 

log = logging.getLogger('Sugargame')
log.setLevel(logging.DEBUG)

class _MockEvent(object):
    def __init__(self, keyval):
        self.keyval = keyval

class Translator(object):
    key_trans = {
        'Alt_L': pygame.K_LALT,
        'Alt_R': pygame.K_RALT,
        'Control_L': pygame.K_LCTRL,
        'Control_R': pygame.K_RCTRL,
        'Shift_L': pygame.K_LSHIFT,
        'Shift_R': pygame.K_RSHIFT,
        'Super_L': pygame.K_LSUPER,
        'Super_R': pygame.K_RSUPER,
        'KP_Page_Up' : pygame.K_KP9, 
        'KP_Page_Down' : pygame.K_KP3,
        'KP_End' : pygame.K_KP1, 
        'KP_Home' : pygame.K_KP7,
        'KP_Up' : pygame.K_KP8,
        'KP_Down' : pygame.K_KP2,
        'KP_Left' : pygame.K_KP4,
        'KP_Right' : pygame.K_KP6,

    }
    
    mod_map = {
        pygame.K_LALT: pygame.KMOD_LALT,
        pygame.K_RALT: pygame.KMOD_RALT,
        pygame.K_LCTRL: pygame.KMOD_LCTRL,
        pygame.K_RCTRL: pygame.KMOD_RCTRL,
        pygame.K_LSHIFT: pygame.KMOD_LSHIFT,
        pygame.K_RSHIFT: pygame.KMOD_RSHIFT,
    }
    
    def __init__(self, mainwindow, inner_evb):
        """Initialise the Translator with the windows to which to listen"""
        self._mainwindow = mainwindow
        self._inner_evb = inner_evb

        # Enable events
        # (add instead of set here because the main window is already realized)
        self._mainwindow.add_events(
            gtk.gdk.EXPOSURE_MASK | \
            gtk.gdk.KEY_PRESS_MASK | \
            gtk.gdk.KEY_RELEASE_MASK \
        )
        
        self._inner_evb.set_events(
            gtk.gdk.POINTER_MOTION_MASK | \
            gtk.gdk.POINTER_MOTION_HINT_MASK | \
            gtk.gdk.BUTTON_MOTION_MASK | \
            gtk.gdk.BUTTON_PRESS_MASK | \
            gtk.gdk.BUTTON_RELEASE_MASK
        )

        self._mainwindow.set_flags(gtk.CAN_FOCUS)
        self._inner_evb.set_flags(gtk.CAN_FOCUS)
        
        # Internal data
        self.__stopped = False
        self.__keystate = [0] * 323
        self.__button_state = [0,0,0]
        self.__mouse_pos = (0,0)
        self.__repeat = (None, None)
        self.__held = set()
        self.__held_time_left = {}
        self.__held_last_time = {}
        self.__tick_id = None
        
        self.__hooked = False

    def hook_pygame(self):
        # Callback functions to link the event systems
        self.m_quit = self._mainwindow.connect('unrealize', self._quit_cb)
        self.m_keydown = self._mainwindow.connect('key_press_event', self._keydown_cb)
        self.m_keyup = self._mainwindow.connect('key_release_event', self._keyup_cb)
        self.m_expose = self._mainwindow.connect('expose-event', self._expose_cb)
        
        self.i_keydown = self._inner_evb.connect('key_press_event', self._keydown_cb)
        self.i_keyup = self._inner_evb.connect('key_release_event', self._keyup_cb)
        self.i_mousedown = self._inner_evb.connect('button_press_event', self._mousedown_cb)
        self.i_mouseup = self._inner_evb.connect('button_release_event', self._mouseup_cb)
        self.i_mousemove = self._inner_evb.connect('motion-notify-event', self._mousemove_cb)
        self.i_resize = self._inner_evb.connect('configure-event', self._resize_cb)
        
        # Hook pygame functions to this class functions
        pygame.key.get_pressed = self._get_pressed
        pygame.key.set_repeat = self._set_repeat
        pygame.mouse.get_pressed = self._get_mouse_pressed
        pygame.mouse.get_pos = self._get_mouse_pos
        
        self.real_pygame_set_mode = pygame.display.set_mode
        pygame.display.set_mode = self._set_display_mode
        
        self.__hooked = True
        
    def unhook_pygame(self):
        if self.__hooked:
            self._mainwindow.disconnect(self.m_quit)
            self._mainwindow.disconnect(self.m_keydown)
            self._mainwindow.disconnect(self.m_keyup)
            self._mainwindow.disconnect(self.m_expose)
            
            self._mainwindow.disconnect(self.i_keydown)
            self._mainwindow.disconnect(self.i_keyup)
            self._mainwindow.disconnect(self.i_mousedown)
            self._mainwindow.disconnect(self.i_mouseup)
            self._mainwindow.disconnect(self.i_mousemove)
            self._mainwindow.disconnect(self.i_resize)
            self.__hooked = False
        
    def _expose_cb(self, event, widget):
        if pygame.display.get_init():
            pygame.event.post(pygame.event.Event(pygame.VIDEOEXPOSE))
        return False # continue processing
    
    def _resize_cb(self, widget, event):
        evt = pygame.event.Event(pygame.VIDEORESIZE, 
                                 size=(event.width,event.height), width=event.width, height=event.height)
        pygame.event.post(evt)
        return False # continue processing

    def _quit_cb(self, data=None):
        self.__stopped = True
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _keydown_cb(self, widget, event):
        key = event.keyval
        if key in self.__held:
            return True
        else:
            if self.__repeat[0] is not None:
                self.__held_last_time[key] = pygame.time.get_ticks()
                self.__held_time_left[key] = self.__repeat[0]
            self.__held.add(key)
            
        return self._keyevent(widget, event, pygame.KEYDOWN)
        
    def _keyup_cb(self, widget, event):
        key = event.keyval
        if self.__repeat[0] is not None:
            if key in self.__held:
                # This is possibly false if set_repeat() is called with a key held
                del self.__held_time_left[key]
                del self.__held_last_time[key]
        self.__held.discard(key)

        return self._keyevent(widget, event, pygame.KEYUP)
        
    def _keymods(self):
        mod = 0
        for key_val, mod_val in self.mod_map.iteritems():
            mod |= self.__keystate[key_val] and mod_val
        return mod
        
    def _keyevent(self, widget, event, type):
        key = gtk.gdk.keyval_name(event.keyval)
        if key is None:
            log.warning("Missing key %s" % event.keyval)
            # No idea what this key is.
            return False 
        
        log.debug("Key event. Key: %s, Type: %s" % (key, type))
        
        keycode = None
        if key in self.key_trans:
            keycode = self.key_trans[key]
        elif hasattr(pygame, 'K_'+key.upper()):
            keycode = getattr(pygame, 'K_'+key.upper())
        elif hasattr(pygame, 'K_'+key.lower()):
            keycode = getattr(pygame, 'K_'+key.lower())
        elif key == 'XF86Start':
            # view source request, specially handled...
            self._mainwindow.view_source()
        else:
            print 'Key %s unrecognized' % key
            
        if keycode is not None:
            if type == pygame.KEYDOWN:
                mod = self._keymods()
            self.__keystate[keycode] = type == pygame.KEYDOWN
            if type == pygame.KEYUP:
                mod = self._keymods()
            ukey = unichr(gtk.gdk.keyval_to_unicode(event.keyval))
            if ukey == '\000':
                ukey = ''
            evt = pygame.event.Event(type, key=keycode, unicode=ukey, mod=mod)
            self._post(evt)
            
        return True

    def _get_pressed(self):
        return self.__keystate

    def _get_mouse_pressed(self):
        return self.__button_state

    def _mousedown_cb(self, widget, event):
        self.__button_state[event.button-1] = 1
        return self._mouseevent(widget, event, pygame.MOUSEBUTTONDOWN)

    def _mouseup_cb(self, widget, event):
        self.__button_state[event.button-1] = 0
        return self._mouseevent(widget, event, pygame.MOUSEBUTTONUP)
        
    def _mouseevent(self, widget, event, type):
        evt = pygame.event.Event(type, button=event.button, pos=(event.x, event.y))
        self._post(evt)
        return True
        
    def _mousemove_cb(self, widget, event):
        # From http://www.learningpython.com/2006/07/25/writing-a-custom-widget-using-pygtk/
        # if this is a hint, then let's get all the necessary 
        # information, if not it's all we need.
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state

        rel = (x - self.__mouse_pos[0], y - self.__mouse_pos[1])
        self.__mouse_pos = (x, y)
        
        self.__button_state = [
            state & gtk.gdk.BUTTON1_MASK and 1 or 0,
            state & gtk.gdk.BUTTON2_MASK and 1 or 0,
            state & gtk.gdk.BUTTON3_MASK and 1 or 0,
        ]
        
        evt = pygame.event.Event(pygame.MOUSEMOTION,
                                 pos=self.__mouse_pos, rel=rel, buttons=self.__button_state)
        self._post(evt)
        return True
        
    def _tick_cb(self):
        cur_time = pygame.time.get_ticks()
        for key in self.__held:
            delta = cur_time - self.__held_last_time[key] 
            self.__held_last_time[key] = cur_time
            
            self.__held_time_left[key] -= delta
            if self.__held_time_left[key] <= 0:
                self.__held_time_left[key] = self.__repeat[1]
                self._keyevent(None, _MockEvent(key), pygame.KEYDOWN)
                
        return True
        
    def _set_repeat(self, delay=None, interval=None):
        if delay is not None and self.__repeat[0] is None:
            self.__tick_id = gobject.timeout_add(10, self._tick_cb)
        elif delay is None and self.__repeat[0] is not None:
            gobject.source_remove(self.__tick_id)
        self.__repeat = (delay, interval)
        
    def _get_mouse_pos(self):
        return self.__mouse_pos

    def _post(self, evt):
        try:
            pygame.event.post(evt)
        except pygame.error, e:
            if str(e) == 'Event queue full':
                print "Event queue full!"
                pass
            else:
                raise e

    def _set_display_mode(self, resolution=(0,0), flags=0, depth=0):
        """ Hook version of pygame.event.set_mode
      
        It calls the real pygame function and then takes the new resolution
        and centers the inner event box in the main window.
        """
        self.real_pygame_set_mode(resolution, flags, depth)
      
        # Center the widget sometimes doesn't work right
        #width, height = resolution
        #window_rect = self._mainwindow.get_allocation()
      
        #x, y = 0, 0
      
        #if width < window_rect.width:
            #x = (window_rect.width - width) / 2.0

        #if height < window_rect.height:
            #y = (window_rect.height - height) / 2.0

        #rect = gtk.gdk.Rectangle(x, y, width, height)
      
        #self._inner_evb.size_allocate(rect)
