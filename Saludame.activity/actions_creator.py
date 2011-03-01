# -*- coding: utf-8 -*-

import effects
import actions
import os

BARS_DECREASE_RATE = -0.1

#SOUNDS
BLIP_PATH = os.path.normpath("assets/sound/blip.ogg")
CHANGE_PLACE_PATH = os.path.normpath("assets/sound/place_change.ogg")
CHANGE_CLOTHES_PATH = os.path.normpath("assets/sound/clothes_change.ogg")

#ANIMATIONS
APPLE_PATH = os.path.normpath("assets/food/apple")
STEW_PATH = os.path.normpath("assets/food/stew")
CHEW_PATH = os.path.normpath("assets/kid/actions/eat")
DRINK_PATH = os.path.normpath("assets/kid/actions/drink")
CHANGE_CLOTHES_ANIMATION_PATH = os.path.normpath("assets/kid/actions/twister")

#EFFECTS
##BACKGROUND EFFECTS
#BAR DECREASE

bar_dec_effect = effects.Effect(None, [("nutrition", BARS_DECREASE_RATE), ("spare_time", BARS_DECREASE_RATE), ("physica", BARS_DECREASE_RATE), ("hygiene", BARS_DECREASE_RATE), ("responsability", BARS_DECREASE_RATE)])

#actions list tuple format:
#[("action's id","icon_path","picture_path", appereance_probability, time_span,
#    kid_animation_frame_rate,kid_animation_loop_times, kid_animation_path, window_animation_frame_rate,
#    window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, action's effect)]

### ACTIONS THAT AFFECT STATUS BARS

