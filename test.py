import turtle
import time
import random
import os
import sys

# Charger le meilleur score depuis un fichier
if os.path.exists("meilleur_score.txt"):
    with open("meilleur_score.txt", "r") as file:
        meilleur_score = int(file.read())
else:
    meilleur_score = 0

# Charger compteur temps depuis fichier
if os.path.exists("compteur_temps.txt"):
    with open("compteur_temps.txt", "r") as f:
        compteur_temps = int(f.read())
else:
    compteur_temps = 0

# Variables de jeu
score_joueur = 0
temps_délai = 0.1
segments = []
jeu_en_cours = False
pause_active = False
fond_pause = None

# Apparition super nourriture
snake_great_food_visible = False
snake_great_food_timer = 0

# Augmention du serpent
segment = turtle.Turtle()
segment.speed(0)
segment.shape("square")
segment.color("blue")
segment.penup()
segment.hideturtle()



# Création de l'écran
wind = turtle.Screen()
wind.title("Snake Maze 🐍")
wind.bgcolor("dark green")
wind.setup(width=600, height=600)
wind.tracer(0)

# Affichage game over
def afficher_game_over():
    snake.hideturtle()
    snake_food.hideturtle()
    snake_great_food.hideturtle()
    for segment in segments:
        segment.hideturtle()
    wind.bgcolor("black")
    pen_game_over = turtle.Turtle()
    pen_game_over.hideturtle()
    pen_game_over.color("white")
    pen_game_over.penup()
    pen_game_over.goto(0, 0)
    pen_game_over.write("💀 GAME OVER 💀", align="center", font=("Arial", 28, "bold"))
    wind.update()
    time.sleep(2.5)
    pen_game_over.clear()
    wind.bgcolor("dark green")


# Créer le serpent
snake = turtle.Turtle()
snake.speed(0)
snake.shape("square")
snake.color("dark blue")
snake.penup()
snake.goto(0, 0)
snake.direction = "stop"

# Nourriture normale
snake_food = turtle.Turtle()
snake_food.shape("circle")
snake_food.color("red")
snake_food.penup()
snake_food.goto(0, 100)

# Super nourriture
snake_great_food = turtle.Turtle()
snake_great_food.shape("circle")
snake_great_food.color("yellow")
snake_great_food.penup()
snake_great_food.hideturtle()

# Score
pen_score = turtle.Turtle()
pen_score.speed(0)
pen_score.color("white")
pen_score.penup()
pen_score.hideturtle()
pen_score.goto(-280, 170)
pen_score.write(f"Score : {score_joueur}", align="left", font=("Arial", 18, "normal"))

# Meilleur score
pen_best = turtle.Turtle()
pen_best.speed(0)
pen_best.color("yellow")
pen_best.penup()
pen_best.hideturtle()
pen_best.goto(-280, 200)
pen_best.write(f"Meilleur Score : {meilleur_score}", align="left", font=("Arial", 18, "normal"))

# Titre principal
pen_title = turtle.Turtle()
pen_title.hideturtle()
pen_title.color("white")
pen_title.penup()
pen_title.goto(0, 250)
pen_title.write("🐍 SNAKE MAZE 🐍", align="center", font=("Arial", 28, "bold"))

# Écran de démarrage
pen_start = turtle.Turtle()
pen_start.hideturtle()
pen_start.color("white")
pen_start.penup()
pen_start.goto(0, -170)
pen_start.write("Appuie sur ESPACE pour démarrer\nAppuie sur B pour quitter", align="center", font=("Arial", 20, "bold"))

# Compteur temps
pen_timer = turtle.Turtle()
pen_timer.hideturtle()
pen_timer.color("yellow")
pen_timer.penup()
pen_timer.goto(0, -290)

# Bordures
pen_bordure = turtle.Turtle()
pen_bordure.hideturtle()
pen_bordure.color("white")
pen_bordure.pensize(4)
pen_bordure.penup()

# Texte pause
pen_pause = turtle.Turtle()
pen_pause.hideturtle()
pen_pause.color("white")
pen_pause.penup()

# Fond gris pause
def dessiner_fond_pause():
    fond = turtle.Turtle()
    fond.hideturtle()
    fond.color("gray")
    fond.penup()
    fond.goto(-300, 300)
    fond.begin_fill()
    for _ in range(2):
        fond.forward(600)
        fond.right(90)
        fond.forward(600)
        fond.right(90)
    fond.end_fill()
    return fond

