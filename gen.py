import map
import random

# Generated room tracking
Lx = []
Ly = []

def create_square(new_x, new_y, new_id, new_genID):
    map.x.append(new_x)
    map.y.append(new_y)
    map.id.append(new_id)
    map.genID.append(new_genID)

def start():
    Lx.append(0)
    Ly.append(0)
    create_square(0, 0, "x", 0)
    create_square(1, 0, "□", 0)
    create_square(-1, 0, "□", 0)
    create_square(0, 1, "C", 0)
    create_square(2, 0, "□", 4)
    create_square(-2, 0, "□", 1)

def create_mon(new_id):
    if new_id != "□" and new_id != "C":
        if new_id == "K":
            create_monster(4, 3, 0, 2, "K")
        elif new_id == "S":
            create_monster(2, 3, 0, 1, "S")
        elif new_id == "F":
            create_monster(6, 6, 0, 3, "F")
        elif new_id == "L":
            create_monster(10, 3, 1, 4, "L")
        elif new_id == "O":
            create_monster(10, 8, 2, 6, "O")
        elif new_id == "T":
            create_monster(16, 6, 3, 7, "T")
        elif new_id == "G":
            create_monster(10, 6, 4, 7, "G")
        elif new_id == "Ø":
            create_monster(20, 10, 2, 12, "Ø")

def create_monster(new_hp, new_damage, new_defense, new_exp, new_id):
    map.Mhp.append(new_hp)
    map.Mdamage.append(new_damage)
    map.Mdefense.append(new_defense)
    map.Mexp.append(new_exp)
    map.Mid.append(new_id)
    map.MplaceID.append(len(map.id)-1) 

def emptyT(xc, yc):
    create_square(xc, yc, "□", 0)
    create_square(xc, yc+1, "□", 0)
    create_square(xc, yc-1, "□", 0)
    create_square(xc, yc+2, "□", 3)
    create_square(xc, yc-2, "□", 2)
    create_square(xc+1, yc, "□", 0)
    create_square(xc-1, yc, "□", 0)
    create_square(xc+2, yc, "□", 4)
    create_square(xc-2, yc, "□", 1)

def central(xc, yc, Mc, M1, M2):
    create_square(xc, yc, Mc, 0)
    create_mon(Mc)
    create_square(xc, yc+1, "□", 0)
    create_square(xc, yc-1, "□", 0)
    create_square(xc, yc+2, "□", 3)
    create_square(xc, yc-2, "□", 2)
    create_square(xc+1, yc, "□", 0)
    create_square(xc-1, yc, "□", 0)
    create_square(xc+2, yc, "□", 4)
    create_square(xc-2, yc, "□", 1)
    create_square(xc-1, yc-1, M1, 0)
    create_mon(M1)
    create_square(xc-1, yc+1, M2, 0)
    create_mon(M2)
    create_square(xc+1, yc-1, M2, 0)
    create_mon(M2)
    create_square(xc+1, yc+1, M1, 0)
    create_mon(M1)

def chest_allyH(xc, yc, M):
    create_square(xc, yc, "□", 0)
    create_square(xc, yc+1, "C", 0)
    create_square(xc+1, yc, M, 0)
    create_mon(M)
    create_square(xc-1, yc, M, 0)
    create_mon(M)
    create_square(xc+2, yc, "□", 4)
    create_square(xc-2, yc, "□", 1)

def chest_allyV(xc, yc, M):
    create_square(xc, yc, "□", 0)
    create_square(xc, yc+1, M, 0)
    create_mon(M)
    create_square(xc-1, yc, "C", 0)
    create_square(xc, yc-1, M, 0)
    create_mon(M)
    create_square(xc, yc+2, "□", 3)
    create_square(xc, yc-2, "□", 2)

