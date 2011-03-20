# -*- coding: utf-8 -*-

INSTANCE_FILE_PATH = "game.save"
GAME_VERSION = "1.0"

MAX_LEVEL = 9 #max qty of game levels  

CONTROL_INTERVAL = 16   # Qty of signal calls until a new control is performed (actions, events, weather, etc.) 

MAX_IDLE_TIME = 50 # Qty of control intervals until the kid executes an attention action.
ATTENTION_ACTION = "attention" #action that executes when the character is idle so much time

HOUR_COUNT_CYCLE = 320 #control intevals that have to pass to management the time of day ... 320 = 5 min. apróx

import random
import effects
import character
import events
import sound_manager

instance = None

class GameManager:
    """
    Clase gestora del sistema. Se encarga del control de las acciones
    y los eventos del juego.
    """
    
    def __init__(self, character, bars_controller, actions_list, events_list, places_dictionary, weathers, environments_dictionary, weather_effects, moods_list, windows_controller, level_conf, events_actions_res):
        """
        Constructor de la clase
        """
        global instance
        instance = self

        #level configuration list
        self.level_conf = level_conf
        
        self.character = character
        self.bars_controller = bars_controller
        self.windows_controller = windows_controller
        
        #management
        self.count = 0 #sirve como 'clock' interno, para mantener un orden de tiempo dentro de la clase.
        self.pause = False
        
        self.idle_time = 0
        
        #events, actions, moods
        self.events_actions_res = events_actions_res#this is a dic {(event_id, action_id):prob} where prob is the action probability to solve the event
        self.personal_events_list = self.__get_personal_events(events_list)
        self.social_events_list = self.__get_social_events(events_list)
        self.events_dict = dict([(e.name, e) for e in events_list])
        
        self.actions_list = actions_list
        self.moods_list = moods_list

        self.background_actions = []
        
        #character states
        self.active_char_action = None #Active character action, Action instance
        self.active_events = [] #active personal events
        self.active_social_events = []
        self.active_mood = None
        #self.__check_active_mood() # sets active_mood -> doesn't work because status bars aren't ready
        
        self.places_dictionary = places_dictionary
        self.weathers = weathers
        
        #for events handling:
        self.events_interval = self.level_conf[self.character.level - 1]["time_between_events"]

        #environment
        self.environments_dictionary = environments_dictionary
        self.current_weather = self.weathers[0] # default weather
        self.environment = None
        
        # time of day
        self.hour = 2 # value between 0 and 3
                      # 0 night, 1 morning, 2 noon, 3 afternoon
        self.hour_count = HOUR_COUNT_CYCLE # managment cycles that have to pass for handling the hour
        self.day_dic = {0 : "night", 1 : "morning", 2 : "noon", 3 : "afternoon"}
        self.current_time = self.day_dic[self.hour] #current time of day

        # menu handling
        self.menu_active = False
        
        # weather
        self.weather_effects = weather_effects
        self.environment_effect = None  # this is an Effect that represents the effect on the character by the environment: weather + place + clothes
        self.update_environment_effect()

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
            #handle actions.
            self.__handle_active_character_action() #handle active character action (performing and animation)
            if self.count >= CONTROL_INTERVAL:
                self.bars_controller.calculate_score()  # calculates the score of the score_bar
                self.__control_background_actions() # background actions
                self.__control_level() # Checks if level must be changed
                self.__control_active_events() # handle active events
                self.__check_active_mood() # check if the active character mood
                self.__handle_time()
                self.__check_idle_time()
                if self.environment_effect:
                    self.environment_effect.activate()
                else:
                    self.update_environment_effect()
                
                self.count = 0

    def get_current_level_conf(self):
        """
        returns the current level configuration dictionary
        """
        assert self.character.level > 0
        return self.level_conf[self.character.level -1]

    def __check_idle_time(self):
        """ checks if the kid is idle for so much time (more than MAX_IDLE_TIME). If he is, then
        plays an attention action.
        """
        if self.active_char_action:
            self.idle_time = 0
        elif self.idle_time <= MAX_IDLE_TIME:
            self.idle_time += 1
        else:
            self.idle_time = 0
            self.execute_action(ATTENTION_ACTION)
            

