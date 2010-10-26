# -*- coding: utf-8 -*-

CONTROL_INTERVAL = 15 #cantidad de señales hasta que realiza un checkeo de las acciones.

class GameManager:
    """
    Clase gestora del sistema. Se encarga del control de las acciones
    y los eventos del juego.
    """
    
    def __init__(self, character, bars_controller, actions_list, places_list):
        """
        Constructor de la clase
        """
        self.character = character
        self.bars_controller = bars_controller
        self.count = 0 #sirve como 'clock' interno, para mantener un orden de tiempo dentro de la clase.
        
        self.actions_list = actions_list 
        self.places_list = places_list
        
        self.background_actions = []
        self.active_char_action = None #Active character action, Action instance

    def set_active_action(self, id_action):
        #place = get_place(self.character.actual_place) 
        #if(place.allowed_action(action_id)): #continúa con la acción, solo si es permitida en el lugar
        if(True): #dont check char's place yet
            action = self.get_action(id_action)
            if(action):
                action.perform()  
                self.active_char_action = action

    def add_background_action(self, id_action):
        """
        Add a background action.
        """
        action = self.get_action(id_action)
        if(action):
            self.background_actions.append(action)

    def signal(self):
        """
        Increment signal, it means that an iteration has been completed 
        """
        self.count += 1
        if(self.count >= CONTROL_INTERVAL):
            self.__control_active_actions()
            self.bars_controller.calculate_score()
            self.count = 0
    
    def __control_score(self):
        """
        """
        None
        
    def __control_active_actions(self):
            
        for action in self.background_actions:
            action.perform()
            action.time_span = 1 #that means background actions never stop
            
        if(self.active_char_action): #if the character is performing an action
            self.active_char_action.perform()
    
    def __control_active_events(self):
        None
    
    def get_place(self, id_place):
        """
        Returns the place asociated to the id_place
        """
        for place in self.places_list:
            if(place.id == id_place):
                return place
    
    def get_action(self, id_action):
        """
        Returns the action asociated to the id_action
        """
        for action in self.actions_list:
            if(action.id == id_action):
                return action
        



