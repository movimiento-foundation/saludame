# -*- coding: utf-8 -*-

class kid:
    """
    kid entity (por poner un ejemplo)
    """
    
    def __init__(self, name, age, sex, energy=100, hunger=100, hygiene=100, social=100, vitamins=100):
        self.name = name
        self.age = age
        self.sex = sex
        #states   por poner un ejemplo.
        self.energy = energy
        self.hunger = hunger
        self.hygiene = hygiene
        self.social = social
        self.vitamins = vitamins
        
    def increse_energy(self, value):
        self.energy += value
    
    def increse_hunger(self, value):
        self.hunger += value
    
    def increse_hygiene(self, value):
        self.hygiene += value

    def increse_social(self, value):
        self.social += value
        
    def increse_vitamins(self, value):
        self.vitamins += value
