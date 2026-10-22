a = int(input())
b = int(input())
count = 0
rest = a
while rest >= b:
    rest -= b
    count += 1
print(count)