actions_list = [
    #id, icon, picture, appereance_probability, time_span, kid_animation_frame_rate, kid_animation_loop_times, kid_animation_path, window_animation_frame_rate, window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, effect

    # Atention, default action when idle for long time
    ("attention", 0.3, 5, 40, 0, "assets/kid/actions/atention", 3, 1, None, 4, None,
        effects.Effect(None, []), None, None, None
    ),
    
    # Fruit
    ("eat_apple", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 20)]), None, None, None
    ),
    
    ("eat_orange", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)]), None, None, None
    ),

    ("eat_banana", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)]), None, None, None
    ),

    ("eat_kiwi", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, APPLE_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 3.0), ("weight", 0.5)]), None, None, None
    ),

    # Meals
    ("eat_stew", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("v_frutas", 1.0), ("c_huevos", 0.5), ("g_aceites", 1.0), ("agua", 1.0), ("weight", 1.0)]), None, None, None
    ),
    ("eat_churrasco", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("v_frutas", 1.0), ("c_huevos", 0.5), ("g_aceites", 1.0), ("agua", 1.0), ("weight", 1.0)]), None, None, None
    ),
    ("eat_beaver", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("g_aceites", 2.0), ("weight", 1.0)]), None, None, None
    ),
    ("eat_milanesa", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("g_aceites", 2.0), ("weight", 2.0)]), None, None, None
    ),
    ("eat_torta_frita", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_huevos", 3.0), ("weight", 1.0)]), None, None, None
    ),
    ("salad", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 2.0), ("weight", 0.5)]), None, None, None
    ),
    ("pascualina", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 2.0), ("c_leguminosas", 1.0), ("weight", 1.0)]), None, None, None
    ),
    ("tortilla_verdura", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("v_frutas", 2.0), ("g_aceites", 1.0), ("weight", 1.0)]), None, None, None
    ),
    
    # Breakfast
    ("leche", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos", 2.0), ("agua", 1.0), ("weight", 2.0)]), None, ["morning", "afternoon"], None
    ),
    
    ("leche_chocolatada", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos", 2.0), ("dulces", 2.0), ("agua", 1.0), ("weight", 2.0)]), None, ["morning", "afternoon"], None
    ),
    
    ("leche_cafe", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos", 2.0), ("agua", 1.0), ("weight", 2.0)]), None, ["morning", "afternoon"], None
    ),
    
    ("tostadas_membrillo", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 1.5), ("dulces", 1.5), ("weight", 1.0)]), None, ["morning", "afternoon"], None
    ),
    
    ("tostadas_queso", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 1.5), ("l_quesos", 1.5), ("weight", 1.0)]), None, ["morning", "afternoon"], None
    ),
    
    ("galletitas_saladas", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("weight", 1.0)]), None, ["morning", "afternoon"], None
    ),
    
    ("galletitas_dulces", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("weight", 1.0)]), None, ["morning", "afternoon"], None
    ),
    
    ("galletitas_dulce_leche", 0.3, 5, 70, 3, CHEW_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("c_leguminosas", 2.0), ("dulces", 2.0), ("weight", 1.0)]), None, ["morning", "afternoon"], None
    ),
    
    ("leche_cereales", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, STEW_PATH, 4, BLIP_PATH,
        effects.Effect(None, [("l_quesos", 2.0), ("c_leguminosas", 1.0), ("agua", 1.0), ("weight", 2.0)]), None, ["morning", "afternoon"], None
    ),
    
    # Liquid
    ("agua", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)]), None, None, None
    ),
    ("limonada", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)]), None, None, None
    ),
    ("jugo_naranja", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)]), None, None, None
    ),
    ("jugo_peras", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)]), None, None, None
    ),
    ("jugo_zanahorias", 0.3, 5, 70, 3, DRINK_PATH, 3, 1, None, 4, BLIP_PATH,
        effects.Effect(None, [("agua", 1.0)]), None, None, None
    ),
    
    # Sports
    ("sport_football", 0.3, 5, 70, 0, "assets/kid/actions/football", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -7.0), ("defenses", 1.0), ("weight", -1.5), ("nutrition", -2.0), ("water", -2.0), ("shower", -5.0), ("w_hands", -8.0), ("sports", 6.0), ("fun", 8.0), ("relaxing", -6.0)]), None, None, None
    ),
    ("sport_jump", 0.3, 5, 70, 0, "assets/kid/actions/ropejump", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -3.0), ("defenses", 0.5), ("weight", -0.5), ("nutrition", -1.0), ("water", -1.0), ("shower", -2.0), ("w_hands", -2.0), ("sports", 3.0), ("fun", 5.0), ("relaxing", -2.0)]), None, None, None
    ),
    ("sport_run", 0.3, 5, 70, 0, "assets/kid/actions/run", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -5.0), ("defenses", 1.0), ("weight", -1.5), ("nutrition", -2.0), ("water", -2.0), ("shower", -5.0), ("w_hands", -6.0), ("sports", 7.0), ("fun", 3.0), ("relaxing", -5.0)]), None, None, None
    ),
    
    # Do
    ("housekeeping", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/clean", 4, None,
        effects.Effect(None, [("energy", -2.0), ("shower", -2.0), ("w_hands", -2.0), ("sports", 1.0), ("fun", -2.0), ("relaxing", -3.0), ("housekeeping", 6.0)]), None, None, None
    ),
    ("homework", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/clean", 4, None,
        effects.Effect(None, [("energy", -3.0), ("weight", -0.5), ("nutrition", -0.5), ("sports", -2.0), ("fun", -2.0), ("relaxing", -3.0), ("homework", 8.0)]), None, None, None
    ),
    ("study_xo", 0.3, 5, 70, 0, "assets/kid/actions/studyXO", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -3.0), ("weight", -0.5), ("nutrition", -0.5), ("sports", -2.0), ("fun", -1.0), ("relaxing", -3.0), ("responsability", 2.0)]), None, None, None
    ),
    ("help_field", 0.3, 5, 70, 0, "assets/kid/actions/twister", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -4.0), ("defenses", 1.0), ("weight", -1.0), ("nutrition", -0.5), ("water", -1.5), ("shower", -4.0), ("w_hands", -7.0), ("sports", -2), ("fun", -2), ("relaxing", -4), ("responsability", -4.0)]), None, None, None
    ),
    ("help_cook", 0.3, 5, 70, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/cook", 4, None,
        effects.Effect(None, [("energy", -2.0), ("shower", -1.0), ("w_hands", -5.0), ("relaxing", -1.0)]), None, None, None
    ),
    ("relax", 0.3, 5, 70, 0, "assets/kid/actions/rest", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", 4.0), ("defenses", 1.0), ("fun", 1.0), ("relaxing", 5.0)]), None, None, None
    ),
