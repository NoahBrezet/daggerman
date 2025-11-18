import random

x = []
y = []
id = []
standon = []
exp = 0
lvl = 1
max_hp = 10
hp = 10
weapon = "dagger"
weapon_damage = 2
extra_damage = 0
armor = "Nothing"
armor_defense = 0
extra_defense = 0
extra_slot = "Nothing"
board_dict = {}

def roll(num_sides):
    roll = random.randint(1, num_sides)
    return roll

def create_square(x_coord, y_coord, identifier):
    x.append(x_coord)
    y.append(y_coord)
    id.append(identifier)
    standon.append(False)

def show_board():
    k = id.index("x")
    board_dict = {}
    for n in range(len(id)):
        board_dict[(x[n], y[n])] = id[n]
    for i in range(-3, 4):
        for j in range(-3, 4):
            cell = board_dict.get((x[k]+j, y[k]+i), " ")
            print(cell, end=" ")
        print()

def move(dx, dy):
    k = id.index("x")
    for n in range(len(id)):
        board_dict[(x[n], y[n])] = id[n]
    if board_dict.get((x[k]+dx, y[k]+dy), " ") == "□":
        id[k] = "□"
        id[next(i for i, (xx, yy) in enumerate(zip(x, y)) if xx == x[k]+dx and yy == y[k]+dy)] = "x"
        k = id.index("x")
        if standon[k] == False:
            gen()
            standon[k] = True
        action_taken = True

def place_object(identifier):
    k = id.index("x")
    for n in range(len(id)):
        board_dict[(x[n], y[n])] = id[n]
    while True:
        n = roll(4)
        if n == 1 and board_dict.get((x[k]-1, y[k]), " ") == " ":
            create_square(x[k]-1, y[k], identifier)
            return
        elif n == 2 and board_dict.get((x[k]+1, y[k]), " ") == " ":
            create_square(x[k]+1, y[k], identifier)
            return
        elif n == 3 and board_dict.get((x[k], y[k]-1), " ") == " ":
            create_square(x[k], y[k]-1, identifier)
            return
        elif n == 4 and board_dict.get((x[k], y[k]+1), " ") == " ":
            create_square(x[k], y[k]+1, identifier)
            return

def gen():
    k = id.index("x")
    for f in range(len(id)):
        board_dict[(x[f], y[f])] = id[f]
    if board_dict.get((x[k]-1, y[k]), " ") != " " and board_dict.get((x[k]+1, y[k]), " ") != " " and board_dict.get((x[k], y[k]-1), " ") != " " and board_dict.get((x[k], y[k]+1), " ") != " ":
        return
    n = roll(30)
    if n <= 20:
        place_object("□")
    elif n <= 22:
        place_object("□")
        if board_dict.get((x[k]-1, y[k]), " ") != " " and board_dict.get((x[k]+1, y[k]), " ") != " " and board_dict.get((x[k], y[k]-1), " ") != " " and board_dict.get((x[k], y[k]+1), " ") != " ":
            return
        place_object("□")
    elif lvl == 1:
        if n <= 25:
            place_object("S")
        elif n <= 28:
            place_object("K")
        else:
            place_object("C")
    elif lvl == 2:
        if n <= 24:
            place_object("K")
        elif n <= 26:
            place_object("L")
        elif n <= 28:
            place_object("F")
        else:
            place_object("C")
    elif lvl >= 3:
        if n <= 24:
            place_object("F")
        elif n <= 26:
            place_object("O")
        elif n <= 28:
            place_object("T")
        else:
            place_object("C")

def equip():
    print("Do you want to equip this item? (y/n)")
    choice = input()
    return choice