def chestroomH(xc, yc, M1, M2, gen):
    if gen == 1:
        xc2 = xc-5
        if (xc2/5, yc/5) in zip(Lx, Ly):
            able = False
        else:
            able = True
            Lx.append(xc2/5)
            Ly.append(yc/5)
    if gen == 4:
        xc2 = xc+5
        if (xc2/5, yc/5) in zip(Lx, Ly):
            able = False
        else:
            Lx.append(xc2/5)
            Ly.append(yc/5)
            able = True
            save = xc
            xc = xc2
            xc2 = save
    if able == True:
        create_square(xc, yc, M1, 0)
        create_mon(M1)
        create_square(xc, yc-1, M2, 0)
        create_mon(M2)
        create_square(xc, yc+1, M2, 0)
        create_mon(M2)
        create_square(xc-1, yc, "□", 0)
        create_square(xc+1, yc, "□", 0)
        create_square(xc+2, yc, "□", 4)
        create_square(xc-2, yc, "□", 0)
        create_square(xc-1, yc-1, "□", 0)
        create_square(xc-1, yc+1, "□", 0)
        create_square(xc+1, yc-1, "□", 0)
        create_square(xc+1, yc+1, "□", 0)
        create_square(xc-2, yc-1, "C", 0)
        create_square(xc-2, yc+1, "□", 0)
        create_square(xc2, yc, M1, 0)
        create_mon(M1)
        create_square(xc2, yc-1, M2, 0)
        create_mon(M2)
        create_square(xc2, yc+1, M2, 0)
        create_mon(M2)
        create_square(xc2-1, yc, "□", 0)
        create_square(xc2+1, yc, "□", 0)
        create_square(xc2+2, yc, "□", 0)
        create_square(xc2-2, yc, "□", 1)
        create_square(xc2-1, yc-1, "□", 0)
        create_square(xc2-1, yc+1, "□", 0)
        create_square(xc2+1, yc-1, "□", 0)
        create_square(xc2+1, yc+1, "□", 0)
        create_square(xc2+2, yc-1, "C", 0)
        create_square(xc2+2, yc+1, "□", 0)
    else:
        if M2 != "□" and M2 != "C":
            chest_allyH(xc, yc, M2)
        else:
            chest_allyH(xc, yc, M1)

def chestroomV(xc, yc, M1, M2, gen):
    if gen == 2:
        yc2 = yc-5
        if (xc/5, yc2/5) in zip(Lx, Ly):
            able = False
        else:
            able = True
            Lx.append(xc/5)
            Ly.append(yc2/5)
    if gen == 3:
        yc2 = yc+5
        if (xc/5, yc2/5) in zip(Lx, Ly):
            able = False
        else:
            Lx.append(xc/5)
            Ly.append(yc2/5)
            able = True
            save = yc
            yc = yc2
            yc2 = save
    if able == True:
        create_square(xc, yc, M1, 0)
        create_mon(M1)
        create_square(xc-1, yc, M2, 0)
        create_mon(M2)
        create_square(xc+1, yc, M2, 0)
        create_mon(M2)
        create_square(xc, yc-1, "□", 0)
        create_square(xc, yc+1, "□", 0)
        create_square(xc, yc+2, "□", 3)
        create_square(xc, yc-2, "□", 0)
        create_square(xc-1, yc-1, "□", 0)
        create_square(xc-1, yc+1, "□", 0)
        create_square(xc+1, yc-1, "□", 0)
        create_square(xc+1, yc+1, "□", 0)
        create_square(xc-1, yc-2, "C", 0)
        create_square(xc+1, yc-2, "□", 0)
        create_square(xc, yc2, M1, 0)
        create_mon(M1)
        create_square(xc-1, yc2, M2, 0)
        create_mon(M2)
        create_square(xc+1, yc2, M2, 0)
        create_mon(M2)
        create_square(xc, yc2-1, "□", 0)
        create_square(xc, yc2+1, "□", 0)
        create_square(xc, yc2+2, "□", 0)
        create_square(xc, yc2-2, "□", 2)
        create_square(xc-1, yc2-1, "□", 0)
        create_square(xc-1, yc2+1, "□", 0)
        create_square(xc+1, yc2-1, "□", 0)
        create_square(xc+1, yc2+1, "□", 0)
        create_square(xc-1, yc2+2, "C", 0)
        create_square(xc+1, yc2+2, "□", 0)
    else:
        if M2 != "□" and M2 != "C":
            chest_allyV(xc, yc, M2)
        else:
            chest_allyV(xc, yc, M1)

