# -*- coding: utf-8 -*-

import challenges
import random

class ChallengesLoader:
    def __init__(self, container, rect, frame_rate, windows_controller, bg_color=(0, 0, 0)):
        self.multiple_choice_challenges = []
        self.container = container
        self.rect = rect
        self.frame_rate = frame_rate
        self.windows_controller = windows_controller
        self.bg_color = bg_color
        

    def load_challenge(self, question, answers, correct_answer, image=None):
        challenge = challenges.MultipleChoice(self.container, self.rect, self.frame_rate, self.windows_controller, self.bg_color)
        
        challenge.set_question(question)
        challenge.set_answers (answers)
        challenge.set_correct_answer (correct_answer)
        challenge.set_image(image)
        
        self.multiple_choice_challenges.append(challenge)
        
    def get_challenge(self):
        r = random.randrange(0, len(self.multiple_choice_challenges))
        return self.multiple_choice_challenges[r]
        
    
