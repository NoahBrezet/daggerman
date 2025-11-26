import random
import map
import gen as g

# Player stats
exp = 0
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

def find_index_at(xc, yc):
    for i, (xx, yy) in enumerate(zip(map.x, map.y)):
        if xx == xc and yy == yc:
            return i
    return None

def roll(num_sides):
    roll = random.randint(1, num_sides)
    return roll

def board_dict_update():
    global board_dict
    board_dict.clear()
    for n in range (len(map.id)):
        board_dict[(map.x[n], map.y[n])] = map.id[n]

def show_board():
    k = map.id.index("x")
    board_dict_update()
    for i in range(-3, 4):
        for j in range(-3, 4):
            cell = board_dict.get((map.x[k]+j, map.y[k]+i), " ")
            print(cell, end=" ")
        print()

def move(dx, dy):
    global action_taken
    k = map.id.index("x")
    board_dict_update()
    if board_dict.get((map.x[k]+dx, map.y[k]+dy), " ") == "□":
        target_idx = find_index_at(map.x[k]+dx, map.y[k]+dy)
        if target_idx is None:
            return
        map.id[k] = "□"
        map.id[target_idx] = "x"
        k = map.id.index("x")
        if map.genID[k] == 1:
            g.gen(1)
        if map.genID[k] == 2:
            g.gen(2)
        if map.genID[k] == 3:
            g.gen(3)
        if map.genID[k] == 4:
            g.gen(4)
        action_taken = True

def move_object(dx,dy):
    global board_dict, m, moved
    src_idx = map.MplaceID[m]
    target_idx = find_index_at(map.x[src_idx]+dx, map.y[src_idx]+dy)
    if target_idx is not None and board_dict.get((map.x[src_idx]+dx, map.y[src_idx]+dy), " ") == "□":
        moved = True
        map.id[src_idx] = "□"
        map.id[target_idx] = map.Mid[m]
        map.MplaceID[m] = target_idx
        return True

def equip():
    print("Do you want to equip this item? (y/n)")
    choice = input()
    return choice

