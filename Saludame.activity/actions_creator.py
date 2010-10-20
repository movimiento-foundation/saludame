# -*- coding: utf-8 -*-

import effects



### EFFECT STATUS ### SE CREA EL EFECTO PERO NO SE CARGA CON EL BAR_CONTROLLER

### nutrition ones ###

### fun ones ###

### hygiene ones ###

### physica ones ###
eff_st_phy_energy_dec = effects.EffectStatus(1, "", None)


### EFFECTS ###



action_effect = "an_effect"

### ANIMATIONS ###

### PATH ###



#actions list tuple format:

#[("action's id","icon_path","picture_path", appereance_probability, time_span, 
#    kid_animation_frame_rate,kid_animation_loop_times, kid_animation_path, window_animation_frame_rate,
#    window_animation_loop_times, window_animation_path, sound_loop_times, sound_path, action's effect)]


actions = [("sport_jump", "icon_path", "picture_path", 0.3, 2, 3, 3, "kid_animation_path", 3, 1, "windows_animation_path", 4, "sound_path", action_effect)]



class ActionsLoader:
    """
    Crea las acciones (Action) y sus efectos (Effect y EffectStatus) asociados.
    """
    
    def __init__(self, bar_controller):
        self.__load_actions()
        
    def get_actions_dictionary(self): 
        
        None   
    
    def __load_actions(self):
        None









