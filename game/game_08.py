# ==============================================
# ИГРА «ПОДЗЕМЕЛЬЕ: ТИХИЙ КОЛОДЕЦ»
# Автор: Хакимов Алексаднр
# Дата: ноябрь 2026
#
# Этап 8 — журнал как таблица, лидерборд, итог забега.
# При равенстве рекорда врага берётся первый раунд.
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

# --- Main loop ------------------------------------
menu_last = 8
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
                    if i % 3 == 0:
                        hit_damage = crit_damage
                        crit_count += 1
                        print(f"Strike {i}: {hit_damage:.1f} — critical!")
                    else:
                        hit_damage = damage
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
                    enemy_hp = 45
                    round_n = 0
                    print(f"You descend the stairs. A {enemy} emerges from the darkness!")
                    while enemy_hp > 0 and health > 0:
                        round_n += 1
                        if round_n % 3 == 0:
                            hit = crit_damage
                            crit = True
                        else:
                            hit = damage
                            crit = False
                        enemy_hp -= hit
                        line = f"Round {round_n}: hero deals {hit:.1f}"
                        line += " — critical!" if crit else "."
                        if enemy_hp <= 0:
                            line += " Enemy falls."
                            log.append([round_n, hit, 0])
                        else:
                            blow = random.randint(2, 6)
                            health -= blow
                            line += f" {enemy.capitalize()} health: {enemy_hp:.1f}. {enemy.capitalize()} hits for {blow}."
                            log.append([round_n, hit, blow])
                        print(line)
                    if enemy_hp <= 0:
                        enemies.remove(enemy)
                        print(f"{enemy.capitalize()} defeated! {len(enemies)} enemies left in the dungeon.")
                    print(f"Battle: {round_n} rounds.")

            case "8":
                if not log:
                    print("You haven't fought yet.")
                else:
                    top = sorted(log, key=lambda r: r[1], reverse=True)[:3]
                    print("Leaderboard (hero damage):")
                    for i in range(len(top)):
                        print(f"{i + 1}. Round {top[i][0]}: {top[i][1]:.1f}")
                    worst = max(log, key=lambda r: r[2])
                    print(f"Strongest enemy hit: {worst[2]} (round {worst[0]}).")

            case "0":
                print("You climb back toward the light. The dungeon stays behind.")
                outcome = "exit"
                running = False

        if running:
            actions += 1
            print()
            print(f"Health: {health} Stamina: {stamina} Enemies left: {len(enemies)}")

        if health <= 0:
            print(f"{hero_name} collapses. The dungeon claims another seeker.")
            outcome = "death"
            running = False

except (KeyboardInterrupt, EOFError):
    print()
    print("The player ended the session.")

finally:
    print(frame)
    if outcome == "death":
        print(f"You did not make it, {hero_name}. Actions: {actions}.")
    elif outcome == "exit":
        print(f"Run over, {hero_name}. Actions: {actions}.")
    else:
        print(f"Session interrupted, {hero_name}. Actions: {actions}.")
    total = sum(r[1] for r in log)
    rounds = len(log)
    if rounds > 0:
        print(f"Damage: {total:.1f} across {rounds} rounds, average {total / rounds:.1f}.")
    else:
        print("No battles this run.")
    print(frame)
