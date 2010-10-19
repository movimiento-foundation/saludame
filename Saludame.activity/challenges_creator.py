# -*- coding: utf-8 -*-

import challenges
import random

class ChallengesCreator:
    
    def __init__(self, container, rect, frame_rate, windows_controller, bg_color=(0, 0, 0)):
             
        # Windows attributes
        self.container = container
        self.rect = rect
        self.frame_rate = frame_rate
        self.windows_controller = windows_controller
        self.bg_color = bg_color
        
        # Multiple Choice window
        self.challenge = challenges.MultipleChoice(self.container, self.rect, self.frame_rate, self.windows_controller, self.bg_color)
        
        # Tuples of challenges   
        self.challenges = []
        
    def create_challenges(self):
        """
        En un futuro esto se va a cargar de un archivo.
        Por ahora lo hardcodeamos.
        """        
        self._create_challenge("Which foods do we need to eat every day?", ["Some food from each group every day", "Some fruits and vegetables only", "Some food from all the groups but not fats and sugar"], 0)
        self._create_challenge("What is the most important meal of the day?", ["Breakfast", "Lunch", "Merienda", "Diner"], 0)
        self._create_challenge("How regularly should children exercise?", ["Once a month", "Once a week", "Once a day"], 0)
        self._create_challenge("Potatoes, cereals, bread and pasta contain high amounts of this nutrient:", ["Minerals", "Protein", "Carbohydrates"], 0)        

    def _create_challenge(self, question, answers, correct_answer, image=None):     
        """
        Create a new challenge (tuple)
        """
        challenge = (question, answers, correct_answer, image) 
        self.challenges.append(challenge)        
    
    def get_challenge(self):
        """
        Load and return a random "created" challenge
        """
        r = random.randrange(0, len(self.challenges))
        # Obtain a challenge tuple
        c = self.challenges[r]
              
        # Set multiple choice attributes
        self.challenge.set_question(c[0])
        self.challenge.set_answers (c[1])
        self.challenge.set_correct_answer (c[2])
        
        # If challenge has an image
        if (c[3]):
            self.challenge.set_image(c[3])       
        
        return self.challenge
