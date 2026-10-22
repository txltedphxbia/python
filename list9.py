n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
s = 0
for x in a:
    s += x
avg = s / n
b = []
for x in a:
    if x > avg:
        b.append(x)
print(b)
print(len(b))