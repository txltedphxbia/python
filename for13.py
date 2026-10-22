n = int(input())

total = 0.0
for k in range(1, n + 1):
    term = (10 + k) / 10
    if k % 2 == 1:
        total += term
    else:
        total -= term

print(total)