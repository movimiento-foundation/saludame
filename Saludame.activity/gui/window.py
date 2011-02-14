# -*- coding: utf-8 -*-

import pygame
import widget

class Window:
    
    # Una ventana contiene 'n' widgets
    
    def __init__(self, container, rect, frame_rate, windows_controller, register_id, bg_color=None):
        self.container = container
        self.rect = pygame.Rect(container.left + rect.left, container.top + rect.top, rect.width, rect.height)
        self.frame_rate = frame_rate
        self.background = pygame.Surface(rect.size)
        self.bg_color = bg_color
        self.bg_image = None
        self.windows_controller = windows_controller
        self.parent = None
        
        # Register
        self.register_id = register_id
        self.windows_controller.register_new_window(register_id, self)
        
        self.widgets = [] # Widgets contained in the window
        self.windows = [] # SubWindows contained in the window
        self.buttons = [] # Buttons contained in the window
        self.childs = [] # The sum of widgets, buttons and subwindows, usefull to keep adding order
        
        self.repaint = True
        
        self.visible = True
        self.__erased = True           # after hidding a window it's background should be restored, that's why we need this flag
        
        self.dirty_background = True    # Indicates the background its dirty, so it must be redrawn and so every child.
        self.dirty = True               # Indicates the window has at least a dirty child
    
    def get_register_id(self):
        return self.register_id
    
    def set_bg_image(self, image, alpha=True):
        if not isinstance(image, pygame.Surface):
            # Is a path, convert it to a surface
            self.bg_image = pygame.image.load(image).convert_alpha()
        else:
            self.bg_image = image
        
    def set_bg_color(self, color):
        self.bg_color = color
        
    def dispose(self):
        self.windows_controller.unregister_window(self)
    
    def update(self, frames):
        if self.visible:
            for win in self.windows:
                if frames % win.frame_rate == 0:
                    win.update(frames)
            
            for widget in self.widgets:
                if frames % widget.frame_rate == 0:
                    widget.update(frames)

    # Abstract function.
    def pre_draw(self, screen):
        return []
    
    # Logica de pintado de cualquier ventana
    def draw(self, screen, frames, forced=False):
        
        changes = []
        
        if self.visible:
            
            if self.repaint:                    # repaint is old, keep it for compatibility
                self.dirty_background = True
                
            if self.dirty_background:
                forced = True

            # Restores the regions where dirty windows/widgets are
            changes += self._restore_background(screen, forced)
            self.repaint = self.dirty = self.dirty_background = False
            
            changes += self.pre_draw(screen)
            
            for child in self.childs:
                if isinstance(child, Window):
                    if child.dirty or child.dirty_background or forced:
                        changes.extend(child.draw(screen, frames, forced))
                else:
                    if child.dirty or forced:
                        changes.append(child.draw(screen))

            if forced:
                changes = [self.rect]   # When the whole window was forced, the changes are the whole window
            
        return changes
    
    def _restore_background(self, screen, forced):
        """ Restores the background in the dirty regions"""
        
        changes = []
        if self.bg_image:
            if forced:
                screen.blit(self.bg_image, self.rect.topleft)
            else:
                for win in self.windows:
                    
                    if win.bg_image:
                        # No need to restore the screen, the subwindow will be redrawn over it
                        pass
                    
                    elif win.visible and (win.dirty or win.dirty_background):
                        relative_rect = win.rect.move([-coord for coord in self.rect.topleft])
                        screen.blit(self.bg_image, win.rect.topleft, relative_rect)
                        
                    elif not win.visible and not win.__erased:
                        win.__erased = True
                        relative_rect = win.rect.move([-coord for coord in self.rect.topleft])
                        screen.blit(self.bg_image, win.rect.topleft, relative_rect)
                        changes.append(win.rect)
                
                for widget in self.widgets:
                    if widget.dirty:
                        screen.blit(self.bg_image, widget.rect_absolute.topleft, widget.rect_in_container)
        return changes
        
    def set_dirty(self):
        self.dirty = True
        if self.parent and not self.parent.dirty:
            self.parent.set_dirty()
    
    def set_dirty_background(self):
        self.dirty_background = True
        if self.parent and not self.parent.dirty:
            self.parent.set_dirty()
    
    def hide(self):
        if self.visible:
            self.visible = False
            self.__erased = False
            self.set_dirty_background()
    
    def show(self):
        self.visible = True
        
    def add_child(self, widget):
        self.widgets.append(widget)
        self.childs.append(widget)
        widget.parent = self
        
    def remove_child(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
            self.childs.remove(widget)
            self.set_dirty_background()
        
    def add_button(self, button):
        self.add_child(button)
        self.buttons.append(button)
        button.parent = self
        
    def remove_button(self, button):
        if button in self.buttons:
            self.buttons.remove(button)
            self.remove_child(button)
            button.parent = None
            self.set_dirty_background()
    
    def clear_childs(self):
        for widget in self.widgets:
            widget.parent = None
            self.childs.remove(widget)
        self.buttons = []
        self.widgets = []
        self.set_dirty_background()
        
    def add_window(self, window):
        self.windows.append(window)
        self.childs.append(window)
        window.parent = self
        
    def remove_window(self, window):
        self.windows.remove(window)
        self.childs.remove(window)
        self.set_dirty_background()
    
    def enable_repaint(self):
        self.repaint = True
        for win in self.windows:
            win.enable_repaint()
    
    def is_transparent(self):
        return (self.bg_image or self.bg_color)
        
    def contains_point(self, x, y):
        return self.rect.collidepoint(x,y)
    
    def handle_mouse_down(self, (x, y)):
        stop = False
        
        for child in reversed(self.childs):
            
            if child.contains_point(x, y):
                if isinstance(child, widget.Widget):
                    # Tooltips
                    if child.showing_tooltip:
                        self.windows_controller.hide_active_tooltip()
                        child.showing_tooltip = False
                stop = child.handle_mouse_down((x, y))
                if stop:
                    break
            
        return stop
        
    def handle_mouse_over(self, (x, y)):
        
        for win in self.windows:
            if win.rect.collidepoint(x, y):
                self.windows_controller.set_mouse_on_window(win.register_id)
                win.handle_mouse_over((x,y))
        
        for widget in self.widgets:
            if widget.contains_point(x, y):
                if not widget.over:
                    # Tooltips
                    if widget.tooltip: # Si el boton tiene tooltip entonces lo mostramos
                        self.windows_controller.hide_active_tooltip()
                        self.windows_controller.show_tooltip(widget.tooltip)
                        widget.showing_tooltip = True
                    if widget.super_tooltip:
                        self.windows_controller.hide_active_tooltip()
                        self.windows_controller.show_super_tooltip(widget.super_tooltip)
                        widget.showing_tooltip = True
                    widget.on_mouse_over()
                    return # No seguimos buscando el botón
            else:
                # Ineficiente! Por ahora lo dejo asi para PROBAR
                # Esta todo el tiempo haciendo esto! Cambiar
                if widget.showing_tooltip:
                    # Si estabamos mostrando el tooltip ahora debemos esconderlo
                    self.windows_controller.hide_active_tooltip()
                    widget.showing_tooltip = False
                if widget.over:
                    widget.on_mouse_out()
    
    # It will be overridden by cooking challenge or other D&D challenge
    def handle_mouse_motion(self, (x, y)):
        pass

    # It will be overridden by cooking challenge or other D&D challenge
    def handle_mouse_up(self, pos):
        pass
    
    def move(self, (x, y)):
        """ Moves the window the given offset, notifying all its subitems """
        self.rect.move_ip(x, y)
        for win in self.windows:
            win.move(x, y, self.rect)
        
        # Buttons are usually in widget list, so they are not moved
        for widget in self.widgets:
            if not (self.rect is widget.container):
                widget.container.move_ip(x, y)
            widget.rect_absolute.move_ip(x, y)
       
    def get_background_and_owner(self):
        if self.bg_image:
            return (self.bg_image, self)
        elif self.bg_color:
            return (self.bg_color, self)
        elif self.parent:
            return self.parent.get_background_and_owner()
        else:
            return (None, None)
    
    def get_background(self):
        return self.get_background_and_owner()[0]
