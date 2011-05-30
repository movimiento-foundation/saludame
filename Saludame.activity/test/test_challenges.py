# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
import challenges_creator

def run_mc_challenges():
    mc_challenges = challenges_creator.get_mc_challenges()

    for challenge_type, challenges in mc_challenges.items():
        print challenge_type
        print ""
        
        for c in challenges:
            question, answers, correct, level, image = c
            print question
            for ans in answers:
                print ans
            
            sys.stdin.readline()
            print ""
            print ""

run_mc_challenges()
