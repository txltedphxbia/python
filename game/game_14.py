# ==============================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ»
# Автор: Хакимов Александр
# Дата: ноябрь 2026
#
# Этап 14 — цветной вывод.
# ==============================================
import random

import dungeon_v14 as dungeon

try:
    from colorama import Fore, Style, init
    init()
    COLOR = True
except ImportError:
    COLOR = False

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


num_to_verb = {"1": "look", "2": "go", "3": "rest", "4": "listen",
               "5": "torch", "6": "train", "7": "descend", "8": "leaders",
               "9": "shop", "10": "backpack", "11": "drink", "0": "exit"}

commands = ["look", "go [north|south|west|east]", "rest", "listen", "torch", "train", "descend",
            "leaders", "shop", "backpack", "drink potion",
            "buy <item> [count]", "map", "scout", "exit"]

MENU = ["What do you do? (number or command; help for help)",
        "1 - look around (look)",
        "2 - go forward (go)",
        "3 - rest (rest)",
        "4 - listen (listen)",
        "5 - light a torch (torch)",
        "6 - train (train)",
        "7 - descend deeper (descend)",
        "8 - leaderboard (leaders)",
        "9 - shop (shop)",
        "10 - backpack (backpack)",
        "11 - drink potion (drink)",
        "0 - exit the dungeon (exit)"]

MAP = [
    ["#", "#", "#", "#", "#"],
    ["#", ".", ".", "#", "#"],
    ["#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", "#", "S", ".", "#"],
]
DIRECTIONS = {"north": (-1, 0), "south": (1, 0), "west": (0, -1), "east": (0, 1)}
LOOT = {(1, 1): "old coin", (2, 3): "dusty potion", (3, 3): "guard's gem"}
hero_r, hero_c = 4, 2
visited = {(4, 2)}
found_loot = set()


def scout(r, c, seen):
    """Рекурсивно считает комнаты, достижимые из клетки (r, c).
    Границы карты проверяются явно: нижняя стена открыта.
    """
    if not (0 <= r < len(MAP) and 0 <= c < len(MAP[r])):
        return 0
    if (r, c) in seen or MAP[r][c] == "#":
        return 0
    seen.add((r, c))
    total = 1
    for dr, dc in DIRECTIONS.values():
        total += scout(r + dr, c + dc, seen)
    return total


def paint(text, color_name):
    """Красит строку, если colorama доступна; иначе возвращает как есть."""
    if not COLOR:
        return text
    return getattr(Fore, color_name) + text + Style.RESET_ALL


