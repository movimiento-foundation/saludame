# -*- coding: utf-8 -*-

import effects
import actions
import os

BARS_DECREASE_RATE = -0.1

#SOUNDS
BLIP_PATH = os.path.normpath("assets/sound/blip.ogg")
CHANGE_PLACE_PATH = os.path.normpath("assets/sound/place_change.ogg")
CHANGE_CLOTHES_PATH = os.path.normpath("assets/sound/clothes_change.ogg")
TWISTER_SOUND = os.path.normpath("assets/sound/place_change.ogg")

#ANIMATIONS
CHANGE_CLOTHES_ANIMATION_PATH = os.path.normpath("assets/kid/actions/twister")
CHEW_PATH = os.path.normpath("assets/kid/actions/eat")
DRINK_PATH = os.path.normpath("assets/kid/actions/drink")

# Action Icons
FRUIT_PATH = os.path.normpath("assets/action-icons/fruits")
BREAKFAST_PATH = os.path.normpath("assets/action-icons/breakfast")
STEW_PATH = os.path.normpath("assets/action-icons/stew")
ORCHARD_PATH = os.path.normpath("assets/action-icons/orchard")
COLD_DRINK_PATH = os.path.normpath("assets/action-icons/colddrink")
HOT_DRINK_PATH = os.path.normpath("assets/action-icons/hotdrink")

# BAR DECREASE EFFECT
# Formula to convert effects per minute into effects per CONTROL_INTERVAL
# factor = CONTROL_INTEVAL/(60 * FPS)
factor = float(16) / (60 * 14)
bars_rate_per_minute = [("energy",-2), ("defenses",-0.5), ("weight",0), ("c_leguminosas",-1.5), ("v_frutas",-1.5), ("c_huevos",-0.5), ("dulces",-10), ("g_aceites",-5), ("l_quesos",-5), ("agua",-2), ("shower",-1), ("w_hands",-1), ("b_teeth",-1), ("toilet",-2), ("sports",-1), ("fun",-1), ("relaxing",-1), ("housekeeping",-2), ("homework",-2), ("h_check",-0.2), ("farm",0)]
bar_dec_effect = effects.Effect(None, [(bar, rate*factor) for bar, rate in bars_rate_per_minute])

# Consequences of food actions (triggered events after eating)
CONS_FOOD = ["nauseas", "cepillar_dientes"]
CONS_MEAL = CONS_FOOD + ["stomach_ache"]

#actions list tuple format:
#[("action's id","icon_path","picture_path", appereance_probability, time_span,
#    kid_animation_frame_rate,kid_animation_loop_times, kid_animation_path, window_animation_frame_rate,
#    window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, action's effect)]

