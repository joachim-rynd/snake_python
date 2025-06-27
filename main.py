import os
import time
import random
import sys
import termios
import tty
import select


TROPHIES_FILE = "trophies.txt"
unlocked_trophies = []

def save_trophies():
    try:
        with open(TROPHIES_FILE, "w", encoding="utf-8") as f:
            for troph in unlocked_trophies:
                f.write(troph + "\n")
    except Exception as e:
        print(f"Erreur sauvegarde trophées: {e}")

def load_trophies():
    global unlocked_trophies
    if os.path.exists(TROPHIES_FILE):
        try:
            with open(TROPHIES_FILE, "r", encoding="utf-8") as f:
                unlocked_trophies = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Erreur chargement trophées: {e}")
            unlocked_trophies = []
    else:
        unlocked_trophies = []

def get_trophy(score):
    global unlocked_trophies
    msg = ""
    troph = None
    if score >= 50:
        msg = "C'est bon tu as fini le jeu tu as la médaille de diamant 💎"
        troph = "C'est bon tu as fini le jeu tu as la médaille de diamant 💎"
    elif score >= 40:
        msg = "Woaaaa tu es fort, tu as la médaille de platine ⚪"
        troph = "Woaaaa tu es fort, tu as la médaille de platine ⚪"
    elif score >= 30:
        msg = "Incroyable, tu as la médaille d'or 🥇"
        troph = "Incroyable, tu as la médaille d'or 🥇"
    elif score >= 20:
        msg = "C'est mieux, tu as la médaille d'argent 🥈"
        troph = "C'est mieux, tu as la médaille d'argent 🥈"
    elif score >= 10:
        msg = "Bien, tu as la médaille de bronze 🥉"
        troph = "Bien, tu as la médaille de bronze 🥉"
    else:
        # Cas <10, message spécial mais pas de trophée ajouté
        msg = "NUL, fais plus pour la médaille de bronze!"
        return msg

    # Ajouter trophée s'il n'est pas déjà dans la liste
    if troph and troph not in unlocked_trophies:
        unlocked_trophies.append(troph)

    return msg

