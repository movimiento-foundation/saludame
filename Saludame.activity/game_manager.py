# -*- coding: utf-8 -*-


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
        
        self.active_actions = []

    def add_active_action(self, id_action):
        #place = get_place(self.character.actual_place) 
        #if(place.allowed_action(action_id)): #continúa con la acción, solo si es permitida en el lugar
        if(True): #dont check char's place yet
            action = self.get_action(id_action)
            if(action):
                action.perform()  
                self.active_actions.append(action)

    def signal(self):
        """
        Señal de incremento, indica que se completó una iteración
        en el sistema.
        """
        self.count += 1
        self.__control_active_actions()
        
    def __control_active_actions(self):
        if (self.count == 15):
            
            for action in self.active_actions:
                action.perform()
            self.count = 0
    
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
        


