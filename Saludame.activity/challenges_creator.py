# -*- coding: utf-8 -*-

import challenges
import random

from gettext import gettext as _

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
        self.challenge.set_bg_image("assets/windows/window_1.png")
        
        # Tuples of challenges   
        self.challenges = []
        
    def create_challenges(self):
        self._create_challenge(_("Which foods do we need to eat every day?"), [_("Some food from each group every day"), _("Some fruits and vegetables only"), _("Some food from all the groups but not fats and sugar")], 0, 10, 10)
        self._create_challenge(_("What is the most important meal of the day?"), [_("Breakfast"), _("Lunch"), _("Tea"), _("Dinner")], 0, 10, 10)
        self._create_challenge(_("How regularly should children exercise?"), [_("Once a month"), _("Once a week"), _("Once a day")], 2, 10, 10)
        self._create_challenge(_("What percentage of the body is made up of water?"), ["30%", "70%", "90%"], 1, 10, 10)

    def _create_challenge(self, question, answers, correct_answer, win_points, lose_points, image=None):
        """
        Create a new challenge (tuple)
        """
        challenge = (question, answers, correct_answer, win_points, lose_points, image) 
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
        self.challenge.set_answers(c[1])
        self.challenge.set_correct_answer(c[2])
        self.challenge.set_win_points(c[3])
        self.challenge.set_lose_points(c[4])
        
        # If challenge has an image
        if c[5]:
            self.challenge.set_image(c[5])
        
        return self.challenge