## Environment handling
   
    def update_environment(self):
        """
        Sets the character environment and send a message to the
        windows_controller
        """
        environment_id = (self.character.current_place, self.current_weather[0])
        self.environment = self.environments_dictionary[environment_id]
        
        self.windows_controller.set_environment(self.environment, self.current_time)
    
    def update_environment_effect(self):
        """
        Create and action with the effect on the character by the environment, taking current_place +
        clothes + current_weather.
        """
        outdoor = self.places_dictionary[self.character.current_place]["outdoor"]
        affected_bars = self.weather_effects[(self.character.clothes, self.current_weather[0], outdoor)]
        effect = effects.Effect(self.bars_controller, affected_bars)
        
        self.environment_effect = effect
        print "environment effect updated: ", affected_bars

### time of day
   
    def __handle_time(self):
        if not self.hour_count:
            sound_manager.instance.play_time_change()
            
            self.hour_count = HOUR_COUNT_CYCLE
            
            self.hour += 1
            
            if self.hour > 3:
                self.hour = 0 #night
            
            self.current_time = self.day_dic[self.hour]
            print "cambio el momento del día a: ", self.current_time
            self.update_environment()
            
            if self.hour == 1: #temporal para cambiar el clima
                self.change_current_weather()
        else:
            self.hour_count -= 1
        
        
### weather
    
    def change_current_weather(self):
        """changes the current weather
        """
        self.set_current_weather(self.get_random_weather())

    def set_current_weather(self, weather):
        """
        Set the current weather.
        """
        self.current_weather = weather
        self.update_environment_effect()
        self.update_environment()
    
    def get_random_weather(self):
        """
        Returns a random weather, based on the appearance 
        probability of each one, and in the current character
        level.
        """
        aux = 0
        allowed_weathers = [weather for weather in self.weathers if weather[4] <= self.character.level]
        ranges = self.get_weather_prob_ranges(allowed_weathers)
        if ranges:
            max_rand = ranges[-1][1]
            if max_rand == 0:
                #if they havent probabilities, then it returns default.
                return self.weathers[0]
            else:
                rand = random.random()*max_rand
                for i in range(0, len(ranges)):
                    if rand >= ranges[i][0] and rand <= ranges[i][1]:
                        return self.weathers[i]
        else:
            return self.weathers[0] #default weather

    def get_weather_prob_ranges(self, weather_list):
        """ maps the probability_appreance of each weather to a range.
        """
        if len(weather_list) > 0:    
            previous = 0
            ranges = []
            for weath in weather_list:
                ranges += [(previous, previous + weath[2])]
                previous += weath[2]
            return ranges
        else:
            return None
            
    
    
### location

    def set_character_location(self, place_id):
        """
        Set the character location.
        """
        print "character went to: ", place_id
        self.character.current_place = place_id
        
        self.update_environment()
        self.update_environment_effect()
            
### Clothes
    def set_character_clothes(self, clothes_id):
        """
        Set the character clothes.
        """
        self.character.set_clothes(clothes_id)
        print "character's clothes: ", clothes_id
        
        self.update_environment_effect()
        self.windows_controller.update_clothes()
                