# Fonction pause
def pause_jeu():
    global pause_active, jeu_en_cours, fond_pause
    if jeu_en_cours and not pause_active:
        pause_active = True
        fond_pause = dessiner_fond_pause()
        pen_pause.goto(0, 100)

        pen_pause.write("⏸️ PAUSE ⏸️\nESPACE : Reprendre\nB : Retour menu", align="center", font=("Arial", 20, "bold"))
        snake.hideturtle()
        snake_food.hideturtle()
        snake_great_food.hideturtle()

        # Cacher tous les segments du serpent
        for segment in segments:
            segment.hideturtle()

# Message félicitation
msg = turtle.Turtle()
msg.color("yellow")
msg.penup()

msg.hideturtle()





# Affichage compteur temps
def afficher_compteur_non_bloquant():
    global compteur_temps
    if jeu_en_cours and not pause_active:
        compteur_temps += 1
        with open("compteur_temps.txt", "w") as f:
            f.write(str(compteur_temps))

    pen_timer.clear()
    if not jeu_en_cours:
        heures = compteur_temps // 3600
        minutes = (compteur_temps % 3600) // 60
        secondes = compteur_temps % 60
        temps_format = f"Temps écoulé : {heures:02d}h {minutes:02d}m {secondes:02d}s"
        pen_timer.write(temps_format, align="center", font=("Arial", 16, "normal"))

    wind.ontimer(afficher_compteur_non_bloquant, 1000)


# Réinitialiser le jeu
def reset_jeu():
    global jeu_en_cours, score_joueur, temps_délai, snake_great_food_visible, snake_great_food_timer, fond_pause
    jeu_en_cours = False
    snake.goto(0, 0)
    
    snake.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    if score_joueur < 50 and score_joueur > 1:
        msg.write(f"Tu es nul, que {score_joueur} points", align="center", font=("Arial", 20, "normal"))
    if score_joueur <= 1:
        msg.write(f"Tu es nul, que {score_joueur} point", align="center", font=("Arial", 20, "normal"))
    if score_joueur >= 50 and score_joueur < 150:
        msg.write(f"C'est mieux tu as {score_joueur} points", align="center", font=("Arial", 20, "normal"))
    if score_joueur >= 150 and score_joueur < 250:
        msg.write(f"Pas mal,  tu as {score_joueur} points", align="center", font=("Arial", 20, "normal"))
    if score_joueur >= 250 and score_joueur < 350:
        msg.write(f"Trop fort ! tu as {score_joueur} points", align="center", font=("Arial", 20, "normal"))
    if score_joueur >= 350 and score_joueur < 500:
        msg.write(f"Incroyable tu as {score_joueur} points", align="center", font=("Arial", 20, "normal"))
    
    temps_délai = 0.1
    pen_bordure.clear()
    pen_score.clear()
    pen_best.clear()
    snake.hideturtle()
    snake_food.hideturtle()
    snake_great_food.hideturtle()
    snake_great_food_visible = False
    snake_great_food_timer = 0
    if fond_pause:
        fond_pause.clear()
    pen_pause.clear()
    pen_score.goto(-80, 80)
    pen_score.write(f"Score : {score_joueur}", align="left", font=("Arial", 25, "normal"))
    pen_best.goto(-180, 130)
    pen_best.write(f"Meilleur Score : {meilleur_score}", align="left", font=("Arial", 30, "normal"))
    pen_start.clear()
    pen_start.goto(0, -170)
    pen_start.write("Appuie sur ESPACE pour démarrer\nAppuie sur B pour quitter", align="center", font=("Arial", 20, "bold"))
    pen_title.clear()
    pen_title.goto(0, 250)
    pen_title.write("🐍 SNAKE MAZE 🐍", align="center", font=("Arial", 28, "bold"))
    score_joueur = 0

# Contrôles serpent
def go_up():
    if snake.direction != "down":
        snake.direction = "up"
def go_down():
    if snake.direction != "up":
        snake.direction = "down"
def go_left():
    if snake.direction != "right":
        snake.direction = "left"
def go_right():
    if snake.direction != "left":
        snake.direction = "right"
def move():
    if snake.direction == "up":
        snake.sety(snake.ycor() + 20)
    elif snake.direction == "down":
        snake.sety(snake.ycor() - 20)
    elif snake.direction == "left":
        snake.setx(snake.xcor() - 20)
    elif snake.direction == "right":
        snake.setx(snake.xcor() + 20)

