# ==============================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ»
# Автор: Хакимов Алексаднр
# Дата: ноябрь 2026
#
# Этап 11 — словари: цены, рюкзак, карточки врагов.
# ==============================================
import random

# --- Title ----------------------------------------
title = "DUNGEON: THE SILENT WELL"
frame = "=" * 30
print(frame)
print("   " + title + "   ")
print(frame)
print()

# --- Meeting the hero -----------------------------
print("What is the hero's name?")
hero_name = input()
print(f"Welcome, {hero_name}!")
print("You enter the dungeon. Dark and damp-smelling.")
print()

# --- Hero setup -----------------------------------
print("Hero setup.")
print("Health, strength, agility, endurance — one number per line:")
while True:
    try:
        health = int(input())
        strength = int(input())
        agility = int(input())
        endurance = int(input())
        if not 10 <= health <= 1000:
            raise ValueError(f"Health must be between 10 and 1000, got {health}")
        if not 1 <= strength <= 50:
            raise ValueError(f"Strength must be between 1 and 50, got {strength}")
        if not (0 <= agility <= 50 and 0 <= endurance <= 50):
            raise ValueError("Agility and endurance must be between 0 and 50")
        break
    except ValueError as e:
        if str(e).startswith("invalid literal"):
            print("Oops: one of the lines is not a number. Enter all four again:")
        else:
            print(f"{e}. Enter all four again:")

# --- Damage calculation ---------------------------
base_attack = 10
damage = base_attack + strength * 1.5
crit_damage = damage * 2
stamina = health // 10 + endurance
max_health = health
max_stamina = stamina

# --- Hero sheet -----------------------------------
print("Hero characteristics:")
print(f"Health:    {health}")
print(f"Strength:  {strength}")
print(f"Agility:   {agility}")
print(f"Endurance: {endurance}")
print()
print(f"Hero damage: {damage:.1f}")
print(f"Critical damage: {crit_damage:.1f}")
print(f"Stamina reserve: {stamina}")
print()

# --- Enemies and log ------------------------------
enemies = ["skeleton", "ghoul", "spider", "bat"]
log = []
actions = 0
inventory = {}
gold_total = 0
ability_bonus = 0

# --- Функции --------------------------------------
prices = {"potion": 10, "torch_oil": 15, "war_elixir": 40}

enemy_stats = {
    "skeleton": {"hp": 45, "damage": 6, "loot": 25},
    "ghoul": {"hp": 30, "damage": 4, "loot": 15},
    "spider": {"hp": 20, "damage": 3, "loot": 10},
    "bat": {"hp": 12, "damage": 2, "loot": 5},
}


def hero_hit(strike_n):
    """Урон героя в удар номер strike_n.
    Возвращает пару (hit, crit): урон и признак критического удара.
    Читает глобальные damage и crit_damage, ничего не меняет.
    """
    if strike_n % 3 == 0:
        return crit_damage, True
    return damage, False


def fight(enemy, hero_health, bonus=0):
    """Бой с enemy до гибели одного из двоих.
    bonus — плоская надбавка к урону героя (после крита), по умолчанию 0.
    Карточка врага берётся из enemy_stats по имени: ключи hp, damage, loot.
    Печатает строки раундов. Глобальные переменные не меняет.
    Возвращает (rounds, won, hero_health, loot): таблицу раундов, признак
    победы, здоровье героя после боя и трофеи (0 при поражении).
    """
    stats = enemy_stats[enemy]
    enemy_hp = float(stats["hp"])
    rounds = []
    round_n = 0
    print(f"You descend the stairs. A {enemy} emerges from the darkness!")
    while enemy_hp > 0 and hero_health > 0:
        round_n += 1
        hit, crit = hero_hit(round_n)
        hit = hit + bonus
        enemy_hp -= hit
        line = f"Round {round_n}: hero deals {hit:.1f}"
        line += " — critical!" if crit else "."
        if enemy_hp <= 0:
            line += " Enemy falls."
            rounds.append([round_n, hit, 0])
        else:
            blow = stats["damage"]
            hero_health -= blow
            line += f" {enemy.capitalize()} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow}."
            rounds.append([round_n, hit, blow])
        print(line)
    won = enemy_hp <= 0
    loot = stats["loot"] if won else 0
    return rounds, won, hero_health, loot


def buy(price, gold, quantity=1):
    """Покупает quantity штук товара ценой price за золото gold.
    quantity по умолчанию 1. Возвращает (gold_left, ok): остаток золота
    и признак успешной покупки. Ничего не печатает.
    """
    cost = price * quantity
    if gold >= cost:
        return gold - cost, True
    return gold, False


def print_leaderboard(rounds_log):
    """Печатает топ-3 раундов по урону героя и рекорд врага.
    Возвращает None: контракт функции — печать, а не данные.
    """
    if not rounds_log:
        print("You haven't fought yet.")
        return
    top = sorted(rounds_log, key=lambda r: r[1], reverse=True)[:3]
    print("Leaderboard (hero damage):")
    for i in range(len(top)):
        print(f"{i + 1}. Round {top[i][0]}: {top[i][1]:.1f}")
    worst = max(rounds_log, key=lambda r: r[2])
    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")


def print_run_summary(rounds_log):
    """Печатает суммарный и средний урон забега. Возвращает None.
    Безопасна на пустом журнале.
    """
    total = sum(r[1] for r in rounds_log)
    rounds = len(rounds_log)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("No battles this run.")


