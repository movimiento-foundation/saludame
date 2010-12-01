# -*- coding: utf-8 -*-

CONTROL_INTERVAL = 16   # Qty of signal calls until a new control is performed (actions, events, weather, etc.)
EVENTS_OCCURRENCE_INTERVAL = 10 #per control interval after an event

HOUR_COUNT_CYCLE = 10 #control intevals that have to pass to management the time of day

import random
import effects
import character
import events

instance = None

class GameManager:
    """
    Clase gestora del sistema. Se encarga del control de las acciones
    y los eventos del juego.
    """
    
    def __init__(self, character, bars_controller, actions_list, events_list, places_list, environments_dictionary, moods_list, windows_controller):
        """
        Constructor de la clase
        """
        global instance
        instance = self
        
        self.character = character
        self.bars_controller = bars_controller
        self.windows_controller = windows_controller
        
        #management
        self.count = 0 #sirve como 'clock' interno, para mantener un orden de tiempo dentro de la clase.
        self.pause = False
        
        #evenst, actions, moods
        self.personal_events_list = self.__get_personal_events(events_list)
        self.social_events_list = self.__get_social_events(events_list)
        self.actions_list = actions_list
        self.moods_list = moods_list        

        self.background_actions = []
        
        #character states
        self.active_char_action = None #Active character action, Action instance
        self.active_event = None
        self.active_social_event = None
        self.active_mood = None
        self.__check_active_mood() # sets active_mood
        
        self.places_list = places_list
        
        #for events handling:
        self.events_interval = EVENTS_OCCURRENCE_INTERVAL
        
        #environment
        self.environments_dictionary = environments_dictionary
        self.current_weather = "sunny" # default weather
        self.current_place = "schoolyard" # default place
        
        # time of day
        self.hour = 2 # value between 0 and 3
                      # 0 night, 1 morning, 2 noon, 3 afternoon
        self.hour_count = HOUR_COUNT_CYCLE # managment cycles that have to pass for handling the hour
        self.day_dic = {0 : "night", 1 : "morning", 2 : "noon", 3 : "afternoon"}
        self.current_time = self.day_dic[self.hour] #current time of day
        
        self.level = 1
        
        #for testing
        self.p_i = 0

        
# management

    def pause_game(self):
        self.pause = True
    
    def continue_game(self):
        self.pause = False
    
    def signal(self):
        """
        Increment signal, it means that a main iteration has been completed 
        """
        if not self.pause:
            self.count += 1
            if(self.count >= CONTROL_INTERVAL):
                self.__control_active_actions() # handle active character actions
                self.bars_controller.calculate_score()  # calculates the score of the score_bar
                self.__control_level() # Checks if level must be changed
                self.__control_active_events() # handle active events
                self.__check_active_mood() # check if the active character mood
                self.__handle_time()
                
                self.count = 0
    
## Environment handling
   
    def update_environment(self):
        """
        Sets the character environment and send a message to the
        windows_controller
        """
        environment_id = self.current_place + "_" + self.current_weather
        environment = self.environments_dictionary[environment_id]
        
        self.windows_controller.set_environment(environment)

### time of day
   
    def __handle_time(self):
        if not self.hour_count:
            self.hour_count = HOUR_COUNT_CYCLE
            
            self.hour += 1
            
            if self.hour > 3:
                self.hour = 0 #night
            
            self.current_time = self.day_dic[self.hour]
            print "cambio el momento del día a: ", self.current_time
            
            if self.hour == 1: #temporal para cambiar el clima
                self.set_current_weather(self.get_random_weather())
            
            self.update_environment()
        else:
            self.hour_count -= 1
        
        
### weather

    def set_current_weather(self, weather):
        """
        Set the current weather.
        """
        self.current_weather = weather
    
    def get_random_weather(self):
        """
        Returns a random weather, never returns the previous weather.
        """
        l = ["rainy", "sunny", "cold", "normal"]
        i = random.randint(0, 3)
        if i == self.p_i:
            return self.get_random_weather()
        else:
           self.p_i = i
        
        print "se genero el clima: ", l[i]
        
        return l[i]
        
### location

    def set_character_location(self, place_id):
        """
        Set the character location.
        """
        print "character went to: ", place_id
        self.current_place = place_id
        
        self.update_environment()

    def get_place(self, place_id):
        """
        Returns the place asociated to the place_id
        """
        for place in self.places_list:
            if(place.id == place_id):
                return place
                
## Actions handling
    
    def execute_action(self, action_id):
        action = self.get_action(action_id)
        
        if action:
            if isinstance(action.effect, effects.Effect): #this action affects status bars
                self.set_active_action(action_id)
            elif isinstance(action.effect, effects.LocationEffect): #this action affects  character location
                if(self.active_char_action):
                    self.interrupt_active_action(None)
                action.perform()
                action.reset()        
    
    def interrupt_active_action(self, action_id):
        """
        Stops the active action if exist, and set as active the
        action with the 'action_id'. If the action_id is 'None', just
        stops the active action.
        """
        self.active_char_action.reset()
        self.active_char_action = None
        self.windows_controller.stop_actual_action_animation()
        
        if(action_id):
            action = self.get_action(action_id)
            if(action):
                self.active_char_action = action
     
    def add_background_action(self, action_id):
        """
        Add a background action.
        """
        action = self.get_action(action_id)
        if(action):
            self.background_actions.append(action)
    
    def get_active_action(self):
        """
        Return the character active action
        """
        return self.active_char_action
    
    def set_active_action(self, action_id):
        """
        Set the active char actions
        """
        #place = get_place(self.character.actual_place) 
        #if(place.allowed_action(action_id)): #continúa con la acción, solo si es permitida en el lugar
        if(not self.active_char_action): #Si existe una accion activa no la interrumpe
            if(True): #dont check char's place yet
                action = self.get_action(action_id)
                if(action):
                    action.perform() 
                    self.windows_controller.show_action_animation(action)
                    self.active_char_action = action
            
    def get_action(self, action_id):
        """
        Returns the action asociated to the id_action
        """
        for action in self.actions_list:
            if(action.id == action_id):
                return action
    
    def __control_active_actions(self):
        """
        Controls active game actions.
        """
        for action in self.background_actions:
            action.perform()
            action.time_span = 1 #that means background actions never stop
            
        if self.active_char_action: #if the character is performing an action: 
            if self.active_char_action.time_left > 0:
                self.active_char_action.perform()
            else: #if the action was completed: 
                self.active_char_action.reset()
                self.active_char_action = None
                self.windows_controller.stop_actual_action_animation()
                
