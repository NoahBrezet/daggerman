import random
import map
import gen

# Player stats
exp = 0
max_hp = 10
hp = 10
weapon = "dagger"
weapon_damage = 2
extra_damage = 0
armor = "Notthing"
armor_defense = 3
extra_defense = 0
extra_slot = "Nothing"
adventurer_extra_slot = "Nothing"
adventurer_extra_damage = 0
adventurer_extra_defense = 0
spells_known = []
class_attack = 0
class_defense = 0

wormHP = 50
wormphase = 0

board_dict = {}

Pclass = "None"  # Possible classes: adventurer, roque, wizard

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
        if map.genID[k] != 0:
            gen.gen(map.genID[k])
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

def equip(itemType):
    while True:
        print("Do you want to equip this item? (y/n)")
        if itemType == "w":
            print(f"Current weapon: {weapon} (Damage 1d{weapon_damage})")
        elif itemType == "a":
            print(f"Current armor: {armor} (Defense +{armor_defense})")
        elif itemType == "e":
            print(f"Current extra slot: {extra_slot}")
        choice = input()
        if choice == "y" or choice == "n":
            return choice

def monster_defeat(monsterID):
    global hp, max_hp, weapon, weapon_damage, exp
    print(f"You defeated the {map.id[map.MplaceID[monsterID]]}!")
    exp_gain = map.Mexp[monsterID]
    print(f"You gain {exp_gain} EXP!")
    if map.lvl == 5 and map.id[map.MplaceID[monsterID]] == "Ŧ":
        map.lvl = 6
        exp = 0
        print(f"You leveled up! You are now level 6!")
        max_hp += 5
        hp = max_hp
        print(f"Your max HP increased to {max_hp}!")
        print("You found a kings dagger! (Damage 1d16)")
        if equip("w") == "y":
            weapon = "king's dagger"
            weapon_damage = 16
    exp += exp_gain
    map.id[map.MplaceID[monsterID]] = "□"
    map.Mhp.pop(monsterID)
    map.Mdamage.pop(monsterID)
    map.Mdefense.pop(monsterID)
    map.Mexp.pop(monsterID)
    map.Mid.pop(monsterID)
    map.MplaceID.pop(monsterID)
    if exp >= (map.lvl**2+map.lvl)/2 * 10 and map.lvl != 5 and map.lvl != 8:
        exp -= (map.lvl**2+map.lvl)/2 * 10
        map.lvl += 1
        print(f"You leveled up! You are now level {map.lvl}!")
        max_hp += 5
        hp = max_hp
        print(f"Your max HP increased to {max_hp}!")

def spell(spell_name):
    global spells_known, extra_slot, extra_damage, extra_defense
    if Pclass == "wizard":
        if spell_name not in spells_known:
            print(f"You learn the {spell_name[0:-13]} spell!")
            spells_known.append(spell_name)
    else:
        if equip("e") == "y":
            extra_slot = spell_name
            extra_damage = 0
            extra_defense = 0

