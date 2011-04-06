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
                             "score_vector" : (-8, -4, 0 , 5, 10), # incremento central en 10 por motivos de testeo
                             "true_or_false_vector" : (-10, -5, 5, 10, 15, 20),
                             "multiple_choice_vector" : (12, 7, -5),
                             "master_challenge_text" : "Tienes nuevas acciones, ¿te animas a encontrarlas?",
                             "min_qty_correct_ans" : 3, #min qty of corrent answers to pass master challenge.
                             "slide" : None,
                             "events_qty" : 2,
                             "events_qty_personal" : 1,
                             "events_qty_social" : 1,
                             "time_between_events" : 175
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
                             "time_between_events" : 160
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
                             "time_between_events" : 145
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
                             "master_challenge_text" : u"¡Muy bien! A partir de este nivel te puede tocar\nclima frio, ten cuidado porque pierdes energía más rápido.",
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
                             "s_qty_social" : 3,
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

    def __init__(self, gender, name):
        # loaders
        self.bars_loader = status_bars_creator.BarsLoader()
        
        # status bars
        self.status_bars_controller = self.bars_loader.get_bar_controller()
        self.character_bars = self.bars_loader.get_third_level_bars() #the third level status bars
        
        # places
        self.places_dictionary = None
        
        # character
        self.character = character.Character(gender, name, 1, 0, "school")
        
        # events
        self.events_list = self.__load_events(self.status_bars_controller)
        
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
        
        self.game_man = game_manager.GameManager(self.character, self.status_bars_controller, None, self.events_list, self.get_places(), self.weathers, self.get_environments_dictionary(), self.get_weather_effects(), self.moods_list, self.level_conf, self.events_actions_res)
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
        #(directory_path, kid_animation_path, id, description, appereance_probability, time_span, kind, event_status, effect, kid_message, level=1, preferred_mood=9)
        
        sick_3 = 0; sick_2 = 1; sick_1 = 2; sad_3 = 3; sad_2 = 4; sad_1 = 5; angry_3 = 6; angry_2 = 7; angry_1 = 8; normal = 9; happy_1 = 10; happy_2 = 11; happy_3 = 12
        
        # Formula to convert effects per minute into effects per CONTROL_INTERVAL
        # factor = CONTROL_INTEVAL/(60 * FPS)
        factor = float(16) / (60 * 14)
        m = lambda x: x * factor
        import operator
        
        _events = []
        
        # Personal Events
        # probabiliy configuration: (bar, type, threshold, probability_percentaje)
        probability = ("all", [("v_frutas", "indirect", 20, 60)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("fun", -5), ("h_check", -5)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "constipation", u"Estreñimiento", "neg", None, None, probability, effect, u"Me duele la panza y no\npuedo ir al baño", "id.5fyq0oytfruc", 1, sick_2)
        _events.append(event)
        
        probability = ("all", [("w_hands", "indirect", 10, 60), ("defenses", "indirect", 10, 60)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("fun", -5), ("agua", -10), ("defenses", -5), ("toilet", -25), ("h_check", -5)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "diarrhea", u"Diarrea", "neg", None, None, probability, effect, u"Tengo diarrea", "id.dbnmu9igerdx", 1, sick_2)
        _events.append(event)
        
        probability = ("any", [("nutrition", "indirect", 40, 40), ("relaxing", "indirect", 40, 40)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("fun", -5), ("relaxing", -5), ("h_check", -5)])
        event = events.PersonalEvent("assets/events/personal/headache", None, "headache", u"Dolor de cabeza", "neg", None, None, probability, effect, u"Me duele la cabeza", "id.2g0bjuai8neo", 1, sick_1)
        _events.append(event)
        
        probability = ("all", [("nutrition", "indirect", 15, 75), ("energy", "indirect", 15, 75)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -5), ("weight", -2)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "hunger", u"Hambre", "neg", None, None, probability, effect, u"¡Tengo hambre!", "id.62xnnrmqecu9", 1, angry_2)
        _events.append(event)
        
        probability = ("all", [("agua", "indirect", 15, 75)])
        effect = effects.Effect(bars_controller, [("energy", -10)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "thirsty", u"Sed", "neg", None, None, probability, effect, u"¡Tengo sed!", "id.xxt52ebrysva", 1, angry_2)
        _events.append(event)
        
        probability = ("all", [("relaxing", "indirect", 30, 70), ("nutrition", "indirect", 30, 70), ("defenses", "indirect", 30, 70)])
        effect = effects.Effect(bars_controller, [("defenses", -10), ("fun", -15)])
        event = events.PersonalEvent("assets/events/personal/tired", None, "tired", u"Muy Cansado", "neg", None, None, probability, effect, u"Ufff, que cansancio\nque tengo", "id.eqc221j1lpwb", 1, sad_2)
        _events.append(event)
        
        probability = ("all", [("w_hands", "indirect", 30, 70)])
        effect = effects.Effect(bars_controller, [("defenses", -10)])
        event = events.PersonalEvent("assets/events/personal/dirty_hands", None, "dirty_hands", u"Manos sucias", "neg", None, None, probability, effect, u"Puaj, mis manos\nestán sucias", "id.i65x9lfgkdh", 1, sad_1)
        _events.append(event)
        
        probability = ("all", [("b_teeth", "indirect", 40.0, 60), ("dulces", "direct", 75, 60.0), ("nutrition", "indirect", 50, 60.0)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -10), ("fun", -10), ("relaxing", -10), ("h_check", -10)])
        event = events.PersonalEvent("assets/events/personal/toothache", None, "dolor_dientes", u"Dolor de dientes", "neg", None, None, probability, effect, u"¡Ayyyy, mis dientes!", "id.55bloxrmmb9h", 1, sad_3)
        _events.append(event)
        
        probability = ("all", [("fun", "indirect", 90, 50)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("fun", -15), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/bored", None, "bored", u"Aburrido", "neg", None, m(5), probability, effect, u"Que aburrimiento tengo", "id.rj4a3l5xh6jr", 1, sad_1)
        _events.append(event)
        
        probability = ("all", [("fun", "constant", 90, 50), ("defenses", "constant", 90, 50), ("relaxing", "constant", 90, 50)])
        effect = effects.Effect(bars_controller, [("energy", +10), ("defenses", +10)])
        event = events.PersonalEvent("assets/events/personal/happy", None, "happy", u"Feliz", "pos", None, m(2), probability, effect, u"Estoy de muy bien humor", "id.l4dkflvt1jlf", 1, happy_3)
        _events.append(event)
        
        probability = ("all", [("nutrition", "constant", 90, 50), ("defenses", "constant", 90, 50), ("relaxing", "constant", 90, 50), ("energy", "constant", 90, 50)])
        effect = effects.Effect(bars_controller, [("defenses", +10)])
        event = events.PersonalEvent("assets/events/personal/energetic", None, "energetic", u"Mucha energía", "pos", None, m(2), probability, effect, u"¡Guauuu, que energía tengo!", "id.1qjxykbd4ira", 1, happy_2)
        _events.append(event)
        
        probability = ("all", [("physica", "constant", 90, 50), ("hygiene", "constant", 90, 50), ("nutrition", "constant", 90, 50)])
        effect = effects.Effect(bars_controller, [("fun", +10), ("defenses", +10)])
        event = events.PersonalEvent("assets/events/social/friend1_pos", None, "me_veo_bien", u"Me veo bien", "pos", None, m(2), probability, effect, u"Yupiiii, que bien me veo", "id.nny40i7jwdy8", 1, happy_3)
        _events.append(event)
        
        probability = ("all", [("sports", "indirect", 10, 80), ("energy", "constant", 10, 80)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -5), ("fun", -10)])
        event = events.PersonalEvent("assets/events/personal/tired", None, "sedentarismo", u"Sedentarismo", "neg", None, m(5), probability, effect, u"Me agito mucho.\n¿Qué me pasa?", "id.grn7m6ehjqck", 1, angry_1)
        _events.append(event)
        
        probability = ("all", [("overall_bar", "constant", 50, 30)])
        effect = effects.Effect(bars_controller, [("energy", -5), ("defenses", -10), ("agua", -5)])
        event = events.PersonalEvent("assets/events/personal/sunburn", None, "quemaduras_sol", u"Quemaduras por el sol", "neg", None, m(5), probability, effect, u"¡Me arde todo el cuerpo\npor el sol!", "id.jupzdcewf6v2", 1, sick_2)
        event.add_restriction("place", ["schoolyard", "square"])
        event.add_restriction("weather", ["hot"])
        _events.append(event)
        
        probability = ("all", [("w_hands", "indirect", 20, 60)])
        effect = effects.Effect(bars_controller, [("defenses", -15), ("toilet", -20), ("energy", -15), ("fun", -5), ("h_check", -5), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/nausea", None, "nausea", u"Nauseas y vómitos", "neg", None, None, probability, effect, u"Me parece que voy a vomitar", "id.b905vudodsyj", 1, sick_2)
        _events.append(event)
        
        probability = ("all", [("nutrition", "direct", 90, 90)])
        effect = effects.Effect(bars_controller, [("defenses", -10), ("energy", -10), ("fun", -5), ("h_check", -5), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/stomach_ache", None, "stomach_ache", u"Dolor de panza", "neg", None, m(5), probability, effect, u"Comí demasiado,\nme duele la panza", "id.3lsidk9rtp7m", 1, sick_1)
        _events.append(event)
        
        probability = ("all", [("w_hands", "indirect", 30, 90), ("shower", "indirect", 30, 90), ("defenses", "indirect", 30, 90), ("energy", "indirect", 30, 90)])
        effect = effects.Effect(bars_controller, [("defenses", -15), ("energy", -15), ("fun", -10), ("weight", -1), ("h_check", -5), ("relaxing", -10)])
        event = events.PersonalEvent("assets/events/personal/sick", None, "flu", u"Gripe", "neg", None, None, probability, effect, u"Que mal me siento, creo que me engripé", "id.spl2hjco8uic", 1, sick_3)
        _events.append(event)
        
        #probability = ("all", [("overall_bar", "constant", 100.0, 15.0)])
        #effect = effects.Effect(bars_controller, [("defenses", -20), ("energy", -10), ("fun", -5), ("h_check", -20), ("relaxing", -10)])
        #event = events.PersonalEvent("assets/events/personal/nausea", None, "intoxicacion", u"Intoxicacion", "neg", None, None, probability, effect, "Me duele la cabeza y me pican las manos. Debe ser por la fumigación.", "id.irlzb3wkwmi2", 1, sick_2)
        #_events.append(event)
        
        probability = ("all", [("homework", "direct", 75, 70)])
        effect = effects.Effect(bars_controller, [("fun", +10), ("energy", +10), ("defenses", +10)])
        event = events.PersonalEvent("assets/events/social/friend1_pos", None, "contento_deberes", u"Muy contento", "pos", None, m(2), probability, effect, u"¡Que bien que hice\nmis deberes!", "", 1, happy_2)
        _events.append(event)
        
        probability = ("all", [("housekeeping", "direct", 75, 70)])
        effect = effects.Effect(bars_controller, [("fun", +10), ("energy", +10), ("defenses", +10)])
        event = events.PersonalEvent("assets/events/social/friend1_pos", None, "contento_cocinar", u"Muy contento", "pos", None, m(2), probability, effect, u"¡Que rico que cocinamos!", "", 1, happy_2)
        _events.append(event)
        
        # Social events
        mother = "assets/characters/mother.png"
        father = "assets/characters/father.png"
        doctor = "assets/characters/doctor.png"
        teacher = "assets/characters/teacher.png"
        
        doctor_neg = "assets/events/social/doc_neg"; doctor_pos = "assets/events/social/doc_pos"; 
        teacher_neg = "assets/events/social/teacher_neg"; teacher_pos = "assets/events/social/teacher_pos"
        mother_neg = "assets/events/social/mother_neg"; mother_pos = "assets/events/social/mother_pos"
        father_neg = "assets/events/social/father_neg"; father_pos = "assets/events/social/father_pos"
        friend_neg = "assets/events/social/friend1_neg"; friend_pos = "assets/events/social/friend1_pos"
        
        #(directory_path, person_path, name, description, appereance_probability, time_span, condicioned_bars, message, level, message_time_span)
        
        # Parents
        probability = ("any", [("housekeeping", "indirect", 30, 30)])
        effect = effects.Effect(bars_controller, [("housekeeping", -10)])
        event = events.SocialEvent(father_neg, father, "ayuda_cocinar", u"Ayudar a cocinar", "neg", None, m(5), probability, effect, u"¿Vamos a cocinar algo juntos?", "", 1, normal)
        event.add_restriction("place", ["livingroom", "bedroom"])
        _events.append(event)
        
        probability = ("any", [("housekeeping", "indirect", 30, 30)])
        effect = effects.Effect(bars_controller, [("housekeeping", -10)])
        event = events.SocialEvent(mother_neg, mother, "ayuda_limpiar", u"Ayudar con la limpieza", "neg", None, m(5), probability, effect, u"Recuerda ordenar y\nlimpiar tu cuarto.", "", 1, normal)
        event.add_restriction("place", ["livingroom", "bedroom"])
        _events.append(event)
        
        probability = ("any", [("housekeeping", "indirect", 30, 30)])
        effect = effects.Effect(bars_controller, [("housekeeping", -10)])
        event = events.SocialEvent(mother_neg, mother, "ayuda_campo", u"Ayuda en el campo", "neg", None, m(5), probability, effect, u"¿Me puedes ayudar\ncon las tareas\ndel campo?", "", 1, normal)
        event.add_restriction("place", ["livingroom", "bedroom"])
        _events.append(event)

        probability = ("any", [("v_frutas", "indirect", 30, 50)])
        effect = effects.Effect(bars_controller, [("defenses", -10), ("energy", -10)])
        event = events.SocialEvent(father_neg, father, "falta_verduras", u"Falta frutas y verduras", "neg", None, m(5), probability, effect, u"No comiste suficientes\nfrutas y verduras.", "id.tjyof1vhdtvp", 1, normal)
        event.add_restriction("place", ["livingroom", "bedroom", "square"])
        _events.append(event)

        probability = ("all", [("g_aceites", "direct", 99, 50.0)])
        effect = None
        event = events.SocialEvent(mother_neg, mother, "demasiadas_grasas", u"Demasiadas grasas", "neg", None, m(5), probability, effect, u"Cuídate de comer\ndemasiadas grasas", "id.k16o9g5weilb", 1, normal)
        event.add_restriction("place", ["livingroom", "bedroom", "square"])
        _events.append(event)

        probability = ("all", [("dulces", "direct", 99, 50.0)])
        effect = None
        event = events.SocialEvent(father_neg, father, "demasiados_dulces", u"Demasiados dulces", "neg", None, m(5), probability, effect, u"Cuídate de comer\ndemasiados dulces", "id.rdmsw7zadfjg", 1, normal)
        event.add_restriction("place", ["livingroom", "bedroom", "square"])
        _events.append(event)

        probability = ("all", [("relaxing", "indirect", 15, 90.0)])
        effect = effects.Effect(bars_controller, [("defenses", -5), ("energy", -5)])
        event = events.SocialEvent(father_neg, father, "ir_a_dormir", u"Ir a dormir", "neg", None, m(5), probability, effect, u"Llegó la hora\nde ir dormir", "id.mm0q0bwd72vv", 1, normal)
        event.add_restriction("place", ["livingroom", "bedroom", "square"])
        event.add_restriction("time", ["night"])
        _events.append(event)
        
        # Teacher
        probability = ("all", [("farm", "indirect", 1, 75)])
        effect = effects.Effect(bars_controller, [("defenses", -5), ("energy", -5)])
        event = events.SocialEvent(teacher_pos, teacher, "huerta_preparar", u"Preparar tierra", "pos", None, None, probability, effect, u"Vamos a preparar la\ntierra para empezar\nla huerta", "id.nz1g0op683cl", 1, normal)
        event.add_restriction("place", ["classroom", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("farm", "range", (2, 25), (100, 100))])
        effect = effects.Effect(bars_controller, [("farm", -5)])
        event = events.SocialEvent(teacher_pos, teacher, "huerta_sembrar", u"Sembrar", "pos", None, None, probability, effect, u"La tierra de la\nhuerta esta lista para\nsembrar algo.", "id.lq84xe5zxl1c", 1, normal)
        event.add_restriction("place", ["classroom", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("farm", "range", (26, 50), (100, 100))])
        effect = effects.Effect(bars_controller, [("farm", -5)])
        event = events.SocialEvent(teacher_pos, teacher, "huerta_mantener", u"Mantener huerta", "pos", None, None, probability, effect, u"La huerta necesita\nmantenimiento.", "id.lb7rtj5o423g", 1, normal)
        event.add_restriction("place", ["classroom", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("farm", "range", (51, 75), (100, 100))])
        effect = effects.Effect(bars_controller, [("farm", -5)])
        event = events.SocialEvent(teacher_pos, teacher, "huerta_cosechar", u"Cosechar", "pos", None, None, probability, effect, u"¡Juupi! En la huerta\nhay vegetales listos\npara cosechar.", "id.8qqtv41o4kam", 1, normal)
        event.add_restriction("place", ["classroom", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("farm", "direct", 99, 100)])
        effect = None
        event = events.SocialEvent(teacher_pos, teacher, "huerta_plato", u"Nuevo plato de la huerta", "pos", None, None, probability, effect, u"¡Ahora podemos comer\nun plato de la\nhuerta!", "", 1, normal)
        event.add_restriction("place", ["classroom", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("farm", "range", (1, 25), (10, 10))])
        effect = effects.Effect(bars_controller, [("farm", -20)])
        event = events.SocialEvent(teacher_neg, teacher, "huerta_erosion", u"Erosión en la huerta", "neg", None, None, probability, effect, u"¡Uf! La lluvia dañó\nnuestra huerta.", "", 1, normal)
        event.add_restriction("place", ["classroom", "schoolyard"])
        event.add_restriction("weather", ["rainy"])
        _events.append(event)
        
        probability = ("all", [("farm", "range", (51, 75), (10, 10))])
        effect = effects.Effect(bars_controller, [("farm", -5)])
        event = events.SocialEvent(teacher_neg, teacher, "huerta_seca", u"La huerta se secó", "neg", None, None, probability, effect, u"¡Uf! Los plantines se\nsecaron con el calor.", 1, 150)
        event.add_restriction("place", ["classroom", "schoolyard"])
        event.add_restriction("weather", ["hot"])
        _events.append(event)
        
        probability = ("all", [("farm", "range", (75, 100), (10, 10))])
        effect = effects.Effect(bars_controller, [("farm", -5)])
        event = events.SocialEvent(teacher_neg, teacher, "huerta_tormenta", u"Tormenta daña huerta", "neg", None, None, probability, effect, u"¡Dios mio, una\ntormenta destrozó\nnuestra huerta!", "", 1, normal)
        event.add_restriction("place", ["classroom", "schoolyard"])
        event.add_restriction("weather", ["rainy"])
        _events.append(event)
        
        probability = ("all", [("homework", "direct", 75, 80)])
        effect = effects.Effect(bars_controller, [("homework", 5)])
        event = events.SocialEvent(teacher_pos, teacher, "sote", u"Un sote", "pos", None, m(2), probability, effect, u"¡Muy bien, tienes un SOTE!", "", 1, normal)
        event.add_restriction("place", ["classroom", "schoolyard", "livingroom", "bedroom"])
        _events.append(event)
        
        probability = ("all", [("overall_bar", "range", (0, 100), (100, 100))])
        effect = effects.Effect(bars_controller, [("homework", -10)])
        event = events.SocialEvent(teacher_neg, teacher, "tunica", u"Sin túnica", "neg", None, m(5), probability, effect, u"¡Debes usar tu túnica\nen el aula!", "", 1, normal)
        event.add_restriction("place", ["classroom"])
        event.add_restriction("clothes", ["regular"])
        _events.append(event)

        probability = ("all", [("b_teeth", "indirect", 50, 100)])
        effect = effects.Effect(bars_controller, [("h_check", -10), ("b_teeth", -10)])
        event = events.SocialEvent(teacher_neg, teacher, "cepillar_dientes", u"Cepillar dientes", "neg", None, None, probability, effect, u"Tienes que cepillarte\nlos dientes después\nde comer", "id.kb5hjowcg47d", 1, normal)
        event.add_restriction("place", ["classroom"])
        _events.append(event)
        
        # Doctor
        probability = ("all", [("h_check", "indirect", 10, 90)])
        effect = effects.Effect(bars_controller, [("h_check", -5)])
        event = events.SocialEvent(doctor_neg, doctor, "control_salud", u"Control de salud", "neg", None, m(5), probability, effect, u"Hace tiempo que\nno te veo para un\ncontrol de salud.", "id.ng2amhr4x7gm", 1, normal)
        event.add_restriction("place", ["square", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("v_frutas", "indirect", 15, 80)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -10)])
        event = events.SocialEvent(doctor_neg, doctor, "falta_vitaminas", u"Falta vitaminas", "neg", None, m(5), probability, effect, u"Debes consumir suficientes\nvitaminas para estar\nsaludable.", "id.yigvxy2572ym", 1, normal)
        event.add_restriction("place", ["square", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("l_quesos", "indirect", 15, 80), ("c_huevos", "indirect", 15, 80)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -10)])
        event = events.SocialEvent(doctor_neg, doctor, "falta_proteinas", u"Falta proteínas", "neg", None, m(5), probability, effect, u"Necesitas proteínas.\nSon nutritientes básicos\npara nuestra vida.", "id.s39z55w4679l", 1, normal)
        event.add_restriction("place", ["square", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("v_frutas", "indirect", 15, 80), ("c_leguminosas", "indirect", 15, 80)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -10)])
        event = events.SocialEvent(doctor_neg, doctor, "falta_fibras", u"Falta fibras", "neg", None, m(5), probability, effect, u"Acuérdate de consumir\ntodos los días alimentos\nricos en fibras.", "id.cqmvj24se15y", 1, normal)
        event.add_restriction("place", ["square", "schoolyard"])
        _events.append(event)
        
        probability = ("all", [("agua", "indirect", 15, 80)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -10)])
        event = events.SocialEvent(doctor_neg, doctor, "falta_agua", u"Falta agua", "neg", None, m(5), probability, effect, u"Recuerda tomar suficiente\nagua con este calor.", "id.8xy2r5xi8xgw", 1, normal)
        event.add_restriction("place", ["square", "schoolyard"])
        event.add_restriction("weather", ["hot"])
        _events.append(event)
        
        probability = ("all", [("c_leguminosas", "indirect", 15, 80), ("energy", "indirect", 15, 80)])
        effect = effects.Effect(bars_controller, [("energy", -10), ("defenses", -10)])
        event = events.SocialEvent(doctor_neg, doctor, "falta_carbohidratos", u"Falta carbohidratos", "neg", None, m(5), probability, effect, u"Recuerda que los carbohidratos\nson una importante fuente\nde energía.", "id.ugyv9gkcna2i", 1, normal)
        event.add_restriction("place", ["square", "schoolyard"])
        _events.append(event)

        probability = ("all", [("physica", "direct", 80, 90), ("hygiene", "direct", 80, 90), ("h_check", "direct", 80, 90)])
        effect = effects.Effect(bars_controller, [("h_check", +10)])
        event = events.SocialEvent(doctor_pos, doctor, "estas_saludable", u"Estás saludable", "pos", None, m(2), probability, effect, u"Bien, tu control de\nsalud indica que estás\nsaludable.", "id.ctawbbooru2u", 1, normal)
        event.add_restriction("place", ["square", "schoolyard"])
        _events.append(event)

        # AMIG@
        probability = ("all", [("sports", "direct", 70, 80)])
        effect = effects.Effect(bars_controller, [("energy", +5), ("fun", +10)])
        event = events.SocialEvent(friend_pos, self.get_friend(), "nuevos_amigos", u"Me hice nuevos amigos", "pos", None, m(2), probability, effect, u"¿Quieres participar conmigo\nen el campeonato?", "", 1, normal)
        _events.append(event)
        
        probability = ("all", [("sports", "direct", 80, 80)])
        effect = effects.Effect(bars_controller, [("energy", +5), ("fun", +15)])
        event = events.SocialEvent(friend_pos, self.get_friend(), "amigo_alienta", u"Un amigo me alienta", "pos", None, m(2), probability, effect, u"¡Muy bien!\nHiciste muchos goles.", "", 1, normal)
        _events.append(event)
        
        probability = ("all", [("hygiene", "direct", 70, 80)])
        effect = effects.Effect(bars_controller, [("energy", +5), ("fun", +15)])
        event = events.SocialEvent(friend_pos, self.get_friend(), "amigo_cumplido", u"Un amigo me da un cumplido", "pos", None, m(2), probability, effect, u"¡Te ves bien!", "", 1, normal)
        _events.append(event)
        
        probability = ("all", [("sports", "indirect", 25, 80)])
        effect = effects.Effect(bars_controller, [("energy", -5), ("weight", +1)])
        event = events.SocialEvent(friend_neg, self.get_friend(), "amigo_deportes", u"Amigo invita a hacer deportes", "neg", None, m(5), probability, effect, u"¿Vamos a hacer deporte\npara el campeonato?", "id.cfzkxmujas29", 1, normal)
        _events.append(event)
        
        return _events
    
    def get_friend(self):
        if self.character.sex == "boy":        
            return "assets/characters/friend_girl.png"
        else:
            return "assets/characters/friend_boy.png"

    def __load_events_actions_resolutions(self):
        """ A list of tuples containing all the events and the actions that can solve them, with a probability rate. """
        """ Alternatively insted of an action can configure a third option that is an effect, so every action with that effect higher than 0
            will trigger the rule """
        events_actions_res = {("constipation", "doctor") : 30,
                              ("constipation", None, "v_frutas") : 60,
                              ("constipation", None, "agua") : 40,
                              ("constipation", None, "sports") : 50,
                              
                              ("diarrhea", "doctor") : 40,
                              ("diarrhea", None, "agua") : 60,
                              
                              ("headache", "doctor") : 60,
                              ("headache", "relax") : 40,
                              ("headache", "sleep") : 40,
                              
                              ("borracho", "relax") : 50,
                              ("borracho", "agua") : 60,
                              
                              #("hambre", "___") : ___,
                              
                              ("sed", "agua") : 100,
                              
                              ("tired", "relax") : 100,
                              ("tired", "sleep") : 100,
                              
                              ("dirty_hands", "wash_hands") : 100,
                              ("dirty_hands", "shower") : 100,
                              
                              ("dolor_dientes", "brush_teeth") : 100,
                              ("dolor_dientes", "dentist") : 100,
                              ("dolor_dientes", "doctor") : 50,
                              
                              ("bored", None, "sports") : 100,
                              ("bored", None, "fun") : 100,
                              
                              ("sedentarismo", None, "sports") : 40,
                              
                              ("quemaduras_sol", "goto_classroom") : 15,
                              ("quemaduras_sol", "goto_bedroom") : 15,
                              ("quemaduras_sol", "goto_livingroom") : 15,
                              ("quemaduras_sol", "doctor") : 30,
                              ("quemaduras_sol", None, "agua") : 60,
                              
                              ("nausea", None, "agua") : 30,
                              ("nausea", "doctor") : 70,
                              
                              ("stomach_ache", "relax") : 90,
                              ("stomach_ache", "sleep") : 90,
                              ("stomach_ache", "doctor") : 70,
                              
                              ("flu", None, "agua") : 30,
                              ("flu", "doctor") : 70,
                              ("flu", "relax") : 30,
                              ("flu", "sleep") : 30,
                              ("flu", None, "v_frutas") : 10,
                              
                              ("intoxicacion", "doctor") : 100,
            }
        
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
        m_happy1 = actions.Mood("happy_1", 10, "assets/kid/moods/happy3", "happy")
        m_happy2 = actions.Mood("happy_2", 11, "assets/kid/moods/happy2", "happy")
        m_happy3 = actions.Mood("happy_3", 12, "assets/kid/moods/happy1", "happy")
        
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
    
