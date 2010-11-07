# -*- coding: utf-8 -*-

import effects
import actions
import os

BARS_DECREASE_RATE = -0.2

#ANIMATIONS
BLIP_PATH = os.path.normpath("assets/sound/blip.ogg")
APPLE_PATH = os.path.normpath("assets/food/apple")
STEW_PATH = os.path.normpath("assets/food/stew")

#EFFECTS
##BACKGROUND EFFECTS
#BAR DECREASE

bar_dec_effect = effects.Effect(None, [("nutrition", BARS_DECREASE_RATE), ("spare_time", BARS_DECREASE_RATE), ("physica", BARS_DECREASE_RATE), ("hygiene", BARS_DECREASE_RATE)])

### ANIMATIONS ###

#actions list tuple format:
#[("action's id","icon_path","picture_path", appereance_probability, time_span, 
#    kid_animation_frame_rate,kid_animation_loop_times, kid_animation_path, window_animation_frame_rate,
#    window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, action's effect)]


actions_list = [
    #id, icon, picture, appereance_probability, time_span, kid_animation_frame_rate, kid_animation_loop_times, kid_animation_path, window_animation_frame_rate, window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, effect
    
    # Sports
    ("sport_football",  "icon_path",    "picture_path", 0.3, 12, 0, 0, "kid_animation_path", 3, 1, None, 4, "sound_path", 
        effects.Effect(None, [("energy", -0.5), ("sports", 2.0), ("shower", -0.5), ("fun", 2.0)])
    ),

    ("sport_run",  "icon_path",    "picture_path", 0.3, 12, 0, 0, "kid_animation_path", 3, 1, None, 4, "sound_path", 
        effects.Effect(None, [("energy", -0.5), ("sports", 2.0), ("shower", -0.5), ("fun", 2.0)])
    ),
    
    ("sport_hide_seek",  "icon_path",    "picture_path", 0.3, 12, 0, 0, "kid_animation_path", 3, 1, None, 4, "sound_path", 
        effects.Effect(None, [("energy", -0.5), ("sports", 2.0), ("shower", -0.5), ("fun", 2.0)])
    ),
    
    # Fruit
    ("eat_apple",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)])
    ),
    
    ("eat_orange",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)])
    ),

    ("eat_banana",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)])
    ),

    ("eat_kiwi",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)])
    ),

    # Meals
    ("eat_stew",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("v_frutas", 1.0), ("c_huevos", 0.5), ("g_aceites", 1.0), ("agua", 1.0), ("weight", 1.0)])
    ),
    ("eat_churrasco",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("v_frutas", 1.0), ("c_huevos", 0.5), ("g_aceites", 1.0), ("agua", 1.0), ("weight", 1.0)])
    ),
    ("eat_beaver",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("g_aceites", 2.0), ("weight", 1.0)])
    ),
    ("eat_milanesa",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("g_aceites", 2.0), ("weight", 2.0)])
    ),
    ("eat_torta_frita",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("weight", 1.0)])
    ),
    ("salad",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 2.0), ("weight", 0.5)])
    ),
    ("pascualina",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("v_frutas", 2.0), ("c_leguminosas", 1.0), ("weight", 1.0)])
    ),
    ("tortilla_verdura",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("v_frutas", 2.0), ("g_aceites", 1.0), ("weight", 1.0)])
    ),
    
    # Breakfast
    ("tostadas_membrillo",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("c_leguminosas", 1.5), ("dulces", 1.5), ("weight", 1.0)])
    ),
    
    ("tostadas_queso",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("c_leguminosas", 1.5), ("l_quesos", 1.5), ("weight", 1.0)])
    ),
    
    ("galletitas_saladas",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("c_leguminosas", 2.0), ("weight", 1.0)])
    ),
    
    ("galletitas_dulces",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("c_leguminosas", 2.0), ("weight", 1.0)])
    ),
    
    ("galletitas_dulce_leche",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("c_leguminosas", 2.0), ("dulces", 2.0), ("weight", 1.0)])
    ),
    
    ("leche_chocolatada",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("l_quesos", 2.0), ("dulces", 2.0), ("agua", 1.0), ("weight", 2.0)])
    ),
    
    ("leche_cafe",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("l_quesos", 2.0), ("agua", 1.0), ("weight", 2.0)])
    ),
    
    ("leche",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("l_quesos", 2.0), ("agua", 1.0), ("weight", 2.0)])
    ),
    
    ("leche_cereales",       "icon_path",    "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, STEW_PATH, 4, None,
        effects.Effect(None, [("l_quesos", 2.0), ("c_leguminosas", 1.0), ("agua", 1.0), ("weight", 2.0)])
    ),
    
    ("BARS_DEC", None, None, 1.0, -1, 0, 0, None, 0, 0, None, 0, None, bar_dec_effect)
]

class ActionsLoader:
    """
    Crea las acciones (Action) y sus efectos (Effect y EffectStatus) asociados.
    """
    
    def __init__(self, bar_controller):
        self.bar_controller = bar_controller
        self.actions_list = self.__load_actions()
        
        
    def get_actions_list(self): 
        return self.actions_list
    
    def __load_actions(self):
        return [actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], action[10], action[11], action[12], self.__set_bar_controller(action[13])) for action in actions_list]
        
    def __set_bar_controller(self, effect_status):
        effect_status.set_bar_controller(self.bar_controller)
        return effect_status