## Actions handling
    
    def execute_action(self, action_id):
        action = self.get_action(action_id)
        
        if action:
            if isinstance(action.effect, effects.Effect): #this action affects status bars
                self.set_active_action(action_id)
            elif isinstance(action.effect, effects.LocationEffect): #this action affects character location
                if self.active_char_action:
                    self.interrupt_active_action(None)
                action.perform()
                action.reset()
            elif isinstance(action.effect, effects.ClothesEffect): #this action affects character clothes
                if self.active_char_action:
                    self.interrupt_active_action(None)
                action.perform()
                action.reset()
    
    def interrupt_active_action(self, action_id):
        """
        Stops the active action if exist, and set as active the
        action with the 'action_id'. If the action_id is 'None', just
        stops the active action.
        """
        if self.active_char_action:
            self.active_char_action.reset()
            self.active_char_action = None
            self.windows_controller.stop_current_action_animation()
        
        if action_id:
            action = self.get_action(action_id)
            if action:
                self.active_char_action = action
     
    def add_background_action(self, action_id):
        """
        Add a background action.
        """
        action = self.get_action(action_id)
        if action:
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
        
        if not self.active_char_action: #if there is not an active character action
            action = self.get_action(action_id)
            if action:
                action.perform()
                self.windows_controller.show_action_animation(action)
                self.active_char_action = action
            
    def get_action(self, action_id):
        """
        Returns the action asociated to the id_action
        """
        for action in self.actions_list:
            if action.id == action_id:
                return action
            
    def get_lowest_bar(self):
        return self.bars_controller.get_lowest_bar()

    def __try_solve_events(self, action_id):
        """Try to solve an active event with the active character
        action"""

        for evt in self.active_events:
            if (evt.name, action_id) in self.events_actions_res:
                rand = random.randint(0,100)
                print evt.name," ", action_id
                prob = self.events_actions_res[(evt.name, action_id)]
                print "TRYING SOLVE ", evt.name," performing: ", action_id, " PROBABILITY: ", prob
                if rand <= prob:
                    print "EVENT SOLVED "
                    self.remove_personal_event(evt)
                else:
                    print "EVENT NOT SOLVED"

        for evt in self.active_social_events:
            if (evt.name, action_id) in self.events_actions_res:
                rand = random.randint(0,100)
                prob = self.events_actions_res[(evt.name, action_id)]
                print "TRYING SOLVE ", evt.name," performing: ", action_id, " PROBABILITY: ", prob
                if rand <= prob:
                    print "EVENT SOLVED "
                    self.remove_social_event(evt)
                else:
                    print "EVENT NOT SOLVED"

    def __handle_active_character_action(self):
        if self.active_char_action:
            #handle performance
            if self.count >= CONTROL_INTERVAL:
                if self.active_char_action.time_left > 0:
                    self.active_char_action.perform()
 
            #handle animation
            if self.active_char_action.kid_frames_left > 0:
                self.active_char_action.decrease_frames_left()
                if self.active_char_action.kid_frames_left == 0:
                    self.windows_controller.stop_current_action_animation()
                    self.__try_solve_events(self.active_char_action.id)
            
            #when the action ends to run (animation and performance), tries to solve an event and reset the action
            if self.active_char_action.kid_frames_left == 0 and self.active_char_action.time_left == 0:
                self.active_char_action.reset()
                cons = self.active_char_action.effect.get_consequence(self.events_dict, self.bars_controller.get_bars_status())
                self.active_char_action = None
                if cons:
                    self.check_consequence_event(cons)
    
    def __control_background_actions(self):
        """
        Controls active background actions.
        """
        for action in self.background_actions:
            action.perform()
            action.time_span = -1 #that means background actions never stop
            
## Moods handling

    def __check_active_mood(self):
        """
        Check the active mood, and set it according to the character state.
        """
        mood = None
        event_preferred_mood = 12 # set in highest mood rank (happy 1)
        overall_bar_percent = self.bars_controller.get_overall_percent()
        overall_bar_mood = 9 # set in normal mood
        
        if overall_bar_percent < 0.33:
            overall_bar_mood = 5 #set mood in sad grade 1
        elif overall_bar_percent > 0.66:
            overall_bar_mood = 10 #set mood in happy 3
        
        mood = self.moods_list[overall_bar_mood]
        
        event_preferred_moods = [event.preferred_mood for event in self.active_events]
        #event_preferred_moods += [event.preferred_mood for event in self.active_social_events]
        if event_preferred_moods:
            event_preferred_mood = min(event_preferred_moods)
        
            if event_preferred_mood <= overall_bar_mood: # choose the lowest value
                mood = self.moods_list[event_preferred_mood]
        
        if mood <> self.active_mood:
            self.active_mood = mood
            self.windows_controller.set_mood(mood)
            self.character.mood = mood
            print "cambio estado de animo a: ", self.active_mood.name
            sound_manager.instance.set_music(mood.music)

