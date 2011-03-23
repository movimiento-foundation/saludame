# -*- coding: utf-8 -*-

import menu_creator
import status_bars_creator
import actions_creator
import character
import game_manager
import events
import actions
import effects

from gettext import gettext as _

CONFIGURATION_LEVEL_LIST = [{# LEVEL 1
                             "score_vector" : (0, 0, 0, 0, 0), #(-8, -4, 0 , 5, 10), # incremento central en 10 por motivos de testeo
                             "true_or_false_vector" : (-10, -5, 5, 10, 15, 20),
                             "multiple_choice_vector" : (12, 7, -5),
                             "master_challenge_text" : "Tienes nuevas acciones, ¿te animas a encontrarlas?",
                             "min_qty_correct_ans" : 3, #min qty of corrent answers to pass master challenge.
                             "slide" : None,
                             "events_qty" : 2,
                             "events_qty_personal" : 1,
                             "events_qty_social" : 1,
                             "time_between_events" : 30 #menos tiempo para probar más fácil 175 #three minutes aprox.
                             },
                             {# LEVEL 2
                             "score_vector" : (-8, -4, 0 , 5, 10),
                             "true_or_false_vector" : (-10, -5, 5, 10, 15, 20),
                             "multiple_choice_vector" : (12, 7, -5),
                             "master_challenge_text" : "Vas muy bien! Cuando llueva recuerda ponerte bajo techo.",
                             "min_qty_correct_ans" : 3,
                             "slide" : None,
                             "events_qty" : 2,
                             "events_qty_personal" : 1,
                             "events_qty_social" : 1,
                             "time_between_events" : 120 #menos tiempo para probar más fácil 160
                             },
                             {# LEVEL 3
                             "score_vector" : (-8, -4, 0 , 5, 10),
                             "true_or_false_vector" : (-10, -5, 5, 10, 15, 20),
                             "multiple_choice_vector" : (12, 7, -5),
                             "master_challenge_text" : u"¡Vas muy bien, continúa!",
                             "min_qty_correct_ans" : 3,
                             "slide" : "assets/slides/history3.jpg",
                             "events_qty" : 2,
                             "events_qty_personal" : 1,
                             "events_qty_social" : 2,
                             "time_between_events" : 120 #menos tiempo para probar más fácil 145
                             },
                             {# LEVEL 4
                             "score_vector" : (-10, -6, 0 , 3, 7),
                             "true_or_false_vector" : (-12, -7, 3, 9, 13, 18),
                             "multiple_choice_vector" : (10, 5, -7),
                             "master_challenge_text" : "Vas muy bien! ¿Has visitado la plaza?",
                             "min_qty_correct_ans" : 4,
                             "slide" : None,
                             "events_qty" : 2,
                             "events_qty_personal" : 2,
                             "events_qty_social" : 2,
                             "time_between_events" : 130
                             },
                             {# LEVEL 5
                             "score_vector" : (-10, -6, 0 , 3, 7),
                             "true_or_false_vector" : (-12, -7, 3, 9, 13, 18),
                             "multiple_choice_vector" : (10, 5, -7),
                             "master_challenge_text" : u"Muy bien! Recuerda que el clima frio puede hacer que pierdas más energía.",
                             "min_qty_correct_ans" : 4,
                             "slide" : None,
                             "events_qty" : 3,
                             "events_qty_personal" : 1,
                             "events_qty_social" : 2,
                             "time_between_events" : 115
                             },
                             {# LEVEL 6
                             "score_vector" : (-10, -6, 0 , 3, 7),
                             "true_or_false_vector" : (-12, -7, 3, 9, 13, 18),
                             "multiple_choice_vector" : (10, 5, -7),
                             "master_challenge_text" : u"¡Vas muy bien, continúa!",
                             "min_qty_correct_ans" : 4,
                             "slide" : "assets/slides/history4.jpg",
                             "events_qty" : 3,
                             "events_qty_personal" : 2,
                             "events_qty_social" : 2,
                             "time_between_events" : 100
                             },
                             {# LEVEL 7
                             "score_vector" : (-12, -8, 0 , 2, 5),
                             "true_or_false_vector" : (-15, -10, 1, 6, 10, 15),
                             "multiple_choice_vector" : (8, 3, -9),
                             "master_challenge_text" : u"Estás muy cerca de ganar el campeonato.",
                             "min_qty_correct_ans" : 5,
                             "slide" : None,
                             "events_qty" : 3,
                             "events_qty_personal" : 3,
                             "events_qty_social" : 3,
                             "time_between_events" : 85
                             },
                             {# LEVEL 8
                             "score_vector" : (-12, -8, 0 , 2, 5),
                             "true_or_false_vector" : (-15, -10, 1, 6, 10, 15),
                             "multiple_choice_vector" : (8, 3, -9),
                             "master_challenge_text" : u"Llegaste al último nivel, si continúas saludable ganarás el campeonato.",
                             "min_qty_correct_ans" : 5,
                             "slide" : None,
                             "events_qty" : 4,
                             "events_qty_personal" : 2,
                             "events_qty_social" : 3,
                             "time_between_events" : 70
                             },
                             {# LEVEL 9
                             "score_vector" : (-12, -8, 0 , 2, 5),
                             "true_or_false_vector" : (-15, -10, 1, 6, 10, 15),
                             "multiple_choice_vector" : (8, 3, -9),
                             "master_challenge_text" : u"¡Vas muy bien, continúa!",
                             "min_qty_correct_ans" : 5,
                             "slide" : "assets/slides/win.jpg",
                             "events_qty" : 4,
                             "events_qty_personal" : 3,
                             "events_qty_social" : 3,
                             "time_between_events" : 55
                             }]                              

