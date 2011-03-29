# -*- coding: utf-8 -*-

import challenges
import random

from gettext import gettext as _

class ChallengesCreator:
    
    def __init__(self, container, rect, frame_rate, windows_controller, game_man, bg_color=(0, 0, 0)):
             
        # Windows attributes
        self.container = container
        self.rect = rect
        self.frame_rate = frame_rate
        self.windows_controller = windows_controller
        self.bg_color = bg_color

        self.game_man = game_man
        
        # Multiple Choice and Master window
        self.mc_challenge = challenges.MultipleChoice(self.container, self.rect, self.frame_rate, self.windows_controller, self, "mc_challenge_window", self.bg_color)
        
        # True or False window
        self.tf_challenge = challenges.TrueOrFalse(self.container, self.rect, self.frame_rate, self.windows_controller, self, "tf_challenge_window", self.bg_color)
        
        # Cooking window
        #self.cooking_challenge = challenges.Cooking(self.container, self.rect, self.frame_rate, self.windows_controller, "cooking_challenge_window", self.bg_color)
        
        # Tuples of mc_challenges
        self.mc_challenges = []
        
        # Dict of true or false tuples
        self.tf_challenges = {}
        
        
    def create_challenges(self):
        # Common multiple choice
        self._create_mc_challenge(_("Which foods do we need to eat every day?"), [_("Some food from each group every day"), _("Some fruits and vegetables only"), _("Some food from all the groups but not fats and sugar")], 0, 10, 10)
        self._create_mc_challenge(_("What is the most important meal of the day?"), [_("Break\nfast"), _("Lunch"), _("Tea"), _("Dinner")], 0, 10, 10)
        self._create_mc_challenge(_("How regularly should children exercise?"), [_("Once a month"), _("Once a week"), _("Once a day")], 2, 10, 10)
        self._create_mc_challenge(_("What percentage of the body is made up of water?"), ["30%", "70%", "90%"], 1, 10, 10)
        
        # True or false
        # 0 = False | 1 = True
        
        self.tf_challenges = {}
        
        # Physica
        self.tf_challenges["physica"] = [
            self._create_tf_challenge(_("La alimentación adecuada previene muchas enfermedades \nimportantes"), 1, 10, 10),
            self._create_tf_challenge(_("Si no nos vacunamos con las vacunas obligatorias podemos \nenfermarnos"), 1, 10, 10),
            self._create_tf_challenge(_("Cuando estamos ingiriendo alimentos en menor proporción \na lo que necesitamos, podemos volvernos más \nsusceptibles a las infecciones "), 1, 10, 10),
        ]
        
        # Hygiene
        self.tf_challenges["hygiene"] = [
            self._create_tf_challenge(_("Muchos alimentos pueden estar contaminados con agroquímicos, \ny pesticidas porque son frecuentemente usados"), 1, 10, 10),
            self._create_tf_challenge(_("Si no voy a comer no necesito lavarme las manos "), 0, 10, 10),
            self._create_tf_challenge(_("Lo primero que hay que hay que hacer cuando vamos a lavarnos \nlas manos es ponernos jabón"), 0, 10, 10),
        ]
        
        # Nutrition
        self.tf_challenges["nutrition"] = [
            self._create_tf_challenge(_("Cuando aprendemos hábitos saludables estamos cuidando nuestra \nsalud"), 1, 10, 10),
            self._create_tf_challenge(_("Tomar mucha agua, hacer ejercicio y comer frutas y verduras \nayuda a mover el intestino sin dificultad"), 1, 10, 10),
            self._create_tf_challenge(_("El desayuno no es importante en nuestra alimentación"), 0, 10, 10),
        ]
        
        # Spare time
        self.tf_challenges["spare_time"] = [
            self._create_tf_challenge(_("La actividad física mejora nuestra imagen"), 1, 10, 10),
            self._create_tf_challenge(_("La actividad física  no nos ayuda prevenir enfermedades \ncomo el sobrepeso y la obesidad "), 0, 10, 10),
            self._create_tf_challenge(_("Ser sedentarios no tiene importancia y no afecta nuestra \nsalud"), 0, 10, 10),
        ]
        
        # Responsability
        self.tf_challenges["responsability"] = [
            self._create_tf_challenge(_("Hay que hacer los deberes en la escuela"), 1, 10, 10),
            self._create_tf_challenge(_("Es bueno ayudar en las tareas domésticas"), 0, 10, 10),
        ]
    
    def _create_mc_challenge(self, question, answers, correct_answer, win_points, lose_points, image=None):
        """
        Create a new mc_challenge (tuple)
        """
        challenge = (question, answers, correct_answer, win_points, lose_points, image)
        self.mc_challenges.append(challenge)
        
    def _create_tf_challenge(self, question, correct_answer, win_points, lose_points, image=None):
        """
        Create a new tf_challenge (tuple)
        """
        challenge = (question, [_("False"), _("True")], correct_answer, win_points, lose_points, image)
        return challenge
    
    def get_challenge(self, kind):
        """
        Load and return a random "created" mc_challenge
        """
        if kind == "mc":
            r = random.randrange(0, len(self.mc_challenges))
            c = self.mc_challenges[r]
            
            # Set challenge attributes
            self.mc_challenge.set_question(c[0])
            self.mc_challenge.set_answers(c[1])
            self.mc_challenge.set_correct_answer(c[2])
            self.mc_challenge.set_win_points(c[3])
            self.mc_challenge.set_lose_points(c[4])
            
            # If challenge has an image
            if c[5]:
                self.mc_challenge.set_image(c[5])
                
            return self.mc_challenge
            
        elif kind == "tf":
            self.tf_challenge.kind = "normal"
            bar = self.game_man.get_lowest_bar()
            
            challenges = self.tf_challenges[bar.id]
            
            r = random.randrange(0, len(challenges))
            c = challenges[r]
            
            # Set challenge attributes
            self.tf_challenge.set_question(c[0])
            self.tf_challenge.set_answers(c[1])
            self.tf_challenge.set_correct_answer(c[2])
            self.tf_challenge.set_win_points(c[3])
            self.tf_challenge.set_lose_points(c[4])
            
            # If challenge has an image
            if c[5]:
                self.tf_challenge.set_image(c[5])
                
            return self.tf_challenge
                
        elif kind == "master":
            self.tf_challenge.kind = "master"
            
            if self.game_man.character.level < 4:
                self.game_man.character.limit = 3
            elif self.game_man.character.level < 7:
                self.game_man.character.limit = 4
            else:
                self.game_man.character.limit = 5
                
            r = random.randrange(0, len(self.mc_challenges))
            c = self.mc_challenges[r]
            
            # Set challenge attributes
            self.tf_challenge.set_question(c[0])
            self.tf_challenge.set_answers(c[1])
            self.tf_challenge.set_correct_answer(c[2])
            self.tf_challenge.set_win_points(c[3])
            self.tf_challenge.set_lose_points(c[4])
            
            # If challenge has an image
            if c[5]:
                self.tf_challenge.set_image(c[5])
                
            return self.tf_challenge
