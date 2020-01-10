# -*- coding: utf-8 -*-

# Copyright (C) 2011 ceibalJAM! - ceibaljam.org
# This file is part of Saludame.
#
# Saludame is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Saludame is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Saludame. If not, see <http://www.gnu.org/licenses/>.

GAME_VERSION = "1.0"

MAX_LEVEL = 9 #max qty of game levels  

CONTROL_INTERVAL = 16   # Qty of signal calls until a new control is performed (actions, events, weather, etc.) 

CHALLENGES_INTERVAL = 300

MAX_IDLE_TIME = 50 # Qty of control intervals until the kid executes an attention action.
ATTENTION_ACTION = "attention" #action that executes when the character is idle so much time

HOUR_COUNT_CYCLE = 200  # control intevals that have to pass to change the time of day ... 200 = 4 min. apróx

# Game Over: If the overall bar stays under the threshold for a whole interval, the game will end
GAME_OVER_INTERVAL = 120
GAME_OVER_THRESHOLD = 20

import random
import effects
import character
import events
import sound_manager

instance = None

class GameManager():
    """
    Clase gestora del sistema. Se encarga del control de las acciones
    y los eventos del juego.
    """
    
    def __init__(self, character, bars_controller, actions_list, events_list, places_dictionary, weathers, environments_dictionary, weather_effects, moods_list, level_conf, events_actions_res, events_forbidden_actions, conditions):
        """
        Constructor de la clase
        """
        
        #Singleton
        global instance
        instance = self

        self.started = False
        self.game_over = False
        
        #level configuration list
        self.level_conf = level_conf
        
        self.character = character
        self.bars_controller = bars_controller
        self.windows_controller = None
        
        #management
        self.count = 0 #sirve como 'clock' interno, para mantener un orden de tiempo dentro de la clase.
        self.pause = False
        
        self.idle_time = 0
        self.challenge_cicles = CHALLENGES_INTERVAL
        self.game_over_cicles = GAME_OVER_INTERVAL
        
        #events, actions, moods
        self.personal_events_list = self.__get_personal_events(events_list)
        self.social_events_list = self.__get_social_events(events_list)
        self.events_dict = dict([(e.name, e) for e in events_list])
                
        self.actions_list = actions_list
        self.moods_list = moods_list
        
        self.events_actions_res = events_actions_res#this is a dic {(event_id, action_id):prob} where prob is the action probability to solve the event
        self.events_forbidden_actions = events_forbidden_actions

        self.conditions = conditions
        
        self.background_actions = []
        
        #character states
        self.active_char_action = None #Active character action, Action instance
        self.active_events = [] #active personal events
        self.active_social_events = []
        self.active_mood = None
        
        self.places_dictionary = places_dictionary
        self.weathers = weathers
        
        #for events handling:
        self.events_interval = self.get_level_conf_value("time_between_events")
        
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
        
        # weather effects
        self.weather_effects = weather_effects
        self.environment_effect = None  # this is an Effect that represents the effect on the character by the environment: weather + place + clothes
        
        self.update_environment()
        
        self.old_place = None
        
        self.windows_controller = None

    def start(self, windows_controller):
        self.windows_controller = windows_controller
        self.started = True
        
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
                self.__control_score() # calculates the score of the score_bar
                self.__control_background_actions() # background actions
                self.__control_level() # Checks if level must be changed
                self.__control_active_events() # handle active events
                self.__check_active_mood() # check if the active character mood
                self.__handle_time()
                self.__check_idle_time()
                self.__control_challenges()
                self.__control_game_over()
                if self.environment_effect:
                    self.environment_effect.activate(1)
                else:
                    self.update_environment_effect()
                
                self.count = 0

    def __control_score(self):
        score_vector_per_minute = self.get_level_conf_value("score_vector")
        score_vector_per_cicle = [float(value)*2/60 for value in score_vector_per_minute]
        self.bars_controller.calculate_score(score_vector_per_cicle)
        
    def get_current_level_conf(self):
        """
        returns the current level configuration dictionary
        """
        assert self.character.level > 0
        return self.level_conf[self.character.level - 1]

    def get_level_conf_value(self, key):
        return self.level_conf[self.character.level - 1][key]
    
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
        Sets the character environment and send a message to the windows_controller
        """
        environment_id = (self.character.current_place, self.current_weather[0])
        self.environment = self.environments_dictionary[environment_id]
        
        self.update_environment_effect()
        
        if self.started:
            self.windows_controller.set_environment(self.environment, self.current_time)
        
        self.check_environment_events()
    
    def update_environment_effect(self):
        """
        Create and action with the effect on the character by the environment, taking current_place +
        clothes + current_weather.
        """
        outdoor = self.places_dictionary[self.character.current_place]["outdoor"]
        affected_bars = self.weather_effects[(self.character.clothes, self.current_weather[0], outdoor)]
        effect = effects.Effect(affected_bars)
        effect.set_bar_controller(self.bars_controller)
        
        self.environment_effect = effect
        print "environment effect updated: ", affected_bars

### time of day
   
    def __handle_time(self):
        if not self.hour_count:
            self.change_time()
        else:
            self.hour_count -= 1
        
    def change_time(self):
        sound_manager.instance.play_time_change()
        
        self.hour_count = HOUR_COUNT_CYCLE
        
        self.hour += 1
        
        if self.hour > 3:
            self.hour = 0 #night
        
        self.current_time = self.day_dic[self.hour]
                
        if self.hour == 1:
            # Changes the weather and updates the envirnoment
            self.change_current_weather()
        else:
            self.update_environment()
    
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
                        return allowed_weathers[i]
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
            
    
    def get_restrictions(self):
        """ returns a dictionary with all the environmental restrictions """
        return {
            "clothes": self.character.clothes,
            "place": self.character.current_place,
            "weather": self.current_weather,
            "time": self.current_time,
        }
        
### location

    def set_character_location(self, place_id):
        """
        Set the character location.
        """                    
        self.character.current_place = place_id
        
        self.update_environment()
            
### Clothes
    def set_character_clothes(self, clothes_id):
        """
        Set the character clothes.
        """
        self.character.set_clothes(clothes_id)
        
        self.update_environment_effect()
        self.windows_controller.update_clothes()
                
## Actions handling
    def check_action_condition(self, condition):
        bars_status_dict = self.bars_controller.get_bars_status()
        for c in self.conditions:
            if c.id == condition:
                return c.evaluate(bars_status_dict)
                
    
    def execute_action(self, action_id, action_label=None):
        action = self.get_action(action_id)
        
        if action and action.effect:
            self.set_active_action(action_id)
            self.check_forbidden_action(action, action_label)
    
    def check_forbidden_action(self, action, action_label):
        for evt in self.active_events + self.active_social_events:
            forbidden_actions = self.events_forbidden_actions.get(evt.name)
            if forbidden_actions:
                if action.id in forbidden_actions:
                    self.set_forbidden_action(evt, action_label)
                    break
            
    def set_forbidden_action(self, event, action_label):
        self.windows_controller.windows["panel_window"].add_info_button_event(event, action_label)
    
    def interrupt_active_action(self, action_id):
        """
        Stops the active action if exist, and set as active the
        action with the 'action_id'. If the action_id is 'None', just
        stops the active action.
        """
        if self.active_char_action:
            if self.active_char_action.background:
                self.set_character_location(self.old_place)
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
        Sets the active char action, and asks the gui to show it
        """
        if not self.active_char_action: #if there is not an active character action
            action = self.get_action(action_id)
            if action:
                self.old_place = self.character.current_place
                
                action.perform(0)
                self.windows_controller.show_action_animation(action)
                self.active_char_action = action
    
    def get_action(self, action_id):
        """
        Returns the action asociated to the id_action
        """
        for action in self.actions_list:
            if action.id == action_id:
                return action
    
    def __try_solve_events(self, action_id):
        """Try to solve an active event with the active character
        action"""
        action = [action for action in self.actions_list if action.id == action_id][0]
        
        for evt in self.active_events:
            solved = self.__check_event_resolution(evt, action)
            if solved:
                sound_manager.instance.play_event_solved()
                self.remove_personal_event(evt)

        for evt in self.active_social_events:
            solved = self.__check_event_resolution(evt, action)
            if solved:
                sound_manager.instance.play_event_solved()
                self.remove_social_event(evt)
    
    def __check_event_resolution(self, evt, action):
        action_id = action.id
        
        prob = self.events_actions_res.get( (evt.name, action_id) )
        if prob:
            rand = random.randint(0, 100)
            print "TRYING SOLVE: %s performing: %s with probability: %s" % (evt.name, action_id, prob)
            if rand <= prob:
                print "EVENT SOLVED"
                return True
        
        elif action.effect:
            positive_impacts = [impact for impact in action.effect.effect_status_list if impact[1] > 0]
            for impact in positive_impacts:
                status_bar = impact[0]
                prob = self.events_actions_res.get( (evt.name, None, status_bar) )
                if prob:
                    rand = random.randint(0, 100)
                    print "TRYING SOLVE: %s perfroming: %s with effect: %s, with probability: %s" % (evt.name, action_id, status_bar, prob)
                    if rand <= prob:
                        print "EVENT SOLVED"
                        return True
        
        return False
    
    def __handle_active_character_action(self):
        if self.active_char_action:
            # handle effects, once per CONTROL_INTERVAL
            if self.count >= CONTROL_INTERVAL:
                if self.active_char_action.time_left > 0:
                    self.active_char_action.perform(CONTROL_INTERVAL)
                else:
                    if self.active_char_action.background:
                        self.set_character_location(self.old_place)
            
            # handle animation - every frame
            if self.active_char_action.time_left > 0:
                self.active_char_action.decrease_frames_left()
                if self.active_char_action.time_left == 0:
                    self.windows_controller.stop_current_action_animation()
                    self.__try_solve_events(self.active_char_action.id)
            
            # check if the action ended
            if self.active_char_action.time_left == 0:
                self.finish_action()
    
    def finish_action(self):
        # perform missed cicles
        self.active_char_action.perform(self.count)
        
        if self.active_char_action.effect:
            effect = self.active_char_action.effect
            
            new_place = effect.get_new_place()
            if new_place:
                # The action changed character's place
                self.set_character_location(new_place)
            else:
                # Restore background
                if self.active_char_action.background:
                    self.set_character_location(self.old_place)
            
            new_clothes = effect.get_new_clothes()
            if new_clothes:
                self.set_character_clothes(new_clothes)
                
            change_time = effect.get_change_time()
            if change_time:
                self.change_time()
        
        # reset the action
        self.active_char_action.reset()
        
        # check consequences should be triggered
        cons = self.active_char_action.effect.get_consequence(self.events_dict, self.bars_controller.get_bars_status(), self.get_restrictions())
        self.active_char_action = None
        if cons:
            self.check_consequence_event(cons)
                    
    def __control_background_actions(self):
        """
        Controls active background actions.
        """
        for action in self.background_actions:
            action.perform(CONTROL_INTERVAL)
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
            print "Mood changed to: ", self.active_mood.name
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
            print "Personal event: ", event.name
    
    def add_random_social_event(self):
        event = self.__get_random_event(self.social_events_list)
        if event:
            self.add_social_event(event)
    
    def add_social_event(self, event):
        if not (event in self.active_social_events):
            self.active_social_events.append(event)
            self.windows_controller.add_social_event(event)
            print "Social event: ", event.name

    def __control_active_events(self):
        """
        Active events handler
        """
        self.__handle_personal_events()
        self.__handle_social_events()
        
        if self.events_interval == 0 and not self.menu_active and not self.active_char_action:
            if random.randint(0, 1):
                # add personal
                if len(self.active_events) < self.get_level_conf_value("events_qty_personal"):
                    self.add_random_personal_event()
            else:
                # add social
                if len(self.active_social_events) < self.get_level_conf_value("events_qty_social"):
                    self.add_random_social_event()
            
            self.events_interval = self.get_level_conf_value("time_between_events")
        elif self.events_interval > 0:
            self.events_interval -= 1

    def check_consequence_event(self, event):
        """ Check if an event can be added """
        if event.event_type == "personal":
            if len(self.active_events) < self.get_level_conf_value("events_qty_personal"):
                self.add_personal_event(event)
        else:
            if len(self.active_social_events) < self.get_level_conf_value("events_qty_social"):
                self.add_social_event(event)
    
    def check_environment_events(self):
        """ Checks if any event should be triggered by an environment change """

        events_list = self.events_dict.values()
        events_list = [event for event in events_list if event.trigger == "environment"]     # Subset of events which are triggered randomly

        allowed_events = [evt for evt in events_list if evt.level <= self.character.level]      # verify wich events are allowed in the current level.

        self.__update_events_probability(allowed_events) # it updates the probabilities of the list's events
        allowed_events = [evt for evt in events_list if evt.get_probability() > 0]

        if len(allowed_events) > 0:
            event = random.choice(allowed_events)
            if event.event_type == "personal":
                if len(self.active_events) < self.get_level_conf_value("events_qty_personal"):
                    self.add_personal_event(event)
            else:
                if len(self.active_social_events) < self.get_level_conf_value("events_qty_social"):
                    self.add_social_event(event)
    
    def remove_social_event(self, event):
        """ removes an active social event """
        self.windows_controller.remove_social_event(event)
        self.windows_controller.windows["panel_window"].remove_info_button_event(event)
        event.reset()
        self.active_social_events.remove(event)
        self.__check_active_mood()

    def remove_personal_event(self, event):
        """removes an active personal event
        """
        self.windows_controller.remove_personal_event(event)
        self.windows_controller.windows["panel_window"].remove_info_button_event(event)
        event.reset()
        self.active_events.remove(event)
        self.__check_active_mood()

    def __handle_social_events(self):
        """
        Handle social events
        """
        for event in self.active_social_events:
            if event.time_left is None or event.time_left:
                event.perform()
            else:
                self.remove_social_event(event)
    
    def __handle_personal_events(self):
        """
        Handle personal events
        """
        for event in self.active_events:
            
            if event.time_left is None or event.time_left:
                event.perform()
            else:
                self.remove_personal_event(event)
    
    def __get_random_event(self, events_list):
        """
        Get a random event
        """
        events_list = [event for event in events_list if event.trigger == "random"]     # Subset of events which are triggered randomly
        
        allowed_events = [evt for evt in events_list if evt.level <= self.character.level]#verify wich events are allowed in the current level.
        self.__update_events_probability(allowed_events) # it updates the probabilities of the list's events
        
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
        restrictions = self.get_restrictions()
        bars_status_dict = self.bars_controller.get_bars_status()
        #updates events probability
        for evt in events_list:
            evt.update_probability(bars_status_dict, restrictions)
            
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
            self._master_challenge()
    