# Démarrer
def demarrer_jeu():
    global jeu_en_cours, pause_active, fond_pause, snake_great_food_visible, snake_great_food_timer
    score_joueur = 0
    msg.clear()
    msg.hideturtle()

    if pause_active:
        pause_active = False
        pen_pause.clear()
        snake.showturtle()
        snake_food.showturtle()

        # Cacher la super nourriture apparue pendant la pause
        if snake_great_food_visible:
            snake_great_food.hideturtle()
            snake_great_food_visible = False
            snake_great_food_timer = 0

        for segment in segments:
            segment.showturtle()
        if fond_pause:
            fond_pause.clear()

    if not jeu_en_cours:
        pen_start.clear()
        pen_title.clear()
        pen_timer.clear()
        pen_score.clear()
        pen_best.clear()
        pen_score.goto(-250, 260)
        pen_score.write(f"Score : {score_joueur}", align="left", font=("Arial", 18, "normal"))
        pen_best.goto(-80, 260)
        pen_best.write(f"Meilleur Score : {meilleur_score}", align="left", font=("Arial", 18, "normal"))
        jeu_en_cours = True
        pen_bordure.goto(-295, 295)
        pen_bordure.pendown()
        for _ in range(4):
            pen_bordure.forward(580)
            pen_bordure.right(90)
        pen_bordure.penup()
        snake.showturtle()
        snake_food.showturtle()


# Quitter ou retour au menu
def quitter_jeu():
    global pause_active, fond_pause
    if pause_active:
        pause_active = False
        pen_pause.clear()
        if fond_pause:
            fond_pause.clear()
        reset_jeu()
    else:
        wind.bye()
        sys.exit()

# Contrôles clavier
wind.listen()
wind.onkeypress(go_up, "z")
wind.onkeypress(go_down, "s")
wind.onkeypress(go_left, "q")
wind.onkeypress(go_right, "d")
wind.onkeypress(demarrer_jeu, "space")
wind.onkeypress(quitter_jeu, "b")
wind.onkeypress(pause_jeu, "p")

# Lancer le compteur
afficher_compteur_non_bloquant()

# Boucle principale
try:
    while True:
        wind.update()
        if not jeu_en_cours or pause_active:
            continue

        # Collision mur
        if abs(snake.xcor()) > 275 or abs(snake.ycor()) > 275:
            time.sleep(0.3)
            afficher_game_over()
            reset_jeu()

        # Collision nourriture normale
        if snake.distance(snake_food) < 20:
            x = random.randint(-270, 270)
            y = random.randint(-270, 270)
            snake_food.goto(x, y)
            segment = turtle.Turtle()
            segment.speed(0)
            segment.shape("square")
            segment.color("blue")
            segment.penup()
            segments.append(segment)
            score_joueur += 5
            if score_joueur > meilleur_score:
                meilleur_score = score_joueur
                with open("meilleur_score.txt", "w") as file:
                    file.write(str(meilleur_score))
            pen_score.clear()
            pen_best.clear()
            pen_score.write(f"Score : {score_joueur}", align="left", font=("Arial", 18, "normal"))
            pen_best.write(f"Meilleur Score : {meilleur_score}", align="left", font=("Arial", 18, "normal"))
            temps_délai -= 0.001

        # Super nourriture aléatoire
        if not snake_great_food_visible and random.random() < 0.02:
            x = random.randint(-270, 270)
            y = random.randint(-270, 270)
            snake_great_food.goto(x, y)
            snake_great_food.showturtle()
            snake_great_food_visible = True
            snake_great_food_timer = 50
        elif snake_great_food_visible:
            snake_great_food_timer -= 1
            if snake_great_food_timer <= 0:
                snake_great_food.hideturtle()
                snake_great_food_visible = False

    # Collision super nourriture
        if snake_great_food_visible and snake.distance(snake_great_food) < 20:
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("blue")
            new_segment.penup()
            segments.append(new_segment)

            score_joueur += 10
            if score_joueur > meilleur_score:
                meilleur_score = score_joueur
                with open("meilleur_score.txt", "w") as file:
                    file.write(str(meilleur_score))
            pen_score.clear()
            pen_best.clear()
            pen_score.write(f"Score : {score_joueur}", align="left", font=("Arial", 18, "normal"))
            pen_best.write(f"Meilleur Score : {meilleur_score}", align="left", font=("Arial", 18, "normal"))
            temps_délai -= 0.001
            snake_great_food.hideturtle()
            snake_great_food_visible = False


        # Déplacement corps
        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)
        if segments:
            segments[0].goto(snake.xcor(), snake.ycor())
        move()

        # Collision avec soi-même
        for segment in segments:
            if segment.distance(snake) < 20:
                time.sleep(0.3)
                afficher_game_over()
                reset_jeu()
        time.sleep(temps_délai)
except turtle.Terminator:
    print("Merci d’avoir joué ! À bientôt 👋")