## Events handling

    def add_random_personal_event(self):
        event = self.__get_random_event(self.personal_events_list) #get a new random event
        if event:
            self.add_personal_event(event)
            
    def add_personal_event(self, event):
        if not (event in self.active_events):
            self.windows_controller.add_personal_event(event)   # notify windows controller
            self.active_events.append(event)
            print "se disparó el evento: ", event.name
    
    def add_random_social_event(self):
        event = self.__get_random_event(self.social_events_list)
        if event:
            self.add_social_event(event)
    
    def add_social_event(self, event):
        if not (event in self.active_social_events):
            self.active_social_events.append(event)
            self.windows_controller.add_social_event(event)
            print "se disparó el evento: ", event.name

    def __control_active_events(self):
        """
        Active events handler
        """
        self.__handle_personal_events()
        self.__handle_social_events()
        
        if self.events_interval == 0 and not self.menu_active and not self.active_char_action:
            if random.randint(0, 1):
                # add personal
                if len(self.active_events) < self.level_conf[self.character.level - 1]["events_qty_personal"]:
                    self.add_random_personal_event()
            else:
                # add social
                if len(self.active_social_events) < self.level_conf[self.character.level - 1]["events_qty_social"]:
                    self.add_random_social_event()
            
            self.events_interval = self.level_conf[self.character.level - 1]["time_between_events"]
        elif self.events_interval > 0:
            self.events_interval -= 1

    def check_consequence_event(self, event):
        """ Check if an event can be added """
        if event in self.personal_events_list:
            if len(self.active_events) < self.level_conf[self.character.level - 1]["events_qty_personal"]:
                self.add_personal_event(event)
        else:
            if len(self.active_social_events) < self.level_conf[self.character.level - 1]["events_qty_social"]:
                self.add_social_event(event)
        
    def remove_social_event(self, event):
        """removes an active social event
        """
        self.windows_controller.remove_social_event(event)
        event.reset()
        self.active_social_events.remove(event)

    def remove_personal_event(self, event):
        """removes an active personal event
        """
        self.windows_controller.remove_personal_event(event)
        event.reset()
        self.active_events.remove(event)

    def __handle_social_events(self):
        """
        Handle social events
        """
        for event in self.active_social_events:
            if event.time_left:
                event.perform()
            else:
                self.remove_social_event(event)
    
    def __handle_personal_events(self):
        """
        Handle personal events
        """
        for event in self.active_events:
            
            if event.time_left:
                event.perform()
            else:
                self.remove_personal_event(event)
    
    def __get_random_event(self, events_list):
        """
        Get a random event
        """
        self.__update_events_probability(events_list) # it updates the probabilities of the list's events
        allowed_events = [evt for evt in events_list if evt.level <= self.character.level]#verify wich events are allowed in the current level.
        if len(allowed_events) > 0:
            probability_ranges = self.__calculate_ranges(allowed_events) # calculate the ranges for these events
            max_rand = probability_ranges[-1][1]    # Second member of last event

            if max_rand == 0:
                # There aren't events with probability
                return None
            else:
                rand = random.random()*max_rand
                for i in range(0, len(probability_ranges)):
                    if rand >= probability_ranges[i][0] and rand <= probability_ranges[i][1]:
                        return allowed_events[i]
    
    def __update_events_probability(self, events_list):
        """
        Updates events probability
        """
        bars_status_dict = self.bars_controller.get_bars_status()
        #updates events probability
        for evt in events_list:
            evt.update_probability(bars_status_dict)
            
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
            previous += event.get_probability()
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

