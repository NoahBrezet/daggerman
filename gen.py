import map
import random

Lx = []
Ly = []
Lid = []

def create_square(new_x, new_y, new_id, new_genID):
    map.x.append(new_x)
    map.y.append(new_y)
    map.id.append(new_id)
    map.genID.append(new_genID)

def start():
    Lx.append(0)
    Ly.append(0)
    Lid.append("start")
    create_square(0, 0, "x", 0)
    create_square(1, 0, "□", 0)
    create_square(-1, 0, "□", 0)
    create_square(0, 1, "C", 0)
    create_square(2, 0, "□", 4)
    create_square(-2, 0, "□", 1)

def create_monster(new_hp, new_damage, new_defense, new_exp, new_id):
    map.Mhp.append(new_hp)
    map.Mdamage.append(new_damage)
    map.Mdefense.append(new_defense)
    map.Mexp.append(new_exp)
    map.Mid.append(new_id)
    map.MplaceID.append(len(map.id)-1) 

def gen(gen):
    map.genID[map.id.index("x")] = 0
    xnow = map.x[map.id.index("x")]
    ynow = map.y[map.id.index("x")]
    if gen == 1:
        xcentre = xnow-3
        ycentre = ynow
        if (xcentre/5, ycentre/5) in zip(Lx, Ly):
            return
        Lx.append(xcentre/5)
        Ly.append(ycentre/5)
    elif gen == 4:
        xcentre = xnow+3
        ycentre = ynow
        if (xcentre/5, ycentre/5) in zip(Lx, Ly):
            return
        Lx.append(xcentre/5)
        Ly.append(ycentre/5)
    elif gen == 2:
        xcentre = xnow
        ycentre = ynow-3
        if (xcentre/5, ycentre/5) in zip(Lx, Ly):
            return
        Lx.append(xcentre/5)
        Ly.append(ycentre/5)
    elif gen == 3:
        xcentre = xnow
        ycentre = ynow+3
        if (xcentre/5, ycentre/5) in zip(Lx, Ly):
            return
        Lx.append(xcentre/5)
        Ly.append(ycentre/5)
    if gen == 1 or gen == 4:
        if map.lvl == 1:
            room = random.randint(1,6)
            if room == 1:
                create_square(xcentre, ycentre, "□", 0)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "□", 0)
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
                create_square(xcentre+1, ycentre, "□", 0)
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
            elif room == 2:
                create_square(xcentre, ycentre, "□", 0)
                create_square(xcentre, ycentre+1, "C", 0)
                create_square(xcentre+1, ycentre, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre-1, ycentre, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
            elif room == 3:
                create_square(xcentre, ycentre, "□", 0)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "S", 0)
                create_monster(2,3,0,1,"S")
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
                create_square(xcentre+1, ycentre, "S", 0)
                create_monster(2,3,0,1,"S")
                create_square(xcentre-1, ycentre, "S", 0)
                create_monster(2,3,0,1,"S")
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
            elif room == 4:
                create_square(xcentre, ycentre, "□", 0)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "□", 0)
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
                create_square(xcentre+1, ycentre, "□", 0)
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
                create_square(xcentre+1, ycentre+1, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre-1, ycentre-1, "K", 0)
                create_monster(4, 2, 0, 2, "K")
            elif room == 5:
                create_square(xcentre, ycentre, "C", 0)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "□", 0)
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
                create_square(xcentre+1, ycentre, "□", 0)
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
                create_square(xcentre+1, ycentre-1, "□", 0)
                create_square(xcentre-1, ycentre+1, "□", 0)
                create_square(xcentre+1, ycentre-1, "□", 0)
                create_square(xcentre-1, ycentre+1, "□", 0)
            elif room == 6:
                create_square(xcentre, ycentre, "C", 0)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "□", 0)
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
                create_square(xcentre+1, ycentre, "□", 0)
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
                create_square(xcentre+1, ycentre-1, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre-1, ycentre+1, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre+1, ycentre+1, "S", 0)
                create_monster(2,3,0,1,"S")
                create_square(xcentre-1, ycentre-1, "S", 0)
                create_monster(2,3,0,1,"S")
    if gen == 2 or gen == 3:
        if map.lvl == 1:
            room = random.randint(1,6)
            if room == 1:
                create_square(xcentre, ycentre, "□", 0)
                create_square(xcentre+1, ycentre, "□", 0)
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "□", 0)
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
            elif room == 2:
                create_square(xcentre, ycentre, "□", 0)
                create_square(xcentre+1, ycentre, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre, ycentre+1, "C", 0)
                create_square(xcentre-1, ycentre, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
            elif room == 3:
                create_square(xcentre, ycentre, "□", 0)
                create_square(xcentre+1, ycentre, "S", 0)
                create_monster(2,3,0,1,"S")
                create_square(xcentre, ycentre+1, "S", 0)
                create_monster(2,3,0,1,"S")
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre, ycentre-1, "S", 0)
                create_monster(2,3,0,1,"S")
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
            elif room == 4:
                create_square(xcentre, ycentre, "□", 0)
                create_square(xcentre+1, ycentre, "□", 0)
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "□", 0)
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
                create_square(xcentre+1, ycentre+1, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre-1, ycentre-1, "K", 0)
                create_monster(4, 2, 0, 2, "K")
            elif room == 5:
                create_square(xcentre, ycentre, "C", 0)
                create_square(xcentre+1, ycentre, "□", 0)
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "□", 0)
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
                create_square(xcentre+1, ycentre-1, "□", 0)
                create_square(xcentre-1, ycentre+1, "□", 0)
                create_square(xcentre+1, ycentre-1, "□", 0)
                create_square(xcentre-1, ycentre+1, "□", 0)
            elif room == 6:
                create_square(xcentre, ycentre, "C", 0)
                create_square(xcentre+1, ycentre, "□", 0)
                create_square(xcentre-1, ycentre, "□", 0)
                create_square(xcentre+2, ycentre, "□", 4)
                create_square(xcentre-2, ycentre, "□", 1)
                create_square(xcentre, ycentre+1, "□", 0)
                create_square(xcentre, ycentre-1, "□", 0)
                create_square(xcentre, ycentre+2, "□", 3)
                create_square(xcentre, ycentre-2, "□", 2)
                create_square(xcentre+1, ycentre-1, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre-1, ycentre+1, "K", 0)
                create_monster(4, 2, 0, 2, "K")
                create_square(xcentre+1, ycentre+1, "S", 0)
                create_monster(2,3,0,1,"S")
                create_square(xcentre-1, ycentre-1, "S", 0)
                create_monster(2,3,0,1,"S")
