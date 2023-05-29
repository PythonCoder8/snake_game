import pygame
import random

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

clock = pygame.time.Clock()

# Set snake attributes
snake_size = 12
snake_speed = 15

# Set fonts
msg_font = pygame.font.SysFont("Consolas", 20)
score_font = pygame.font.SysFont("Consolas", 25)


def display_score(score):
    text = score_font.render(f"Score: {str(score)}", True, white)
    root.blit(text, [0, 0])


def draw_snake(snake_size, snake_pxls):
    for pxl in snake_pxls:
        global snake
        snake = pygame.draw.rect(root, green, [pxl[0], pxl[1], snake_size, snake_size])


l_active = True
r_active = True
u_active = True
d_active = True


def run():
    # Set game variables
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
            root.fill(black)
            game_over_msg = msg_font.render(
                "Game Over! Would you like to start a new game? (y/n)", True, red
            )
            root.blit(game_over_msg, [20, 150])
            display_score(snake_len - 1)
            pygame.display.flip()

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                global l_active
                global r_active
                global u_active
                global d_active

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
        if x >= dimensions[0] or x < 0 or y >= dimensions[1] or y < 0:
            game_closed = True

        x += x_speed
        y += y_speed

        root.fill(black)

        food = pygame.draw.rect(root, red, [food_x, food_y, snake_size, snake_size])

        snake_pxls.append([x, y])

        if len(snake_pxls) > snake_len:
            del snake_pxls[0]

        for pxl in snake_pxls[:-1]:
            if pxl == [x, y]:
                game_closed = True

        draw_snake(snake_size, snake_pxls)
        display_score(snake_len - 1)

        pygame.display.flip()

        collide = snake.colliderect(food)

        if collide:
            food_x = (
                round(random.randrange(0, dimensions[0] - snake_size) / 10.0) * 10.0
            )
            food_y = (
                round(random.randrange(0, dimensions[1] - snake_size) / 10.0) * 10.0
            )
            snake_len += 1
            pygame.display.flip()

        clock.tick(snake_speed)

    pygame.quit()
    quit()


run()