<<<<<<< HEAD
    ("talk", 0.3, 5, 70, 0, None, 3, 1, "assets/action-icons/talktofriend", 4, None,
        effects.Effect(None, [("fun", 3.0)]), None, None, None
    ),
    ("clean", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/clean", 4, None,
        effects.Effect(None, [("energy", -2.0), ("shower", -1.0), ("w_hands", -4.0), ("sports", 1.0), ("fun", -2.0), ("relaxing", -2.0), ("housekeeping", 2)]), None, None, None
    ),
    ("wash_hands", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/washhands", 4, None,
        effects.Effect(None, [("defenses", 2.0), ("shower", 10.0), ("w_hands", 10.0)]), None, None, None
    ),
    ("brush_teeth", 0.3, 5, 70, 0, "assets/kid/actions/brushteeth", 3, 1, None, 4, None,
        effects.Effect(None, [("defenses", 1.0), ("b_teeth", 10.0)]), None, None, None, 1, "un link"
    ),
    ("shower", 0.3, 5, 70, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/shower", 4, None,
        effects.Effect(None, [("energy", -1.0), ("defenses", 2.0), ("water", -1.0), ("shower", 10.0)]), None, None, None, 1, "un link"
    ),
    
    # Farm
    ("farm_plow", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/trident", 4, None,
        effects.Effect(None, [("energy", -4.0), ("weight", -1.0), ("nutrition", -0.5), ("water", -3.5), ("shower", -6.0), ("w_hands", -10.0), ("sports", 3.0), ("fun", 3.0), ("relaxing", -4.0), ("Huerta", 15.0)]), None, None, None
    ),
    ("farm_sow", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/sow", 4, None,
        effects.Effect(None, [("energy", -4.0), ("weight", -1.0), ("nutrition", -0.5), ("water", -3.5), ("shower", -6.0), ("w_hands", -10.0), ("sports", 3.0), ("fun", 3.0), ("relaxing", -4.0), ("Huerta", 15.0)]), None, None, None
    ),
    ("farm_irrigate", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/irrigate", 4, None,
        effects.Effect(None, [("energy", -4.0), ("weight", -1.0), ("nutrition", -0.5), ("water", -3.5), ("shower", -6.0), ("w_hands", -10.0), ("sports", 3.0), ("fun", 3.0), ("relaxing", -4.0), ("Huerta", 5.0)]), None, None, None
    ),
    ("farm_fumigate", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/fumigate", 4, None,
        effects.Effect(None, [("energy", -4.0), ("weight", -1.0), ("nutrition", -0.5), ("water", -3.5), ("shower", -6.0), ("w_hands", -10.0), ("sports", 3.0), ("fun", 3.0), ("relaxing", -4.0), ("Huerta", 5.0)]), None, None, None
    ),
    ("farm_clean", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/sow", 4, None,
        effects.Effect(None, [("energy", -4.0), ("weight", -1.0), ("nutrition", -0.5), ("water", -3.5), ("shower", -6.0), ("w_hands", -10.0), ("sports", 3.0), ("fun", 3.0), ("relaxing", -4.0), ("Huerta", 5.0)]), None, None, None
    ),
    ("farm_harvest", 0.3, 5, 28, 0, "assets/kid/actions/twister", 3, 1, "assets/action-icons/harvest", 4, None,
        effects.Effect(None, [("energy", -4.0), ("weight", -1.0), ("nutrition", -0.5), ("water", -3.5), ("shower", -6.0), ("w_hands", -10.0), ("sports", 3.0), ("fun", 3.0), ("relaxing", -4.0), ("Huerta", 15.0)]), None, None, None
    ),
    
    # Fun
    ("playXO", 0.3, 5, 70, 1, "assets/kid/actions/playXO", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -2.0), ("hands", -1.0), ("sports", -3.0), ("fun", 6.0), ("rest", -2.0)]), None, None, None, 1, "un link"
    ),
    ("hidenseek", 0.3, 5, 70, 0, "assets/kid/actions/hidenseek", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -3.0), ("weight", -1.0), ("nutrition", -1.0), ("shower", -2.0), ("w_hands", -2.0), ("sports", 2.0), ("fun", 6.0), ("relaxing", -4.0)]), None, None, None
    ),
    ("hopscotch", 0.3, 5, 70, 0, "assets/kid/actions/hopscotch", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -3.0), ("weight", -1.0), ("nutrition", -1.0), ("shower", -2.0), ("w_hands", -2.0), ("sports", 1.0), ("fun", 6.0), ("relaxing", -4.0)]), None, None, None
    ),
    ("tv", 0.3, 5, 70, 0, "assets/kid/actions/tv", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -2.0), ("sports", -3.0), ("fun", 4.0), ("relaxing", 1.0)]), None, None, None
    ),
    ("read", 0.3, 5, 70, 1, "assets/kid/actions/read", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -2.0), ("sports", -3.0), ("fun", 5.0), ("relaxing", 1.0)]), None, None, None, 1, "un link"
    ),
    ("music", 0.3, 5, 70, 1, None, 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -1.0), ("sports", -4.0), ("fun", 5.0), ("relaxing", 2.0)]), None, None, None, 1, "un link"
    ),
    #("sing", 0.3, 5, 70, 1, "assets/kid/actions/sing", 3, 1, None, 4, None,
        #effects.Effect(None, [("fun", 4.0)]), None, None, None, 1, "un link"
    #),
    ("crazy", 0.3, 5, 70, 0, "assets/kid/actions/crazy", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -1.0), ("fun", 4.0), ("relaxing", 1.0)]), None, None, None
    ),
    ("dance", 0.3, 5, 70, 0, "assets/kid/actions/dance", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", -4.0), ("nutrition", -1.0), ("shower", -1.0), ("sports", -2.0), ("fun", 6.0), ("relaxing", 4.0)]), None, None, None, 1, "un link"
    ),
    
    # Go to
    ("sleep", 0.3, 5, 70, 0, "assets/kid/actions/sleep", 3, 1, None, 4, None,
        effects.Effect(None, [("energy", 9.0), ("defenses", 2.0), ("nutrition", -3.0), ("water", -4.0), ("shower", -4.0), ("w_hands", -4.0), ("b_teeth", -4.0), ("toilet", -8.0), ("sports", -3.0), ("relaxing", 9.0), ("housekeeping", -3.0), ("homework", -3.0)]), None, None, None
    ),
    ("toilet", 0.3, 3, 35, 3, "assets/kid/actions/toilet", 3, 1, None, 4, None,
        effects.Effect(None, [("defenses", 1.0), ("w_hands", -10.0), ("toilet", 10.0), ("fun", -1.0)]), None, None, None, 1, "/elPropioLinkDePrueba/link"
    ),
    ("dentist", 0.3, 3, 35, 3, "assets/kid/actions/twister", 3, 1, "assets/action-icons/dentist", 4, None,
        effects.Effect(None, [("h_check", 8.0)]), None, None, None, 1, "/elPropioLinkDePrueba/link"
    ),
    ("doctor", 0.3, 3, 35, 3, "assets/kid/actions/twister", 3, 1, "assets/action-icons/doctor", 4, None,
        effects.Effect(None, [("h_check", 8.0)]), None, None, None, 1, "/elPropioLinkDePrueba/link"
    ),
    
    # Default action - affects the bars continuously
    ("BARS_DEC", 1.0, -1, 0, 0, None, 0, 0, None, 0, None, bar_dec_effect, None, None, None)
]

