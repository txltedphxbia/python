n = int(input())
a = []
for i in range(n):
    a.append(int(input()))
b = a[1::2]
print(b)
s = 0
for x in b:
    s += x
print(s)