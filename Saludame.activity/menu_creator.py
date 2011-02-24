# -*- coding: utf-8 -*-

import menu
import pygame
from gettext import gettext as _
import utilities
import gui

items = [
    # ("display_name", "action_id", "super_tooltip", [Children], place_restrictions, time_restrictions),
    
    (_("Eat..."), None, None, [
        
        (_("Comidas completas..."), None, None, [
            
            (_("Stew"), "eat_stew", "Eat a stew with \nfrench fries", None),
            (_("Currasco"), "eat_churrasco", "Eat a churrasco with \nfrench fries", None),
            #(_("Carpincho"), "eat_beaver", None),
            (_("Milanesa"), "eat_milanesa", None, None),
            (_("Torta frita"), "eat_torta_frita", None, None),
            (_("Ensalada"), "salad", None, None),
            (_("Pascualina"), "pascualina", None, None),
            #(_("Tortilla de verdura"), "tortilla_verdura", None),
            
        ]),
        
        (_("Fruta..."), None, None, [
            
            (_("Manzana"), "eat_apple", None, None),
            (_("Naranja"), "eat_orange", None, None),

            (_("Banana"), "eat_banana", None, None),
            (_("Kiwi"), "eat_kiwi", None, None),
            
        ]),
        
        (_("Desayuno y merienda..."), None, None, [
            
            (_("Tostadas con membrillo"), "tostadas_membrillo", None, None),
            (_("Queso"), "tostadas_queso", None, None),
            (_("Galletitas saladas"), "galletitas_saladas", None, None),
            (_("Galletitas dulces"), "galletitas_dulces", None, None),
            (_("Galletitas con dulce de leche"), "galletitas_dulce_leche", None, None),
            (_("Leche chocolatada"), "leche_chocolatada", None, None),
            (_("Café con leche"), "leche_cafe", None, None),
            (_("Leche"), "leche", None, None),
            (_("Leche con cereales"), "leche_cereales", None, None)],
            ["schoolyard", "home"], ["morning", "afternoon"]
        ),
        
        (_("Líquidos..."), None, None, [
            
            (_("Agua"), "agua", None, None),
            (_("Limonada"), "limonada", None, None),
            (_("Jugo de naranja"), "jugo_naranja", None, None),
            (_("Jugo de peras"), "jugo_peras", None, None),
            (_("Jugo de zanahorias"), "jugo_zanahorias", None, None),
            
        ]),
        
    ]),
    
    (_("Deportes..."), None, None, [
        (_("Run"), "sport_run", None, None),
        (_("Jump the rope"), "sport_jump", None, None),
        (_("Play footbal"), "sport_football", None, None),
    ]),
    
    (_("Tiempo libre..."), None, None, [
        (_("Go to sleep"), "sp_sleep", None, None),
        (_("Talk with a friend"), "sp_talk", None, None),
        (_("Do homework"), "sp_study", None, None),
        (_("Clean up the bedroom"), "sp_clean", None, None),
        (_("Cocinar"), "sp_cook", None, None),
        (_("Huerta..."), None, None, [
            (_("Arar"), "sp_plow", None, None),
            (_("Cosechar"), "sp_harvest", None, None),
            (_("Regar"), "sp_irrigate", None, None),
            (_("Sembrar"), "sp_sow", None, None),
            (_("Limpiar"), "sp_clean_earth", None, None),
        ]),
        (_("Diversión..."), None, None, [
            (_("Locuras"), "crazy", None, None),
            (_("Bailar"), "dance", None, None),
            (_("Escondida"), "hidenseek", None, None),
            (_("Jugar XO"), "playXO", None, None),
            (_("Leer"), "read", None, None),
            (_("Cantar"), "sing", None, None),
        ]),
        
    ]),
    
    (_("Ir a..."), None, None, [
       (_("Schoolyard"), "goto_schoolyard", None, None),
       (_("Country"), "goto_country", None, None),
       (_("Classroom"), "goto_classroom", None, None),
       (_("Square"), "goto_square", None, None),
       (_("Home..."), None, None, [
            (_("Living room"), "goto_living", None, None),
            (_("Bedroom"), "goto_bedroom", None, None),
            (_("Kitchen"), "goto_kitchen", None, None),
        ])
   ]),
   
    (_("Cambiar de ropa..."), None, None, [
        (_("School"), "change_school_clothes", None, None),
        (_("Sunny"), "change_sunny_clothes", None, None),
        (_("Rainy"), "change_rainy_clothes", None, None),
    ]),
   
   (_("Higiene..."), None, None, [
       (_("Bañarse"), "shower", None, None),
       (_("Cepillarse los dientes"), "brush_teeth", None, None),
       (_("Lavarse las manos"), "wash_hands", None, None),
       (_("Ir al baño"), "toilet", None, None),
       (_("Ir al Dentista"), "dentist", None, None),
       (_("Ir al Doctor"), "doctor", None, None),
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
    if item_tuple[3] != None:
        subitems = [create_item(sub_item, a_menu, container, font) for sub_item in item_tuple[3]]
    else:
        subitems = []
    lenght = len(item_tuple)
    item = None
    if lenght == 4:
        item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], "", item_tuple[1], item_tuple[2], subitems, a_menu, font)
    elif lenght == 5: # the item has place restrictions
        item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], "", item_tuple[1], item_tuple[2], subitems, a_menu, font, item_tuple[4])
    elif lenght == 6: # the item has time restrictions
        item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], "", item_tuple[1], item_tuple[2], subitems, a_menu, font, item_tuple[4], item_tuple[5])
    return item
