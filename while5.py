n = int(input())
k = 0
rest = n
while rest > 1:
    rest //= 2
    k += 1
print(k)