def attack(dx, dy):
    k = id.index("x")
    target_x = x[k] + dx
    target_y = y[k] + dy
    for n in range(len(id)):
        if x[n] == target_x and y[n] == target_y:
            if id[n] == "C":
                action_taken = True
                print("You open the chest and find treasure!")
                id[n] = "□"
                if lvl == 1:
                    treasure_roll = roll(4)
                    if treasure_roll == 1:
                        print("You found a dagger! (Damage 1d3)")
                        if equip() == "y":
                            weapon = "dagger"
                            weapon_damage = 3
                    elif treasure_roll == 2:
                        print("You found a Leather Armor! (Defense +1)")
                        if equip == "y":
                            armor = "Leather Armor"
                            armor_defense = 1
                    elif treasure_roll == 3:
                        print("You found a attack ring! (Damage +1)")
                        if equip() == "y":
                            extra_slot = "attack ring 1"
                            extra_damage = 1
                            extra_defense = 0
                    elif treasure_roll == 4:
                        print ("You found a a defense amulet! (Defense +1)")
                        if equip() == "y":
                            extra_slot = "defense amulet 1"
                            extra_defense = 1
                            extra_damage = 0
                if lvl == 2:
                    treasure_roll = roll(6)
                    if treasure_roll == 1:
                        print("You found a short sword! (Damage 1d6)")
                        if equip() == "y":
                            weapon = "short sword"
                            weapon_damage = 6
                    elif treasure_roll == 2:
                        print("You found a Chainmail Armor! (Defense +2)")
                        if equip() == "y":
                            armor = "Chainmail Armor"
                            armor_defense = 2
                    elif treasure_roll == 3:
                        print("You found a swift dagger! (Damage 1d3)")
                        if equip() == "y":
                            weapon = "swift dagger"
                            weapon_damage = 3
                    elif treasure_roll == 4:
                        print("You found a attack ring! (Damage +1)")
                        if equip() == "y":
                            extra_slot = "attack ring 1"
                            extra_damage = 1
                            extra_defense = 0
                    elif treasure_roll == 5:
                        print ("You found a a defense amulet! (Defense +1)")
                        if equip() == "y":
                            extra_slot = "defense amulet 1"
                            extra_defense = 1
                            extra_damage = 0
                    elif treasure_roll == 6:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip() == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                if lvl >= 3:
                    treasure_roll = roll(6)
                    if treasure_roll == 1:
                        print("You found a longsword! (Damage 1d8)")
                        if equip() == "y":
                            weapon = "longsword"
                            weapon_damage = 8
                    elif treasure_roll == 2:
                        print("You found a Plate Armor! (Defense +3)")
                        if equip() == "y":
                            armor = "Plate Armor"
                            armor_defense = 3
                    elif treasure_roll == 3:
                        print("You found a swift dagger! (Damage 1d4)")
                        if equip() == "y":
                            weapon = "swift dagger"
                            weapon_damage = 4
                    elif treasure_roll == 4:
                        print("You found a attack ring! (Damage +2)")
                        if equip() == "y":
                            extra_slot = "attack ring 2"
                            extra_damage = 2
                            extra_defense = 0
                    elif treasure_roll == 5:
                        print ("You found a a defense amulet! (Defense +2)")
                        if equip() == "y":
                            extra_slot = "defense amulet 2"
                            extra_defense = 2
                            extra_damage = 0
                    elif treasure_roll == 6:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip() == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
            elif id[n] != "□":
                action_taken = True
                print(f"You attack the {id[n]}!")
                # Here you would implement combat mechanics
            else:
                return

x.append(0)
y.append(0)
id.append("x")
standon.append(True)
create_square(1, 0, "□")
create_square(-1, 0, "□")

print ("You are 'x'.")
print ("Squares you can stand on are marked with '□'.")
print ("After we ask you for your action you can type w a s or d to move.")
print ("Or you can type ww aa ss or dd to attack in that direction.")
print ("you can also type i to see your inventory and statts.")
print ("You can type m to see every monster that you can currently fight.")
print ("You can type quit to end the game.")
print ("if you want the instructions again type h.")
print ("Later you may get more options.")
print ("You can open chests by attacking them.")
print ("Good luck!")

while True:
    action_taken = False
    print()
    show_board()
    print()
    print("choose an action: ")
    action = input()
    if action == "i":
        print(f"HP: {hp}/{max_hp}, EXP: {exp}, Level: {lvl}, Exp to next level: {lvl * 10- exp}")
        print(f"Weapon: {weapon} (Damage: 1d{weapon_damage})")
        print(f"Armor: {armor} (Defense: {armor_defense})")
        print(f"Extra Slot: {extra_slot}")
        print()
    elif action == "quit":
        break
    elif action == "a":
        move(-1, 0)
    elif action == "d":
        move(1, 0)
    elif action == "w":
        move(0, -1)
    elif action == "s":
        move(0, 1)
    elif action == "h":
        print ("You are 'x'.")
        print ("Squares you can stand on are marked with '□'.")
        print ("After we ask you for your action you can type w a s or d to move.")
        print ("Or you can type ww aa ss or dd to attack in that direction.")
        print ("you can also type i to see your inventory and statts.")
        print ("You can type m to see every monster that you can currently fight.")
        print ("You can type quit to end the game.")
        print ("if you want the instructions again type h.")
        print ("Later you may get more options.")
        print ("You can open chests by attacking them.")
        print ("Good luck!")
    elif action == "m":
        print("level 1 monsters:")
        print("K - Kobold (HP: 4, Damage: 1d2)")
        print("S - slime (HP: 2, Damage: 1d3) slimes can't move")
        if lvl >= 2:
            print("level 2 monsters:")
            print("L - Lizardman (HP: 10, Damage: 1d3, defense: 1)")
            print("F - Freakish Abberation (HP: 6, Damage: 1d6)")
            if lvl >= 3:
                print("level 3 monsters:")
                print("O - Orc (HP: 10, Damage: 1d8, defense: 2)")
                print("T - Troll (HP: 16, Damage: 1d6, defense: 3)")
    elif action == "aa":
        action_taken = True
        attack(-1, 0)
    elif action == "dd":
        action_taken = True
        attack(1, 0)
    elif action == "ww":
        action_taken = True
        attack(0, -1)
    elif action == "ss":
        action_taken = True
        attack(0, 1)
# print ("GAME OVER")