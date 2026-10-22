price = float(input())

for i in range(12, 21, 2):
    kg = i / 10
    print(f"{kg:.1f} кг: {price * kg:.2f}")