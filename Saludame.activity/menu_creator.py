# -*- coding: utf-8 -*-

import menu
import pygame
from gettext import gettext as _
import utilities
import gui

items = [
    # ("display_name", "path_to_icon.png", "action_id", "super_tooltip", [Children]),
    
    (_("Eat..."), "assets/icons/icon_parent.png", None, None, [
        
        (_("Comidas completas..."), "assets/icons/icon_parent.png", None, None, [
            
            (_("Stew"), "assets/icons/icon.png", "eat_stew", "Eat a stew with \nfrench fries", None),
            (_("Currasco"), "assets/icons/icon.png", "eat_churrasco", "Eat a churrasco with \nfrench fries", None),
            #(_("Carpincho"), "assets/icons/icon.png", "eat_beaver", None),
            (_("Milanesa"), "assets/icons/icon.png", "eat_milanesa", None, None),
            (_("Torta frita"), "assets/icons/icon.png", "eat_torta_frita", None, None),
            (_("Ensalada"), "assets/icons/icon.png", "salad", None, None),
            (_("Pascualina"), "assets/icons/icon.png", "pascualina", None, None),
            #(_("Tortilla de verdura"), "assets/icons/icon.png", "tortilla_verdura", None),
            
        ]),
        
        (_("Fruta..."), "assets/icons/icon_parent.png", None, None, [
            
            (_("Manzana"), "assets/icons/icon.png", "eat_apple", None, None),
            (_("Naranja"), "assets/icons/icon.png", "eat_orange", None, None),

            (_("Banana"), "assets/icons/icon.png", "eat_banana", None, None),
            (_("Kiwi"), "assets/icons/icon.png", "eat_kiwi", None, None),
            
        ]),
        
        (_("Desayuno y merienda..."), "assets/icons/icon_parent.png", None, None, [
            
            (_("Tostadas con membrillo"), "assets/icons/icon.png", "tostadas_membrillo", None, None),
            (_("Queso"), "assets/icons/icon.png", "tostadas_queso", None, None),
            (_("Galletitas saladas"), "assets/icons/icon.png", "galletitas_saladas", None, None),
            (_("Galletitas dulces"), "assets/icons/icon.png", "galletitas_dulces", None, None),
            (_("Galletitas con dulce de leche"), "assets/icons/icon.png", "galletitas_dulce_leche", None, None),
            (_("Leche chocolatada"), "assets/icons/icon.png", "leche_chocolatada", None, None),
            (_("Café con leche"), "assets/icons/icon.png", "leche_cafe", None, None),
            (_("Leche"), "assets/icons/icon.png", "leche", None, None),
            (_("Leche con cereales"), "assets/icons/icon.png", "leche_cereales", None, None)],
            ["schoolyard", "home"], ["morning", "afternoon"]
        ),
        
        (_("Líquidos..."), "assets/icons/icon_parent.png", None, None, [
            
            (_("Agua"), "assets/icons/icon.png", "agua", None, None),
            (_("Limonada"), "assets/icons/icon.png", "limonada", None, None),
            (_("Jugo de naranja"), "assets/icons/icon.png", "jugo_naranja", None, None),
            (_("Jugo de peras"), "assets/icons/icon.png", "jugo_peras", None, None),
            (_("Jugo de zanahorias"), "assets/icons/icon.png", "jugo_zanahorias", None, None),
            
        ]),
        
    ]),
    
    (_("Deportes..."), "assets/icons/icon_parent.png", None, None, [
        (_("Run"), "assets/icons/icon.png", "sport_run", None, None),
        (_("Jump the rope"), "assets/icons/icon.png", "sport_jump", None, None),
        (_("Play footbal"), "assets/icons/icon.png", "sport_football", None, None),
    ]),
    
    (_("Tiempo libre..."), "assets/icons/icon_parent.png", None, None, [
        (_("Go to sleep"), "assets/icons/icon.png", "sp_sleep", None, None),
        (_("Talk with a friend"), "assets/icons/icon.png", "sp_talk", None, None),
        (_("Do homework"), "assets/icons/icon.png", "sp_study", None, None),
        (_("Clean up the bedroom"), "assets/icons/icon.png", "sp_clean", None, None),
        
        (_("Diversión..."), "assets/icons/icon_parent.png", None, None, [
            (_("Locuras"), "assets/icons/icon.png", "crazy", None, None),
            (_("Bailar"), "assets/icons/icon.png", "dance", None, None),
            (_("Escondida"), "assets/icons/icon.png", "hidenseek", None, None),
            (_("Jugar XO"), "assets/icons/icon.png", "playXO", None, None),
            (_("Leer"), "assets/icons/icon.png", "read", None, None),
            (_("Cantar"), "assets/icons/icon.png", "sing", None, None),
        ]),
        
    ]),
    
    (_("Ir a..."), "assets/icons/icon_parent.png", None, None, [
       (_("Schoolyard"), "assets/icons/icon.png", "goto_schoolyard", None, None),
       (_("Country"), "assets/icons/icon.png", "goto_country", None, None),
       (_("Classroom"), "assets/icons/icon.png", "goto_classroom", None, None),
       (_("Square"), "assets/icons/icon.png", "goto_square", None, None),
       (_("Home..."), "assets/icons/icon_parent.png", None, None, [
            (_("Living room"), "assets/icons/icon.png", "goto_living", None, None),
            (_("Bedroom"), "assets/icons/icon.png", "goto_bedroom", None, None),
            (_("Kitchen"), "assets/icons/icon.png", "goto_kitchen", None, None),
        ])
   ]),
   
    (_("Cambiar de ropa"), "assets/icons/icon_parent.png", None, None, [
        (_("School"), "assets/icons/icon.png", "change_school_clothes", None, None),
        (_("Sunny"), "assets/icons/icon.png", "change_sunny_clothes", None, None),
        (_("Rainy"), "assets/icons/icon.png", "change_rainy_clothes", None, None),
    ]),
   
   (_("Higiene..."), "assets/icons/icon_parent.png", None, None, [
       (_("Bañarse"), "assets/icons/icon.png", "shower", None, None),
       (_("Lavarse los dientes"), "assets/icons/icon.png", "brush_teeth", None, None),
       (_("Lavarse las manos"), "assets/icons/icon.png", "wash_hands", None, None),
       (_("Ir al baño"), "assets/icons/icon.png", "toilet", None, None),
   ]),
   
]

MENU_FRAME_RATE = 1

def load_menu(game_manager, center, container, windows_controller):
    font = gui.get_font(20)
    m = menu.Menu(1, container, windows_controller, [], center, 90, game_manager, font)
    for item in items:
        an_item = create_item(item, m, container, font)
        m.add_item(an_item)
    m.calculate()
    
    return m
    

def create_item(item_tuple, a_menu, container, font):
    if item_tuple[4] != None:
        subitems = [create_item(sub_item, a_menu, container, font) for sub_item in item_tuple[4]]
    else:
        subitems = []
    lenght = len(item_tuple)
    item = None
    if lenght == 5:
        item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], item_tuple[1], item_tuple[2], item_tuple[3], subitems, a_menu, font)
    elif lenght == 6: # the item has place restrictions
        item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], item_tuple[1], item_tuple[2], item_tuple[3], subitems, a_menu, font, item_tuple[5])
    elif lenght == 7: # the item has time restrictions
        item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], item_tuple[1], item_tuple[2], item_tuple[3], subitems, a_menu, font, item_tuple[5], item_tuple[6])
    return item
