# -*- coding: utf-8 -*-
import menu_creator
import status_bars_creator
import actions_creator
import character_creator
import game_manager
import events
import actions
import effects


class AppLoader:

    def __init__(self, windows_controller):
        ### loaders
        self.bars_loader = status_bars_creator.BarsLoader()
        
        actions_loader = actions_creator.ActionsLoader(self.bars_loader.get_bar_controller())

        ### actions 
        self.actions_list = actions_loader.get_actions_list() 
        
        ### status bars 
        self.status_bars_controller = self.bars_loader.get_bar_controller()
        self.character_bars = self.bars_loader.get_third_level_bars() #the third level status bars
        
        ### events
        self.events_list = self.__load_events(self.status_bars_controller)
        ### places
        character_loader = character_creator.CharacterLoader(self.actions_list, self.character_bars)
        self.places_dictionary = character_loader.get_places_dictionary()
        
        ### character
        self.character = character_loader.get_character()
        #moods
        self.moods_list = self.__load_moods()
        
        ### game manager
        self.game_man = game_manager.GameManager(self.character, self.status_bars_controller, self.actions_list, self.events_list, None, self.moods_list, windows_controller)
        self.game_man.add_background_action("BARS_DEC") #acción de decrementar las barras
        
        ### menu
        #self.menu = menu_creator.load_menu(self.character, (100, 100))
        ### visuals
        
    
    def get_game_manager(self):
        return self.game_man
        
    def get_character(self):
        return self.character
    
    def get_status_bars_controller(self):
        return self.status_bars_controller
    
    def get_status_bars_loader(self):
        return self.bars_loader
    
    def get_menu(self):
        return self.menu
    
    def get_actions(self):
        return self.actions_list
    
    def get_events(self):
        return self.events_list

    
    def __load_events(self, bars_controller):
        #Events constructor params:
        #picture, name, appereance_probability, time_span, kind, event_status, effect, kid_message, 
        #preferred_mood=9, message_time_span = time_span)
        #temporal para testear eventos
        dec = -1.0
        inc = 1.0
        
        ef3 = effects.Effect(bars_controller, [("b_teeth", -1.5)])
        ef4 = effects.Effect(bars_controller, [("energy", -1.4), ("resistencia", -0.9), ("fat", -0.5)])
        ef5 = effects.Effect(bars_controller, [("nutrition", -0.3), ("energy", -1.4), ("resistencia", -0.9), ("fat", -0.5)])
        
        event_ill = events.Event("ill.jpg", None, "ill", 5, 15, "kind", None, ef4, "me siento mal!", 2, 100) #preferred mood sick 1
        event_caries = events.Event("caries.jpg", None, "caries", 5, 15, "kind", None, ef3, "me duele una muela...", 5, 100)
        event_stomach_ache = events.Event("ill.jpg", "assets/events/stomach_ache", "stomach_ache", 5, 15, "kind", None, ef5, "me duele la panza! :(", 2, 100) #preferred mood sick 1
        
        return [event_ill, event_caries, event_stomach_ache]
    
    def __load_moods(self):
        
        #SICK
        m_sick3 = actions.Mood("sick_3", 0, "assets/kid/moods/sick3")
        m_sick2 = actions.Mood("sick_2", 1, "assets/kid/moods/sick2")
        m_sick1 = actions.Mood("sick_1", 2, "assets/kid/moods/sick1")
        #SAD
        m_sad3 = actions.Mood("sad_3", 3, "assets/kid/moods/sad3")
        m_sad2 = actions.Mood("sad_2", 4, "assets/kid/moods/sad2")
        m_sad1 = actions.Mood("sad_1", 5, "assets/kid/moods/sad1")
        #ANGRY
        m_angry3 = actions.Mood("angry_3", 6, "assets/kid/moods/angry3")
        m_angry2 = actions.Mood("angry_2", 7, "assets/kid/moods/angry2")
        m_angry1 = actions.Mood("angry_1", 8, "assets/kid/moods/angry1")
        #NORMAL
        m_normal = actions.Mood("normal", 9, "assets/kid/moods/normal")
        #HAPPY
        m_happy3 = actions.Mood("happy_3", 10, "assets/kid/moods/happy3")
        m_happy2 = actions.Mood("happy_2", 11, "assets/kid/moods/happy2")
        m_happy1 = actions.Mood("happy_1", 12, "assets/kid/moods/happy1")
        
        #Los moods están ordenados en la lista segun su rank
        moods_list = [m_sick3, m_sick2, m_sick1, m_sad3, m_sad2, m_sad1, m_angry3, m_angry2, m_angry1,
                      m_normal, m_happy3, m_happy2, m_happy1]
        
        return moods_list
        
        
        
        