def attack(dx, dy):
    global action_taken, weapon, weapon_damage, armor, armor_defense, extra_slot, extra_damage, extra_defense, exp, max_hp, hp
    k = map.id.index("x")
    target_x = map.x[k] + dx
    target_y = map.y[k] + dy
    for n in range(len(map.id)):
        if map.x[n] == target_x and map.y[n] == target_y:
            if map.id[n] == "C":
                action_taken = True
                print("You open the chest and find treasure!")
                map.id[n] = "□"
                if map.lvl == 1:
                    treasure_roll = roll(50)
                    if treasure_roll <= 10:
                        print("You found a dagger! (Damage 1d3)")
                        if equip() == "y":
                            weapon = "dagger"
                            weapon_damage = 3
                    elif treasure_roll <= 20:
                        print("You found a Leather Armor! (Defense +1)")
                        if equip() == "y":
                            armor = "Leather Armor"
                            armor_defense = 1
                    elif treasure_roll <= 30:
                        print("You found a attack ring! (Damage +1)")
                        if equip() == "y":
                            extra_slot = "attack ring 1"
                            extra_damage = 1
                            extra_defense = 0
                    elif treasure_roll <= 40:
                        print ("You found a a defense amulet! (Defense +1)")
                        if equip() == "y":
                            extra_slot = "defense amulet 1"
                            extra_defense = 1
                            extra_damage = 0
                    elif treasure_roll <= 44:
                        print("You found a short sword! (Damage 1d6)")
                        if equip() == "y":
                            weapon = "short sword"
                            weapon_damage = 6
                    elif treasure_roll <= 48:
                        print("You found a Chainmail Armor! (Defense +2)")
                        if equip() == "y":
                            armor = "Chainmail Armor"
                            armor_defense = 2
                    elif treasure_roll == 49:
                        print ("you found a health potion! (Restores hp to max when used")
                        if equip() == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll == 50:
                        print("You found a dash magic scroll! (Allows you to move twice in one turn)")
                        if equip() == "y":
                            extra_slot = "dash magic scroll"
                            extra_damage = 0
                            extra_defense = 0
                if map.lvl == 2:
                    treasure_roll = roll(50)
                    if treasure_roll <= 10:
                        print("You found a short sword! (Damage 1d6)")
                        if equip() == "y":
                            weapon = "short sword"
                            weapon_damage = 6
                    elif treasure_roll <= 20:
                        print("You found a Chainmail Armor! (Defense +2)")
                        if equip() == "y":
                            armor = "Chainmail Armor"
                            armor_defense = 2
                    elif treasure_roll <= 28:
                        print("You found a swift dagger! (Damage 1d4, use q for swift attack)")
                        if equip() == "y":
                            weapon = "swift dagger"
                            weapon_damage = 4
                    elif treasure_roll <= 36:
                        print("You found a power ring! (Damage, defense +1)")
                        if equip() == "y":
                            extra_slot = "power ring 1"
                            extra_damage = 1
                            extra_defense = 1
                    elif treasure_roll <= 42:
                        print ("You found a heal magic scroll! (heal 2 hp when casted)")
                        if equip() == "y":
                            extra_slot = "heal 2 magic scroll"
                            extra_defense = 0
                            extra_damage = 0
                    elif treasure_roll <= 48:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip() == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll == 49:
                        print("You found a longsword! (Damage 1d8)")
                        if equip() == "y":
                            weapon = "longsword"
                            weapon_damage = 8
                    elif treasure_roll == 50:
                        print("You found a dash magic scroll! (Allows you to move twice in one turn)")
                        if equip() == "y":
                            extra_slot = "dash magic scroll"
                            extra_damage = 0
                            extra_defense = 0
                if map.lvl == 3:
                    treasure_roll = roll(50)
                    if treasure_roll <= 10:
                        print("You found a longsword! (Damage 1d8)")
                        if equip() == "y":
                            weapon = "longsword"
                            weapon_damage = 8
                    elif treasure_roll <= 20:
                        print("You found a chainmail armor! (Defense +2)")
                        if equip() == "y":
                            armor = "chainmail armor"
                            armor_defense = 2
                    elif treasure_roll <= 28:
                        print("You found a swift dagger! (Damage 1d6, use q for swift attack)")
                        if equip() == "y":
                            weapon = "swift dagger"
                            weapon_damage = 6
                    elif treasure_roll <= 36:
                        print("You found a attack ring! (Damage +2)")
                        if equip() == "y":
                            extra_slot = "attack ring 2"
                            extra_damage = 2
                            extra_defense = 0
                    elif treasure_roll <= 42:
                        print ("You found a a defense amulet! (Defense +2)")
                        if equip() == "y":
                            extra_slot = "defense amulet 2"
                            extra_defense = 2
                            extra_damage = 0
                    elif treasure_roll <= 48:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip() == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll == 49:
                        print("You found a greatsword! (Damage 1d12)")
                        if equip() == "y":
                            weapon = "greatsword"
                            weapon_damage = 12
                    elif treasure_roll == 50:
                        print("You found a heal 4 magic scroll! (heal 4 hp when casted)")
                        if equip() == "y":
                            extra_slot = "heal 4 magic scroll"
                            extra_defense = 0
                            extra_damage = 0
                elif map.lvl >= 4:
                    treasure_roll = roll(50)
                    if treasure_roll <= 8:
                        print("You found a greatsword! (Damage 1d12)")
                        if equip() == "y":
                            weapon = "greatsword"
                            weapon_damage = 12
                    elif treasure_roll <= 16:
                        print("You found a plate armor! (Defense +3)")
                        if equip() == "y":
                            armor = "plate armor"
                            armor_defense = 3
                    elif treasure_roll <= 22:
                        print("You found a swift dagger! (Damage 1d8, use q for swift attack)")
                        if equip() == "y":
                            weapon = "swift dagger"
                            weapon_damage = 8
                    elif treasure_roll <= 28:
                        print("You found a dash dagger! (Damage 1d8, use q for dash attack)")
                        if equip() == "y":
                            weapon = "dash dagger"
                            weapon_damage = 8
                    elif treasure_roll <= 34:
                        print("You found a power ring! (Damage, defense +2)")
                        if equip() == "y":
                            extra_slot = "power ring 2"
                            extra_damage = 2
                            extra_defense = 2
                    elif treasure_roll <= 39:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip() == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll <= 44:
                        print("You found a heal 4 magic scroll! (heal 6 hp when casted)")
                        if equip() == "y":
                            extra_slot = "heal 4 magic scroll"
                            extra_defense = 0
                            extra_damage = 0
                    elif treasure_roll <= 47:
                        print("You found a magic missile magic scroll! (ranged attack to one side when casted)")
                        if equip() == "y":
                            extra_slot = "magic missile magic scroll"
                            extra_defense = 0
                            extra_damage = 0
                    elif treasure_roll <= 50:
                        print("You found a dagger transmutation magic scroll! (transform dagger into another type when casted)")
                        if equip() == "y":
                            extra_slot = "dagger transmutation magic scroll"
                            extra_defense = 0
                            extra_damage = 0
                return
            elif map.id[n] != "□":
                action_taken = True
                print(f"You attack the {map.id[n]}!")
                monster_index = next((m for m in range(len(map.MplaceID)) if map.MplaceID[m] == n), None)
                if monster_index is None:
                    return
                attack_roll = roll(weapon_damage) + extra_damage - map.Mdefense[monster_index]
                if attack_roll <= 0:
                    print("Your attack did no damage!")
                    return
                print(f"You deal {attack_roll} damage!")
                map.Mhp[monster_index] -= attack_roll
                if map.Mhp[monster_index] <= 0:
                    print(f"You defeated the {map.id[n]}!")
                    exp_gain = map.Mexp[monster_index]
                    print(f"You gain {exp_gain} EXP!")
                    exp += exp_gain
                    map.id[n] = "□"
                    map.Mhp.pop(monster_index)
                    map.Mdamage.pop(monster_index)
                    map.Mdefense.pop(monster_index)
                    map.Mexp.pop(monster_index)
                    map.Mid.pop(monster_index)
                    map.MplaceID.pop(monster_index)
                    if exp >= (2*map.lvl-1) * 10:
                        exp -= map.lvl * 10
                        map.lvl += 1
                        print(f"You leveled up! You are now level {map.lvl}!")
                        max_hp += 5
                        hp = max_hp
                        print(f"Your max HP increased to {max_hp}!")
                return
            else:
                return

