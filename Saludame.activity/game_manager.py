# -*- coding: utf-8 -*-


class GameManager:
    """
    Clase gestora del sistema. Se encarga del control de las acciones
    y los eventos del juego.
    """
    
    def __init__(self, character, bars_controller):
        """
        Constructor de la clase
        """
        self.character = character
        self.bars_controller = bars_controller
        self.count = 0 #sirve como 'clock' interno, para mantener un orden de tiempo dentro de la clase.
        self.active_actions = []
        

    def add_active_action(self, action):
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

