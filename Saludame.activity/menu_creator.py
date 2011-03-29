# -*- coding: utf-8 -*-

import menu
import pygame
from gettext import gettext as _
import utilities
import gui

MA = ["morning", "afternoon"]
NN = ["night", "noon"]

CC = ["bedroom", "livingroom"]
EP = ["schoolyard", "square"]
ALL_BUT_SQUARE = ["bedroom", "livingroom", "schoolyard", "classroom"]

items = [
    # ("display_name", "action_id", "tooltip", [Children], place_restrictions, time_restrictions),
    
    (_("Alimentarse..."), None, None, [
        
        # Platos desayuno y merienda
        (_("Platos..."), None, None, [
            (_("Pan con queso"), "pan_queso", None, None),
            (_("Pan con manteca"), "pan_manteca", None, None),
            (_("Galletas con dulce"), "galletas_dulce", None, None),
            (_("Torta frita"), "torta_frita", None, None),
            (_("Refuerzo fiambre"), "refuerzo_fiambre", None, None),
            (_("Bizcochos"), "bizcochos", None, None),
            (_("Torta"), "torta", None, None),
            (_("Rosca Chicharrones"), "rosca_chicharrones", None, None),
        ], [], MA),
        
        # Platos almuerzo y cena
        (_("Platos..."), None, None, [
            ("Sopa de verduras", "sopa_verduras", None, None),
            ("Ensopado con carne y verduras", "e_carne_verduras", None, None),
            ("Guiso con arroz, carne, lentejas y verduras", "g_arroz_carne_lenteja_verdura", None, None),
            ("Puchero", "puchero", None, None),
            ("Milanesa frita con papas fritas", "milanesa_papas_fritas", None, None),
            ("Costilla de cordero con huevo frito", "costilla_cordero_huevo", None, None),
            ("Cordero y arroz con choclo", "cordero_arroz_choclo", None, None),
            ("Churrasco con puré de zapallo", "churrasco_pure_zapallo", None, None),
            ("Pollo al horno con ensalada", "pollo_horno_ensalada", None, None),
            ("Lengua con polenta", "lengua_polenta", None, None),
            ("Hamburguesa con papas fritas", "hamburguesa_papas_fritas", None, None),
            ("Albóndigas con fideos", "albondiga_fideo", None, None),
            ("Carne al horno con papas y boniatos", "carne_papas", None, None),
            ("Asado de vaca con ensalada", "carne_vaca_ensalada", None, None),
            ("Asado de cordero con puré", "carne_cordero_pure", None, None),
            ("Tarta de jamón y queso", "tarta_jamon_queso", None, None),
            ("Panchos con huevo frito", "panchos_huevo", None, None),
            ("Chorizo al pan", "choripan", None, None),
            ("Polenta con tuco", "polenta", None, None),
            ("Tallarines con tuco", "tallarines", None, None),
            ("Ñoquis con tuco", "ñoquis", None, None),
            ("Ravioles de verdura con tuco", "ravioles_verdura", None, None),
            ("Tortilla de papa y ensalada", "tortilla_papa", None, None),
            ("Pizza", "pizza", None, None),
            ("Tarta de zapallo", "tarta_zapallo", None, None),
            ("Pascualina", "pascualina", None, None),
            ("Canelones de verdura", "canelones_verdura", None, None),
            ("Zapallitos rellenos", "zapallitos_rellenos", None, None),     
        ], [], NN),
           
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
        
        (_("Bebidas..."), None, None, [
            # Ambos
            ("Agua", "agua", None, None),
            ("Jugo natural", "jugo_natural", None, None),
            ("Leche", "leche", None, None),
            ("Licuado con leche", "licuado", None, None),
            ("Refresco", "refresco", None, None),
            
            # Desayuno
            ("Leche chocolatada", "leche_chocolatada", None, None, [], MA),
            ("Yogur", "yogur", None, None, [], MA),
            ("Mate", "mate", None, None, [], MA),
            ("Café", "cafe", None, None, [], MA),
            
            # Cena
            ("Agua con gas", "agua_c_gas", None, None, [], NN),
            ("Jugo de compota", "jugo_compota", None, None, [], NN),
            ("Jugo artificial", "jugo_artificial", None, None, [], NN),
            ("Vino", "vino", None, None, [], NN),
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
            # Desayuno
            ("Avena con leche", "avena_leche", None, None, [], MA),
            ("Arroz con leche", "arroz_leche", None, None, [], MA),
            ("Crema", "crema", None, None, [], MA),
            ("Flan", "flan", None, None, [], MA),
            
            # Cena
            ("Martín fierro", "martin_fierro", None, None, [], NN),
            ("Torta frita", "torta_frita", None, None, [], NN),
            ("Torta dulce", "torta_dulce", None, None, [], NN),
        ]),
    ]),
    
    (_("Diversión..."), None, None, [
        (_("Jugar XO"), "playXO", None, None),
        (_("Escondida"), "hidenseek", None, None, EP),
        #(_("Jugar con Amigo"), "play_friend", None, None),
        (_("Rayuela"), "hopscotch", None, None, None, EP),
        (_("Ver televisión"), "tv", None, None, "livingroom"),
        (_("Leer"), "read", None, None),
        (_("Escuchar música"), "music", None, None, CC),
        (_("Locuras"), "crazy", None, None),
        (_("Bailar"), "dance", None, None, ["bedroom", "livingroom", "school", "square"]),
        (_("Cantar"), "sing", None, None, ["bedroom", "livingroom", "school", "square"]),
    ]),
    
    (_("Hacer..."), None, None, [
        (_("Talk with a friend"), "talk", None, None),
        (_("Do homework"), "homework", None, None),
        (_("Clean up the bedroom"), "clean", None, None, ["bedroom"]),
        (_("Tareas domésticas"), "housekeeping", None, None, CC),
        (_("Ayudar en el campo"), "help_field", None, None, CC),
        (_("Cocinar"), "help_cook", None, None, CC),
        (_("Descanzar"), "relax", None, None, CC + ["square"]),
        (_("Cambiar de ropa..."), None, None, [
            (_("School"), "change_school_clothes", None, None),
            (_("Normal"), "change_regular_clothes", None, None),
        ]),
        (_("Deporte..."), None, None, [
            (_("Run"), "sport_run", None, None, EP),
            (_("Jump the rope"), "sport_jump", None, None, EP),
            (_("Play footbal"), "sport_football", None, None, EP),
        ]),
        (_("Go to sleep"), "sleep", None, None, ["bedroom"]),
    ]),
    
    (_("Ir a..."), None, None, [
        (_("Schoolyard"), "goto_schoolyard", None, None),
        (_("Classroom"), "goto_classroom", None, None),
        (_("Square"), "goto_square", None, None),
        (_("Home..."), None, None, [
            (_("Living room"), "goto_livingroom", None, None),
            (_("Bedroom"), "goto_bedroom", None, None),
        ]),
        (_("Ir al médico..."), None, None, [
            (_("Dentista"), "dentist", None, None),
            (_("Doctor"), "doctor", None, None),
        ])
   ]),
   
   (_("Higiene..."), None, None, [
       (_("Bañarse"), "shower", None, None, ALL_BUT_SQUARE),
       (_("Cepillarse los dientes"), "brush_teeth", None, None, ALL_BUT_SQUARE),
       (_("Lavarse las manos"), "wash_hands", None, None, ALL_BUT_SQUARE),
       (_("Ir al baño"), "toilet", None, None, ALL_BUT_SQUARE),
   ]),
   
   (_("Huerta..."), None, None, [
       (_("Preparar tierra"), "farm_plow", None, None, ALL_BUT_SQUARE),
       (_("Sembrar"), "farm_sow", None, None, ALL_BUT_SQUARE),
       (_("Mantener"), None , None, [
           (_("Regar"), "farm_irrigate", None, None),
           (_("Fumigar"), "farm_fumigate", None, None),
           (_("Limpiar"), "farm_clean", None, None),
       ], ALL_BUT_SQUARE),
       (_("Cocechar"), "farm_harvest", None, None, ALL_BUT_SQUARE),
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
    
    label = item_tuple[0]
    if not isinstance(label, unicode):
        label = unicode(label.decode("utf-8"))
        
    action_id = item_tuple[1]
    tooltip = item_tuple[2]

    place_restrictions = None
    time_restrictions = None
    if lenght > 4: # the item has place restrictions
        place_restrictions = item_tuple[4]
    
    if lenght > 5: # the item has time restrictions
        time_restrictions = item_tuple[5]
    
    item = menu.Item(container, MENU_FRAME_RATE, label, "", action_id, tooltip, subitems, a_menu, font, place_restrictions, time_restrictions)
    return item