def attack(dx, dy):
    global action_taken, weapon, weapon_damage, armor, armor_defense, extra_slot, extra_damage, extra_defense, wormHP, class_attack
    k = map.id.index("x")
    target_x = map.x[k] + dx
    target_y = map.y[k] + dy
    if Pclass == "roque":
        if weapon.endswith("dagger"):
            class_attack = 1
        else:
            class_attack = 0
    for n in range(len(map.id)):
        if map.x[n] == target_x and map.y[n] == target_y:
            if map.id[n] == "C":
                action_taken = True
                print("You open the chest and find treasure!")
                map.id[n] = "□"
                treasure_roll = roll(50)
                if map.lvl == 1:
                    if treasure_roll <= 10:
                        print("You found a dagger! (Damage 1d3)")
                        if equip("w") == "y":
                            weapon = "dagger"
                            weapon_damage = 3
                    elif treasure_roll <= 20:
                        print("You found a Leather Armor! (Defense +1)")
                        if equip("a") == "y":
                            armor = "Leather Armor"
                            armor_defense = 1
                    elif treasure_roll <= 30:
                        print("You found a attack ring! (Damage +1)")
                        if equip("e") == "y":
                            extra_slot = "attack ring 1"
                            extra_damage = 1
                            extra_defense = 0
                    elif treasure_roll <= 40:
                        print ("You found a a defense amulet! (Defense +1)")
                        if equip("e") == "y":
                            extra_slot = "defense amulet 1"
                            extra_defense = 1
                            extra_damage = 0
                    elif treasure_roll <= 44:
                        print("You found a short sword! (Damage 1d6)")
                        if equip("w") == "y":
                            weapon = "short sword"
                            weapon_damage = 6
                    elif treasure_roll <= 48:
                        print("You found a Chainmail Armor! (Defense +2)")
                        if equip("a") == "y":
                            armor = "Chainmail Armor"
                            armor_defense = 2
                    elif treasure_roll == 49:
                        print ("you found a health potion! (Restores hp to max when used")
                        if equip("e") == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll == 50:
                        print("You found a dash magic scroll! (Allows you to move twice in one turn)")
                        spell("dash magic scroll")
                elif map.lvl == 2:
                    if treasure_roll <= 10:
                        print("You found a short sword! (Damage 1d6)")
                        if equip("w") == "y":
                            weapon = "short sword"
                            weapon_damage = 6
                    elif treasure_roll <= 20:
                        print("You found a Chainmail Armor! (Defense +2)")
                        if equip("a") == "y":
                            armor = "Chainmail Armor"
                            armor_defense = 2
                    elif treasure_roll <= 28:
                        print("You found a swift dagger! (Damage 1d4, use q for swift attack)")
                        if equip("w") == "y":
                            weapon = "swift dagger"
                            weapon_damage = 4
                    elif treasure_roll <= 36:
                        print("You found a power ring! (Damage, defense +1)")
                        if equip("e") == "y":
                            extra_slot = "power ring 1"
                            extra_damage = 1
                            extra_defense = 1
                    elif treasure_roll <= 42:
                        print ("You found a heal magic scroll! (heal 2 hp when casted)")
                        spell("heal 2 magic scroll")
                    elif treasure_roll <= 48:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip("e") == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll == 49:
                        print("You found a longsword! (Damage 1d8)")
                        if equip("w") == "y":
                            weapon = "longsword"
                            weapon_damage = 8
                    elif treasure_roll == 50:
                        print("You found a dash magic scroll! (Allows you to move twice in one turn)")
                        spell("dash magic scroll")
                elif map.lvl == 3:
                    if treasure_roll <= 10:
                        print("You found a longsword! (Damage 1d8)")
                        if equip("w") == "y":
                            weapon = "longsword"
                            weapon_damage = 8
                    elif treasure_roll <= 20:
                        print("You found a chainmail armor! (Defense +2)")
                        if equip("a") == "y":
                            armor = "chainmail armor"
                            armor_defense = 2
                    elif treasure_roll <= 28:
                        print("You found a swift dagger! (Damage 1d6, use q for swift attack)")
                        if equip("w") == "y":
                            weapon = "swift dagger"
                            weapon_damage = 6
                    elif treasure_roll <= 36:
                        print("You found a attack ring! (Damage +2)")
                        if equip("e") == "y":
                            extra_slot = "attack ring 2"
                            extra_damage = 2
                            extra_defense = 0
                    elif treasure_roll <= 42:
                        print ("You found a a defense amulet! (Defense +2)")
                        if equip("e") == "y":
                            extra_slot = "defense amulet 2"
                            extra_defense = 2
                            extra_damage = 0
                    elif treasure_roll <= 48:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip("e") == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll == 49:
                        print("You found a greatsword! (Damage 1d12)")
                        if equip("w") == "y":
                            weapon = "greatsword"
                            weapon_damage = 12
                    elif treasure_roll == 50:
                        print("You found a heal 4 magic scroll! (heal 4 hp when casted)")
                        spell("heal 4 magic scroll")
                elif map.lvl <= 5:
                    if treasure_roll <= 8:
                        print("You found a greatsword! (Damage 1d12)")
                        if equip("w") == "y":
                            weapon = "greatsword"
                            weapon_damage = 12
                    elif treasure_roll <= 16:
                        print("You found a plate armor! (Defense +3)")
                        if equip("a") == "y":
                            armor = "plate armor"
                            armor_defense = 3
                    elif treasure_roll <= 22:
                        print("You found a swift dagger! (Damage 1d8, use q for swift attack)")
                        if equip("w") == "y":
                            weapon = "swift dagger"
                            weapon_damage = 8
                    elif treasure_roll <= 28:
                        print("You found a dash dagger! (Damage 1d8, use q for dash attack)")
                        if equip("w") == "y":
                            weapon = "dash dagger"
                            weapon_damage = 8
                    elif treasure_roll <= 34:
                        print("You found a power ring! (Damage, defense +2)")
                        if equip("e") == "y":
                            extra_slot = "power ring 2"
                            extra_damage = 2
                            extra_defense = 2
                    elif treasure_roll <= 39:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip("e") == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll <= 44:
                        print("You found a heal 4 magic scroll! (heal 6 hp when casted)")
                        spell("heal 4 magic scroll")
                    elif treasure_roll <= 47:
                        print("You found a magic missile magic scroll! (ranged attack to one side when casted)")
                        spell("magic missile magic scroll")
                    elif treasure_roll <= 50:
                        print("You found a dagger transmutation magic scroll! (transform dagger into another type when casted)")
                        spell("dagger transmutation magic scroll")
                elif map.lvl == 6:
                    if treasure_roll <= 6:
                        print("You found a giantssword! (Damage 1d20)")
                        if equip("w") == "y":
                            weapon = "giantssword"
                            weapon_damage = 20
                    elif treasure_roll <= 12:
                        print("You found a plate armor! (Defense +4)")
                        if equip("a") == "y":
                            armor = "plate armor"
                            armor_defense = 4
                    elif treasure_roll <= 18:
                        print("You found a swift dagger! (Damage 1d16, use q for swift attack)")
                        if equip("w") == "y":
                            weapon = "swift dagger"
                            weapon_damage = 16
                    elif treasure_roll <= 24:
                        print("You found a dash dagger! (Damage 1d16, use q for dash attack)")
                        if equip("w") == "y":
                            weapon = "dash dagger"
                            weapon_damage = 16
                    elif treasure_roll <= 28:
                        print("You found a power ring! (Damage, defense +3)")
                        if equip("e") == "y":
                            extra_slot = "power ring 3"
                            extra_damage = 3
                            extra_defense = 3
                    elif treasure_roll <= 33:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip("e") == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll <= 40:
                        print("You found a heal 8 magic scroll! (heal 8 hp when casted)")
                        spell("heal 8 magic scroll")
                    elif treasure_roll <= 45:
                        print("You found a magic missile magic scroll! (ranged attack to one side when casted)")
                        spell("magic missile magic scroll")
                    elif treasure_roll <= 50:
                        print("You found a dagger transmutation magic scroll! (transform dagger into another type when casted)")
                        spell("dagger transmutation magic scroll")
                elif map.lvl >= 7:
                    if treasure_roll <= 6:
                        print("You found a giantssword! (Damage 1d20)")
                        if equip("w") == "y":
                            weapon = "giantssword"
                            weapon_damage = 20
                    elif treasure_roll <= 12:
                        print("You found a plate armor! (Defense +5)")
                        if equip("a") == "y":
                            armor = "plate armor"
                            armor_defense = 5
                    elif treasure_roll <= 18:
                        print("You found a swift dagger! (Damage 1d20, use q for swift attack)")
                        if equip("w") == "y":
                            weapon = "swift dagger"
                            weapon_damage = 20
                    elif treasure_roll <= 24:
                        print("You found a dash dagger! (Damage 1d20, use q for dash attack)")
                        if equip("w") == "y":
                            weapon = "dash dagger"
                            weapon_damage = 20
                    elif treasure_roll <= 28:
                        print("You found a heal 8 magic scroll! (heal 8 hp when casted)")
                        spell("heal 8 magic scroll")
                    elif treasure_roll <= 33:
                        print("You found a magic missile magic scroll! (ranged attack to one side when casted)")
                        spell("magic missile magic scroll")
                    elif treasure_roll <= 40:
                        print("You found a kill sphere magic scroll! (kill all creature next to you with 8 hp or less left)")
                        spell("kill sphere magic scroll")
                    elif treasure_roll <= 45:
                        print("You found a kill magic scroll! (kill a creature with 12 hp or less left)")
                        spell("kill magic scroll")
                    elif treasure_roll <= 50:
                        print("You found a dagger transmutation magic scroll! (transform dagger into another type when casted)")
                        spell("dagger transmutation magic scroll")
                return
            elif map.id[n] == "◉":
                action_taken = True
                print(f"You attack the purple worm!")
                attack_roll = roll(weapon_damage) + extra_damage + class_attack - 12
                if attack_roll <= 0:
                    print("Your attack did no damage!")
                    return
                print(f"You deal {attack_roll} damage!")
                wormHP -= attack_roll
            elif map.id[n] != "□":
                action_taken = True
                print(f"You attack the {map.id[n]}!")
                monster_index = next((m for m in range(len(map.MplaceID)) if map.MplaceID[m] == n), None)
                if monster_index is None:
                    return
                attack_roll = roll(weapon_damage) + extra_damage + class_attack - map.Mdefense[monster_index]
                if attack_roll <= 0:
                    print("Your attack did no damage!")
                    return
                print(f"You deal {attack_roll} damage!")
                map.Mhp[monster_index] -= attack_roll
                if map.Mhp[monster_index] <= 0:
                    monster_defeat(monster_index)
                return
            else:
                return

