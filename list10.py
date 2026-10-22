n = int(input())
a = []
for i in range(n):
    a.append(input())
imax = 0
imin = 0
for i in range(len(a)):
    if len(a[i]) > len(a[imax]):
        imax = i
    if len(a[i]) < len(a[imin]):
        imin = i
print(a[imax])
print(len(a[imax]))
print(a[imin])
print(len(a[imin]))