def gen(gen):
    map.genID[map.id.index("x")] = 0
    xnow = map.x[map.id.index("x")]
    ynow = map.y[map.id.index("x")]
    room = random.randint(1,6)
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
            if room == 1:
                emptyT(xcentre,ycentre)
            elif room == 2:
                chest_allyH(xcentre, ycentre, "K")
            elif room == 3:
                central(xcentre, ycentre, "□", "S", "S")
            elif room == 4:
                central(xcentre, ycentre, "□", "□", "K")
            elif room == 5:
                chest_allyH(xcentre, ycentre, "□")
            elif room == 6:
                central(xcentre, ycentre, "C", "S", "K")
        elif map.lvl == 2:
            if room == 1:
                chestroomH(xcentre, ycentre, "□", "F", gen)
            elif room == 2:
                emptyT(xcentre,ycentre)
            elif room == 3:
                central(xcentre, ycentre, "C", "K", "L")
            elif room == 4:
                central(xcentre, ycentre, "L", "□", "□")
            elif room == 5:
                chest_allyH(xcentre, ycentre, "L")
            elif room == 6:
                central(xcentre, ycentre, "F", "□", "□")
        elif map.lvl == 3:
            if room == 1:
                chestroomH(xcentre, ycentre, "F", "F", gen)
            if room == 2:
                central(xcentre, ycentre, "T", "□", "□")
            if room == 3:
                central(xcentre, ycentre, "□", "O", "□")
            if room == 4:
                emptyT(xcentre, ycentre)
            if room == 5:
                chest_allyH(xcentre, ycentre, "T")
            if room == 6:
                central(xcentre, ycentre, "□", "O", "O")
        elif map.lvl >= 4:
            if room == 1:
                emptyT(xcentre, ycentre)
            if room == 2:
                chest_allyH(xcentre, ycentre, "G")
            if room == 3:
                chestroomH(xcentre, ycentre, "□", "G", gen)
            if room == 4:
                central(xcentre, ycentre, "Ø", "O", "□")
            if room == 5:
                central(xcentre, ycentre, "□", "T", "□")
            if room == 6:
                central(xcentre, ycentre, "O", "O", "O")
    if gen == 2 or gen == 3:
        if map.lvl == 1:
            if room == 1:
                emptyT(xcentre,ycentre)
            elif room == 2:
                chest_allyV(xcentre, ycentre, "K")
            elif room == 3:
                central(xcentre, ycentre, "□", "S", "S")
            elif room == 4:
                central(xcentre, ycentre, "□", "□", "K")
            elif room == 5:
                chest_allyV(xcentre, ycentre, "□")
            elif room == 6:
                central(xcentre, ycentre, "C", "S", "K")
        elif map.lvl == 2:
            if room == 1:
                chestroomV(xcentre, ycentre, "□", "F", gen)
            elif room == 2:
                emptyT(xcentre,ycentre)
            elif room == 3:
                central(xcentre, ycentre, "C", "K", "L")
            elif room == 4:
                central(xcentre, ycentre, "L", "□", "□")
            elif room == 5:
                chest_allyV(xcentre, ycentre, "L")
            elif room == 6:
                central(xcentre, ycentre, "F", "□", "□")
        elif map.lvl == 3:
            if room == 1:
                chestroomV(xcentre, ycentre, "F", "F", gen)
            if room == 2:
                central(xcentre, ycentre, "T", "□", "□")
            if room == 3:
                central(xcentre, ycentre, "□", "O", "□")
            if room == 4:
                emptyT(xcentre, ycentre)
            if room == 5:
                chest_allyV(xcentre, ycentre, "T")
            if room == 6:
                central(xcentre, ycentre, "□", "O", "O")
        elif map.lvl >= 4:
            if room == 1:
                emptyT(xcentre, ycentre)
            if room == 2:
                chest_allyH(xcentre, ycentre, "G")
            if room == 3:
                chestroomH(xcentre, ycentre, "□", "G", gen)
            if room == 4:
                central(xcentre, ycentre, "Ø", "O", "□")
            if room == 5:
                central(xcentre, ycentre, "□", "T", "□")
            if room == 6:
                central(xcentre, ycentre, "O", "O", "O")