# Score handling
    def add_points(self, points):
        score_bar = self.bars_controller.score_bar
        score_bar.increase(points)
        self.character.score = score_bar.value
        
# Save, load and reset game
    def reset_game(self, gender=None):
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
            
        self.game_over = False

        # character
        self.character.reset(gender)
        
        self.active_events = []
        self.active_social_events = []
        self.events_interval = self.get_level_conf_value("time_between_events")
        
        # bars
        self.bars_controller.reset()
        
        # weather
        self.current_weather = self.weathers[0] # default weather
        self.update_environment()

        self.windows_controller.update_clothes()
        
        # hour
        self.hour = 2
        self.hour_count = HOUR_COUNT_CYCLE
        self.current_time = self.day_dic[self.hour]
        
        if self.windows_controller:
            while self.windows_controller.get_active_window() <> "main_window":
                self.windows_controller.close_active_window()
            self.windows_controller.windows["customization_window"].reload()
            self.windows_controller.set_active_window("customization_window")
        
        print "game reseted successfully... "

    def serialize(self):
        """
        Save the game instance
        """
        game_status = {}
        ## save bars status
        bars_status_dic = self.bars_controller.get_bars_status()
        ## save character properties
        char_properties = self.character.get_status()
        ##
        game_status.update(bars_status_dic)
        game_status.update(char_properties)
        game_status.update({"version" : GAME_VERSION})
        
        return str(game_status)

    def parse_game(self, data):
        """ loads the game from a string """
        game_status = eval(data)
        #load bars status
        self.bars_controller.load_bars_status(game_status)
        #character properties
        self.character.load_properties(game_status)
        self.update_environment()
        self.game_over = False
        print "Game loaded. Version ", game_status["version"]

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

