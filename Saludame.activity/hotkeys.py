# -*- coding: utf-8 -*-

from game_manager import GameManager
import pygame

##HOTKEYS HANDLERS

def alt_l_plus_handling():
    print "SUBIR DE NIVEL"

def alt_l_minus_handling():
    print "BAJAR DE NIVEL"

def alt_c_1_handling():
    print u"SUPER DESAFÍO"

def alt_c_2_handling():
    print "MASTER CHALLENGE"

def alt_c_3_handling():
    print "TRUE OR FALSE"

def alt_c_4_handling():
    print "COOKING"

def alt_shift_s_handling():
    print "ADD SOCIAL EVENT"

def alt_shift_p_handling():
    print "ADD PERSONAL EVENT"

def alt_shift_w_handling():
    print "GET NEW WEATHER"

## HOTKEYS DEF
ALT_L_PLUS = (pygame.K_LALT, pygame.K_l, pygame.K_PLUS)
ALT_L_MINUS = (pygame.K_LALT, pygame.K_l, pygame.K_MINUS)
ALT_C_1 = (pygame.K_LALT, pygame.K_c, pygame.K_1)
ALT_C_2 = (pygame.K_LALT, pygame.K_c, pygame.K_2)
ALT_C_3 = (pygame.K_LALT, pygame.K_c, pygame.K_3)
ALT_C_4 = (pygame.K_LALT, pygame.K_c, pygame.K_4)
ALT_SHIFT_S = (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_s)
ALT_SHIFT_P = (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_p)
ALT_SHIFT_W = (pygame.K_LALT, pygame.K_LSHIFT, pygame.K_w)

##HOTKEYS DIC
hotkeys = {ALT_L_PLUS: alt_l_plus_handling,
           ALT_L_MINUS: alt_l_minus_handling, 
           ALT_C_1: alt_c_1_handling, 
           ALT_C_2: alt_c_2_handling, 
           ALT_C_3: alt_c_3_handling, 
           ALT_C_4: alt_c_4_handling, 
           ALT_SHIFT_S: alt_shift_s_handling, 
           ALT_SHIFT_P: alt_shift_p_handling, 
           ALT_SHIFT_W: alt_shift_w_handling
           }

class HotKeyHandler:
    
    def __init__(self):
        """constructor
        """
        self.buff = [] #pressed keys buffer

    def handle_keydown(self, event):
        """handle key down
        """
        print 
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

