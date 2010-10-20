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



    def signal(self):
        """
        Señal de incremento, indica que se completó una iteración
        en el sistema.
        """
        self.count += 1
        
    def __control_active_actions(self):
        None
    
    def __control_active_events(self):
        None