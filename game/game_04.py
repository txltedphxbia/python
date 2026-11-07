# ==============================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ»
# Автор: Хакимов Александр
# Дата: октябрь 2026
#
# Этап 4 — тренировочный бой: цикл ударов, криты, статистика.
# ==============================================

# --- Заголовок ------------------------------------
title = "ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ"
frame = "=" * 31
print(frame)
print("   " + title + "   ")
print(frame)
print()

# --- Знакомство с героем --------------------------
print("Как зовут героя?")
hero_name = input()
print(f"Добро пожаловать, {hero_name}!")
print("Ты входишь в подземелье. Здесь темно и пахнет сыростью.")
print()

# --- Настройка героя -------------------------------
print("Настройка героя.")
print("Здоровье, сила, ловкость, выносливость — по одному числу в строке:")
health = int(input())
strength = int(input())
agility = int(input())
endurance = int(input())

# --- Расчёт урона ----------------------------------
base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = health // 10 + endurance
max_stamina = stamina

# --- Формуляр героя --------------------------------
print("Характеристики героя:")
print(f"Здоровье:     {health}")
print(f"Сила:         {strength}")
print(f"Ловкость:     {agility}")
print(f"Выносливость: {endurance}")
print()
print(f"Урон героя: {damage:.1f}")
print(f"Критический урон: {crit_damage:.1f}")
print(f"Запас сил: {stamina}")
print()

# --- Меню действий ---------------------------------
print("Что делаешь?")
print("1 - осмотреться")
print("2 - идти вперёд")
print("3 - отдохнуть")
print("4 - прислушаться")
print("5 - зажечь факел")
print("6 - тренировка")
print()

# --- Выбор действия --------------------------------
choice = input()
match choice:
    case "1":
        print("Вы осмотрелись. Комната пуста, только пыль на полу.")

    case "2":
        stamina = max(stamina - 2, 0)
        print("Вы осторожно идёте вперёд. Пол скрипит под ногами.")

    case "3":
        stamina = min(stamina + 1, max_stamina)
        print("Вы садитесь на пол и переводите дух. Силы возвращаются.")

    case "4":
        print("Вы замираете и слушаете. Где-то в глубине капает вода.")

    case "5":
        stamina = max(stamina - 1, 0)
        print("Вы зажигаете факел. Тени отступают от стен.")

    case "6":
        strikes = 6
        total_damage = 0.0
        crit_count = 0
        print("Вы подходите к тренировочному чучелу.")
        print("Оно стоит здесь с тех пор, как сюда приходил последний искатель.")
        print()
        print(f"Наносите {strikes} ударов.")
        for i in range(1, strikes + 1):
            if i % 3 == 0:
                hit_damage = crit_damage
                crit_count += 1
                print(f"Удар {i}: {hit_damage:.1f} — критический!")
            else:
                hit_damage = damage
                print(f"Удар {i}: {hit_damage:.1f}")
            total_damage += hit_damage
        print()
        print(f"Итог: {strikes} ударов, критических: {crit_count}.")
        print(f"Общий урон: {total_damage:.1f}")
        print(f"Средний урон: {total_damage / strikes:.1f}")
        stamina = max(stamina - 3, 0)

    case _:
        print("Такого действия нет.")

print()
print(f"Здоровье: {health} Запас сил: {stamina}")

# --- Прощание --------------------------------------
print()
print(frame)
print(f"Удачи, {hero_name}!")
print(frame)
