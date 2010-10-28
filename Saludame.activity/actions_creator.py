# -*- coding: utf-8 -*-

import effects
import actions

BARS_DECREASE_RATE = -0.4

#ANIMATIONS
BLIP_PATH = os.path.normpath("assets/sound/blip.ogg")
APPLE_PATH = os.path.normpath("assets/food/apple")

#EFFECTS
##BACKGROUND EFFECTS
#BAR DECREASE
bar_dec_effect = effects.Effect(None, [("nutrition", BARS_DECREASE_RATE), ("fun", BARS_DECREASE_RATE), ("physica", BARS_DECREASE_RATE), ("hygiene", BARS_DECREASE_RATE)])

##ACTION EFFECTS
#SPORT
sport_effect = effects.Effect(None, [("energy", -3.0), ("sports", 6.0), ("shower", -1.0), ("playing", 5.0)])

#EAT APPLE
eat_effect = effects.Effect(None, [("energy", 5.0), ("v_frutas", 10.0)])

### ANIMATIONS ###



#actions list tuple format:
#[("action's id","icon_path","picture_path", appereance_probability, time_span, 
#    kid_animation_frame_rate,kid_animation_loop_times, kid_animation_path, window_animation_frame_rate,
#    window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, action's effect)]


actions_list = [("sport_football", "icon_path", "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, "windows_animation_path", 4, "sound_path", sport_effect),
                ("eat_apple", "icon_path", "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, APPLE_PATH, 4, BLIP_PATH, eat_effect),
                ("BARS_DEC", None, None, 1.0, -1, 0, 0, None, 0, 0, None, 0, None, bar_dec_effect)]



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











