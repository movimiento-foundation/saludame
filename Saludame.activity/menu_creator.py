# -*- coding: utf-8 -*-

import menu
import pygame

example = [
    ("name", "assets/icons/icon.png", "tooltip", None, "action_id"),
    ("eat", "assets/icons/icon2.png", "comer algo", [
        ("apple", "assets/icons/icon.png", "Eat an apple", None, "eat_apple"),
        ("meat", "assets/icons/icon.png", "Eat meat", None, "eat_meat")
    ], None),
    ("sport", "assets/icons/icon.png", "Do sports...", [
        ("run", "assets/icons/icon.png", "Run", None, "sport_run"),
        ("jump rope", "assets/icons/icon.png", "Jump the rope", None, "sport_jump"),
        ("football", "assets/icons/icon.png", "Play footbal", None, "sport_football")
    ], None),
    ("sleep", "assets/icons/icon.png", "Go to sleep", None, "sleep_sleep"),
    ("talk", "assets/icons/icon3.png", "talk with a friend", None, "talk_talk"),
    ("study", "assets/icons/icon2.png", "do the homeworks", None, "study_study"),
    ("clean", "assets/icons/icon3.png", "clean up the bedroom", None, "clean_clean")
]

MENU_FRAME_RATE = 1

def load_menu(character, (pos_x, pos_y), container, windows_controller):
    
    center = 260, 200
    
    m = menu.Menu(1, container, windows_controller, [], center, 90, character)
    for item in example:
        an_item = create_item(item, m, container)
        m.add_item(an_item)
    m.calculate()
    
    return m
    

def create_item(item_tuple, a_menu, container):
    if(item_tuple[3] != None):
        an_item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], item_tuple[1], item_tuple[2], [create_item(sub_item, a_menu, container) for sub_item in item_tuple[3]], item_tuple[4], a_menu)
    else:
        an_item = menu.Item(container, MENU_FRAME_RATE, item_tuple[0], item_tuple[1], item_tuple[2], [], item_tuple[4], a_menu)
    return an_item
    