# Challenges
    def get_lowest_bar(self):
        return self.bars_controller.get_lowest_bar()

    def __control_challenges(self):
        if self.challenge_cicles == 0:
            self.challenge_cicles = CHALLENGES_INTERVAL
            if random.randint(0, 1):
                self._mc_challenges()
            else:
                self._tf_challenges()
        self.challenge_cicles -= 1
        
    def _mc_challenges(self):
        self.challenges_creator.get_challenge("mc")
        self.windows_controller.set_active_window("mc_challenge_window")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Múltiple Opción: %s" % (self.get_lowest_bar().label),  u"Tu barra de %s está baja. \nPara ganar puntos tienes que acertar \nla respuesta correcta.\n\n¡Suerte!" % (self.get_lowest_bar().label))
        self.windows_controller.set_active_window("info_challenge_window")
        sound_manager.instance.play_popup()
        
    def _tf_challenges(self):
        self.challenges_creator.get_challenge("tf")
        self.windows_controller.set_active_window("tf_challenge_window")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Verdadero o Falso: %s" %(self.get_lowest_bar().label), u"Tu barra de %s está baja. \nPara ganar puntos tienes que acertar \nlas preguntas de verdero o falso.\n\n¡Suerte!" % (self.get_lowest_bar().label))
        self.windows_controller.set_active_window("info_challenge_window")
        sound_manager.instance.play_popup()
        
    def _master_challenge(self):
        # The master challenge occurs when the player completed a level.
        # If it is answered correctly the player wins some points, so he starts the new level with these points
        # Otherwise it loses some points, and continues in the same level, so he has to continue playing to
        # reach the master challenge again.
        self.challenges_creator.get_challenge("master")
        self.windows_controller.set_active_window("tf_challenge_window")
        
        min_correct = self.get_level_conf_value("min_qty_correct_ans")
        self.windows_controller.windows["info_challenge_window"].update_content(u"Super Desafío",  u"¡Estás por pasar de nivel!\nPara superarlo tienes que responder\ncorrectamente a %s de las 5 preguntas\nque siguen.\n\n¡Suerte!" % min_correct)
        self.windows_controller.set_active_window("info_challenge_window")
        sound_manager.instance.play_popup()

# Game Over
    def __control_game_over(self):
        percentaje = self.bars_controller.get_overall_percent()
        if percentaje*100 >= GAME_OVER_THRESHOLD:
            self.game_over_cicles = GAME_OVER_INTERVAL
        else:
            self.game_over_cicles -= 1
        
        if self.game_over_cicles == 0:
            self.windows_controller.windows["slide_window"].show_slide("assets/slides/loose.jpg", self.__game_over_cb)
            self.windows_controller.set_active_window("slide_window")
        
    def __game_over_cb(self):
        self.game_over = True
        