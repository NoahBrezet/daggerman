import random

x = []
y = []
id = []
standon = []
exp = 0
lvl = 1
hp = 10
weapon = "dagger"
weapon_damage = 2
armor = "Nothing"
armor_defense = 0
extra_slot = "Nothing"

def roll_dice(num_dice, num_sides):
    rolls = []
    for _ in range(num_dice):
        rolls.append(random.randint(1, num_sides))
    return rolls

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
    board_dict = {}
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

def gen():
    a = 0

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
print ("Later you may get more options.")
print ("Good luck!")

while True:
    action_taken = False
    print()
    show_board()
    print()
    print("choose an action: ")
    action = input()
    if action == "i":
        print(f"HP: {hp}, EXP: {exp}, Level: {lvl}, Exp to next level: {lvl * 10- exp}")
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

            

        

# print ("GAME OVER")