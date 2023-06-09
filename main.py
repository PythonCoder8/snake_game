"""Snake Game

This is a remake of the classic 80's game Snake 
programmed in python using the pygame module.
Control the snake using the arrow keys to eat the food.
Every time the snake eats an apple the user's score 
increases by 1. When the score reaches a multiple of 10,
the user advances to the next level where the speed of the
snake is increased by 4.
"""

import random
import pygame

pygame.init()

# Set Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Create window and set attributes
dimensions = (600, 400)
root = pygame.display.set_mode(dimensions)
pygame.display.set_caption("Snake Game")
img = pygame.image.load("img\icon.png")
pygame.display.set_icon(img)

clock = pygame.time.Clock()

# Set snake attributes
snake_size = 12
snake_speed = 12

scores = []

# Set fonts
msg_font = pygame.font.SysFont("Consolas", 20)
score_font = pygame.font.SysFont("Consolas", 25)

level = 1


# Display game information
def display_score(score):
    score_text = score_font.render(f"Score: {str(score)}", True, white)
    if scores == []:
        high_score_text = score_font.render("High Score:  ", True, white)
    else:
        high_score_text = score_font.render(
            f"High Score: {str(max(scores))}", True, white
        )
    level_text = score_font.render(f"Level {str(level)}", True, white)
    root.blit(score_text, [0, 0])
    root.blit(high_score_text, [210, 0])
    root.blit(level_text, [500, 0])


# Draw snake
def draw_snake(snake_size, snake_pxls):
    for pxl in snake_pxls:
        global snake
        snake = pygame.draw.rect(root, green, [pxl[0], pxl[1], snake_size, snake_size])


# Set key variables
l_active = True
r_active = True
u_active = True
d_active = True


def run():
    # Set game variables
    global l_active
    global r_active
    global u_active
    global d_active
    global snake_speed
    global level
    game_over = False
    game_closed = False
    x = dimensions[0] / 2
    y = dimensions[1] / 2
    x_speed = 0
    y_speed = 0
    snake_pxls = []
    snake_len = 1
    food_x = round(random.randrange(0, dimensions[0] - snake_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, dimensions[1] - snake_size) / 10.0) * 10.0

    # Main game loop
    while not game_over:
        while game_closed:
            global l_active
            global r_active
            global u_active
            global d_active
            global scores
            global level
            global snake_speed
            level = 1
            snake_speed = 12
            l_active = True
            r_active = True
            u_active = True
            d_active = True
            scores.append(snake_len - 1)
            root.fill(black)
            game_over_msg = msg_font.render(
                "Game Over! Would you like to start a new game? (y/n)", True, red
            )
            root.blit(game_over_msg, [20, 150])
            display_score(snake_len - 1)
            pygame.display.flip()

            # Get keyboard input after game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        run()
                    if event.key == pygame.K_n:
                        game_over = True
                        game_closed = False
                if event.type == pygame.QUIT:
                    game_over = True
                    game_closed = False

        # Get main keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if l_active:
                        r_active = False
                        u_active = True
                        d_active = True
                        x_speed = -snake_size
                        y_speed = 0
                    else:
                        pass
                if event.key == pygame.K_RIGHT:
                    if r_active:
                        l_active = False
                        u_active = True
                        d_active = True
                        x_speed = snake_size
                        y_speed = 0
                    else:
                        pass
                if event.key == pygame.K_UP:
                    if u_active:
                        d_active = False
                        l_active = True
                        r_active = True
                        x_speed = 0
                        y_speed = -snake_size
                    else:
                        pass
                if event.key == pygame.K_DOWN:
                    if d_active:
                        u_active = False
                        l_active = True
                        r_active = True
                        x_speed = 0
                        y_speed = snake_size
                    else:
                        pass

        # Game over if snake touches border
        if x >= dimensions[0] or x < 0 or y >= dimensions[1] or y < 0:
            pygame.mixer.music.load("sfx\game_over.mp3")
            pygame.mixer.music.play()
            game_closed = True

        # Moves the snake
        x += x_speed
        y += y_speed

        # Background
        root.fill(black)

        # Draw apple
        food = pygame.draw.rect(root, red, [food_x, food_y, snake_size, snake_size])

        snake_pxls.append([x, y])

        # Make sure the snake doesn't keep growing
        if len(snake_pxls) > snake_len:
            del snake_pxls[0]

        # Game over if snake touches itself
        for pxl in snake_pxls[:-1]:
            if pxl == [x, y]:
                pygame.mixer.music.load("sfx\game_over.mp3")
                pygame.mixer.music.play()
                game_closed = True

        # Draw everything
        draw_snake(snake_size, snake_pxls)
        display_score(snake_len - 1)

        # Detect snake eating apple
        collide = snake.colliderect(food)
        if collide:
            pygame.mixer.music.load("sfx\eat.mp3")
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()

            food_x = (
                round(random.randrange(0, dimensions[0] - snake_size) / 10.0) * 10.0
            )
            food_y = (
                round(random.randrange(0, dimensions[1] - snake_size) / 10.0) * 10.0
            )

            snake_len += 1

            if (snake_len - 1) % 10 == 0 and snake_len - 1 != 0:
                pygame.mixer.music.load("sfx\level_up.mp3")
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play()
                snake_speed += 3
                level += 1

        clock.tick(snake_speed)

        pygame.display.flip()

    pygame.quit()
    quit()


run()