### ACTIONS THAT SET CHARACTER LOCATION

locations_ac_list = [("goto_schoolyard", None, 1, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "schoolyard"), None, None, None),
                     ("goto_classroom", None, 1, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "classroom"), None, None, None),
                     ("goto_square", None, 1, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "square"), None, None, None),
                     ("goto_bedroom", None, 1, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "bedroom"), None, None, None),
                     ("goto_livingroom", None, 1, 28, None, None, None, None, None, None, CHANGE_PLACE_PATH, effects.LocationEffect(None, "livingroom"), None, None, None),
                    ]


### ACTIONS THAT SET CHARACTER CLOTHES
clothes_ac_list = [("change_school_clothes", None, 1, 28, None, CHANGE_CLOTHES_ANIMATION_PATH, None, None, None, None, CHANGE_CLOTHES_PATH, effects.ClothesEffect(None, "school"), None, None, None),
                   ("change_regular_clothes", None, 1, 28, None, CHANGE_CLOTHES_ANIMATION_PATH, None, None, None, None, CHANGE_CLOTHES_PATH, effects.ClothesEffect(None, "regular"), None, None, None),
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
        status_actions = [actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], action[10], self.__set_bar_controller(action[11]), action[12], action[13], action[14], self.get_level(action), self.get_link(action)) for action in actions_list]
        
        location_actions = [actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], action[10], self.__set_game_manager(action[11]), action[12], action[13], action[14], self.get_level(action), self.get_link(action)) for action in locations_ac_list]
        
        clothes_actions = [actions.Action(action[0], action[1], action[2], action[3], action[4], action[5], action[6], action[7], action[8], action[9], action[10], self.__set_game_manager(action[11]), action[12], action[13], action[14], self.get_level(action), self.get_link(action)) for action in clothes_ac_list]
        
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
        if len(action) > 15:
            return action[15]
        else:
            return 1 #action's default level
    
    def get_link(self, action):
        if len(action) > 16:
            return action[16]
        else:
            return None
