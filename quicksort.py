import random

def quicksort(array):
    if len(array) <= 1:
        return array
    else:
        pivot = array[0]
        lesser =[]
        greater = []
        for x in array[1:]:
            if x <= pivot:
                lesser.append(x)
            else:
                greater.append(x)
        return quicksort(lesser) + [pivot] + quicksort(greater)

print("Hoeveel random getallen wil je sorteren?")
aantal = int(input())
if aantal <= 0:
    print("Voer een positief getal in.")
    exit()
elif aantal > 998:
    print("Voer een getal in dat kleiner is dan 999.")
    exit()
print("Wat is de maximum waarde van de getallen?")
max_waarde = int(input())
if max_waarde <= 1:
    print("Voer een getal in dat groter is dan 1.")
    exit()

getallen = []
for i in range(aantal):
    getallen.append(random.randint(1, max_waarde))

getallen = quicksort(getallen)
print("De gesorteerde getallen zijn:")
print(getallen)
