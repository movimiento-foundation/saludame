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
    
    (u"Alimentarse...", None, None, [
        
        # Platos desayuno y merienda
        (u"Platos...", None, None, [
            (u"Pan con queso", "pan_queso", None, None),
            (u"Pan con manteca", "pan_manteca", None, None),
            (u"Galletas con dulce", "galletas_dulce", None, None),
            (u"Torta frita", "torta_frita", None, None),
            (u"Refuerzo fiambre", "refuerzo_fiambre", None, None),
            (u"Bizcochos", "bizcochos", None, None),
            (u"Torta casera", "torta_dulce", None, None),
            (u"Rosca Chicharrones", "rosca_chicharrones", None, None),
        ], [], MA),
        
        # Platos almuerzo y cena
        (u"Platos...", None, None, [
            (u"Sopa de verduras", "sopa_verduras", None, None),
            (u"Ensopado", "e_carne_verduras", u"Con carne y verduras", None),
            (u"Guiso", "Con arroz, carne, lentejas y verduras", None, None),
            (u"Puchero", "puchero", None, None),
            (u"Milanesa frita", "milanesa_papas_fritas", u"Con papas fritas", None),
            (u"Costilla de cordero", "costilla_cordero_huevo", u"Con huevo frito", None),
            (u"Cordero", "cordero_arroz_choclo", u"Con arroz y choclo", None),
            (u"Churrasco", "Con puré de zapallo", None, None),
            (u"Pollo al horno", "pollo_horno_ensalada", u"Con ensalada", None),
            (u"Lengua con polenta", "lengua_polenta", None, None),
            (u"Hamburguesa", "hamburguesa_papas_fritas", u"Con papas fritas", None),
            (u"Albóndigas", "albondiga_fideo", u"Con fideos", None),
            (u"Carne al horno", "carne_papas", u"Con papas y boniatos", None),
            (u"Asado de vaca", "carne_vaca_ensalada", u"Con ensalada", None),
            (u"Asado de cordero", "carne_cordero_pure", u"Con puré de papas", None),
            (u"Tarta de jamón y queso", "tarta_jamon_queso", None, None),
            (u"Panchos", "panchos_huevo", u"Con huevo frito", None),
            (u"Chorizo al pan", "choripan", None, None),
            (u"Polenta con tuco", "polenta", None, None),
            (u"Tallarines con tuco", "tallarines", None, None),
            (u"Ñoquis con tuco", "ñoquis", None, None),
            (u"Ravioles de verdura", "ravioles_verdura", u"Con tuco", None),
            (u"Tortilla de papa", "tortilla_papa", u"Con ensalada", None),
            (u"Pizza", "pizza", None, None),
            (u"Tarta de zapallo", "tarta_zapallo", None, None),
            (u"Pascualina", "pascualina", None, None),
            (u"Canelones de verdura", "canelones_verdura", None, None),
            (u"Zapallitos rellenos", "zapallitos_rellenos", None, None),     
        ], [], NN),
           
        (u"Frutas...", None, None, [
            (u"Manzana", "manzana", None, None),
            (u"Naranja", "naranja", None, None),
            (u"Banana", "banana", None, None),
            (u"Ciruelas", "ciruelas", None, None),
            (u"Pelón", "pelon", None, None),
            (u"Ciruelas", "ciruelas", None, None),
            (u"Frutillas", "frutillas", None, None),
            (u"Durazno", "durazno", None, None),
            (u"Mandarina", "mandarina", None, None),
        ]),
        
        (u"Bebidas...", None, None, [
            # Ambos
            (u"Agua", "agua", None, None),
            (u"Jugo natural", "jugo_natural", None, None),
            (u"Leche", "leche", None, None),
            (u"Licuado con leche", "licuado", None, None),
            (u"Refresco", "refresco", None, None),
            
            # Desayuno
            ("Leche con cocoa", "leche_chocolatada", None, None, [], MA),
            ("Yogur", "yogur", None, None, [], MA),
            ("Mate", "mate", None, None, [], MA),
            ("Café", "cafe", None, None, [], MA),
            
            # Cena
            ("Agua con gas", "agua_c_gas", None, None, [], NN),
            ("Jugo de compota", "jugo_compota", None, None, [], NN),
            ("Jugo artificial", "jugo_artificial", None, None, [], NN),
        ]),
        
        (u"Golosinas y Snacks...", None, None, [
            (u"Papas chips", "papas_chips", None, None),
            (u"Ticholos", "ticholos", None, None),
            (u"Rapadura", "rapadura", None, None),
            (u"Caramelo", "caramelo", None, None),
            (u"Galletitas dulces", "galletitas_dulces", None, None),
            (u"Alfajor", "alfajor", None, None),
            (u"Chicle", "chicle", None, None),
            (u"Chupetin", "chupetin", None, None),
            (u"Chocolate", "chocolate", None, None),
        ]),
        
        (u"Otros...", None, None, [
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
        
        (u"Platos de la huerta...", None, None, [
            (u"Pasta la primavera", "pasta_primavera", u"Con fideos, chauchas y brócoli", None),
            (u"Pastel de lentejas", "pastel_lentajas", u"Con arroz, espinaca, morrón y zanahoria", None),
            (u"Tarta de zapallitos", "tarta_zapallitos", u"Con huevos", None),
            (u"Tarta de puerros", "tarta_puerros", u"Con huevos", None),
            (u"Polenta con acelga", "polenta_acelga", u"Con cebolla y morrón", None),
            (u"Budín de chauchas", "budin_chauchas", u"Con huevos, cebolla y morrón", None),
            (u"Guiso de berenjenas", "guiso_berenjenas", u"Con morrón y tomates", None),
            (u"Ensalada de lechuga ", "ensalada_lechuga", u"Con zanahoria y aceite", None),
            (u"Ensalada de remolacha", "ensalada_remolacha", u"Con huevos y aceite", None),
            (u"Ensalada Holandesa", "ensalada_holanesa", u"Con repollo, zanahoria,\ncebolla y aceite", None),
            (u"Ensalada pepinos", "ensalada_pepinos", u"Con tomates, perejil y aceite", None),
        ], [], NN),
    ]),
    
    (u"Diversión...", None, None, [
        (u"Jugar XO", "playXO", None, None),
        (u"Escondida", "hidenseek", None, None, EP),
        #(u"Jugar con Amigo", "play_friend", None, None),
        (u"Rayuela", "hopscotch", None, None, None, EP),
        (u"Ver televisión", "tv", None, None, ["livingroom"]),
        (u"Leer", "read", None, None),
        (u"Escuchar música", "music", None, None, CC),
        (u"Locuras", "crazy", None, None),
        (u"Bailar", "dance", None, None, ["bedroom", "livingroom", "school", "square"]),
        (u"Cantar", "sing", None, None, ["bedroom", "livingroom", "school", "square"]),
    ]),
    
    (u"Hacer...", None, None, [
        (u"Hablar con un amigo", "talk", None, None),
        (u"Hacer deberes", "homework", None, None),
        (u"Limpiar el cuarto", "clean", None, None, ["bedroom"]),
        (u"Tareas domésticas", "housekeeping", None, None, CC),
        (u"Ayudar en el campo", "help_field", None, None, CC),
        (u"Estudiar en la XO", "study_xo", None, None),
        (u"Cocinar", "help_cook", None, None, CC),
        (u"Descanzar", "relax", None, None, CC + ["square"]),
        (u"Cambiar de ropa...", None, None, [
            (u"Escuela", "change_school_clothes", None, None),
            (u"Normal", "change_regular_clothes", None, None),
        ]),
        (u"Deporte...", None, None, [
            (u"Correr", "sport_run", None, None, EP),
            (u"Saltar la cuerda", "sport_jump", None, None, EP),
            (u"Jugar al futbol", "sport_football", None, None, EP),
        ]),
        (u"Ir a dormir", "sleep", None, None, ["bedroom"]),
    ]),
    
    (u"Ir a...", None, None, [
        (u"Escuela", "goto_schoolyard", None, None),
        (u"Clase", "goto_classroom", None, None),
        (u"Plaza", "goto_square", None, None),
        (u"Casa...", None, None, [
            (u"Living", "goto_livingroom", None, None),
            (u"Habitación", "goto_bedroom", None, None),
        ]),
        (u"Ir al médico...", None, None, [
            (u"Dentista", "dentist", None, None),
            (u"Doctor", "doctor", None, None),
        ])
   ]),
   
   (u"Higiene...", None, None, [
       (u"Bañarse", "shower", None, None, ALL_BUT_SQUARE),
       (u"Cepillarse los dientes", "brush_teeth", None, None, ALL_BUT_SQUARE),
       (u"Lavarse las manos", "wash_hands", None, None, ALL_BUT_SQUARE),
       (u"Ir al baño", "toilet", None, None, ALL_BUT_SQUARE),
   ]),
   
   (u"Huerta...", None, None, [
       (u"Preparar tierra", "farm_plow", None, None, ALL_BUT_SQUARE),
       (u"Sembrar", "farm_sow", None, None, ALL_BUT_SQUARE),
       (u"Mantener...", None , None, [
           (u"Regar", "farm_irrigate", None, None),
           (u"Fumigar", "farm_fumigate", None, None),
           (u"Limpiar", "farm_clean", None, None),
       ], ALL_BUT_SQUARE),
       (u"Cocechar", "farm_harvest", None, None, ALL_BUT_SQUARE),
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
