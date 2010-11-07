# -*- coding: utf-8 -*-

import menu
import pygame
from gettext import gettext as _

example = [
    # ("display_name", "path_to_icon.png", "action_id", [Children]),
    
    (_("Eat"), "assets/icons/icon_parent.png", None, [
        
        (_("Complete meals"), "assets/icons/icon_parent.png", None, [
            
            (_("Stew"), "assets/icons/icon.png", "eat_stew", None),
            (_("Currasco"), "assets/icons/icon.png", "eat_churrasco", None),
            (_("Carpincho"), "assets/icons/icon.png", "eat_beaver", None),
            (_("Milanesa"), "assets/icons/icon.png", "eat_milanesa", None),
            (_("Torta frita"), "assets/icons/icon.png", "eat_torta_frita", None),
            (_("Ensalada"), "assets/icons/icon.png", "salad", None),
            (_("Pascualina"), "assets/icons/icon.png", "pascualina", None),
            (_("Tortilla de verdura"), "assets/icons/icon.png", "tortilla_verdura", None),
            
        ]),
        
        ("fruit", "assets/icons/icon_parent.png", _("Fruta"), None, [
            
            ("eat_apple", "assets/icons/icon.png", _("Manzana"), "eat_apple", None),
            ("eat_orange", "assets/icons/icon.png", _("Naranja"), "eat_orange", None),
            ("eat_banana", "assets/icons/icon.png", _("Banana"), "eat_banana"), None,
            ("eat_kiwi", "assets/icons/icon.png", _("Kiwi"), "eat_kiwi", None),
            
        ]),
        
        ("breakfast", "assets/icons/icon_parent.png", _("Desayuno y merienda"), None, [
            
            (_("Tostadas con membrillo"), "assets/icons/icon.png", "tostadas_membrillo", None),
            (_("Queso"), "assets/icons/icon.png", "tostadas_queso", None),
            (_("Galletitas saladas"), "assets/icons/icon.png", "galletitas_saladas", None),
            (_("Galletitas dulces"), "assets/icons/icon.png", "galletitas_dulces", None),
            (_("Galletitas con dulce de leche"), "assets/icons/icon.png", "galletitas_dulce_leche", None),
            (_("Leche chocolatada"), "assets/icons/icon.png", "leche_chocolatada"), None,
            (_("Café con leche"), "assets/icons/icon.png", "leche_cafe", None),
            (_("Leche"), "assets/icons/icon.png", "leche", None),
            (_("Leche con cereales"), "assets/icons/icon.png", "leche_cereales", None),
            
        ]),
        
    ]),
    
    (_("Do sports..."), "assets/icons/icon_parent.png", None, [
        (_("Run"), "assets/icons/icon.png", "sport_run", None),
        (_("Jump the rope"), "assets/icons/icon.png", "sport_jump", None),
        (_("Play footbal"), "assets/icons/icon.png", "sport_football", None)
    ]),
    
    (_("Tiempo libre..."), "assets/icons/icon_parent.png", None, [
        (_("Go to sleep"), "assets/icons/icon.png", "sleep_sleep", None),
        (_("Talk with a friend"), "assets/icons/icon.png", "talk_talk", None),
        (_("Do homework"), "assets/icons/icon.png", "study_study", None),
        (_("Clean up the bedroom"), "assets/icons/icon.png", "clean_clean", None)
    ])
]

MENU_FRAME_RATE = 1

def load_menu(character, center, container, windows_controller):
    
    m = menu.Menu(1, container, windows_controller, [], center, 90, character)
    for item in example:
        an_item = create_item(item, m, container)
        m.add_item(an_item)
    m.calculate()
    
    return m
    

def create_item(item_tuple, a_menu, container):
    if item_tuple[3] != None:
        an_item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], item_tuple[1], item_tuple[2], [create_item(sub_item, a_menu, container) for sub_item in item_tuple[3]], a_menu)
    else:
        an_item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], item_tuple[1], item_tuple[2], [], a_menu)
    return an_item
    






