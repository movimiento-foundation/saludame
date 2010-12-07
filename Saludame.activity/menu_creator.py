# -*- coding: utf-8 -*-

import menu
import pygame
from gettext import gettext as _
import utilities

example = [
    # ("display_name", "path_to_icon.png", "action_id", [Children]),
    
    (_("Eat..."), "assets/icons/icon_parent.png", None, [
        
        (_("Comidas completas..."), "assets/icons/icon_parent.png", None, [
            
            (_("Stew"), "assets/icons/icon.png", "eat_stew", None),
            (_("Currasco"), "assets/icons/icon.png", "eat_churrasco", None),
            #(_("Carpincho"), "assets/icons/icon.png", "eat_beaver", None),
            (_("Milanesa"), "assets/icons/icon.png", "eat_milanesa", None),
            (_("Torta frita"), "assets/icons/icon.png", "eat_torta_frita", None),
            (_("Ensalada"), "assets/icons/icon.png", "salad", None),
            (_("Pascualina"), "assets/icons/icon.png", "pascualina", None),
            #(_("Tortilla de verdura"), "assets/icons/icon.png", "tortilla_verdura", None),
            
        ]),
        
        (_("Fruta..."), "assets/icons/icon_parent.png", None, [
            
            (_("Manzana"), "assets/icons/icon.png", "eat_apple", None),
            (_("Naranja"), "assets/icons/icon.png", "eat_orange", None),
            (_("Banana"), "assets/icons/icon.png", "eat_banana", None),
            (_("Kiwi"), "assets/icons/icon.png", "eat_kiwi", None),
            
        ]),
        
        (_("Desayuno y merienda..."), "assets/icons/icon_parent.png", None, [
            
            (_("Tostadas con membrillo"), "assets/icons/icon.png", "tostadas_membrillo", None),
            (_("Queso"), "assets/icons/icon.png", "tostadas_queso", None),
            (_("Galletitas saladas"), "assets/icons/icon.png", "galletitas_saladas", None),
            (_("Galletitas dulces"), "assets/icons/icon.png", "galletitas_dulces", None),
            (_("Galletitas con dulce de leche"), "assets/icons/icon.png", "galletitas_dulce_leche", None),
            (_("Leche chocolatada"), "assets/icons/icon.png", "leche_chocolatada", None),
            (_("Café con leche"), "assets/icons/icon.png", "leche_cafe", None),
            (_("Leche"), "assets/icons/icon.png", "leche", None),
            (_("Leche con cereales"), "assets/icons/icon.png", "leche_cereales", None),
            
        ]),
        
        (_("Líquidos..."), "assets/icons/icon_parent.png", None, [
            
            (_("Agua"), "assets/icons/icon.png", "agua", None),
            (_("Limonada"), "assets/icons/icon.png", "limonada", None),
            (_("Jugo de naranja"), "assets/icons/icon.png", "jugo_naranja", None),
            (_("Jugo de peras"), "assets/icons/icon.png", "jugo_peras", None),
            (_("Jugo de zanahorias"), "assets/icons/icon.png", "jugo_zanahorias", None),
            
        ]),
        
    ]),
    
    (_("Deportes..."), "assets/icons/icon_parent.png", None, [
        (_("Run"), "assets/icons/icon.png", "sport_run", None),
        (_("Jump the rope"), "assets/icons/icon.png", "sport_jump", None),
        (_("Play footbal"), "assets/icons/icon.png", "sport_football", None),
        (_("Hide and Seek"), "assets/icons/icon.png", "sport_hide_seek", None)
    ]),
    
    (_("Tiempo libre..."), "assets/icons/icon_parent.png", None, [
        (_("Go to sleep"), "assets/icons/icon.png", "sp_sleep", None),
        (_("Talk with a friend"), "assets/icons/icon.png", "sp_talk", None),
        (_("Do homework"), "assets/icons/icon.png", "sp_study", None),
        (_("Clean up the bedroom"), "assets/icons/icon.png", "sp_clean", None)
    ]),
    
    (_("Ir a..."), "assets/icons/icon_parent.png", None, [
       (_("Schoolyard"), "assets/icons/icon.png", "goto_schoolyard", None),
       (_("Country"), "assets/icons/icon.png", "goto_country", None),
       (_("Classroom"), "assets/icons/icon.png", "goto_classroom", None),
       (_("Square"), "assets/icons/icon.png", "goto_square", None),
       (_("Home..."), "assets/icons/icon_parent.png", None, [
            (_("Living room"), "assets/icons/icon.png", "goto_living", None),
            (_("Bedroom"), "assets/icons/icon.png", "goto_bedroom", None),
            (_("Kitchen"), "assets/icons/icon.png", "goto_kitchen", None),
        ])
   ]),
   
    (_("Cambiar de ropa"), "assets/icons/icon_parent.png", None, [
        (_("School"), "assets/icons/icon.png", "change_school_clothes", None),
        (_("Sunny"), "assets/icons/icon.png", "change_sunny_clothes", None),
        (_("Rainy"), "assets/icons/icon.png", "change_rainy_clothes", None),
    ]),
   
   (_("Higiene..."), "assets/icons/icon_parent.png", None, [
       (_("Bañarse"), "assets/icons/icon.png", "shower", None),
       (_("Lavarse los dientes"), "assets/icons/icon.png", "brush_teeth", None),
       (_("Lavarse las manos"), "assets/icons/icon.png", "wash_hands", None),
       (_("Ir al baño"), "assets/icons/icon.png", "toilet", None),
   ])
]

MENU_FRAME_RATE = 1

def load_menu(character, center, container, windows_controller):
    font = utilities.get_font(20)
    m = menu.Menu(1, container, windows_controller, [], center, 90, character, font)
    for item in example:
        an_item = create_item(item, m, container, font)
        m.add_item(an_item)
    m.calculate()
    
    return m
    

def create_item(item_tuple, a_menu, container, font):
    if item_tuple[3] != None:
        subitems = [create_item(sub_item, a_menu, container, font) for sub_item in item_tuple[3]]
    else:
        subitems = []

    return menu.Item(container, MENU_FRAME_RATE, item_tuple[0], item_tuple[1], item_tuple[2], subitems, a_menu, font)

