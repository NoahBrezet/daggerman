import random

a = ["-","-","-"]
b = ["-","-","-"]
c = ["-","-","-"]

def showboard():
    print("  a b c")
    print("1", a[0], b[0], c[0])
    print("2", a[1], b[1], c[1])
    print("3", a[2], b[2], c[2])
    print()

def checkvertical(column):
    if column.count("x") == 3:
        return 2
    if column.count("o") == 3:
        return 3

def checkwin():
    #horizontal
    for i in range(3):
        if a[i] == b[i] == c[i] == "x":
            return 2
        if a[i] == b[i] == c[i] == "o":
            return 3
    #vertical
    for column in (a, b, c):
        result = checkvertical(column)
        if result:
            return result
    #diagonal
    if a[0] == b[1] == c[2] == "x":
        return 2
    if a[0] == b[1] == c[2] == "o":
        return 3
    if a[2] == b[1] == c[0] == "x":
        return 2  
    if a[2] == b[1] == c[0] == "o":
        return 3
    return 0

def almost3(player):
    for i in range(3):
        #vertical
        if a.count(player) == 2 and a.count("-") == 1:
            return ("a", a.index("-"))
        if b.count(player) == 2 and b.count("-") == 1:
            return ("b", b.index("-"))
        if c.count(player) == 2 and c.count("-") == 1:
            return ("c", c.index("-"))
        #horizontal
        if a[i] == b[i] == player and c[i] == "-":
            return ("c", i)
        if a[i] == c[i] == player and b[i] == "-":
            return ("b", i)
        if b[i] == c[i] == player and a[i] == "-":
            return ("a", i)
    #diagonal
    if a[0] == b[1] == player and c[2] == "-":
        return ("c", 2)
    if a[0] == c[2] == player and b[1] == "-":
        return ("b", 1)
    if b[1] == c[2] == player and a[0] == "-":
        return ("a", 0)
    if a[2] == b[1] == player and c[0] == "-":
        return ("c", 0)
    if a[2] == c[0] == player and b[1] == "-":
        return ("b", 1)
    if b[1] == c[0] == player and a[2] == "-":
        return ("a", 2)
    return None

def checkfull():
    for i in range(3):
        if a[i] == "-" or b[i] == "-" or c[i] == "-":
            return False
    return True

win = 0
while win == 0:
    done = 0
    showboard()
    while done == 0:
        print("Name a colunm.")
        column = input()
        print("Name a row.")
        try:
            row = int(input()) - 1   # van "1..3" naar index 0..2
        except ValueError:
            print("Enter a number from 1 to 3.")
            continue
        if column == "a":
            if a[row] == "-":
                a[row] = "x"
                done = 1
        elif column == "b":
            if b[row] == "-":
                b[row] = "x"
                done = 1
        elif column == "c":
            if c[row] == "-":
                c[row] = "x"
                done = 1
        elif column == "no":
            done = 1
        if done == 0:
            print ("Error, try again.")
    win = checkwin()
    if win != 0:
        continue
    if checkfull(): 
        win = 1
        win = checkwin()
        continue
    if almost3("o") is not None:
        col, i = almost3("o")
        if col == "a":
            a[i] = "o"
        elif col == "b":
            b[i] = "o"
        else:
            c[i] = "o"
    elif almost3("x") is not None:
        col, i = almost3("x")
        if col == "a":
            a[i] = "o"
        elif col == "b":
            b[i] = "o"
        else:
            c[i] = "o"
    else:
        empties = []
        for i in range(3):
            if a[i] == "-":
                empties.append(("a", i))
            if b[i] == "-":
                empties.append(("b", i))
            if c[i] == "-":
                empties.append(("c", i))
        if empties:
            col, i = random.choice(empties)
            if col == "a":
                a[i] = "o"
            elif col == "b":
                b[i] = "o"
            else:
                c[i] = "o"
    win = checkwin()
    if checkfull(): 
        win == 1
        win = checkwin()

showboard()

if win == 1:
    print ("It is a draw.")
elif win == 2:
    print ("You win.")
else:
    print ("You lose.")
