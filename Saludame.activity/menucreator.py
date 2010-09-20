# -*- coding: utf-8 -*-

import menu

example = [
    ("name", "assets/icons/icon.png", "tooltip", None),
    ("eat", "assets/icons/icon2.png", "comer algo", [
        ("apple", "assets/icons/icon.png", "Eat an apple", None),
        ("meat", "assets/icons/icon.png", "Eat meat", None)
    ]),
    ("sport", "assets/icons/icon.png", "Do sports...", [
        ("run", "assets/icons/icon.png", "Run", None),
        ("jump rope", "assets/icons/icon.png", "Jump the rope", None),
        ("footbal", "assets/icons/icon.png", "Play footbal", None)
    ]),
    ("sleep", "assets/icons/icon.png", "Go to sleep", None),
    ("talk", "assets/icons/icon3.png", "talk with a friend", None),
    ("study", "assets/icons/icon2.png", "do the homeworks", None),
    ("clean", "assets/icons/icon3.png", "clean up the bedroom", None)
]

def load_menu():
    item_list = []
    for item in example:
        an_item = create_item(item)
        item_list.append(an_item)
    m = menu.Menu(1, item_list,(190,130),90)
    return m
    

def create_item(item_tuple):
    if(item_tuple[3] != None):
        an_item = menu.Item(item_tuple[0], item_tuple[1], item_tuple[2], [create_item(sub_item) for sub_item in item_tuple[3]])
    else:
        an_item = menu.Item(item_tuple[0], item_tuple[1], item_tuple[2], [])
    return an_item
    