def kill_magic(dx, dy, strength):
    global action_taken, weapon, weapon_damage, extra_slot, exp, max_hp, hp
    k = map.id.index("x")
    target_x = map.x[k] + dx
    target_y = map.y[k] + dy
    for n in range(len(map.id)):
        if map.x[n] == target_x and map.y[n] == target_y:
            if map.id[n] != "C" and map.id[n] != "□":
                action_taken = True
                print(f"You attack the {map.id[n]}!")
                monster_index = next((m for m in range(len(map.MplaceID)) if map.MplaceID[m] == n), None)
                if monster_index is None:
                    return
                if map.Mhp[monster_index] <= strength:
                    monster_defeat(monster_index)

def wormmove(dx ,dy):
    global board_dict, moved
    src_idx = map.wormplaceID[0]
    target_idx = find_index_at(map.x[src_idx]+dx, map.y[src_idx]+dy)
    if target_idx is not None and board_dict.get((map.x[src_idx]+dx, map.y[src_idx]+dy), " ") == "□":
        moved = True
        map.id[target_idx] = "◉"
        map.id[map.wormplaceID[2]] = "□"
        map.wormplaceID[2] = map.wormplaceID[1]
        map.wormplaceID[1] = map.wormplaceID[0]
        map.wormplaceID[0] = target_idx

