import random
import map
import gen
import os
import sys
import tty
import termios

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
adventurer_extra_slot = "Nothing"
adventurer_extra_defense = 0
spells_known = ["heal 2 magic scroll"]
class_attack = 0
mission_done = []
mission_choice = ""
shop = []
powerup = "0"
Pclass = "None"  # Possible classes: adventurer, roque, wizard, warrior, necromancer, pyromancer

total_damage_taken = 0  
total_chests_opened = 0
total_damage_done = 0

wormHP = 50 + 10*map.runscompleted

board_dict = {}

def get_single_key():
    """Read a single key from user input without requiring Enter"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

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
        choice = get_single_key()
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
    if map.id[map.MplaceID[monsterID]] == "Ω":
        print("You have defeated the Devil!")
        run_completed()
        show_board()
        exit()
    if powerup == "1":
        hp += map.lvl
    exp += exp_gain
    map.id[map.MplaceID[monsterID]] = "□"
    map.Mhp.pop(monsterID)
    map.Mdamage.pop(monsterID)
    map.Mdefense.pop(monsterID)
    map.Mexp.pop(monsterID)
    map.Mid.pop(monsterID)
    map.MplaceID.pop(monsterID)
    if exp >= (map.lvl**2+map.lvl)/2 * 10 and map.lvl not in [5, 8, 10]:
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
    global action_taken, weapon, weapon_damage, armor, armor_defense, extra_slot, extra_damage, extra_defense, wormHP, class_attack, total_damage_done, total_chests_opened, exp
    k = map.id.index("x")
    target_x = map.x[k] + dx
    target_y = map.y[k] + dy
    if Pclass == "roque":
        if weapon.endswith("dagger"):
            if powerup == "4":
                if map.lvl < 6:
                    class_attack = 3
                elif map.lvl < 9:
                    class_attack = 4
                else:
                    class_attack = 5
            else:
                class_attack = 2
            class_attack = 2
        else:
            class_attack = 0
    for n in range(len(map.id)):
        if map.x[n] == target_x and map.y[n] == target_y:
            if map.id[n] == "C":
                action_taken = True
                total_chests_opened += 1
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
                    elif treasure_roll <= 43:
                        print("You found a short sword! (Damage 1d6)")
                        if equip("w") == "y":
                            weapon = "short sword"
                            weapon_damage = 6
                    elif treasure_roll <= 46:
                        print("You found a Chainmail Armor! (Defense +2)")
                        if equip("a") == "y":
                            armor = "Chainmail Armor"
                            armor_defense = 2
                    elif treasure_roll <= 48:
                        print("You found a magic missile magic scroll! (ranged attack to one side when casted)")
                        spell("magic missile magic scroll")
                    elif treasure_roll <= 50:
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
                    elif treasure_roll <= 43:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip("e") == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll <= 48:
                        print("You found a magic missile magic scroll! (ranged attack to one side when casted)")
                        spell("magic missile magic scroll")
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
                    elif treasure_roll <= 44:
                        print ("You found a health potion! (Restores hp to max when used)")
                        if equip("e") == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    elif treasure_roll <= 48:
                        print("You found a magic missile magic scroll! (ranged attack to one side when casted)")
                        spell("magic missile magic scroll")
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
                elif map.lvl <= 8:
                    if treasure_roll <= 6:
                        if Pclass == "warrior":
                            print("You found a warriorssword! (Damage 1d24)")
                            if equip("w") == "y":
                                weapon = "warriorssword"
                                weapon_damage = 24
                        else:
                            print("You found a giantssword! (Damage 1d20)")
                            if equip("w") == "y":
                                weapon = "giantssword"
                                weapon_damage = 20
                    elif treasure_roll <= 12:
                        print("You found a worm armor! (Defense +5)")
                        if equip("a") == "y":
                            armor = "worm armor"
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
                        if Pclass == "necromancer":
                            print("You found a summon zombie slush magic scroll! (summon a zombie slush when casted)")
                            spell("summon zombie slush magic scroll")
                        else:
                            print("You found a kill magic scroll! (kill a creature with 12 hp or less left)")
                            spell("kill magic scroll")
                    elif treasure_roll <= 50:
                        print("You found a dagger transmutation magic scroll! (transform dagger into another type when casted)")
                        spell("dagger transmutation magic scroll")
                elif map.lvl >= 9:
                    if treasure_roll <= 6:
                        if Pclass == "warrior":
                            print("You found a warriorssword! (Damage 1d30)")
                            if equip("w") == "y":
                                weapon = "warriorssword"
                                weapon_damage = 30
                        else:
                            print("You found a giantssword! (Damage 1d24)")
                            if equip("w") == "y":
                                weapon = "giantssword"
                                weapon_damage = 24
                    elif treasure_roll <= 12:
                        print("You found a master armor! (Defense +6)")
                        if equip("a") == "y":
                            armor = "master armor"
                            armor_defense = 6
                    elif treasure_roll <= 18:
                        print("You found a swift dagger! (Damage 1d24, use q for swift attack)")
                        if equip("w") == "y":
                            weapon = "swift dagger"
                            weapon_damage = 24
                    elif treasure_roll <= 24:
                        print("You found a dash dagger! (Damage 1d24, use q for dash attack)")
                        if equip("w") == "y":
                            weapon = "dash dagger"
                            weapon_damage = 24
                    elif treasure_roll <= 28:
                        print("You found a power ring! (Damage, defense +4)")
                        if equip("e") == "y":
                            extra_slot = "power ring 4"
                            extra_damage = 4
                            extra_defense = 4
                    elif treasure_roll <= 33:
                        print("You found a magic missile magic scroll! (ranged attack to one side when casted)")
                        spell("magic missile magic scroll")
                    elif treasure_roll <= 35:
                        print ("You found a shaking dash magic scroll! (Allows you to move two times and weak monsters around you die)")
                        spell("shaking dash magic scroll")
                    elif treasure_roll <= 40:
                        print("You found a kill sphere magic scroll! (kill all creature next to you with 8 hp or less left)")
                        spell("kill sphere magic scroll")
                    elif treasure_roll <= 45:
                        if Pclass == "necromancer":
                            print("You found a summon zombie slush magic scroll! (summon a zombie slush when casted)")
                            spell("summon zombie slush magic scroll")
                        else:
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
                total_damage_done += attack_roll
                if attack_roll <= 0:
                    print("Your attack did no damage!")
                    return
                print(f"You deal {attack_roll} damage!")
                wormHP -= attack_roll
            elif map.id[n] == "$":
                action_taken = True
                print("You enter the shop!")
                print("What do you want to buy?")
                if "1" in shop:
                    print("1 - 25 exp - power ring (Damage, defense +1)")
                if "2" in shop:
                    print("2 - 50 exp - plate armor (Defense +3)")
                if "3" in shop:
                    print("3 - 150 exp - warriorssword (Damage 1d24)")
                if "4" in shop:
                    print("4 - 300 exp - shaking dash magic scroll (Allows you to move two times and weak monsters around you die)")
                print(f"5 - {(map.lvl**2)*5} exp - health potion (Restores hp to max when used)")
                print("6 - nothing")
                choice = input()
                while choice not in ["1", "2", "3", "4", "5"] or choice not in shop:
                    if choice == "6":
                        print("You leave the shop.")
                        return
                    print("Invalid choice. Please choose again.")
                    choice = input()
                if choice == "1" and "1" in shop:
                    if exp >= 25:
                        exp -= 25
                        print("You bought the power ring!")
                        if equip("e") == "y":
                            extra_slot = "power ring 1"
                            extra_damage = 1
                            extra_defense = 1
                    else:
                        print("You don't have enough EXP!")
                elif choice == "2" and "2" in shop:
                    if exp >= 50:
                        exp -= 50
                        print("You bought the plate armor!")
                        if equip("a") == "y":
                            armor = "plate armor"
                            armor_defense = 3
                    else:
                        print("You don't have enough EXP!")
                elif choice == "3" and "3" in shop:
                    if exp >= 150:
                        exp -= 150
                        print("You bought the warriorssword!")
                        if equip("w") == "y":
                            weapon = "warriorssword"
                            weapon_damage = 24
                    else:
                        print("You don't have enough EXP!")
                elif choice == "4" and "4" in shop:
                    if exp >= 300:
                        exp -= 300
                        print("You bought the shaking dash magic scroll!")
                        spell("shaking dash magic scroll")
                    else:
                        print("You don't have enough EXP!")
                elif choice == "5" and "5" in shop:
                    if exp >= map.lvl**2*5:
                        exp -= map.lvl**2*5
                        print("You bought the health potion!")
                        if equip("e") == "y":
                            extra_slot = "health potion"
                            extra_damage = 0
                            extra_defense = 0
                    else:
                        print("You don't have enough EXP!")
            elif map.id[n] != "□" and map.id[n] != "x":
                action_taken = True
                print(f"You attack the {map.id[n]}!")
                monster_index = next((m for m in range(len(map.MplaceID)) if map.MplaceID[m] == n), None)
                if monster_index is None:
                    return
                attack_roll = roll(weapon_damage) + extra_damage + class_attack - map.Mdefense[monster_index]
                total_damage_done += attack_roll
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

def run_completed():
    global line_num, mission_done
    print(f"Congratulations, {username}! You have completed the run!")
    with open("playerinfo.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    if map.runscompleted == 0:
        lines[line_num] = f"{username},{map.runscompleted+1}\n"
    elif map.runscompleted == 1:
        lines[line_num] = f"{username},{map.runscompleted+1},{Pclass}\n"
    elif map.runscompleted == 2:
        lines[line_num] = f"{username},{map.runscompleted+1},{Pclass},{powerup}\n"
    elif map.runscompleted == 3:
        lines[line_num] = f"{username},{map.runscompleted+1},{Pclass},{powerup},{mission_choice},{shop_choice}\n"
    else:
        existing = list(mission_done)
        shop_save = list(shop)
        mc = globals().get("mission_choice")
        if mc and mc not in existing:
            existing.append(mc)
        missions_str = ",".join(existing)
        shop_str = ",".join(shop_save)
        lines[line_num] = f"{username},{map.runscompleted+1},{Pclass},{powerup},{missions_str},{shop_str}\n"
    with open("playerinfo.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

gen.start()

IsSaved = False
line_num = -1
print("Enter username: ")
username = input()
with open("playerinfo.txt", "r", encoding="utf-8") as f:
    while True:
        line_num += 1
        line = f.readline()
        if not line:
            break
        parts = line.strip().split(",")
        if parts[0] == username:
            map.runscompleted = int(parts[1])
            if map.runscompleted >= 1:
                Pclass = parts[2]
                if map.runscompleted >= 3:
                    powerup = parts[3]
                    if map.runscompleted >= 4:
                        if map.runscompleted > 7:
                            m = 7
                        else:
                            m = map.runscompleted+1
                        for n in range(4, m):
                            if parts[n] != "":
                                mission_done.append(parts[n])
                        for m in range(m, len(parts)):
                            if parts[m] != "":
                                shop.append(parts[m])
            print(f"Welcome back, {username}! You have completed {map.runscompleted} runs.")
            IsSaved = True
            break
if not IsSaved:
    with open("playerinfo.txt", "a", encoding="utf-8") as f:
        f.write(f"{username},0\n")

if map.runscompleted == 0:
    print ("You are 'x'.")
    print ("Squares you can stand on are marked with '□'.")
    print ("After we ask you for your action you can type w a s or d to move.")
    print ("Or you can type W A S or D to attack in that direction.")
    print ("you can also type i to see your inventory and statts.")
    print ("You can type m to see every monster that you can currently fight.")
    print ("You can type P to quit the game.")
    print ("If you start a game without quitting the game will glitch.")
    print ("If you want the instructions again type h.")
    print ("Later you may get more options.")
    print ("You can open chests by attacking them.")
    print ("Good luck!")

if map.runscompleted == 1:
    print()
    print("As an adventurer you can switch between your extra slots and  your adventurer slot by pressing f.")
    print("You can't do special actions from your adventurer slot.")
    print()
    print("As a roque you do +2 damage with daggers.")
    print("You can dash with f to move twice in one turn.")
    print()
    print("As a wizard you can learn spells instead of using a scroll.")
    print()
    print("As a warrior you have 25 percent chance you block an attack.")
    print("You also do +1 damage.")
    print()
    print("As a necromancer you can suck life of almost dead creatures with f gaining +1 hp per level")
    print()
    print("As a pyromancer you can burn stationary enemies with f.")
    print("You also do +1 fire damage.")
    print()
    print("After you complete a run you will keep the class for your next runs.")
    print("What class do you want to be? (adventurer, roque, wizard, warrior, necromancer, pyromancer)")
    Pclass = get_single_key()
    while Pclass not in ["adventurer", "roque", "wizard", "warrior", "necromancer", "pyromancer"]:
        print("Invalid class. Please choose from: adventurer, roque, wizard, warrior, necromancer, pyromancer")
        Pclass = get_single_key()

if map.runscompleted == 2:
    print("Choose a power up for your next run: ")
    print("1 - After defeating a monster you heal your level in hp.")
    print("2 - You get your armor defense times five is added to your max hp.")
    print("3 - Your extra damage is equal to your extra defense +1.")
    print("4 - your damage is increased by 1 and 1 more after each boss.")
    print("After you complete a run you will keep the power up for your next runs.")
    print("Enter the number of your choice: ")
    powerup = get_single_key()
    while powerup not in ["1", "2", "3", "4"]:
        print("Invalid choice. Please choose from: 1, 2, 3, 4")
        powerup = get_single_key()

if map.runscompleted > 2 and map.runscompleted < 7:
    print("Choose a mission: ")
    if "1" not in mission_done:
        print("1 - complete a run without armor.")
    if "2" not in mission_done:
        print("2 - Complete a run without taking more than 240 damage.")
    if "3" not in mission_done:
        print("3 - Complete a run without opening more than 20 chests.")
    if "4" not in mission_done:
        print("4 - complete a run without using your extra slot.")
    mission_choice = get_single_key()
    while mission_choice not in ["1", "2", "3", "4"] or mission_choice in mission_done:
        print("Invalid choice. Please choose a valid mission.")
        mission_choice = get_single_key()
    
    print("You need to attack the shop($) to enter it.")
    print("What do you want in your shop?")
    if "1" not in shop:
        print("1 - 25 exp - power ring (Damage, defense +1)")
    if "2" not in shop:
        print("2 - 50 exp - plate armor (Defense +3)")
    if "3" not in shop:
        print("3 - 150 exp - warriorssword (Damage 1d24)")
    if "4" not in shop:
        print("4 - 300 exp - shaking dash magic scroll (Allows you to move two times and weak monsters around you die)")
    shop_choice = get_single_key()
    while shop_choice not in ["1", "2", "3", "4"] or shop_choice in shop:
        print("Invalid choice. Please choose a valid shop item.")
        shop_choice = get_single_key()
    shop.append(shop_choice)

if map.runscompleted >= 7:
    print("You have completed all missions and shops available. Good luck on your normal run!")

if Pclass == "pyromancer" or Pclass == "warrior":
    class_attack = 1

heal = 0
while True:
    action_taken = False
    print()
    show_board()
    print()
    print("choose an action: ")
    action = get_single_key()
    if action == "i":
        print(f"HP: {hp}/{max_hp}, EXP: {exp}, Level: {map.lvl}, Exp to next level: {(map.lvl**2+map.lvl)/2 * 10 - exp}")
        print(f"Weapon: {weapon} (Damage: 1d{weapon_damage})")
        print(f"Armor: {armor} (Defense: {armor_defense})")
        print(f"Extra Slot: {extra_slot}")
        if Pclass == "adventurer":
            print(f"Adventurer Slot: {adventurer_extra_slot}")
            print("As an adventurer you can switch between your extra slots and  your adventurer slot by pressing f.")
            print("You can't get bonusses or do special actions from your adventurer slot.")
        elif Pclass == "roque":
                print("As a roque you do +2 damage with daggers.")
                print("You can dash with f to move twice in one turn.")
        elif Pclass == "wizard":
            print("Spells known:")
            for spell_name in spells_known:
                print(f"- {spell_name[0:-13]}")
            print("As a wizard you can learn spells instead of using a scroll.")
        elif Pclass == "warrior":
            print("As a warrior you have 25 percent chance you block an attack.")
            print("You also do +1 damage.")
        elif Pclass == "necromancer":
            print("As a necromancer you can suck life of almost dead creatures with f gaining +1 hp per level")
        elif Pclass == "pyromancer":
            print("As a pyromancer you can burn stationary enemies with f.")
            print("You also do +1 fire damage.")
        print(f"Total damage taken: {total_damage_taken}")
        print(f"Total damage done: {total_damage_done}")
        print(f"Total chests opened: {total_chests_opened}")
        if mission_choice == "1":
            print("Mission: Complete a run with only using daggers.")
        elif mission_choice == "2":
            print("Mission: Complete a run without taking more than 100 damage.")
        elif mission_choice == "3": 
            print("Mission: Complete a run without opening more than 12 chests.")
        elif mission_choice == "4":
            print("Mission: Complete a run without using your extra slot.")
        elif mission_choice == "5":
            print("Mission: Complete a run without armor.")
        if powerup == "1":
            print("Powerup: After defeating a monster you heal your level in hp.")
        elif powerup == "2":
            print("Powerup: You get your armor defense times five is added to your max hp.")
        elif powerup == "3":
            print("Powerup: Your extra damage is equal to your extra defense +1.")
        elif powerup == "4":
            print("Powerup: your damage is increased by 1 and 1 more after each boss.")
        print()
    elif action == "P":
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
        print ("A S D or W to attack in that direction.")
        print ("i - see your inventory and statts.")
        print ("m - see monsters you can fight.")
        print ("P - end the game.")
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
        if Pclass == "necromancer":
            print ("f - suck life from almost dead creatures")
        if Pclass == "pyromancer":
            print ("f - burn stationary enemies around you")
        print ("quit - end the game.")
        print ("h - see this help message again.")
        print ("Later you may get more options.")
        print ("You can open chests and shops by attacking them.")
        print ("Good luck!")
    elif action == "m":
        print("level 1 monsters:")
        print(f"K - Kobold (HP: {4+map.runscompleted}, Damage: 1d2)") #exp 2
        print(f"S - slime (HP: {2+map.runscompleted}, Damage: 1d3) can't move") #exp 1
        if map.lvl >= 2:
            print("level 2 monsters:")
            print(f"L - Lizardman (HP: {10+2*map.runscompleted}, Damage: 1d3, Defense: 1)") #exp 4
            print(f"F - Freakish Abberation (HP: {6+map.runscompleted}, Damage: 1d{4+2*map.runscompleted})") #exp 3+runscompleted
            if map.lvl >= 3:
                print("level 3 monsters:")
                print(f"O - Orc (HP: {10+2*map.runscompleted}, Damage: 1d8, Defense: 2)") #exp 6
                print(f"T - Troll (HP: {16+2*map.runscompleted}, Damage: 1d{6+2*map.runscompleted}, Defense: 3)") #exp 7+runscompleted
                if map.lvl >= 4:
                    print("level 4 monsters:")
                    print(f"G - Golem (HP: {10+3*map.runscompleted}, Damage: 1d6, Defense: 4)") #exp 7
                    print(f"Ø - Ogre (HP: {20+2*map.runscompleted}, Damage: 1d10, Defense: 2)") #exp 12
                    if map.lvl >= 5:
                        print("level 5 monsters:")
                        print(f"Ŧ - King troll (HP: {50+10*map.runscompleted}, Damage: 1d{12+2*map.runscompleted}, Defense: 4)") #exp 0
                        print(f"S - strong slime (HP: {2+map.runscompleted}, Damage: 1d6, Defense: {map.lvl})") #exp 12
                        if map.lvl >= 6:
                            print("level 6 monsters:")
                            print(f"B - Giant Beetle (HP: {10+2*map.runscompleted}, Damage: 1d10, Defense: 8)") #exp 16
                            print(f"Þ - Troll riding Giant Beetle (HP: {26+4*map.runscompleted}, Damage: 1d{10+2*map.runscompleted}, Defense: 8)") #exp 30+2*runscompleted
                            print(f"T - Strong Trolls (HP: {16+2*map.runscompleted}, Damage: 1d{10+2*map.runscompleted}, Defense: 4)") #exp 12+2*runscompleted
                            if map.lvl >= 7:
                                print("level 7 monsters:")
                                print(f"E - purple worm egg (HP: {15+3*map.runscompleted}, Damage: 1d8, Defense: 8) can't move") #exp 20
                                print(f"W - giant acid worm (HP: {30+5*map.runscompleted}, Damage: 1d24, Defense: 6)") #exp 40
                                if Pclass == "necromancer":
                                    print(f"Z - zombie slush (HP: 1, Damage: 1d8, Defense: 0)") #exp 50
                                if map.lvl >= 8:
                                    print("level 8 monsters:")
                                    print(f"◉ - Purple worm (HP: {50+10*map.runscompleted} , Damage: 1d20, Defense: 12)")
                                    if map.lvl >= 9:
                                        print("level 9 monsters:")
                                        print(f"D - Demon (HP: {30+5*map.runscompleted}, Damage: 1d20, Defense: 10)") #exp 55
                                        print(f"H - Hellhound (HP: {20+5*map.runscompleted}, Damage: 1d24, Defense: 8)") #exp 40
                                        print(f"P - Prickly demonic cactus (HP: {10+4*map.runscompleted}, Damage: 1d{8+2*map.runscompleted}, Defense: 15) can't move") #exp 20+2*runscompleted
                                        if map.lvl >= 10:
                                            print("level 10 monsters:")
                                            print(f"Ω - Devil (HP: {100+20*map.runscompleted}, Damage: 1d{26+2*map.runscompleted}, Defense: 15)") #exp 0
    elif action == "A":
        attack(-1, 0)
    elif action == "D":
        attack(1, 0)
    elif action == "W":
        attack(0, -1)
    elif action == "S":
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
            move_input = get_single_key()
            if move_input == "a":
                move(-1, 0)
            elif move_input == "d":
                move(1, 0)
            elif move_input == "w":
                move(0, -1)
            elif move_input == "s":
                move(0, 1)
            attack_input = get_single_key()
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
                print(f"{index} - {spell_name[0:-13]}")
                index += 1
            save = extra_slot
            spell_choice = get_single_key()
            if spell_choice.isdigit() and int(spell_choice) < len(spells_known):
                extra_slot = spells_known[int(spell_choice)]
            else:
                print("Not a valid number!")
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
            move_input1 = get_single_key()
            if move_input1 == "a":
                move(-1, 0)
            elif move_input1 == "d":
                move(1, 0)
            elif move_input1 == "w":
                move(0, -1)
            elif move_input1 == "s":
                move(0, 1)
            show_board()
            move_input2 = get_single_key()
            if move_input2 == "a":
                move(-1, 0)
            elif move_input2 == "d":
                move(1, 0)
            elif move_input2 == "w":
                move(0, -1)
            elif move_input2 == "s":
                move(0, 1)
        elif extra_slot == "shaking dash magic scroll":
            print("You can move two times and weak monsters around you die!")
            move_input1 = get_single_key()
            if move_input1 == "a":
                move(-1, 0)
            elif move_input1 == "d":
                move(1, 0)
            elif move_input1 == "w":
                move(0, -1)
            elif move_input1 == "s":
                move(0, 1)
            show_board()
            move_input2 = get_single_key()
            if move_input2 == "a":
                move(-1, 0)
            elif move_input2 == "d":
                move(1, 0)
            elif move_input2 == "w":
                move(0, -1)
            elif move_input2 == "s":
                move(0, 1) 
            kill_magic(-1, 0, 10)
            kill_magic(1, 0, 10)
            kill_magic(0, -1, 10)
            kill_magic(0, 1, 10)
        elif extra_slot == "dagger transmutation magic scroll":
            print("This spell does not take a turn.")
            if weapon == "swift dagger":
                print("You now have a dash dagger!")
                weapon = "dash dagger"
            elif weapon.endswith("dagger"):
                print("You now have a swift dagger!")
                weapon = "swift dagger"
        elif extra_slot == "magic missile magic scroll":
            extra_damage_save = extra_damage
            damage_save = weapon_damage
            save_lvl = map.lvl
            weapon_damage = 2
            extra_damage = map.lvl+2
            print(f"You do 1d2+{extra_damage} damage.")
            print("In wich direction do you want to attack? (w/a/s/d)")
            attack_input = get_single_key()
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
                attack(0, -3)
            elif attack_input == "s":
                attack(0, 1)
                attack(0, 2)
                attack(0, 3)
            if weapon_damage == 2:
                weapon_damage = damage_save
            if extra_damage == map.lvl+2:
                extra_damage = extra_damage_save
        elif extra_slot == "kill magic scroll":
            print("In wich direction do you want to try to kill a monster? (w/a/s/d)")
            attack_input = get_single_key()
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
        elif extra_slot == "summon zombie slush magic scroll":
            for n in range(len(map.id)):
                if map.id[n] == "□":
                    if abs(map.x[n]-map.x[map.id.index("x")]) + abs(map.y[n]-map.y[map.id.index("x")]) <= 1:
                        print("You summon a zombie slush next to you!")
                        map.id[n] = "Z"
                        map.Mhp.append(1)
                        map.Mdamage.append(8)
                        map.Mdefense.append(0)
                        map.Mexp.append(0)
                        map.Mid.append("Z")
                        map.MplaceID.append(n)
        if Pclass == "wizard":
            extra_slot = save
    elif action == "f":
        if Pclass == "roque":
            print("You can move twice this turn!")
            move_input1 = get_single_key()
            if move_input1 == "a":
                move(-1, 0)
            elif move_input1 == "d":
                move(1, 0)
            elif move_input1 == "w":
                move(0, -1)
            elif move_input1 == "s":
                move(0, 1)
            show_board()
            move_input2 = get_single_key()
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
            extra_damage = class_attack
            class_attack = save
            save = extra_defense
            extra_defense = adventurer_extra_defense
            adventurer_extra_defense = save
        elif Pclass == "necromancer":
            print("In wich direction do you want to suck life from a creature? (w/a/s/d)")
            attack_input = get_single_key()
            if attack_input == "a":
                kill_magic(-1, 0, 2*map.lvl)
            if attack_input == "d":
                kill_magic(1, 0, 2*map.lvl)
            if attack_input == "w":
                kill_magic(0, -1, 2*map.lvl)
            if attack_input == "s":
                kill_magic(0, 1, 2*map.lvl)
            if action_taken:
                hp += map.lvl
                if hp > max_hp:
                    hp = max_hp
                print(f"You sucked all life from the creature and restored {map.lvl} HP!")
        elif Pclass == "pyromancer":
            k = map.id.index("x")
            for n in range(len(map.id)):
                if abs(map.x[n]-map.x[k]) + abs(map.y[n]-map.y[k]) <= 1:
                    if map.id[n] in ["S", "E", "P"]:
                        action_taken = True
                        print(f"You burn and kill the {map.id[n]}!")
                        monster_index = next((m for m in range(len(map.MplaceID)) if map.MplaceID[m] == n), None)
                        if monster_index is not None:
                            monster_defeat(monster_index)
    if action_taken:
        k = map.id.index("x")
        m = -1
        while m+1 < len (map.MplaceID):
            m += 1
            if map.Mid[m] == "Z":
                n = len(map.MplaceID)
                map.id[k] = "□"
                map.id[map.MplaceID[m]] = "x"
                attack(-1, 0)
                attack(1, 0)
                attack(0, -1)
                attack(0, 1)
                m = m-(n-len(map.MplaceID))
                map.id[map.MplaceID[m]] = "Z"
                map.id[k] = "x"
                continue
            if abs(map.x[map.MplaceID[m]]-map.x[k]) + abs(map.y[map.MplaceID[m]]-map.y[k]) <= 1:
                print(f"The {map.Mid[m]} attacks you!")
                if Pclass == "warrior":
                    if roll(4) == 1:
                        print("You dodged the attack!")
                        continue
                monster_attack = roll(map.Mdamage[m]) - (armor_defense + extra_defense + adventurer_extra_defense)
                if monster_attack <= 0:
                    print("The monster's attack did no damage!")
                    continue
                total_damage_taken += monster_attack
                print(f"The {map.Mid[m]} deals {monster_attack} damage!")
                hp -= monster_attack
                print (f"Your HP is now {hp}/{max_hp}.")
                if hp <= 0:
                    print("GAME OVER")
                    show_board()
                    exit()
            elif map.Mid[m] in ["S", "E", "P"]:
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
                    monster_attack = roll(24) - (armor_defense + extra_defense)
                    if monster_attack <= 0:
                        print("The monster's attack did no damage!")
                        continue
                    total_damage_taken += monster_attack
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
                print("You defeated the purple worm!")
                if map.runscompleted < 2:
                    run_completed()
                    exit()
                else:
                    map.lvl = 9
                    map.id[map.wormplaceID[0]] = "□"
                    map.id[map.wormplaceID[1]] = "□"
                    map.id[map.wormplaceID[2]] = "□"
                    map.wormplaceID = [-1, -1, -1]
                    exp = 0
                    print(f"You leveled up! You are now level 9!")
                    max_hp += 5
                    hp = max_hp
                    print(f"Your max HP increased to {max_hp}!")
        if map.runscompleted > 1:
            if powerup == "2":
                max_hp += (armor_defense + extra_defense + 1 + map.lvl) * 5
            elif powerup == "3":
                extra_damage = extra_defense +1
            elif powerup == "4":
                if map.lvl < 6:
                    k = 1
                elif map.lvl < 9:
                    k = 2
                else:
                    k = 3
                if Pclass == "warrior" or Pclass == "pyromancer":
                    class_attack = 1 + k
                else:
                    class_attack = k
            if map.runscompleted > 2:
                if mission_choice == "1":
                    if armor != "Nothing":
                        print("You failed the mission by using armor!")
                        exit()  
                elif mission_choice == "2":
                    if total_damage_taken > 240:
                        print("You failed the mission by taking more than 240 damage!")
                        exit()
                elif mission_choice == "3":
                    if total_chests_opened > 20:
                        print("You failed the mission by opening more than 20 chests!")
                        exit()
                elif mission_choice == "4":
                    if extra_slot != "Nothing":
                        print("You failed the mission by using your extra slot!")
                        exit()
