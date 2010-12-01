# -*- coding: utf-8 -*-
import menu_creator
import status_bars_creator
import actions_creator
import character_creator
import game_manager
import events
import actions
import effects

from gettext import gettext as _

class AppLoader:

    def __init__(self, windows_controller):
        ### loaders
        self.bars_loader = status_bars_creator.BarsLoader()
        
        ### status bars 
        self.status_bars_controller = self.bars_loader.get_bar_controller()
        self.character_bars = self.bars_loader.get_third_level_bars() #the third level status bars
        
        ### events
        self.events_list = self.__load_events(self.status_bars_controller)
        ### places
        character_loader = character_creator.CharacterLoader()
        self.places_dictionary = None
        
        ### character
        self.character = character_loader.get_character()
        #moods
        self.moods_list = self.__load_moods()
        
        ### game manager
        
        self.game_man = game_manager.GameManager(self.character, self.status_bars_controller, None, self.events_list, None, character_loader.get_environments_dictionary(), self.moods_list, windows_controller)
        actions_loader = actions_creator.ActionsLoader(self.bars_loader.get_bar_controller(), self.game_man)
        self.actions_list = actions_loader.get_actions_list() 
        self.game_man.actions_list = self.actions_list
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
        #picture, kid_animation_path, id, description, appereance_probability, time_span, kind, event_status, effect, kid_message, 
        #preferred_mood=9, message_time_span = time_span)
        
        #temporal para testear eventos
        dec = -1.0
        inc = 1.0
        
        _events = []
        
        # Personal Events
        # probabiliy configuration: (bar, type, threshold, probability_percentaje)
        probability = [("v_frutas", "indirect", 10.0, 30.0)]
        effect = effects.Effect(bars_controller, [("energy", -1.0), ("fun", -0.5)])
        event = events.PersonalEvent("ill.jpg", None, "constipation", _("Constipation"), 5, 15, "personal", probability, effect, u"Me duele la panza y no \n puedo ir al baño", 2, 50)
        _events.append(event)
        
        probability = [("w_hands", "indirect", 25.0, 30.0)]
        effect = effects.Effect(bars_controller, [("energy", -1.0), ("fun", -0.5), ("agua", -1.0), ("defenses", -0.5)])
        event = events.PersonalEvent("ill.jpg", None, "diarrhea", _("Diarrhea"), 5, 15, "personal", probability, effect, "Tengo diarrea", 2, 50)
        _events.append(event)
        
        probability = [("nutrition", "indirect", 100.0, 20.0), ("relaxing", "indirect", 100.0, 20.0)]
        effect = effects.Effect(bars_controller, [("energy", -1.0), ("fun", -0.5), ("relaxing", -0.5)])
        event = events.PersonalEvent("ill.jpg", None, "headache", _("Headache"), 5, 15, "personal", probability, effect, "Me duele la cabeza", 2, 50)
        _events.append(event)
        
        probability = [("b_teeth", "indirect", 25.0, 50.0), ("dulces", "direct", 75.0, 20.0)]
        effect = effects.Effect(bars_controller, [("energy", -1.0), ("defenses", -1.0), ("fun", -1.0), ("relaxing", -1.0)])
        event = events.PersonalEvent("caries.jpg", None, "caries", _("Caries"), 5, 15, "personal", probability, effect, "Me duele una muela...", 5, 50)
        _events.append(event)
        
        probability = []
        effect = effects.Effect(bars_controller, [("nutrition", -0.3), ("energy", -1.4), ("resistencia", -0.9), ("fat", -0.5)])
        event = events.PersonalEvent("ill.jpg", "assets/events/stomach_ache", "stomach_ache", _("Stomach ache"), 5, 15, "personal", probability, effect, "Me duele la panza! :(", 2, 50)
        _events.append(event)
        
        #Social events
        #(picture, person_path, name, description, appereance_probability, time_span, condicioned_bars, message, message_time_span)
        probability = [("b_teeth", "indirect", 50.0, 70.0), ("dulces", "direct", 75.0, 30.0)]
        
        #editar parametros:
        event = events.SocialEvent("caries.jpg", "assets/characters/teacher.png", "p_caries", _("Prevenir caries"), 5.0, 15, probability, "Deberías lavarte los \ndientes...", 100)
        _events.append(event)
        
        return _events
    
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



