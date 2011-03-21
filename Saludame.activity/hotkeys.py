# -*- coding: utf-8 -*-

import game_manager
import pygame

##HOTKEYS HANDLERS

def alt_l_plus_handling():
    print "SUBIR DE NIVEL"
    if game_manager.instance:
        game_manager.instance.next_level()

def alt_l_minus_handling():
    print "BAJAR DE NIVEL"
    if game_manager.instance:
        game_manager.instance.previous_level()

def alt_c_2_handling():
    print u"MULTIPLE CHOICE"
    if game_manager.instance:
        game_manager.instance.windows_controller.main_window.kidW._cb_button_click_mc_challenges(None)
    
def alt_c_3_handling():
    print "MASTER CHALLENGE"
    if game_manager.instance:
        game_manager.instance.windows_controller.main_window.kidW._cb_button_click_master_challenge(None)

def alt_c_4_handling():
    print "TRUE OR FALSE"
    if game_manager.instance:
        game_manager.instance.windows_controller.main_window.kidW._cb_button_click_tf_challenges(None)

def alt_c_5_handling():
    print "COOKING"
    if game_manager.instance:
        game_manager.instance.windows_controller.main_window.kidW._cb_button_click_cooking_challenge(None)

def alt_shift_o_handling():
    print "ADD SOCIAL EVENT"
    if game_manager.instance:
        game_manager.instance.add_random_social_event()

def alt_shift_p_handling():
    print "ADD PERSONAL EVENT"
    if game_manager.instance:
        game_manager.instance.add_random_personal_event()

def alt_shift_w_handling():
    print "GET NEW WEATHER"
    if game_manager.instance:
        game_manager.instance.change_current_weather()

def alt_shift_g_handling():
    print "RESET GAME"
    if game_manager.instance:
        game_manager.instance.reset_game()

def alt_shift_t_handling():
    print "CHANGE TIME"
    if game_manager.instance:
        game_manager.instance.change_time()

def alt_shift_a_handling():
    print "10 POINTS"
    if game_manager.instance: 
        game_manager.instance.add_points(10)

# HOTKEYS DIC
hotkeys = {
    (pygame.K_LALT, pygame.K_l, pygame.K_PLUS): alt_l_plus_handling,
    (pygame.K_LALT, pygame.K_l, pygame.K_MINUS): alt_l_minus_handling,
    (pygame.K_LALT, pygame.K_c, pygame.K_2): alt_c_2_handling,
    (pygame.K_LALT, pygame.K_c, pygame.K_3): alt_c_3_handling,
    (pygame.K_LALT, pygame.K_c, pygame.K_4): alt_c_4_handling,
    (pygame.K_LALT, pygame.K_c, pygame.K_5): alt_c_5_handling,
    (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_o): alt_shift_o_handling, 
    (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_p): alt_shift_p_handling, 
    (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_w): alt_shift_w_handling,
    (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_t): alt_shift_t_handling,
    (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_g): alt_shift_g_handling,
    (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_a): alt_shift_a_handling,
}

class HotKeyHandler:
    
    def __init__(self):
        """constructor
        """
        self.buff = [] #pressed keys buffer

    def handle_keydown(self, event):
        """handle key down
        """
        self.buff.append(event.key)
        if len(self.buff) >= 3:
            self.verify_hot_key()
            self.buff = []
    
    def handle_keyup(self, event):
        """handle key up
        """
        self.buff = []

    def verify_hot_key(self):
        """verifies if the player is pressing
        hotkeys
        """
        try:
            print "HOTKEY:"
            hotkeys[(self.buff[0], self.buff[1], self.buff[2])]()
        except:
            print u"COMBINACIÓN DE TECLAS NO ENCONTRADA"