# level handling

    def next_level(self):
        """pass to the next level
        """
        if self.character.level < MAX_LEVEL:
            self.character.level += 1
            self.bars_controller.score_bar.value = 1

    def previous_level(self):
        """comes back to the preivous level
        """
        if self.character.level > 1:
            self.character.level -= 1
            self.bars_controller.score_bar.value = self.bars_controller.score_bar.max - 1
        else:
            self.bars_controller.score_bar.value = 1

    def __control_level(self):
        score_bar = self.bars_controller.score_bar
        if score_bar.value == score_bar.max:
            # sets master challenge
            self.set_master_challenge()
            self.next_level()
            
        if score_bar.value == 0:
            # falls back to previous level
            self.previous_level()

    def set_master_challenge(self):
        # The master challenge occurs when the player completed a level.
        # If it is answered correctly the player wins some points, so he starts the new level with these points
        # Otherwise it loses some points, and continues in the same level, so he has to continue playing to
        # reach the master challenge again.
        
        #self.windows_controller.show_master_challenge_intro()
        self.windows_controller.main_window.kidW._cb_button_click_master_challenge(None)
    
# Score handling
    def add_points(self, points):
        score_bar = self.bars_controller.score_bar
        score_bar.increase(points)
        self.character.score = score_bar.value
        
# Save, load and reset game

    def reset_game(self):
        """
        Reset game properties
        """
        # actions
        self.interrupt_active_action(None)
        # events
        for personal_event in self.active_events:
            self.windows_controller.remove_personal_event(personal_event)
        for social_event in self.active_social_events:
            self.windows_controller.remove_social_event(social_event)
        self.active_events = []
        self.active_social_events = []
        self.events_interval = self.level_conf[self.character.level - 1]["time_between_events"]
        # character
        self.character.reset()
        # bars
        self.bars_controller.reset()
        # weather
        self.current_weather = self.weathers[0] # default weather
        self.update_environment()
        self.update_environment_effect()
        self.windows_controller.update_clothes()
        # hour
        self.hour = 2
        self.hour_count = HOUR_COUNT_CYCLE
        self.current_time = self.day_dic[self.hour]
        print "game reseted successfully... "

    def save_game(self):
        """
        Save the game instance
        """
        game_status = {}
        ##save bars status
        bars_status_dic = self.bars_controller.get_bars_status()
        ##save character properties
        char_properties = self.character.get_status()
        ##
        game_status.update(bars_status_dic)
        game_status.update(char_properties)
        game_status.update({"version" : GAME_VERSION})
        
        try:
            f = open(INSTANCE_FILE_PATH, 'w')
            f.write(game_status.__str__())
            f.close()
            
            print "se guardo la partida con exito. Version ", GAME_VERSION
        except:
            print "no se pudo guardar la partida."
            raise

    def load_game(self):
        try:
            f = open(INSTANCE_FILE_PATH)
            str = f.read()
            game_status = eval(str)
            f.close()
            
            #load bars status
            self.bars_controller.load_bars_status(game_status)
            print "status bars loaded..."
            #character properties
            self.character.load_properties(game_status)
            print "character properties loaded..."
            
            self.update_environment()
            self.update_environment_effect()
            self.windows_controller.update_clothes()
            
            print "se cargo la partida con exito. Version ", game_status["version"]
        except:
            print "no se pudo cargar la partida."

    def get_level(self):
        """
        returns the character's  current level
        """
        return self.character.level

    def get_active_events(self):
        """
        returns current events
        """
        events = self.active_events + self.active_social_events
        return events
    
    def get_current_place(self):
        """
        returns character's current location.
        """
        return self.character.current_place
    
    def get_current_hour(self):
        """
        returns current momento of day.
        """
        return self.current_time