# --- Main loop ------------------------------------
menu_last = 11
running = True
outcome = "interrupted"
try:
    while running:
        print("What do you do?")
        print("1 - look around")
        print("2 - go forward")
        print("3 - rest")
        print("4 - listen")
        print("5 - light a torch")
        print("6 - train")
        print("7 - descend deeper")
        print("8 - leaderboard")
        print("9 - shop")
        print("10 - backpack")
        print("11 - drink potion")
        print("0 - exit the dungeon")
        print()

        while True:
            choice = input()
            try:
                menu_number = int(choice)
            except ValueError:
                print("No such option. Enter a menu number.")
                continue
            if 0 <= menu_number <= menu_last:
                choice = str(menu_number)
                break
            print("No such option. Enter a menu number.")

        match choice:
            case "1":
                print("You look around. The room is empty, only dust on the floor.")

            case "2":
                cost = 2
                if stamina >= cost:
                    stamina -= cost
                    print("You go forward carefully. The floor creaks under your feet.")
                else:
                    health -= cost - stamina
                    stamina = 0
                    print("No strength left — you go on sheer will.")

            case "3":
                stamina = min(stamina + 1, max_stamina)
                print("You sit down and catch your breath. Strength returns.")

            case "4":
                print("You freeze and listen. Somewhere deep, water drips into the well.")

            case "5":
                stamina = max(stamina - 1, 0)
                print("You light a torch. Shadows retreat from the walls.")

            case "6":
                strikes = 6
                total_damage = 0.0
                crit_count = 0
                print("You approach the training dummy.")
                print("It has stood here since the last seeker came.")
                print()
                print(f"Delivering {strikes} strikes.")
                for i in range(1, strikes + 1):
                    hit_damage, crit = hero_hit(i)
                    if crit:
                        crit_count += 1
                        print(f"Strike {i}: {hit_damage:.1f} — critical!")
                    else:
                        print(f"Strike {i}: {hit_damage:.1f}")
                    total_damage += hit_damage
                print()
                print(f"Result: {strikes} strikes, critical: {crit_count}.")
                print(f"Total damage: {total_damage:.1f}")
                print(f"Average damage: {total_damage / strikes:.1f}")
                stamina = max(stamina - 3, 0)

            case "7":
                if not enemies:
                    print("You descend the stairs. But the dungeon is empty.")
                else:
                    enemy = random.choice(enemies)
                    rounds, won, health, loot = fight(enemy, health, bonus=ability_bonus)
                    for r in rounds:
                        log.append(r)
                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon. Loot: {loot} gold.")
                    print(f"Battle: {len(rounds)} rounds.")

            case "8":
                print_leaderboard(log)

            case "9":
                print("Shop:")
                for name, price in prices.items():
                    print(f"{name}: {price} gold")
                print("Item name (empty line — not buying):")
                name = input().strip().lower()
                if name != "":
                    if name in prices:
                        price = prices[name]
                        print("Quantity (Enter for one):")
                        qty_line = input()
                        if qty_line == "":
                            qty = 1
                        elif qty_line.isdigit() and int(qty_line) >= 1:
                            qty = int(qty_line)
                        else:
                            qty = 0
                        if qty == 0:
                            print("Quantity must be a positive whole number.")
                        else:
                            if qty_line == "":
                                gold_total, ok = buy(price, gold_total)
                            else:
                                gold_total, ok = buy(price, gold_total, quantity=qty)
                            if ok:
                                if name == "potion":
                                    inventory[name] = inventory.get(name, 0) + qty
                                elif name == "torch_oil":
                                    stamina = min(stamina + 5 * qty, max_stamina)
                                else:
                                    ability_bonus += 2 * qty
                                print(f"Bought {qty} {name} for {price * qty} gold. Gold left: {gold_total}.")
                            else:
                                print(f"Not enough gold: need {price * qty}, have {gold_total}.")
                    else:
                        print("No such item in the shop.")

            case "10":
                if not inventory:
                    print("Backpack is empty.")
                else:
                    print("Backpack:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} pcs")

            case "11":
                if inventory.get("potion", 0) == 0:
                    print("No potions in the backpack.")
                else:
                    health = min(health + 10, max_health)
                    inventory["potion"] -= 1
                    if inventory["potion"] == 0:
                        del inventory["potion"]
                    print(f"You drink a potion. Health: {health}. Potions left: {inventory.get('potion', 0)}.")

            case "0":
                print("You climb back toward the light. The dungeon stays behind.")
                outcome = "exit"
                running = False

        if running:
            actions += 1
            print()
            print(f"Health: {health} Stamina: {stamina} Enemies left: {len(enemies)} Gold: {gold_total}")

        if health <= 0:
            print(f"{hero_name} collapses. The dungeon claims another seeker.")
            outcome = "death"
            running = False

except (KeyboardInterrupt, EOFError):
    print()
    print("The player ended the session.")

finally:
    if inventory:
        print("Left behind in the backpack:")
        for name, qty in inventory.items():
            print(f"{name}: {qty} pcs")
    else:
        print("Left behind in the backpack: nothing.")
    print(frame)
    if outcome == "death":
        print(f"You did not make it, {hero_name}. Actions: {actions}.")
    elif outcome == "exit":
        print(f"Run over, {hero_name}. Actions: {actions}.")
    else:
        print(f"Session interrupted, {hero_name}. Actions: {actions}.")
    print_run_summary(log)
    print(frame)
