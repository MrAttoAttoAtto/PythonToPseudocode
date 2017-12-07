x = 1
y = x == 1
for Index in range(int(1), int(4)+1):
    x = x + 1
    for Mindex in range(int(1), int(4)+1):
        x = x * 2

    print(x)

print(x,y)