gen.start()

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
        print(f"HP: {hp}/{max_hp}, EXP: {exp}, Level: {map.lvl}, Exp to next level: {(map.lvl**2+map.lvl)/2 * 10 - exp}")
        print(f"Weapon: {weapon} (Damage: 1d{weapon_damage})")
        print(f"Armor: {armor} (Defense: {armor_defense})")
        print(f"Extra Slot: {extra_slot}")
        if Pclass == "adventurer":
            print(f"Adventurer Slot: {adventurer_extra_slot}")
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
        if Pclass == "roque":
            print ("f - dash")
        if Pclass == "adventurer":
            print ("f - switch extra slots")
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
                    if map.lvl >= 5:
                        print("level 5 monsters:")
                        print("Ŧ - King troll (HP: 50, Damage: 1d16, Defense: 4)") #exp 0
                        print("S - strong slime (HP: 2, Damage: 1d6, Defense: 5)") #exp 12
                        if map.lvl >= 6:
                            print("level 6 monsters:")
                            print("B - Giant Beetle (HP: 10, Damage: 1d10, Defense: 8)") #exp 16
                            print("Þ - Troll riding Giant Beetle (HP: 26, Damage: 1d12, Defense: 8)") #exp 30
                            print("T - Strong Trolls (HP: 16, Damage: 1d12, Defense: 4)") #exp 12
                            if map.lvl >= 7:
                                print("level 7 monsters:")
                                print("E - purple worm egg (HP: 15, Damage: 1d16, Defense: 8)") #exp 20
                                print("W - giant acid worm (HP: 30, Damage: 1d20, Defense: 6)") #exp 40
                                if map.lvl >= 8:
                                    print("level 8 monsters:")
                                    print("◉ - Purple worm (HP: 50 , Damage: 1d20, Defense: 12)")
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
        if Pclass == "wizard":
            print("What spell do you want to cast?")
            index = 0
            for spell_name in spells_known:
                print(f"{index} - {spell_name}")
                index += 1
            spell_choice = input()
            save = extra_slot
            if isinstance(spell_choice, str):
                extra_slot = spells_known[spell_choice]
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
        elif extra_slot == "heal 8 magic scroll":
            hp += 8
            if hp > max_hp:
                hp = max_hp
            print("You cast the heal spell and restored 8 HP!")
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
            print(f"You do 1d2+{map.lvl} damage.")
            print("In wich direction do you want to attack? (w/a/s/d)")
            attack_input = input()
            extra_damage_save = extra_damage
            damage_save = weapon_damage
            extra_damage = map.lvl
            weapon_damage = 2
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
        elif extra_slot == "kill magic scroll":
            print("In wich direction do you want to try to kill a monster? (w/a/s/d)")
            attack_input = input()
            if attack_input == "a":
                kill_magic(-1, 0, 12)
            if attack_input == "d":
                kill_magic(1, 0, 12)
            if attack_input == "w":
                kill_magic(0, -1, 12)
            if attack_input == "s":
                kill_magic(0, 1, 12)
        elif extra_slot == "kill sphere magic scroll":
            kill_magic(-1, 0, 8)
            kill_magic(1, 0, 8)
            kill_magic(0, -1, 8)
            kill_magic(0, 1, 8)
        if Pclass == "wizard":
            extra_slot = save
    elif action == "f":
        if Pclass == "roque":
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
        elif Pclass == "adventurer":
            save = extra_slot
            extra_slot = adventurer_extra_slot
            adventurer_extra_slot = save
            save = extra_damage
            extra_damage = adventurer_extra_damage
            adventurer_extra_damage = save
            save = extra_defense
            extra_defense = adventurer_extra_defense
            adventurer_extra_defense = save
    if action_taken:
        k = map.id.index("x")
        for m in range(len(map.Mid)):
            if abs(map.x[map.MplaceID[m]]-map.x[k]) + abs(map.y[map.MplaceID[m]]-map.y[k]) <= 1:
                print(f"The {map.Mid[m]} attacks you!")
                if Pclass == "warrior":
                    if roll(4) == 1:
                        print("You dodged the attack!")
                        continue
                monster_attack = roll(map.Mdamage[m]) - (armor_defense + extra_defense + class_defense)
                if monster_attack <= 0:
                    print("The monster's attack did no damage!")
                    continue
                print(f"The {map.Mid[m]} deals {monster_attack} damage!")
                hp -= monster_attack
                print (f"Your HP is now {hp}/{max_hp}.")
                if hp <= 0:
                    print("GAME OVER")
                    show_board()
                    exit()
            elif map.Mid[m] == "S" or map.Mid[m] == "E":
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
        if map.lvl >= 4:
            if hp < max_hp:
                    hp += 1
        else:
            if heal == 0:
                heal = 1
            else:
                if hp < max_hp:
                    hp += 1
                heal = 0
        if map.wormplaceID[0] != -1:
            if wormHP > 0:
                if abs(map.x[map.wormplaceID[0]]-map.x[k]) + abs(map.y[map.MplaceID[m]]-map.y[k]) <= 2:
                    print(f"The purple worm attacks you!")
                    monster_attack = roll(20) - (armor_defense + extra_defense)
                    if monster_attack <= 0:
                        print("The monster's attack did no damage!")
                        continue
                    print(f"The purple worm deals {monster_attack} damage!")
                    hp -= monster_attack
                    print (f"Your HP is now {hp}/{max_hp}.")
                    if hp <= 0:
                        print("GAME OVER")
                        show_board()
                        exit()
                moved = False
                attempts = 0
                while moved == False and attempts < 8:
                    attempts += 1
                    roll_dir = roll(4)
                    if roll_dir == 1:
                        wormmove(-1, 0)
                    elif roll_dir == 2:
                        wormmove(1, 0)
                    elif roll_dir == 3:
                        wormmove(0, -1)
                    elif roll_dir == 4:
                        wormmove(0, 1)
            else:
                print("You defeated the purple worm and have won this run!")
                exit()