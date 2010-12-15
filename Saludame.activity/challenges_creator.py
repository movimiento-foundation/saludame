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
        
        # Multiple Choice window
        self.challenge = challenges.MultipleChoice(self.container, self.rect, self.frame_rate, self.windows_controller, self, self.bg_color)
        self.challenge.set_bg_image("assets/windows/window_1.png")
        
        # Tuples of mc_challenges   
        self.mc_challenges = []
        
        # Tuples of tf_challenges
        self.tf_challenges_physica = []
        self.tf_challenges_hygiene = []
        self.tf_challenges_nutrition = []
        self.tf_challenges_spare_time = []
        
    def create_challenges(self):
        # Common multiple choice
        self._create_mc_challenge(_("Which foods do we need to eat every day?"), [_("Some food from each group every day"), _("Some fruits and vegetables only"), _("Some food from all the groups but not fats and sugar")], 0, 10, 10)
        self._create_mc_challenge(_("What is the most important meal of the day?"), [_("Breakfast"), _("Lunch"), _("Tea"), _("Dinner")], 0, 10, 10)
        self._create_mc_challenge(_("How regularly should children exercise?"), [_("Once a month"), _("Once a week"), _("Once a day")], 2, 10, 10)
        self._create_mc_challenge(_("What percentage of the body is made up of water?"), ["30%", "70%", "90%"], 1, 10, 10)
        
        # True or false
        # 0 = False | 1 = True
        self.tf_challenges_physica.append(self._create_tf_challenge(_("La alimentación adecuada previene muchas enfermedades importantes"), 1, 10, 10))
        self.tf_challenges_physica.append(self._create_tf_challenge(_("Si no nos vacunamos con las vacunas obligatorias podemos enfermarnos"), 1, 10, 10))
        self.tf_challenges_physica.append(self._create_tf_challenge(_("Cuando estamos ingiriendo alimentos en menor proporción a lo que necesitamos, podemos volvernos más susceptibles a las infecciones "), 1, 10, 10))
        
        self.tf_challenges_hygiene.append(self._create_tf_challenge(_("Muchos alimentos pueden estar contaminados con agroquímicos, y pesticidas porque son frecuentemente usados"), 1, 10, 10))
        self.tf_challenges_hygiene.append(self._create_tf_challenge(_("Si no voy a comer no necesito lavarme las manos "), 0, 10, 10))
        self.tf_challenges_hygiene.append(self._create_tf_challenge(_("Lo primero que hay que hay que hacer cuando vamos a lavarnos las manos es ponernos jabón"), 0, 10, 10))
        
        self.tf_challenges_nutrition.append(self._create_tf_challenge(_("Cuando aprendemos hábitos saludables estamos cuidando nuestra salud"), 1, 10, 10))
        self.tf_challenges_nutrition.append(self._create_tf_challenge(_("Tomar mucha agua, hacer ejercicio y comer frutas y verduras ayuda a mover el intestino sin dificultad"), 1, 10, 10))
        self.tf_challenges_nutrition.append(self._create_tf_challenge(_("El desayuno no es importante en nuestra alimentación"), 0, 10, 10))
        
        self.tf_challenges_spare_time.append(self._create_tf_challenge(_("La actividad física mejora nuestra imagen"), 1, 10, 10))
        self.tf_challenges_spare_time.append(self._create_tf_challenge(_("La actividad física  no nos ayuda prevenir enfermedades como el sobrepeso y la obesidad "), 0, 10, 10))
        self.tf_challenges_spare_time.append(self._create_tf_challenge(_("Ser sedentarios no tiene importancia y no afecta nuestra salud"), 0, 10, 10))

    def _create_mc_challenge(self, question, answers, correct_answer, win_points, lose_points, image=None):
        """
        Create a new challenge (tuple)
        """
        challenge = (question, answers, correct_answer, win_points, lose_points, image) 
        self.mc_challenges.append(challenge)
        
    def _create_tf_challenge(self, question, correct_answer, win_points, lose_points, image=None):
        """
        Create a new tf_challenge (tuple)
        """
        challenge = (question, ["False", "True"], correct_answer, win_points, lose_points, image) 
        return challenge
    
    def get_challenge(self, kind):
        """
        Load and return a random "created" challenge
        """
        if kind == "mc":
            self.challenge.kind = "mc"
            r = random.randrange(0, len(self.mc_challenges))
            c = self.mc_challenges[r]
        elif kind == "tf":
        
            self.challenge.kind = "tf"
            
            bar = self.game_man.get_lowest_bar()
            if bar.id == "physica":
                r = random.randrange(0, len(self.tf_challenges_physica))
                c = self.tf_challenges_physica[r]
            elif bar.id == "hygiene":
                r = random.randrange(0, len(self.tf_challenges_hygiene))
                c = self.tf_challenges_hygiene[r]
            elif bar.id == "nutrition":
                r = random.randrange(0, len(self.tf_challenges_nutrition))
                c = self.tf_challenges_nutrition[r]
            elif bar.id == "spare_time":
                r = random.randrange(0, len(self.tf_challenges_spare_time))
                c = self.tf_challenges_spare_time[r]           
        
        # Set multiple choice attributes
        self.challenge.set_question(c[0])
        self.challenge.set_answers(c[1])
        self.challenge.set_correct_answer(c[2])
        self.challenge.set_win_points(c[3])
        self.challenge.set_lose_points(c[4])
        
        # If challenge has an image
        if c[5]:
            self.challenge.set_image(c[5])
        
        return self.challenge
