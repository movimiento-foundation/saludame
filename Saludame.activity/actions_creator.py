# -*- coding: utf-8 -*-

import effects
import actions

BARS_DECREASE_RATE = -0.4

### EFFECT STATUS ### SE CREA EL EFECTO PERO NO SE CARGA CON EL BAR_CONTROLLER

#BACKGROUND EFFECTS - bars decrease
eff_bar_nut_dec = effects.EffectStatus(BARS_DECREASE_RATE, "nutrition", None)

eff_bar_fun_dec = effects.EffectStatus(BARS_DECREASE_RATE, "fun", None)

eff_bar_phy_dec = effects.EffectStatus(BARS_DECREASE_RATE, "physica", None)

eff_bar_hyg_dec = effects.EffectStatus(BARS_DECREASE_RATE, "hygiene", None)

### nutrition ones ###
eff_st_nut_v_fruit_inc = effects.EffectStatus(8.0, "v_frutas", None)

### fun ones ###
eff_st_fun_Sport_inc = effects.EffectStatus(6.0, "Sports", None)
eff_st_fun_pla_inc = effects.EffectStatus(5.0, "Playing", None)
### hygiene ones ###
eff_st_hyg_shw_dec = effects.EffectStatus(-1.0, "shower", None)

### physica ones ###
eff_st_phy_inc = effects.EffectStatus(3.0, "Energy", None)
eff_st_phy_energy_dec = effects.EffectStatus(-3.0, "Energy", None)

### EFFECTS ###
##BACKGROUND EFFECTS
#BAR DECREASE
bar_dec_effect = effects.Effect()
bar_dec_effect.add_effect(eff_bar_nut_dec)
bar_dec_effect.add_effect(eff_bar_fun_dec)
bar_dec_effect.add_effect(eff_bar_phy_dec)
bar_dec_effect.add_effect(eff_bar_hyg_dec)

#SPORT
sport_effect = effects.Effect()
sport_effect.add_effect(eff_st_phy_energy_dec)

sport_effect.add_effect(eff_st_fun_Sport_inc)

sport_effect.add_effect(eff_st_hyg_shw_dec)
sport_effect.add_effect(eff_st_fun_pla_inc)
#EAT APPLE
eat_effect = effects.Effect()

eat_effect.add_effect(eff_st_phy_inc)
eat_effect.add_effect(eff_st_nut_v_fruit_inc)

### ANIMATIONS ###

### PATH ###



#actions list tuple format:

#[("action's id","icon_path","picture_path", appereance_probability, time_span, 
#    kid_animation_frame_rate,kid_animation_loop_times, kid_animation_path, window_animation_frame_rate,
#    window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, action's effect)]


actions_list = [("sport_football", "icon_path", "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, "windows_animation_path", 4, "sound_path", sport_effect),
                ("eat_apple", "icon_path", "picture_path", 0.3, 12, 3, 3, "kid_animation_path", 3, 1, "assets/food/apple", 4, "assets/sound/blip.ogg", eat_effect),
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