# --- Main loop ------------------------------------
running = True
outcome = "interrupted"
try:
    while running:
        print("\n".join(MENU))
        print()

        line = input()
        while line.strip() == "":
            print("Empty command. Type a command or number.")
            line = input()
        cmd = line.strip().lower()
        words = cmd.split()
        verb = words[0]
        if cmd in num_to_verb:
            verb = num_to_verb[cmd]

        match verb:
            case "look":
                print("You look around. The room is empty, only dust on the floor.")

            case "go":
                if len(words) > 1 and words[1] in DIRECTIONS:
                    dr, dc = DIRECTIONS[words[1]]
                    nr, nc = hero_r + dr, hero_c + dc
                    if 0 <= nr < len(MAP) and 0 <= nc < len(MAP[nr]) and MAP[nr][nc] != "#":
                        hero_r, hero_c = nr, nc
                        visited.add((hero_r, hero_c))
                        if (hero_r, hero_c) in LOOT:
                            found = LOOT[(hero_r, hero_c)]
                            if found not in found_loot:
                                found_loot.add(found)
                                print(f"You found {found}! Unique loot: {len(found_loot)}.")
                        print(f"You step {words[1]}. Room ({hero_r}, {hero_c}).")
                    else:
                        print(f"Cannot go {words[1]}: wall or edge.")
                elif len(words) > 1:
                    print(f"Unknown direction: '{words[1]}'. Use north, south, west or east.")
                    continue
                else:
                    cost = 2
                    if stamina >= cost:
                        stamina -= cost
                        print("You go forward carefully. The floor creaks under your feet.")
                    else:
                        health -= cost - stamina
                        stamina = 0
                        print("No strength left — you go on sheer will.")

            case "rest":
                stamina = min(stamina + 1, max_stamina)
                print("You sit down and catch your breath. Strength returns.")

            case "listen":
                print("You freeze and listen. Somewhere deep, water drips into the well.")

            case "torch":
                stamina = max(stamina - 1, 0)
                print("You light a torch. Shadows retreat from the walls.")

            case "train":
                strikes = 6
                total_damage = 0.0
                crit_count = 0
                print("You approach the training dummy.")
                print("It has stood here since the last seeker came.")
                print()
                print(f"Delivering {strikes} strikes.")
                for i in range(1, strikes + 1):
                    hit_damage, crit = dungeon.hero_hit(i, damage, crit_damage)
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

            case "descend":
                if not enemies:
                    print("You descend the stairs. But the dungeon is empty.")
                else:
                    enemy = random.choice(enemies)
                    rounds, won, health, loot = dungeon.fight(enemy, health, ability_bonus, damage, crit_damage)
                    for r in rounds:
                        log.append(r)
                    if won:
                        gold_total += loot
                        enemies.remove(enemy)
                        print(paint(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon. Loot: {loot} gold.", "YELLOW"))
                    print(f"Battle: {len(rounds)} rounds.")

            case "leaders":
                print_leaderboard(log)

            case "shop":
                print("Shop:")
                for name, price in dungeon.prices.items():
                    print(f"{name}: {price} gold")
                print("Buy with: buy <item> [count]")

            case "buy":
                if len(words) > 2 and words[-1].isdigit():
                    qty = int(words[-1])
                    item = "_".join(words[1:-1])
                else:
                    qty = 1
                    item = "_".join(words[1:])
                if item == "":
                    print("Buy what? Type: buy <item>.")
                    continue
                if item not in dungeon.prices:
                    print("No such item in the shop.")
                    continue
                if qty < 1:
                    print("Quantity must be at least 1.")
                    continue
                unit = dungeon.prices[item]
                gold_total, ok = dungeon.buy(unit, gold_total, quantity=qty)
                if ok:
                    inventory[item] = inventory.get(item, 0) + qty
                    print(f"Bought {qty} {item} for {unit * qty} gold. Gold left: {gold_total}.")
                else:
                    print(f"Not enough gold: need {unit * qty}, have {gold_total}.")

            case "backpack":
                if not inventory:
                    print("Backpack is empty.")
                else:
                    print("Backpack:")
                    for name, qty in inventory.items():
                        print(f"{name}: {qty} pcs")

            case "drink" | "use":
                item = "_".join(words[1:]) or "potion"
                if inventory.get(item, 0) == 0:
                    print(f"No {item} in the backpack.")
                else:
                    if item == "potion":
                        health = min(health + 10, max_health)
                        effect = f"Health: {health}."
                    elif item == "torch_oil":
                        stamina = min(stamina + 5, max_stamina)
                        effect = f"Stamina: {stamina}."
                    else:
                        ability_bonus += 2
                        effect = f"Damage bonus: +{ability_bonus}."
                    inventory[item] -= 1
                    if inventory[item] == 0:
                        del inventory[item]
                    print(f"You use {item}. {effect} Left: {inventory.get(item, 0)}.")

            case "help":
                print("Commands: " + ", ".join(commands) + ".")
                print("Numbers 0-11 work as before.")

            case "map":
                print("Map:")
                for i in range(len(MAP)):
                    cells = []
                    for j in range(len(MAP[i])):
                        cell = "@" if (i, j) == (hero_r, hero_c) else MAP[i][j]
                        cells.append(cell)
                    print(" ".join(cells))

            case "scout":
                print(f"Scout: {scout(hero_r, hero_c, set())} rooms reachable.")

            case "exit":
                print("You climb back toward the light. The dungeon stays behind.")
                outcome = "exit"
                running = False

            case _:
                print(f"Don't understand command: '{line.strip()}'. Type 'help'.")
                continue

        if running:
            actions += 1
            print()
            state = f"Health: {health} Stamina: {stamina} Enemies left: {len(enemies)} Gold: {gold_total}"
            print(paint(state, "GREEN"))

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