WIDTH = 60
HEIGHT = 30
direction = (1, 0)
snake = [(5, 5), (4, 5), (3, 5)]
apple = (random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
gold_apple = None
gold_apple_timer = 0
score = 0

def clear_screen():
    os.system('clear')

def draw_board():
    clear_screen()
    for y in range(HEIGHT):
        line = ''
        for x in range(WIDTH):
            if (x, y) == snake[0]:
                line += 'O'  # Tête
            elif (x, y) in snake:
                line += 'o'  # Corps
            elif (x, y) == apple:
                line += '*'
            elif gold_apple and (x, y) == gold_apple:
                line += '+'
            elif x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1:
                line += '#'
            else:
                line += ' '
        print(line)
    print(f"Score: {score}")

def move_snake():
    global apple, gold_apple, gold_apple_timer, score
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    if (
        new_head in snake or
        new_head[0] == 0 or new_head[0] == WIDTH - 1 or
        new_head[1] == 0 or new_head[1] == HEIGHT - 1
    ):
        return False

    snake.insert(0, new_head)

    if new_head == apple:
        score += 1
        while True:
            apple = (random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
            if apple not in snake and (not gold_apple or apple != gold_apple):
                break
    elif gold_apple and new_head == gold_apple:
        score += 3
        gold_apple = None
        gold_apple_timer = 0
    else:
        snake.pop()

    # Gestion apparition gold_apple
    if not gold_apple:
        if random.random() < 0.02:  # 2% de chance par déplacement
            while True:
                pos = (random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
                if pos not in snake and pos != apple:
                    gold_apple = pos
                    gold_apple_timer = 200  # durée d'apparition (~50 cycles)
                    break
    else:
        gold_apple_timer -= 1
        if gold_apple_timer <= 0:
            gold_apple = None
            gold_apple_timer = 0

    return True

def key_pressed():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    return dr != []

def get_input():
    global direction
    if key_pressed():
        c1 = sys.stdin.read(1)
        if c1 == '\x1b':  # séquence d'échappement (flèches)
            c2 = sys.stdin.read(1)
            if c2 == '[':
                c3 = sys.stdin.read(1)
                if c3 == 'A' and direction != (0, 1):      # flèche HAUT
                    direction = (0, -1)
                elif c3 == 'B' and direction != (0, -1):  # flèche BAS
                    direction = (0, 1)
                elif c3 == 'D' and direction != (1, 0):   # flèche GAUCHE
                    direction = (-1, 0)
                elif c3 == 'C' and direction != (-1, 0):  # flèche DROITE
                    direction = (1, 0)
        else:
            key = c1.lower()
            if key == 'z' and direction != (0, 1):
                direction = (0, -1)
            elif key == 's' and direction != (0, -1):
                direction = (0, 1)
            elif key == 'q' and direction != (1, 0):
                direction = (-1, 0)
            elif key == 'd' and direction != (-1, 0):
                direction = (1, 0)

def show_trophies():
    clear_screen()
    print("=" * 40)
    print("=", " " * 9 + "TROPHÉES DÉBLOQUÉS", " " * 8, "=")
    print("=" * 40)
    if not unlocked_trophies:
        print("\nAucun trophée débloqué pour le moment.\n")
    else:
        # Affiche du meilleur au moins bon, y compris Platine
        order = ["C'est bon tu as fini le jeu tu as la médaille de diamant 💎", "Woaaaa tu es fort, tu as la médaille de platine ⚪", "Incroyable, tu as la médaille d'or 🥇", "C'est mieux, tu as la médaille d'argent 🥈", "Bien, tu as la médaille de bronze 🥉"]
        sorted_trophies = [t for t in order if t in unlocked_trophies]
        for troph in sorted_trophies:
            print(f" - {troph}")
            print("\nAppuie sur [B] pour retourner au menu...")
            while True:
                if key_pressed():
                    key = sys.stdin.read(1).lower()
                    if key == 'b':
                        break
    print(" ")
    print(" [B] : Pour retourner au menu.")
    sys.stdin.read(1)

def game_loop():
    global direction, snake, apple, score, gold_apple, gold_apple_timer
    direction = (1, 0)
    snake = [(5, 5), (4, 5), (3, 5)]
    apple = (random.randint(1, WIDTH - 2), random.randint(1, HEIGHT - 2))
    gold_apple = None
    gold_apple_timer = 0
    score = 0

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    try:
        while True:
            draw_board()
            get_input()
            if not move_snake():
                msg = get_trophy(score)
                if score < 10:
                    print("\n" + msg)
                    time.sleep(2.0)
                    print("\nAppuie sur une touche pour retourner au menu.")
                    sys.stdin.read(1)
                else:
                    print("\n" + msg)
                    time.sleep(2.0)
                    print("\nGame Over! Appuie sur une touche pour retourner au menu.")
                    sys.stdin.read(1)
                break
            if direction in [(0, -1), (0, 1)]:
                time.sleep(0.17)
            else:
                time.sleep(0.1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def menu():
    load_trophies()
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)

    try:
        while True:
            clear_screen()
            print("=" * 40)
            print("=", " " * 9 + "🐍  SNAKE GAME  🐍", " " * 8, "=")
            print("=" * 40)
            print()
            print(" Utilise les flèches ou ZQSD pour déplacer le serpent.")
            print(" Mange les pommes '*' pour grandir.")
            print(" Les pommes dorées'+' donne 3 points !")
            print()
            print(" [ESPACE] : Jouer")
            print(" [T]      : Voir trophées débloqués")
            print(" [B]      : Quitter")
            print()
            print("=" * 40)
            print("Appuie sur la touche correspondante...")

            if key_pressed():
                key = sys.stdin.read(1).lower()
                if key == ' ':
                    game_loop()
                elif key == 't':
                    show_trophies()
                    
                elif key == 'b':
                    save_trophies()
                    clear_screen()
                    print("Merci d’avoir joué ! Au revoir 👋")
                    break
            time.sleep(0.1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    menu()