g.start()

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

heal = 0
while True:
    action_taken = False
    print()
    show_board()
    print()
    print("choose an action: ")
    action = input()
    if action == "i":
        print(f"HP: {hp}/{max_hp}, EXP: {exp}, Level: {map.lvl}, Exp to next level: {(2*map.lvl-1) * 10 - exp}")
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
        print ("w a s or d to move.")
        print ("aa ss dd or ww to attack in that direction.")
        print ("i - see your inventory and statts.")
        print ("m - see monsters you can fight.")
        if extra_slot == "health potion":
            print ("r - restore hp to max.")
        if weapon == "swift dagger":
            print ("q - swift attack.")
        if extra_slot[-12:-1] == "magic scroll":
            print ("e - cast spell.")
        print ("quit - end the game.")
        print ("h - see this help message again.")
        print ("Later you may get more options.")
        print ("You can open chests by attacking them.")
        print ("Good luck!")
    elif action == "m":
        print("level 1 monsters:")
        print("K - Kobold (HP: 4, Damage: 1d2)") #exp 2
        print("S - slime (HP: 2, Damage: 1d3) slimes can't move") #exp 1
        if map.lvl >= 2:
            print("level 2 monsters:")
            print("L - Lizardman (HP: 10, Damage: 1d3, Defense: 1)") #exp 4
            print("F - Freakish Abberation (HP: 6, Damage: 1d6)") #exp 3
            if map.lvl >= 3:
                print("level 3 monsters:")
                print("O - Orc (HP: 10, Damage: 1d8, Defense: 2)") #exp 6
                print("T - Troll (HP: 16, Damage: 1d6, Defense: 3)") #exp 7
                if map.lvl >= 4:
                    print("level 4 monsters:")
                    print("G - Golem (HP: 10, Damage: 1d6, Defense: 4)") #exp 7
                    print("Ø - Ogre (HP: 20, Damage: 1d10, Defense: 2)") #exp 12
    elif action == "aa":
        attack(-1, 0)
    elif action == "dd":
        attack(1, 0)
    elif action == "ww":
        attack(0, -1)
    elif action == "ss":
        attack(0, 1)
    elif action == "r":
        if extra_slot == "health potion":
            hp = max_hp
            print("You used the health potion and restored your HP to max!")
            extra_slot = "Nothing"
            action_taken = True
    elif action == "q":
        if weapon == "swift dagger":
            attack(0, -1)
            attack(-1, 0)
            attack(1, 0)
            attack(0, 1)
        elif weapon == "dash dagger":
            print("You can move and attack after!")
            move_input = input("Move (w/a/s/d): ")
            if move_input == "a":
                move(-1, 0)
            elif move_input == "d":
                move(1, 0)
            elif move_input == "w":
                move(0, -1)
            elif move_input == "s":
                move(0, 1)
            attack_input = input("Attack (w/a/s/d):")
            if attack_input == "a":
                attack(-1, 0)
            elif attack_input == "d":
                attack(1, 0)
            elif attack_input == "w":
                attack(0, -1)
            elif attack_input == "s":
                attack(0, 1)
    elif action == "e":
        if extra_slot == "heal 2 magic scroll":
            hp += 2
            if hp > max_hp:
                hp = max_hp
            print("You cast the heal spell and restored 2 HP!")
            action_taken = True
        elif extra_slot == "heal 4 magic scroll":
            hp += 4
            if hp > max_hp:
                hp = max_hp
            print("You cast the heal spell and restored 4 HP!")
            action_taken = True
        elif extra_slot == "dash magic scroll":
            print("You can move twice this turn!")
            move_input1 = input("First move (w/a/s/d): ")
            if move_input1 == "a":
                move(-1, 0)
            elif move_input1 == "d":
                move(1, 0)
            elif move_input1 == "w":
                move(0, -1)
            elif move_input1 == "s":
                move(0, 1)
            show_board()
            move_input2 = input("Second move (w/a/s/d): ")
            if move_input2 == "a":
                move(-1, 0)
            elif move_input2 == "d":
                move(1, 0)
            elif move_input2 == "w":
                move(0, -1)
            elif move_input2 == "s":
                move(0, 1)
        elif extra_slot == "dagger transmutation magic scroll":
            print("This spell does not take a turn.")
            if weapon == "swift dagger":
                print("You now have a dash dagger!")
                weapon = "dash dagger"
            elif weapon.endswith("dagger"):
                print("You now have a swift dagger!")
                weapon = "swift dagger"
        elif extra_slot == "magic missile magic scroll":
            print("You do 1d4+2 damage.")
            print("In wich direction do you want to attack? (w/a/s/d)")
            attack_input = input()
            extra_damage_save = extra_damage
            damage_save = weapon_damage
            extra_damage = 2
            weapon_damage = 4
            if attack_input == "a":
                attack(-1, 0)
                attack(-2, 0)
                attack(-3, 0)
            elif attack_input == "d":
                attack(1, 0)
                attack(2, 0)
                attack(3, 0)
            elif attack_input == "w":
                attack(0, -1)
                attack(0, -2)
                attack(0 ,-3)
            elif attack_input == "s":
                attack(0, 1)
                attack(0 ,2)
                attack(0, 3)
            extra_damage = extra_damage_save
            weapon_damage = damage_save
    if action_taken:
        k = map.id.index("x")
        for m in range(len(map.Mid)):
            if abs(map.x[map.MplaceID[m]]-map.x[k]) + abs(map.y[map.MplaceID[m]]-map.y[k]) <= 1:
                print(f"The {map.Mid[m]} attacks you!")
                monster_attack = roll(map.Mdamage[m]) - (armor_defense + extra_defense)
                if monster_attack <= 0:
                    print("The monster's attack did no damage!")
                    continue
                print(f"The {map.Mid[m]} deals {monster_attack} damage!")
                hp -= monster_attack
                print (f"Your HP is now {hp}/{max_hp}.")
                if hp <= 0:
                    print("GAME OVER")
                    exit()
            elif map.Mid[m] == "S":
                continue
            else:
                board_dict_update()
                if board_dict.get((map.x[k]-1, map.y[k]), " ") != "□" and board_dict.get((map.x[k]+1, map.y[k]), " ") != "□" and board_dict.get((map.x[k], map.y[k]-1), " ") != "□" and board_dict.get((map.x[k], map.y[k]+1), " ") != "□":
                    continue
                moved = False
                attempts = 0
                while moved == False and attempts < 8:
                    attempts += 1
                    roll_dir = roll(4)
                    if roll_dir == 1:
                        move_object(-1, 0)
                    elif roll_dir == 2:
                        move_object(1, 0)
                    elif roll_dir == 3:
                        move_object(0, -1)
                    elif roll_dir == 4:
                        move_object(0, 1)
        if heal == 0:
            heal = 1
        else:
            if hp < max_hp:
                hp += 1
            heal = 0
                