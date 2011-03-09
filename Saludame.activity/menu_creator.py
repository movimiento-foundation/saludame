# -*- coding: utf-8 -*-

import menu
import pygame
from gettext import gettext as _
import utilities
import gui

items = [
    # ("display_name", "action_id", "super_tooltip", [Children], place_restrictions, time_restrictions),
    
    (_("Alimentarse..."), None, None, [
        
        (_("Almuerzo..."), None, None, [
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
            
            (_("Frutas..."), None, None, [
                (_("Manzana"), "manzana", None, None),
                (_("Naranja"), "naranja", None, None),
                (_("Banana"), "banana", None, None),
                (_("Ciruelas"), "ciruelas", None, None),
                (_("Pelón"), "pelon", None, None),
                (_("Ciruelas"), "ciruelas", None, None),
                (_("Frutillas"), "frutillas", None, None),
                (_("Durazno"), "durazno", None, None),
                (_("Mandarina"), "mandarina", None, None),
            ]),
        ]),
        
        (_("Desayuno y merienda..."), None, None, [
            
            (_("Bebidas..."), None, None, [
                (_("Leche"), "leche", None, None),
                (_("Leche Chocolatada"), "leche_chocolatada", None, None),
                (_("Café con leche"), "leche_cafe", None, None),
                (_("Yogur"), "yogur", None, None),
                (_("Jugo Natural"), "jugo_natural", None, None),
                (_("Licuado con Leche"), "licuado", None, None),
                (_("refresco"), "refresco", None, None),
                (_("Mate"), "mate", None, None),
                (_("Café"), "cafe", None, None),
            ]),
            
            (_("Platos..."), None, None, [
                (_("Pan con queso"), "pan_queso", None, None),
                (_("Pan con manteca"), "pan_manteca", None, None),
                (_("Galletas con dulce"), "galletas_dulce", None, None),
                (_("Torta frita"), "torta_frita", None, None),
                (_("Refuerzo fiambre"), "refuerzo_fiambre", None, None),
                (_("Bizcochos"), "bizcochos", None, None),
                (_("Torta"), "torta", None, None),
                (_("Rosca Chicharrones"), "rosca_chicharrones", None, None),
            ]),
            
            (_("Frutas..."), None, None, [
                (_("Manzana"), "manzana", None, None),
                (_("Naranja"), "naranja", None, None),
                (_("Banana"), "banana", None, None),
                (_("Ciruelas"), "ciruelas", None, None),
                (_("Pelón"), "pelon", None, None),
                (_("Ciruelas"), "ciruelas", None, None),
                (_("Frutillas"), "frutillas", None, None),
                (_("Durazno"), "durazno", None, None),
                (_("Mandarina"), "mandarina", None, None),
            ]),
            
            (_("Golosinas y Snacks..."), None, None, [
                (_("Papas chips"), "papas_chips", None, None),
                (_("Ticholos"), "ticholos", None, None),
                (_("Rapadura"), "rapadura", None, None),
                (_("Caramelo"), "caramelo", None, None),
                (_("Galletitas dulces"), "galletitas_dulces", None, None),
                (_("Alfajor"), "alfajor", None, None),
                (_("Chicle"), "chicle", None, None),
                (_("Chupetin"), "chupetin", None, None),
                (_("Chocolate"), "chocolate", None, None),
            ]),
            
            (_("Otros..."), None, None, [
                (_("Pan con queso"), "pan_queso", None, None),
                (_("Pan con manteca"), "pan_manteca", None, None),
                (_("Galletas con dulce"), "galletas_dulce", None, None),
                (_("Torta frita"), "torta_frita", None, None),
                (_("Refuerzo fiambre"), "refuerzo_fiambre", None, None),
                (_("Bizcochos"), "bizcochos", None, None),
                (_("Torta"), "torta", None, None),
                (_("Rosca Chicharrones"), "rosca_chicharrones", None, None),
            ])
        ],
        None, ["morning", "afternoon"]
        ),
        
        (_("Líquidos..."), None, None, [
            
            (_("Agua"), "agua", None, None),
            (_("Limonada"), "limonada", None, None),
            (_("Jugo de naranja"), "jugo_naranja", None, None),
            (_("Jugo de peras"), "jugo_peras", None, None),
            (_("Jugo de zanahorias"), "jugo_zanahorias", None, None),
            
        ]),
        
    ]),
    
    (_("Diversión..."), None, None, [
        (_("Jugar XO"), "playXO", None, None),
        (_("Escondida"), "hidenseek", None, None),
        #(_("Jugar con Amigo"), "play_friend", None, None),
        (_("Rayuela"), "hopscotch", None, None),
        (_("Ver televisión"), "tv", None, None),
        (_("Leer"), "read", None, None),
        (_("Escuchar música"), "music", None, None),
        (_("Locuras"), "crazy", None, None),
        (_("Bailar"), "dance", None, None),
        (_("Cantar"), "sing", None, None),
    ]),
    
    (_("Hacer..."), None, None, [
        (_("Talk with a friend"), "talk", None, None),
        (_("Do homework"), "study", None, None),
        (_("Clean up the bedroom"), "clean", None, None),
        (_("Cocinar"), "help_cook", None, None),
        (_("Cambiar de ropa..."), None, None, [
            (_("School"), "change_school_clothes", None, None),
            (_("Normal"), "change_regular_clothes", None, None),
        ]),
        (_("Deporte..."), None, None, [
            (_("Run"), "sport_run", None, None),
            (_("Jump the rope"), "sport_jump", None, None),
            (_("Play footbal"), "sport_football", None, None),
        ]),
    ]),
    
    (_("Ir a..."), None, None, [
        (_("Schoolyard"), "goto_schoolyard", None, None),
        (_("Classroom"), "goto_classroom", None, None),
        (_("Square"), "goto_square", None, None),
        (_("Home..."), None, None, [
            (_("Living room"), "goto_livingroom", None, None),
            (_("Bedroom"), "goto_bedroom", None, None),
        ]),
        (_("Ir al baño"), "toilet", None, None),
        (_("Go to sleep"), "sleep", None, None),
        (_("Ir al médico..."), None, None, [
            (_("Dentista"), "dentist", None, None),
            (_("Doctor"), "doctor", None, None),
        ])
   ]),
   
   (_("Higiene..."), None, None, [
       (_("Bañarse"), "shower", None, None),
       (_("Cepillarse los dientes"), "brush_teeth", None, None),
       (_("Lavarse las manos"), "wash_hands", None, None),
   ]),
   
   (_("Huerta..."), None, None, [
       (_("Preparar tierra"), "farm_plow", None, None),
       (_("Sembrar"), "farm_sow", None, None),
       (_("Mantener"), None , None, [
           (_("Regar"), "farm_irrigate", None, None),
           (_("Fumigar"), "farm_fumigate", None, None),
           (_("Limpiar"), "farm_clean", None, None),
       ]),
       (_("Cocechar"), "farm_harvest", None, None),
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