actions_list = [
    #id, appereance_probability, time_span_in_frames, kid_animation_loop_times, kid_animation_path, window_animation_frame_rate, window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, effect
    
    # Atention, default action when idle for long time
    ("attention", 0.3, 40, 0, "assets/kid/actions/atention", 3, 1, None, 4, "assets/sound/atention.ogg",
        effects.Effect(None, []), None, None, None
    ),
    
    # Drinks
    ("agua_c_gas", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("agua",12.5), ("defenses",10), ("toilet",-30)]), None, None, None
    ),
    ("agua", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("agua",12.5), ("defenses",10), ("toilet",-30)]), None, None, None
    ),
    ("jugo_natural", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",40), ("agua",12.5), ("energy",5), ("defenses",10), ("b_teeth",-30), ("toilet",-30)]), None, None, None
    ),
    ("jugo_compota", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("agua",12.5), ("defenses",10), ("b_teeth",-30), ("toilet",-30)]), None, None, None
    ),
    ("jugo_artificial", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("agua",12.5), ("energy",10), ("weight",0.5), ("b_teeth",-30), ("toilet",-30)]), None, None, None
    ),
    ("vino", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("energy",10), ("defenses",-50), ("weight",0.5), ("b_teeth",-30), ("toilet",-30)]), None, None, None
    ),
    ("refresco", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("agua",12.5), ("energy",10), ("weight",0.5), ("b_teeth",-30), ("toilet",-30)]), None, None, None
    ),
    ("mate", 0.3, 70, 0, DRINK_PATH, 3, 1, "assets/action-icons/mate", 4, BLIP_PATH,
        effects.Effect(None, [("b_teeth",-30), ("toilet",-30)]), None, [], None
    ),
    ("cafe", 0.3, 70, 0, DRINK_PATH, 3, 1, HOT_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("b_teeth",-30), ("toilet",-30)]), None, [], None
    ),
    
    # Milk
    ("leche", 0.3, 70, 0, DRINK_PATH, 3, 1, HOT_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos",50), ("agua",6.25), ("energy",20), ("defenses",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("leche_chocolatada", 0.3, 70, 0, DRINK_PATH, 3, 1, HOT_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",12.5), ("l_quesos",50), ("agua",6.25), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("yogur", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos",50), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("licuado", 0.3, 70, 0, DRINK_PATH, 3, 1, COLD_DRINK_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",40), ("dulces",25), ("l_quesos",50), ("agua",12.5), ("energy",20), ("defenses",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    
    # Meals - breakfast, tea
    ("pan_queso", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("l_quesos",50), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("pan_manteca", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("g_aceites",50), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("galletas_dulce", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("dulces",25), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("torta_frita", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("g_aceites",50), ("energy",10), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("refuerzo_fiambre", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("c_huevos",50), ("energy",10), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("bizcochos", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("dulces",25), ("energy",10), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),  
    ("torta", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("dulces",25), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("rosca_chicharrones", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("g_aceites",50), ("energy",10), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    
    # Meals - Launch, Dinner
    ("sopa_verduras", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("agua",6.25), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("e_carne_verduras", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("c_huevos",50), ("g_aceites",50), ("agua",6.25), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("g_arroz_carne_lenteja_verdura", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",20), ("c_huevos",50), ("g_aceites",50), ("agua",6.25), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("puchero", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("v_frutas",20), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("milanesa_papas_fritas", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("c_huevos",50), ("g_aceites",100), ("energy",20), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("costilla_cordero_huevo", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos",100), ("g_aceites",100), ("energy",20), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("cordero_arroz_choclo", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("churrasco_pure_zapallo", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("pollo_horno_ensalada", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",40), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("lengua_polenta", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",10), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("hamburguesa_papas_fritas", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("c_huevos",50), ("g_aceites",100), ("energy",20), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("albondiga_fideo", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",10), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("carne_papas", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("carne_vaca_ensalada", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",40), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("carne_cordero_pure", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("tarta_jamon_queso", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("panchos_huevo", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos",100), ("g_aceites",100), ("energy",20), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("choripan", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("polenta", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",10), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("tallarines", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",10), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("ñoquis", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",10), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("ravioles_verdura", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("v_frutas",30), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("tortilla_papa", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",40), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("pizza", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",10), ("g_aceites",50), ("energy",20), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("tarta_zapallo", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("v_frutas",20), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("pascualina", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("v_frutas",20), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("canelones_verdura", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("v_frutas",20), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    ("zapallitos_rellenos", 0.3, 70, 0, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("g_aceites",50), ("energy",20), ("b_teeth",-30), ("toilet",-30)], CONS_MEAL), None, None, None),
    
    # Farm
    ("pasta_primavera", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",40), ("c_huevos",50), ("g_aceites",50), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("pastel_lentajas", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",60), ("g_aceites",50), ("energy",15), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("tarta_zapallitos", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("v_frutas",30), ("g_aceites",50), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("tarta_puerros", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("v_frutas",30), ("g_aceites",50), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("polenta_acelga", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",40), ("g_aceites",50), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("budin_chauchas", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",30), ("dulces",12.5), ("g_aceites",50), ("l_quesos",25), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("guiso_berenjenas", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",40), ("v_frutas",40), ("c_huevos",50), ("g_aceites",50), ("agua",6.25), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("ensalada_lechuga", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",40), ("g_aceites",50), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("ensalada_remolacha", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",40), ("g_aceites",50), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("ensalada_holanesa", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",40), ("g_aceites",50), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),
    ("ensalada_pepinos", 0.3, 70, 0, CHEW_PATH, 3, 1, ORCHARD_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",40), ("g_aceites",50), ("energy",20), ("defenses",5), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None),

    # Fruit
    ("manzana", 0.3, 70, 0, CHEW_PATH, 3, 1, FRUIT_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("naranja", 0.3, 70, 0, CHEW_PATH, 3, 1, FRUIT_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("banana", 0.3, 70, 0, CHEW_PATH, 3, 1, FRUIT_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("ciruelas", 0.3, 70, 0, CHEW_PATH, 3, 1, FRUIT_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("pelon", 0.3, 70, 0, CHEW_PATH, 3, 1, FRUIT_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("frutillas", 0.3, 70, 0, CHEW_PATH, 3, 1, FRUIT_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("durazno", 0.3, 70, 0, CHEW_PATH, 3, 1, FRUIT_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("mandarina", 0.3, 70, 0, CHEW_PATH, 3, 1, FRUIT_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    
    # Sweets & Snacks
    ("papas_chips", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("energy",20), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("ticholos", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("energy",20), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("rapadura", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("energy",20), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("caramelo", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("energy",10), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("galletitas_dulces", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",50), ("energy",20), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("alfajor", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",10), ("dulces",50), ("g_aceites",50), ("energy",20), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("chicle", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("energy",10), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("chocolate", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",50), ("g_aceites",50), ("energy",20), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    ("chupetin", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("energy",10), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, None, None
    ),
    
    # Deserts
    ("arroz_leche", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("dulces",25), ("l_quesos",50), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("ensalada_frutas", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("dulces",25), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("crema", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("dulces",25), ("l_quesos",50), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("torta_manzana", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("v_frutas",10), ("dulces",25), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("flan", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("l_quesos",50), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("compota", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas",20), ("dulces",25), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("helado", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("l_quesos",50), ("energy",10), ("weight",1), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    
    # Others
    ("avena_leche", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("dulces",25), ("l_quesos",50), ("energy",10), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("martin_fierro", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("dulces",25), ("l_quesos",50), ("energy",10), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("torta_frita", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("dulces",25), ("g_aceites",50), ("energy",10), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    ("torta_dulce", 0.3, 70, 0, CHEW_PATH, 3, 1, BREAKFAST_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas",20), ("dulces",25), ("energy",10), ("weight",2), ("b_teeth",-30), ("toilet",-30)], CONS_FOOD), None, [], None
    ),
    
    # Sports
    ("sport_football", 0.3, 70, 0, "assets/kid/actions/football", 3, 1, None, 1, "assets/sound/jump_rope.ogg",
        effects.Effect(None, [("energy",-70), ("defenses",10), ("weight",-15), ("c_leguminosas",-20), ("v_frutas",-20), ("dulces",-10), ("g_aceites",-5), ("agua",-40), ("shower",50), ("w_hands",80), ("sports",60), ("fun",80), ("relaxing",-60)]), None, None, None
    ),
    ("sport_jump", 0.3, 70, 0, "assets/kid/actions/ropejump", 3, 1, None, 1, "assets/sound/saltar_cuerda.ogg",
        effects.Effect(None, [("energy",-30), ("defenses",5), ("weight",-5), ("c_leguminosas",-10), ("v_frutas",-10), ("dulces",-5), ("g_aceites",-2.5), ("agua",-20), ("shower",20), ("w_hands",20), ("sports",30), ("fun",50), ("relaxing",-20)]), None, None, None
    ),
    ("sport_run", 0.3, 70, 0, "assets/kid/actions/run", 3, 1, None, 1, None,
        effects.Effect(None, [("energy",-50), ("defenses",10), ("weight",-15), ("c_leguminosas",-20), ("v_frutas",-20), ("dulces",-10), ("g_aceites",-5), ("agua",-40), ("shower",50), ("w_hands",60), ("sports",70), ("fun",30), ("relaxing",-50)]), None, None, None
    ),
    
    # Do
    ("housekeeping", 0.3, 70, 1, "assets/kid/actions/twister", 3, 2, "assets/action-icons/clean", 1, [TWISTER_SOUND, "assets/sound/work.ogg"],
        effects.Effect(None, [("energy",-20), ("shower",-20), ("w_hands",-20), ("sports",10), ("fun",-20), ("relaxing",-30), ("housekeeping",60)]), None, None, None
    ),
    ("homework", 0.3, 70, 0, "assets/kid/actions/read", 3, 1, None, 1, "assets/sound/work.ogg",
        effects.Effect(None, [("energy",-30), ("weight",-5), ("c_leguminosas",-10), ("v_frutas",-10), ("dulces",-10), ("sports",-20), ("fun",-20), ("relaxing",-30), ("homework",80)], ["contento_deberes"]), None, None, None
    ),
    ("study_xo", 0.3, 70, 0, "assets/kid/actions/studyXO", 3, 1, None, 1, "assets/sound/play_xo.ogg",
        effects.Effect(None, [("energy",-30), ("weight",-5), ("c_leguminosas",-10), ("v_frutas",-10), ("dulces",-10), ("sports",-20), ("fun",-10), ("relaxing",-30)]), None, None, None
    ),
    ("help_field", 0.3, 70, 1, "assets/kid/actions/twister", 3, 2, None, 1, [TWISTER_SOUND, "assets/sound/work.ogg"],
        effects.Effect(None, [("energy",-40), ("defenses",10), ("weight",-10), ("c_leguminosas",-10), ("v_frutas",-10), ("dulces",-10), ("g_aceites",-5), ("agua",-20), ("shower",-40), ("w_hands",-70), ("sports",20), ("fun",-20), ("relaxing",-40)]), None, None, None
    ),
    ("help_cook", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/cook", 1, [TWISTER_SOUND, "assets/sound/work.ogg"],
        effects.Effect(None, [("energy",-20), ("shower",-10), ("w_hands",-50), ("relaxing",-10)], ["contento_cocinar"]), None, None, None
    ),
    ("relax", 0.3, 70, 0, "assets/kid/actions/rest", 3, 1, None, 1, ["assets/sound/relax.ogg"],
        effects.Effect(None, [("energy",40), ("defenses",10), ("fun",10), ("relaxing",40)]), None, None, None
    ),
    ("talk", 0.3, 70, 0, None, 3, 1, "assets/action-icons/talktofriend", 1, "assets/sound/talk.ogg",
        effects.Effect(None, [("fun",30)]), None, None, None
    ),
    ("clean", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/clean", 2, [TWISTER_SOUND, "assets/sound/work.ogg"],
        effects.Effect(None, [("energy",-20), ("shower",-10), ("w_hands",-40), ("sports",10), ("fun",-20), ("relaxing",-20), ("housekeeping",20)]), None, None, None
    ),
    ("sleep", 0.3, 150, 1, "assets/kid/actions/sleep", 3, 1, None, 2, [None, "assets/sound/sleep.ogg"],
        effects.Effect(None, [("energy",90), ("defenses",20), ("c_leguminosas",-50), ("v_frutas",-50), ("c_huevos",-30), ("dulces",-40), ("g_aceites",-20), ("l_quesos",-20), ("agua",-70), ("shower",-40), ("w_hands",-40), ("b_teeth",-40), ("toilet",-80), ("sports",-30), ("relaxing",90), ("housekeeping",-30), ("homework",-30)]), None, None, None, 1, None, "sleep"
    ),
    
    ("wash_hands", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/washhands", 2, [TWISTER_SOUND, "assets/sound/wash_hands.ogg"],
        effects.Effect(None, [("defenses",20), ("shower",90), ("w_hands",100), ("fun",-10)]), None, None, None
    ),
    ("brush_teeth", 0.3, 70, 0, "assets/kid/actions/brushteeth", 3, 1, None, 1, "assets/sound/brush_teeth.ogg",
        effects.Effect(None, [("defenses",10), ("b_teeth",100), ("fun",-10)]), None, None, None, 1, "un link"
    ),
    ("shower", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/shower", 2, [TWISTER_SOUND, "assets/sound/shower.ogg"],
        effects.Effect(None, [("energy",-10), ("defenses",20), ("agua",-10), ("shower",90), ("fun",-20), ("relaxing",10)]), None, None, None, 1, "un link"
    ),
    ("toilet", 0.3, 100, 1, "assets/kid/actions/toilet", 3, 1, None, 2, [TWISTER_SOUND, "assets/sound/toilet.ogg"],
        effects.Effect(None, [("defenses",10), ("w_hands",-100), ("toilet",100), ("fun",-10)]), None, None, None, 1, "/elPropioLinkDePrueba/link"
    ),
    
    # Farm
    ("farm_plow", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/trident", 2, [TWISTER_SOUND, "assets/sound/farm.ogg"],
        effects.Effect(None, [("energy",-40), ("weight",-10), ("c_leguminosas",-10), ("v_frutas",-10), ("dulces",-10), ("g_aceites",-5), ("agua",-40), ("shower",-60), ("w_hands",-90), ("sports",30), ("fun",30), ("relaxing",-40)]), None, None, None
    ),
    ("farm_sow", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/sow", 2, [TWISTER_SOUND, "assets/sound/farm.ogg"],
        effects.Effect(None, [("energy",-10), ("shower",-10), ("w_hands",-90), ("fun",10), ("relaxing",-10)]), None, None, None
    ),
    ("farm_irrigate", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/irrigate", 2, [TWISTER_SOUND, "assets/sound/farm.ogg"],
        effects.Effect(None, [("energy",-20), ("weight",-5), ("c_leguminosas",-10), ("v_frutas",-10), ("dulces",-10), ("agua",-20), ("shower",-30), ("w_hands",-90), ("sports",10), ("fun",10), ("relaxing",-20)]), None, None, None
    ),
    ("farm_fumigate", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/fumigate", 2, [TWISTER_SOUND, "assets/sound/farm.ogg"],
        effects.Effect(None, [("energy",-10), ("shower",-100), ("w_hands",-90), ("fun",10), ("relaxing",-20)], ["intoxicacion"]), None, None, None
    ),
    ("farm_clean", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/sow", 2, [TWISTER_SOUND, "assets/sound/farm.ogg"],
        effects.Effect(None, [("energy",-20), ("weight",-5), ("c_leguminosas",-10), ("v_frutas",-10), ("dulces",-10), ("shower",-40), ("w_hands",-90), ("sports",10), ("fun",10), ("relaxing",-20)]), None, None, None
    ),
    ("farm_harvest", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/harvest", 2, [TWISTER_SOUND, "assets/sound/farm.ogg"],
        effects.Effect(None, [("energy",-10), ("shower",-10), ("w_hands",-90), ("sports",10), ("fun",40), ("relaxing",-10)]), None, None, None
    ),
    
    # Fun
    ("playXO", 0.3, 70, 0, "assets/kid/actions/playXO", 3, 1, None, 1, "assets/sound/play_xo.ogg",
        effects.Effect(None, [("energy",-20), ("w_hands",-10), ("sports",-30), ("fun",60), ("relaxing",-20)]), None, None, None, 1, "un link"
    ),
    ("hidenseek", 0.3, 70, 0, "assets/kid/actions/hidenseek", 3, 1, None, 1, "assets/sound/hidenseek.ogg",
        effects.Effect(None, [("energy",-30), ("weight",-10), ("c_leguminosas",-10), ("v_frutas",-10), ("dulces",-10), ("g_aceites",-5), ("agua",-10), ("shower",-20), ("w_hands",-20), ("sports",20), ("fun",60), ("relaxing",-40)]), None, None, None
    ),
    ("hopscotch", 0.3, 92, 2, "assets/kid/actions/hopscotch", 3, 1, None, 1, "assets/sound/hopscotch.ogg",
        effects.Effect(None, [("energy",-30), ("weight",-10), ("shower",-20), ("w_hands",-20), ("sports",10), ("fun",60), ("relaxing",-40)]), None, None, None
    ),
    ("tv", 0.3, 70, 0, "assets/kid/actions/tv", 3, 1, None, 1, None,
        effects.Effect(None, [("energy",-20), ("sports",-30), ("fun",40), ("relaxing",10)]), None, None, None
    ),
    ("read", 0.3, 70, 0, "assets/kid/actions/read", 3, 1, None, 1, None,
        effects.Effect(None, [("energy",-20), ("sports",-30), ("fun",50), ("relaxing",10)]), None, None, None, 1, "un link"
    ),
    ("music", 0.3, 70, 0, None, 3, 1, None, 1, "assets/sound/music.ogg",
        effects.Effect(None, [("energy",-10), ("sports",-40), ("fun",50), ("relaxing",20)]), None, None, None, 1, "un link"
    ),
    #("sing", 0.3, 70, 1, "assets/kid/actions/sing", 3, 1, None, 4, None,
        #effects.Effect(None, [("fun", 4.0)]), None, None, None, 1, "un link"
    #),
    ("crazy", 0.3, 70, 0, "assets/kid/actions/crazy", 3, 1, None, 1, "assets/sound/crazy.ogg",
        effects.Effect(None, [("energy",-10), ("fun",40), ("relaxing",-10)]), None, None, None
    ),
    ("dance", 0.3, 70, 0, "assets/kid/actions/dance", 3, 1, None, 1, "assets/sound/music.ogg",
        effects.Effect(None, [("energy",-40), ("weight",-20), ("c_leguminosas",-20), ("v_frutas",-20), ("dulces",-20), ("g_aceites",-10), ("agua",-20), ("shower",-10), ("sports",30), ("fun",60), ("relaxing",-40)]), None, None, None, 1, "un link"
    ),
    
    # Go to
    ("dentist", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/dentist", 1, TWISTER_SOUND,
        effects.Effect(None, [("h_check",80)]), None, None, None, 1, "/elPropioLinkDePrueba/link"
    ),
    ("doctor", 0.3, 70, 1, "assets/kid/actions/twister", 3, 1, "assets/action-icons/doctor", 1, TWISTER_SOUND,
        effects.Effect(None, [("h_check",80)]), None, None, None, 1, "/elPropioLinkDePrueba/link"
    ),
    
    # Default action - affects the bars continuously
    ("BARS_DEC", 1.0, -1, 0, None, 0, 0, None, 0, None, bar_dec_effect, None, None, None)
]

### ACTIONS THAT SET CHARACTER LOCATION

locations_ac_list = [("goto_schoolyard", None, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "schoolyard"), None, None, None),
                     ("goto_classroom", None, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "classroom"), None, None, None),
                     ("goto_square", None, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "square"), None, None, None),
                     ("goto_bedroom", None, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "bedroom"), None, None, None),
                     ("goto_livingroom", None, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "livingroom"), None, None, None),
                    ]


### ACTIONS THAT SET CHARACTER CLOTHES
clothes_ac_list = [("change_school_clothes", None, 28, None, CHANGE_CLOTHES_ANIMATION_PATH, None, None, None, None, CHANGE_CLOTHES_PATH, effects.ClothesEffect(None, "school"), None, None, None),
                   ("change_regular_clothes", None, 28, None, CHANGE_CLOTHES_ANIMATION_PATH, None, None, None, None, CHANGE_CLOTHES_PATH, effects.ClothesEffect(None, "regular"), None, None, None),
                  ]

class ActionsLoader:
    """
    Crea las acciones (Action) y sus efectos (Effect y EffectStatus) asociados.
    """
    
    def __init__(self, bar_controller, game_manager):
        self.bar_controller = bar_controller
        self.game_manager = game_manager
        self.actions_list = self.__load_actions()
        
    def get_actions_list(self):
        return self.actions_list
    
    def __load_actions(self):
        status_actions = []

        for action in actions_list:    
            if len(action) == 17: # Action changes background
                status_actions.append(actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], self.__set_bar_controller(action[10]), action[11], action[12], action[13], self.get_level(action), self.get_link(action), action[16]))
            else:
                status_actions.append(actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], self.__set_bar_controller(action[10]), action[11], action[12], action[13], self.get_level(action), self.get_link(action)))
            
        location_actions = [actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], self.__set_game_manager(action[10]), action[11], action[12], action[13], self.get_level(action), self.get_link(action)) for action in locations_ac_list]
        
        clothes_actions = [actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], self.__set_game_manager(action[10]), action[11], action[12], action[13], self.get_level(action), self.get_link(action)) for action in clothes_ac_list]
        
        return status_actions + location_actions + clothes_actions
        
    def __set_bar_controller(self, effect):
        if effect:
            effect.set_bar_controller(self.bar_controller)
        return effect
    
    def __set_game_manager(self, effect):
        effect.set_game_manager(self.game_manager)
        return effect

    def get_level(self, action):
        """
        returns the action attribute level if it has.
        """
        if len(action) > 14:
            return action[14]
        else:
            return 1 #action's default level
    
    def get_link(self, action):
        if len(action) > 15:
            return action[15]
        else:
            return None
