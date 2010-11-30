# -*- coding: utf-8 -*-

import effects
import actions
import os

BARS_DECREASE_RATE = -0.1

#ANIMATIONS
BLIP_PATH = os.path.normpath("assets/sound/blip.ogg")
APPLE_PATH = os.path.normpath("assets/food/apple")
STEW_PATH = os.path.normpath("assets/food/stew")
CHEW_PATH = os.path.normpath("assets/kid/actions/eat")
JUMP_ROPE_PATH = os.path.normpath("assets/kid/actions/ropejump")

#EFFECTS
##BACKGROUND EFFECTS
#BAR DECREASE

bar_dec_effect = effects.Effect(None, [("nutrition", BARS_DECREASE_RATE), ("spare_time", BARS_DECREASE_RATE), ("physica", BARS_DECREASE_RATE), ("hygiene", BARS_DECREASE_RATE)])



#actions list tuple format:
#[("action's id","icon_path","picture_path", appereance_probability, time_span, 
#    kid_animation_frame_rate,kid_animation_loop_times, kid_animation_path, window_animation_frame_rate,
#    window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, action's effect)]

### ACTIONS THAT AFFECT STATUS BARS

actions_list = [
    #id, icon, picture, appereance_probability, time_span, kid_animation_frame_rate, kid_animation_loop_times, kid_animation_path, window_animation_frame_rate, window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, effect
    
    # Sports
    ("sport_football", "icon_path", "picture_path", 0.3, 8, 0, 0, None, 3, 1, None, 4, "sound_path",
        effects.Effect(None, [("energy", 0.5), ("sports", 2.0), ("shower", -0.5), ("fun", 2.0)])
    ),

    ("sport_run", "icon_path", "picture_path", 0.3, 8, 0, 0, None, 3, 1, None, 4, "sound_path",
        effects.Effect(None, [("energy", 0.5), ("sports", 2.0), ("shower", -0.5), ("fun", 2.0)])
    ),
    
    ("sport_hide_seek", "icon_path", "picture_path", 0.3, 8, 0, 0, None, 3, 1, None, 4, "sound_path",
        effects.Effect(None, [("energy", 0.5), ("sports", 2.0), ("shower", -0.5), ("fun", 2.0)])
    ),
    
    ("sport_jump", "icon_path", "picture_path", 0.3, 8, 0, 0, JUMP_ROPE_PATH, 3, 1, None, 4, "sound_path",
        effects.Effect(None, [("energy", 0.5), ("sports", 2.0), ("shower", -0.5), ("fun", 2.0)])
    ),

    # Fruit
    ("eat_apple", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)])
    ),
    
    ("eat_orange", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)])
    ),

    ("eat_banana", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)])
    ),

    ("eat_kiwi", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)])
    ),

    # Meals
    ("eat_stew", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("v_frutas", 1.0), ("c_huevos", 0.5), ("g_aceites", 1.0), ("agua", 1.0), ("weight", 1.0)])
    ),
    ("eat_churrasco", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("v_frutas", 1.0), ("c_huevos", 0.5), ("g_aceites", 1.0), ("agua", 1.0), ("weight", 1.0)])
    ),
    ("eat_beaver", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("g_aceites", 2.0), ("weight", 1.0)])
    ),
    ("eat_milanesa", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("g_aceites", 2.0), ("weight", 2.0)])
    ),
    ("eat_torta_frita", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("weight", 1.0)])
    ),
    ("salad", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 2.0), ("weight", 0.5)])
    ),
    ("pascualina", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 2.0), ("c_leguminosas", 1.0), ("weight", 1.0)])
    ),
    ("tortilla_verdura", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 2.0), ("g_aceites", 1.0), ("weight", 1.0)])
    ),
    
    # Breakfast
    ("tostadas_membrillo", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 1.5), ("dulces", 1.5), ("weight", 1.0)])
    ),
    
    ("tostadas_queso", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 1.5), ("l_quesos", 1.5), ("weight", 1.0)])
    ),
    
    ("galletitas_saladas", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("weight", 1.0)])
    ),
    
    ("galletitas_dulces", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("weight", 1.0)])
    ),
    
    ("galletitas_dulce_leche", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("dulces", 2.0), ("weight", 1.0)])
    ),
    
    ("leche_chocolatada", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos", 2.0), ("dulces", 2.0), ("agua", 1.0), ("weight", 2.0)])
    ),
    
    ("leche_cafe", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos", 2.0), ("agua", 1.0), ("weight", 2.0)])
    ),
    
    ("leche", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos", 2.0), ("agua", 1.0), ("weight", 2.0)])
    ),
    
    ("leche_cereales", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos", 2.0), ("c_leguminosas", 1.0), ("agua", 1.0), ("weight", 2.0)])
    ),
    
    # Líquidos
    ("agua", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)])
    ),
    ("limonada", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)])
    ),
    ("jugo_naranja", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)])
    ),
    ("jugo_peras", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)])
    ),
    ("jugo_zanahorias", "icon_path", "picture_path", 0.3, 8, 3, 3, CHEW_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)])
    ),
    
    ("BARS_DEC", None, None, 1.0, -1, 0, 0, None, 0, 0, None, 0, None, bar_dec_effect)
]

### ACTIONS THAT SET CHARACTER LOCATION

locations_ac_list = [("goto_schoolyard", None, None, None, 1, None, None, None, None, None, None, None, None, effects.LocationEffect(None, "schoolyard")),
                     ("goto_country", None, None, None, 1, None, None, None, None, None, None, None, None, effects.LocationEffect(None, "country")),
                     ("goto_classroom", None, None, None, 1, None, None, None, None, None, None, None, None, effects.LocationEffect(None, "classroom")),
                     ("goto_square", None, None, None, 1, None, None, None, None, None, None, None, None, effects.LocationEffect(None, "square")),
                     ("goto_living", None, None, None, 1, None, None, None, None, None, None, None, None, effects.LocationEffect(None, "home")),
                     ("goto_bedroom", None, None, None, 1, None, None, None, None, None, None, None, None, effects.LocationEffect(None, "home")),
                     ("goto_kitchen", None, None, None, 1, None, None, None, None, None, None, None, None, effects.LocationEffect(None, "home")),
                     ("goto_bathroom", None, None, None, 1, None, None, None, None, None, None, None, None, effects.LocationEffect(None, "home"))
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
        status_actions = [actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], action[10], action[11], action[12], self.__set_bar_controller(action[13])) for action in actions_list]
        location_actions = [actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], action[10], action[11], action[12], self.__set_game_manager(action[13])) for action in locations_ac_list]
        
        return status_actions + location_actions
        
    def __set_bar_controller(self, effect):
        effect.set_bar_controller(self.bar_controller)
        return effect
    
    def __set_game_manager(self, location_effect):
        location_effect.set_game_manager(self.game_manager)
        return location_effect


