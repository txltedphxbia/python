n = int(input())

product = 1.0
for i in range(11, 11 + n):
    product *= i / 10

print(product)