## Moods handling

    def __check_active_mood(self):
        """
        Check the active mood, and set it according to the character state.
        """
        mood = None
        event_preferred_mood = 12 # set in highest mood rank (happy 1)
        overall_bar_percent = self.bars_controller.get_overall_percent()
        overall_bar_mood = 9 # set in normal mood
        
        if(overall_bar_percent < 0.33): 
            overall_bar_mood = 5 #set mood in sad grade 1
        elif(overall_bar_percent > 0.66):
            overall_bar_mood = 10 #set mood in happy 3
        
        if(self.active_event):
            event_preferred_mood = self.active_event.preferred_mood
        
        if(event_preferred_mood <= overall_bar_mood): # choose the lowest value
            mood = self.moods_list[event_preferred_mood]
        else:
            mood = self.moods_list[overall_bar_mood]
        
        if(mood <> self.active_mood):
            self.active_mood = mood
            self.windows_controller.set_mood(mood)
            print "cambio estado de animo a: ", self.active_mood.name
        
## Events handling

    def __control_active_events(self):
        """
        Active events handler
        """
        self.__handle_personal_events()
        self.__handle_social_events()
         
        if self.events_interval == 0:
            if random.randint(0, 1):
                # add personal
                self.active_event = self.__get_random_event(self.personal_events_list) #get a new random event
                self.windows_controller.add_personal_event(self.active_event) #notify windows controller
                print "se disparó el evento: ", self.active_event.name
            else:
                # add social
                self.active_social_event = self.__get_random_event(self.social_events_list)                
                self.windows_controller.add_social_event(self.active_social_event)
                print "se disparó el evento: ", self.active_social_event.name
            
            self.events_interval = EVENTS_OCCURRENCE_INTERVAL
        else:
            self.events_interval -= 1
        
    
    def __handle_social_events(self):
        """
        Handle social events
        """
        if(self.active_social_event):
            
            if(self.active_social_event.time_left):
                self.active_social_event.perform()
            else:                
                self.windows_controller.remove_social_event(self.active_social_event)
                self.active_social_event.reset()
                self.active_social_event = None
    
    def __handle_personal_events(self):
        """
        Handle personal events
        """
        if(self.active_event):
            
            if(self.active_event.time_left):
                self.active_event.perform()
            else:                
                self.windows_controller.remove_personal_event(self.active_event)
                self.active_event.reset()
                self.active_event = None
    
    def __get_random_event(self, events_list):
        """
        Get a random event
        """
        self.__update_events_probability(events_list) # it updates the probabilities of the list's events
        
        max_rand = self.__calculate_max_rand(events_list) # get the max_rand for the events_list
        
        probability_ranges = self.__calculate_ranges(events_list) # calculate the ranges for these events
        
        rand = random.randint(0, max_rand)
        for i in range(0, len(probability_ranges)):
            if(rand >= probability_ranges[i][0] and rand <= probability_ranges[i][1]):
                return events_list[i]
    
    def __update_events_probability(self, events_list):
        """
        Updates events probability
        """
        #updates events probability
        for evt in events_list:
            print evt.name, " prob: ", evt.update_probability(self.bars_controller.get_bars_status())
            
    def __calculate_max_rand(self, events_list):
        """
        Calculates the max random number
        """
        max_rand = 0
        for event in events_list:
            max_rand += event.get_probability()
        return max_rand
    
    def __calculate_ranges(self, events_list):
        """
        Calculate a probability range for each event and returns
        a list of ranges
        """
        previous = 0
        ranges = []
        for event in events_list:
            ranges += [(previous, previous + event.get_probability())]
            previous += event.get_probability() + 1
        return ranges
    
    def __get_social_events(self, events_list):
        
        social_events = []
        for evt in events_list:
            if isinstance(evt, events.SocialEvent):
                social_events.append(evt)
                
        return social_events
        
    
    def __get_personal_events(self, events_list):
        
        personal_events = []
        for evt in events_list:
            if isinstance(evt, events.PersonalEvent):
                personal_events.append(evt)
                
        return personal_events
    
# Score handling
    def add_points(self, points):
        score_bar = self.bars_controller.score_bar
        score_bar.value += points
        
    def __control_level(self):
        score_bar = [bar for bar in self.bars_controller.bars if bar.id == "score_bar"][0]
        if score_bar.value == 100:
            # sets master challenge
            self.level += 1
            score_bar.value = 1
            self.set_master_challenge()
            
        if score_bar.value == 0:
            # falls back to previous level
            if self.level > 1:
                self.level -= 1
                score_bar.value = 99

    def set_master_challenge(self):
        # The master challenge occurs when the player completed a level.
        # If it is answered correctly the player wins some points, so he starts the new level with these points
        # Otherwise it loses some points, and continues in the same level, so he has to continue playing to
        # reach the master challenge again.
        self.challenges_creator.get_challenge()
        self.windows_controller.set_active_window("challenges_window")
        


