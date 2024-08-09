import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong But Funny™")

# Couleurs car pygames c'est bizzare w الله
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Speed/FPS
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
BLOCK_WIDTH, BLOCK_HEIGHT = 60, 20

# Paddle and ball speed
PADDLE_VEL = 5
BALL_X_VEL = 4 * random.choice((1, -1))
BALL_Y_VEL = 4 * random.choice((1, -1))

# Positions
left_paddle = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)

# Score
left_score = 0
right_score = 0

# Font
font = pygame.font.SysFont('comicsans', 50)
title_font = pygame.font.SysFont('comicsans', 60)

# State of the event
event_text = ""
event_timer = 0
silly_blocks_triggered = False
ball_size_reduction = 0
ball_size_reduction_start_time = 0
the_world_triggered = False
star_platinum_triggered = False
enemy_paddle_stopped = False
stand_paddle = None
star_platinum_paddle = None

# Blocs of Silly Blocks
left_blocks = []
right_blocks = []

def draw_window():
    WIN.fill(BLACK)

    left_score_text = font.render(f"Score: {left_score}", 1, WHITE)
    right_score_text = font.render(f"Score: {right_score}", 1, WHITE)
    WIN.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    WIN.blit(right_score_text, (WIDTH * 3//4 - right_score_text.get_width()//2, 20))

    pygame.draw.rect(WIN, RED, left_paddle)
    pygame.draw.rect(WIN, BLUE, right_paddle)
    pygame.draw.ellipse(WIN, GREEN, ball)
    pygame.draw.aaline(WIN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Affichage blocks
    for block in left_blocks:
        pygame.draw.rect(WIN, WHITE, block)
    for block in right_blocks:
        pygame.draw.rect(WIN, WHITE, block)

    # Affichage de l'event
    if event_text:
        event_display = title_font.render(event_text, 1, WHITE)
        WIN.blit(event_display, (WIDTH//2 - event_display.get_width()//2, HEIGHT//2 - event_display.get_height()//2))

    # Affichage des stand
    if stand_paddle:
        pygame.draw.rect(WIN, YELLOW, stand_paddle)
    if star_platinum_paddle:
        pygame.draw.rect(WIN, PURPLE, star_platinum_paddle)

    pygame.display.update()

def handle_paddle_movement(keys):
    if keys[pygame.K_z] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_VEL
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_VEL
    if not enemy_paddle_stopped:  # paddle stop par le time stop
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_VEL
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_VEL

def handle_ball_movement():
    global BALL_X_VEL, BALL_Y_VEL, left_score, right_score

    ball.x += BALL_X_VEL
    ball.y += BALL_Y_VEL
    
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_Y_VEL *= -1

    if ball.colliderect(left_paddle):
        BALL_X_VEL *= -1
        left_score += 100
    elif ball.colliderect(right_paddle):
        BALL_X_VEL *= -1
        right_score += 100

    for block in left_blocks:
        if ball.colliderect(block):
            BALL_X_VEL *= -1
            left_blocks.remove(block)
            left_score += 50 
            break  
            
    for block in right_blocks:
        if ball.colliderect(block):
            BALL_X_VEL *= -1
            right_blocks.remove(block)
            right_score += 50  # Bonus
            break  

    if ball.left <= 0:
        right_score -= 100
        reset_ball()
    elif ball.right >= WIDTH:
        left_score -= 100
        reset_ball()

def reset_ball():
    global BALL_X_VEL, BALL_Y_VEL
    ball.x = WIDTH//2 - BALL_RADIUS
    ball.y = HEIGHT//2 - BALL_RADIUS
    BALL_X_VEL *= random.choice((1, -1))
    BALL_Y_VEL *= random.choice((1, -1))

def trigger_event(event_name):
    global event_text, event_timer
    event_text = event_name
    event_timer = time.time()

def trigger_stand_the_world():
    global enemy_paddle_stopped, stand_paddle, the_world_start_time
    stand_paddle = pygame.Rect(left_paddle.x + PADDLE_WIDTH + 10, left_paddle.y, PADDLE_WIDTH, PADDLE_HEIGHT)
    enemy_paddle_stopped = True
    the_world_start_time = time.time()
    trigger_event("EVENT : ZA WARUDO")

def trigger_star_platinum():
    global enemy_paddle_stopped, star_platinum_paddle, star_platinum_start_time
    star_platinum_paddle = pygame.Rect(right_paddle.x - PADDLE_WIDTH - 10, right_paddle.y, PADDLE_WIDTH, PADDLE_HEIGHT)
    enemy_paddle_stopped = True
    star_platinum_start_time = time.time()
    trigger_event("EVENT : STAR PLATINUM")

def generate_blocks(paddle, blocks_list):
    for i in range(3):
        block_x = paddle.x + paddle.width + random.randint(0, WIDTH//2 - BLOCK_WIDTH)
        block_y = random.randint(0, HEIGHT - BLOCK_HEIGHT)
        blocks_list.append(pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT))

def main():
    global event_text, enemy_paddle_stopped, ball_size_reduction, ball_size_reduction_start_time, the_world_triggered, star_platinum_triggered, stand_paddle, star_platinum_paddle, silly_blocks_triggered, left_blocks, right_blocks

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        draw_window()

        if event_text and time.time() - event_timer > 3:  # 3 secondes
            event_text = ""
            
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys)
        handle_ball_movement()


        if left_score >= 5000 and not silly_blocks_triggered:
            generate_blocks(left_paddle, right_blocks)
            generate_blocks(right_paddle, left_blocks)
            trigger_event("EVENT : SILLY BLOCKS")
            silly_blocks_triggered = True
        elif left_score >= 10000 and (left_score - 5000) % 10000 == 0:
            generate_blocks(left_paddle, right_blocks)
            generate_blocks(right_paddle, left_blocks)
            trigger_event("EVENT : SILLY BLOCKS")


        if left_score >= 7000 and ball_size_reduction == 0:
            ball_size_reduction = 0.5
            ball_size_reduction_start_time = time.time()
            trigger_event("EVENT : YOURBALLZ")
 
        if left_score >= 20000 and not the_world_triggered:
            trigger_stand_the_world()
            the_world_triggered = True

        if right_score >= 20000 and not star_platinum_triggered:
            trigger_star_platinum()
            star_platinum_triggered = True

        if enemy_paddle_stopped and stand_paddle and time.time() - the_world_start_time > 5:  # 5 secondes
            enemy_paddle_stopped = False
            stand_paddle = None  

        if enemy_paddle_stopped and star_platinum_paddle and time.time() - star_platinum_start_time > 5:  # 5 secondes
            enemy_paddle_stopped = False
            star_platinum_paddle = None  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