class AppLoader:

    def __init__(self, windows_controller, gender, name):
        # loaders
        self.bars_loader = status_bars_creator.BarsLoader()
        
        # status bars
        self.status_bars_controller = self.bars_loader.get_bar_controller()
        self.character_bars = self.bars_loader.get_third_level_bars() #the third level status bars
        
        # events
        self.events_list = self.__load_events(self.status_bars_controller)
        
        # places
        self.places_dictionary = None
        
        # character
        self.character = character.Character(gender, name, 1, 0, "school")
        
        # moods
        self.moods_list = self.__load_moods()
        
        # Environments
        self.places = self.__load_places()
        self.weathers = self.get_weather_list()
        self.environments_dictionary = self.__load_environments()
        self.weather_effects = self.__load_weather_effects()
        
        # Level list
        self.level_conf = CONFIGURATION_LEVEL_LIST
        
        # game manager
        self.events_actions_res = self.__load_events_actions_resolutions()
        
        self.game_man = game_manager.GameManager(self.character, self.status_bars_controller, None, self.events_list, self.get_places(), self.weathers, self.get_environments_dictionary(), self.get_weather_effects(), self.moods_list, windows_controller, self.level_conf, self.events_actions_res)
        actions_loader = actions_creator.ActionsLoader(self.bars_loader.get_bar_controller(), self.game_man)
        self.actions_list = actions_loader.get_actions_list()
        self.game_man.actions_list = self.actions_list
        self.game_man.add_background_action("BARS_DEC") # default effect
        
    
    def get_game_manager(self):
        return self.game_man

    def get_configuration_level_list(self):
        return self.level_conf
        
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

    def get_environments_dictionary(self):
        return self.environments_dictionary
        
    def get_places(self):
        return self.places

    def get_weather_list(self):
        """returns the weather list.
        (weather_id, weather_label, probabilitie_appereance, icon_path, level).
        """
        weather = [("warm", _("Warm"), 35.0, "assets/events/weather/warm.png", 1),
                   ("rainy", _("Rainy"), 25.0, "assets/events/weather/rainy.png", 1),
                   ("cold", _("Cold"), 25.0, "assets/events/weather/cold.png", 1),
                   ("hot", _("Hot"), 25.0, "assets/events/weather/hot.png", 1)]
        return weather

        
    def get_weather_effects(self):
        return self.weather_effects
    
    def __load_events(self, bars_controller):
        #Events constructor params:
        #(directory_path, kid_animation_path, id, description, appereance_probability, time_span, kind, event_status, effect, kid_message, level, preferred_mood=9, message_time_span = time_span)
        
        # Formula to convert effects per minute into effects per CONTROL_INTERVAL
        # factor = CONTROL_INTEVAL/(60 * FPS)
        factor = float(16) / (60 * 14)
        m = lambda x: x*factor
        import operator
        
        _events = []
        
        # Personal Events
        # probabiliy configuration: (bar, type, threshold, probability_percentaje)
        probability = ("all", [("v_frutas", "indirect", 10.0, 30.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("fun", -5), ("h_check", -5)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "constipation", u"Estreñimiento", "neg", None, None, probability, effect, u"Me duele la panza y no \n puedo ir al baño", 1, 2, 150)
        _events.append(event)
        
        probability = ("all", [("w_hands", "indirect", 25.0, 30.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("fun", -5), ("agua", -10), ("defenses", -5), ("toilet", -25), ("h_check", -5)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "diarrhea", u"Diarrea", "neg", None, None, probability, effect, "Tengo diarrea", 1, 2, 150)
        _events.append(event)
        
        probability = ("all", [("nutrition", "indirect", 100.0, 20.0), ("relaxing", "indirect", 100.0, 20.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("fun", -5), ("relaxing", -5), ("h_check", -5)])
        event = events.PersonalEvent("assets/events/personal/headache", None, "headache", u"Dolor de cabeza", "neg", None, None, probability, effect, "Me duele la cabeza", 1, 2, 150)
        _events.append(event)
        
        probability = ("all", [("nutrition", "indirect", 100.0, 20.0), ("relaxing", "indirect", 100.0, 20.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -10), ("relaxing", 10)])
        event = events.PersonalEvent("assets/events/personal/nausea", None, "drunk", u"Borracho", "neg", None, m(2), probability, effect, "Me duele la cabeza", 1, 2, 150)
        _events.append(event)
        
        probability = ("all", [("nutrition", "indirect", 100.0, 20.0), ("relaxing", "indirect", 100.0, 20.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -5), ("weight", -2)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "hunger", u"Hambre", "neg", None, None, probability, effect, "Me duele la cabeza", 1, 2, 150)
        _events.append(event)
        
        probability = ("all", [("nutrition", "indirect", 100.0, 20.0), ("relaxing", "indirect", 100.0, 20.0)])
        effect = effects.Effect(bars_controller, [("energy", -10)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "thirsty", u"Sed", "neg", None, None, probability, effect, "Me duele la cabeza", 1, 2, 150)
        _events.append(event)
        
        probability = ("all", [("nutrition", "indirect", 100.0, 20.0), ("relaxing", "indirect", 100.0, 20.0)])
        effect = effects.Effect(bars_controller, [("defenses", -10), ("fun", -15)])
        event = events.PersonalEvent("assets/events/personal/tired", None, "tired", u"Muy Cansado", "neg", None, None, probability, effect, "Me duele la cabeza", 1, 2, 150)
        _events.append(event)
        
        probability = ("all", [("b_teeth", "indirect", 25.0, 50.0), ("dulces", "direct", 75.0, 20.0)])
        effect = effects.Effect(bars_controller, [("defenses", -10)])
        event = events.PersonalEvent("assets/events/personal/dirty_hands", None, "dirty_hands", u"Manos sucias", "neg", None, None, probability, effect, "Me duele una muela", 1, 5, 150)
        _events.append(event)

        probability = ("all", [("b_teeth", "indirect", 25.0, 50.0), ("dulces", "direct", 75.0, 20.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -10), ("fun", -10), ("relaxing", -10), ("h_check", -10)])
        event = events.PersonalEvent("assets/events/personal/toothache", None, "Dolor de dientes", u"Dolor de dientes", "neg", None, None, probability, effect, "Me duele una muela", 1, 5, 150)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("fun", -15), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/bored", None, "bored", u"Aburrido", "neg", None, m(5), probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("energy", +10), ("defenses", +10)])
        event = events.PersonalEvent("assets/events/personal/happy", None, "happy", u"Feliz", "pos", None, m(2), probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("defenses", +10)])
        event = events.PersonalEvent("assets/events/personal/energetic", None, "energetic", u"Mucha energía", "pos", None, m(2), probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("fun", +10), ("defenses", +10)])
        event = events.PersonalEvent("assets/events/social/friend1_pos", None, "Me veo bien", u"me_veo_bien", "pos", None, m(2), probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -5), ("fun", -10)])
        event = events.PersonalEvent("assets/events/personal/tired", None, "sedentarismo", u"Sedentarismo", "neg", None, m(5), probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("energy", -5), ("defenses", -10), ("agua", -5)])
        event = events.PersonalEvent("assets/events/personal/sunburn", None, "quemaduras_sol", u"Quemaduras por el sol", "neg", None, m(5), probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("defenses", -15), ("toilet", -20), ("energy", -15), ("fun", -5), ("h_check", -5), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/nausea", None, "nausea", u"Nauseas y vómitos", "neg", None, None, probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("defenses", -10), ("energy", -10), ("fun", -5), ("h_check", -5), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "stomach_ache", u"Dolor de panza", "neg", None, m(5), probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("defenses", -15), ("energy", -15), ("fun", -10), ("weight", -1), ("h_check", -5), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/sick", None, "flu", u"Gripe", "neg", None, None, probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("defenses", -20), ("energy", -10), ("fun", -5), ("h_check", -20), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/nausea", None, "intoxicacion", u"Intoxicacion", "neg", None, None, probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("fun", +10), ("energy", +10), ("defenses", +10)])
        event = events.PersonalEvent("assets/events/social/friend1_pos", None, "contento_deberes", u"Muy contento", "pos", None, None, probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        effect = effects.Effect(bars_controller, [("fun", +10), ("energy", +10), ("defenses", +10)])
        event = events.PersonalEvent("assets/events/social/friend1_pos", None, "contento_cocinar", u"Muy contento", "pos", None, None, probability, effect, "Me duele la panza! :(", 1, 2, 50)
        _events.append(event)
        
        # Social events
        #(directory_path, person_path, name, description, appereance_probability, time_span, condicioned_bars, message, level, message_time_span)
        probability = ("all", [("b_teeth", "indirect", 50.0, 70.0), ("dulces", "direct", 75.0, 30.0)])
        event = events.SocialEvent("assets/events/social/mother_neg", "assets/characters/mother.png", "p_caries", _("Prevenir caries"), 5.0, 15, probability, u"Deberías cepillarte los \ndientes", None, 1, 150)
        _events.append(event)

        probability = ("all", [("responsability", "indirect", 60.0, 70.0)])
        event = events.SocialEvent("assets/events/social/father_neg", "assets/characters/father.png", "study", _("Estudiar"), 5.0, 20, probability, u"Debes hacer los deberes", None, 1, 150)
        _events.append(event)

        probability = ("all", [("responsability", "indirect", 60.0, 70.0)])
        event = events.SocialEvent("assets/events/social/teacher_neg", "assets/characters/father.png", "study", _("Estudiar"), 5.0, 20, probability, u"¿Estudiaste las tablas?", None, 1, 150)
        _events.append(event)
        
        probability = ("all", [("responsability", "indirect", 70.0, 70.0)])
        event = events.SocialEvent("assets/events/social/doc_neg", "assets/characters/doctor.png", "health_check", _("Control médico"), 5.0, 30, probability, u"¿Este año fuiste al doctor?", None, 1, 150)
        _events.append(event)

        return _events

    def __load_events_actions_resolutions(self):
        events_actions_res = {("constipation", "arroz_leche") : 70,
                              ("headache", "sleep") : 60,
                              ("study", "homework") : 90,
                              ("p_caries", "brush_teeth") : 60}
        return events_actions_res
    
    def __load_moods(self):
        
        #SICK
        m_sick3 = actions.Mood("sick_3", 0, "assets/kid/moods/sick3", "sick")
        m_sick2 = actions.Mood("sick_2", 1, "assets/kid/moods/sick2", "sick")
        m_sick1 = actions.Mood("sick_1", 2, "assets/kid/moods/sick1", "sick")
        
        #SAD
        m_sad3 = actions.Mood("sad_3", 3, "assets/kid/moods/sad3", "sad")
        m_sad2 = actions.Mood("sad_2", 4, "assets/kid/moods/sad2", "sad")
        m_sad1 = actions.Mood("sad_1", 5, "assets/kid/moods/sad1", "sad")
        
        #ANGRY
        m_angry3 = actions.Mood("angry_3", 6, "assets/kid/moods/angry3", "angry")
        m_angry2 = actions.Mood("angry_2", 7, "assets/kid/moods/angry2", "angry")
        m_angry1 = actions.Mood("angry_1", 8, "assets/kid/moods/angry1", "angry")
        
        #NORMAL
        m_normal = actions.Mood("normal", 9, "assets/kid/moods/normal", "normal")
        
        #HAPPY
        m_happy3 = actions.Mood("happy_3", 10, "assets/kid/moods/happy3", "happy")
        m_happy2 = actions.Mood("happy_2", 11, "assets/kid/moods/happy2", "happy")
        m_happy1 = actions.Mood("happy_1", 12, "assets/kid/moods/happy1", "happy")
        
        #Los moods están ordenados en la lista segun su rank
        moods_list = [m_sick3, m_sick2, m_sick1, m_sad3, m_sad2, m_sad1, m_angry3, m_angry2, m_angry1,
                      m_normal, m_happy3, m_happy2, m_happy1]
        
        return moods_list

    def __load_weather_effects(self):
        weather_effects = {
                   # (clothes_id, weather_id, boolean outdoor) : list of tuples [(id_bar, rate)]
                   # school clothes
                   ("school", "hot", True) : [("fun", 0.5)],
                   ("school", "hot", False) : [("fun", -0.05)],
                   ("school", "rainy", True) : [("fun", 0.05), ("defenses", -1.0)],
                   ("school", "rainy", False) : [("fun", 0.05)],
                   ("school", "warm", True) : [("fun", 0.05)],
                   ("school", "warm", False) : [("fun", 0.05)],
                   ("school", "cold", True) : [("fun", -0.05), ("defenses", -1.0)],
                   ("school", "cold", False) : [("fun", 0.05)],
                   # regular clothes
                   ("regular", "hot", True) : [("fun", 0.5)],
                   ("regular", "hot", False) : [("fun", 0.05)],
                   ("regular", "rainy", True) : [("defenses", -1.0), ("fun", 0.05)],
                   ("regular", "rainy", False) : [("fun", 0.05)],
                   ("regular", "warm", True) : [("fun", 0.5)],
                   ("regular", "warm", False) : [("fun", 0.05)],
                   ("regular", "cold", True) : [("fun", -0.05), ("defenses", -1.0)],
                   ("regular", "cold", False) : [("fun", 0.02)],
        }
        return weather_effects
    
    def __load_places(self):
        places = {
                    "schoolyard" : {"outdoor": True},
                    "square" : {"outdoor": True},
                    "classroom" : {"outdoor": False},
                    "livingroom": {"outdoor": False},
                    "bedroom": {"outdoor": False},
                    "sleep": {"outdoor": False}
                 }
        return places
    
    
    def __load_environments(self):
        environments = {#schoolyard
                        ("schoolyard", "hot") : Environment("assets/background/schoolyard_normal.png"),
                        ("schoolyard", "rainy") : Environment("assets/background/schoolyard_rainy.png"),
                        ("schoolyard", "warm") : Environment("assets/background/schoolyard_normal.png"),
                        ("schoolyard", "cold") : Environment("assets/background/schoolyard_cold.png"),
                        #square
                        ("square", "hot") : Environment("assets/background/square_normal.png"),
                        ("square", "rainy") : Environment("assets/background/square_rainy.png"),
                        ("square", "warm") : Environment("assets/background/square_normal.png"),
                        ("square", "cold") : Environment("assets/background/square_cold.png"),
                        #classroom
                        ("classroom", "hot") : Environment("assets/background/classroom.png"),
                        ("classroom", "rainy") : Environment("assets/background/classroom.png"),
                        ("classroom", "warm") : Environment("assets/background/classroom.png"),
                        ("classroom", "cold") : Environment("assets/background/classroom.png"),
                        #home
                        ("livingroom", "hot") : Environment("assets/background/livingroom.png"),
                        ("livingroom", "rainy") : Environment("assets/background/livingroom.png"),
                        ("livingroom", "warm") : Environment("assets/background/livingroom.png"),
                        ("livingroom", "cold") : Environment("assets/background/livingroom.png"),
                        #country
                        ("bedroom", "hot") : Environment("assets/background/bedroom.png"),
                        ("bedroom", "rainy") : Environment("assets/background/bedroom.png"),
                        ("bedroom", "warm") : Environment("assets/background/bedroom.png"),
                        ("bedroom", "cold") : Environment("assets/background/bedroom.png"),
                        #sleep
                        ("sleep", "hot") : Environment("assets/background/sleep.png"),
                        ("sleep", "rainy") : Environment("assets/background/sleep.png"),
                        ("sleep", "warm") : Environment("assets/background/sleep.png"),
                        ("sleep", "cold") : Environment("assets/background/sleep.png")
                        }                        
        
        return environments

class Environment:
    
    def __init__(self, background_path):
        self.background_path = background_path
    
    def get_background_path(self):
        return self.background_path
    
