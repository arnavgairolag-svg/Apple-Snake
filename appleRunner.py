import pygame
import sys
import random
import math
import time

pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apple Snake")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 165, 0)
brown = (139, 69, 19)
green = (0, 200, 0)
dark_green = (7, 255, 6)
black = (0, 0, 0)
blue = (12, 12, 255)
pink = (255, 105, 180)
gray = (50, 50, 50)

# Snake
snake_position = [400, 400]
snake_body = [[400, 400]]
snake_radius = 10
snake_speed = 5

# Game
score = 0
lives = 3
level = 1
num_apples = 5
num_poison = 2

# Items
def gen_items(n):
    return [[random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20)] for _ in range(n)]

apples = gen_items(num_apples)
poison = gen_items(num_poison)
hearts = []

# Enemies
enemies = []

dx, dy = 0, 0
font = pygame.font.SysFont("Arial", 32)
clock = pygame.time.Clock()
start_time = time.time()

# Particle system
particles = []

def create_particles(x, y, color, count=15):
    for _ in range(count):
        particles.append({
            "x": x,
            "y": y,
            "dx": random.uniform(-2, 2),
            "dy": random.uniform(-2, 2),
            "life": random.randint(20, 40),
            "color": color
        })

def draw_particles():
    for p in particles[:]:
        pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), 3)
        p["x"] += p["dx"]
        p["y"] += p["dy"]
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

# Distance
def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# Title Screen
title_screen = True
while title_screen:
    screen.fill(dark_green)
    title_font = pygame.font.SysFont("Arial", 64, bold=True)
    title_text = title_font.render("APPLE SNAKE", True, red)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)
    instr_font = pygame.font.SysFont("Arial", 28)
    instr_text = instr_font.render("Press SPACE to continue", True, white)
    instr_rect = instr_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(instr_text, instr_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            title_screen = False

# Mode Selection
mode_selected = False
while not mode_selected:
    screen.fill(dark_green)
    title_font = pygame.font.SysFont("Arial", 64, bold=True)
    title_text = title_font.render("APPLE SNAKE", True, red)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
    screen.blit(title_text, title_rect)
    mode_font = pygame.font.SysFont("Arial", 36)
    easy_text = mode_font.render("1. Easy", True, white)
    normal_text = mode_font.render("2. Normal", True, white)
    hard_text = mode_font.render("3. Hard", True, white)
    screen.blit(easy_text, (WIDTH // 2 - 50, HEIGHT // 2 - 30))
    screen.blit(normal_text, (WIDTH // 2 - 50, HEIGHT // 2 + 20))
    screen.blit(hard_text, (WIDTH // 2 - 50, HEIGHT // 2 + 70))
    instr_font = pygame.font.SysFont("Arial", 28)
    instr_text = instr_font.render("Press 1, 2, or 3 to choose mode", True, white)
    instr_rect = instr_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
    screen.blit(instr_text, instr_rect)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                snake_speed = 3
                num_apples = 5
                num_poison = 1
                mode_selected = True
            elif event.key == pygame.K_2:
                snake_speed = 5
                num_apples = 5
                num_poison = 2
                mode_selected = True
            elif event.key == pygame.K_3:
                snake_speed = 7
                num_apples = 5
                num_poison = 4
                mode_selected = True

# Regenerate items
apples = gen_items(num_apples)
poison = gen_items(num_poison)

# Main Game Loop
running = True
while running:
    clock.tick(30)
    screen.fill(dark_green)
    elapsed = time.time() - start_time

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        dx, dy = 0, -snake_speed
    elif keys[pygame.K_DOWN]:
        dx, dy = 0, snake_speed
    elif keys[pygame.K_RIGHT]:
        dx, dy = snake_speed, 0
    elif keys[pygame.K_LEFT]:
        dx, dy = -snake_speed, 0

    # Move snake
    snake_position[0] += dx
    snake_position[1] += dy
    snake_body.insert(0, list(snake_position))

    # Apple collision
    for a in apples[:]:
        if distance(snake_position, a) < snake_radius + 10:
            apples.remove(a)
            score += 1
            snake_body.append(snake_body[-1])
            create_particles(a[0], a[1], red)

    # Poison collision
    for p in poison[:]:
        if distance(snake_position, p) < snake_radius + 10:
            lives -= 1
            poison.remove(p)
            create_particles(p[0], p[1], orange)
            if lives <= 0:
                running = False

    # Heart collision
    for h in hearts[:]:
        if distance(snake_position, h) < snake_radius + 10:
            lives += 1
            hearts.remove(h)
            create_particles(h[0], h[1], pink)

    # Level up
    if not apples:
        level += 1
        num_apples += 2
        num_poison += 1
        snake_speed += 0.5
        apples = gen_items(num_apples)
        poison = gen_items(num_poison)
        if random.random() < 0.5:
            hearts.append([random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20)])
        if level >= 5 and level % 2 == 0 and random.random() < 0.5:
            enemy_pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]
            enemy_body = [list(enemy_pos)]
            enemies.append({"pos": enemy_pos, "body": enemy_body, "dx": random.choice([-2, 2]), "dy": random.choice([-2, 2])})

    # Draw snake with wave
    wave_offset = math.sin(elapsed * 10) * 2
    for i, seg in enumerate(snake_body):
        shade = max(60, 255 - i * 8)
        body_color = (0, 0, shade)
        offset_y = math.sin(i * 0.5 + elapsed * 10) * wave_offset
        pygame.draw.circle(screen, body_color, (seg[0], int(seg[1] + offset_y)), snake_radius)

    # Snake head (eyes + tongue)
    head_x, head_y = snake_position
    eye_size = 3
    tongue_len = 6

    eye_dx, eye_dy = 5, -4
    tongue_dx, tongue_dy = snake_radius, 0
    if dx > 0:
        eye_dx, eye_dy = 5, -4
        tongue_dx, tongue_dy = snake_radius, 0
    elif dx < 0:
        eye_dx, eye_dy = -5, -4
        tongue_dx, tongue_dy = -snake_radius, 0
    elif dy < 0:
        eye_dx, eye_dy = -4, -5
        tongue_dx, tongue_dy = 0, -snake_radius
    elif dy > 0:
        eye_dx, eye_dy = -4, 5
        tongue_dx, tongue_dy = 0, snake_radius

    pygame.draw.circle(screen, blue, (head_x, head_y), snake_radius)
    pygame.draw.circle(screen, white, (head_x - eye_dx, head_y + eye_dy), eye_size)
    pygame.draw.circle(screen, white, (head_x + eye_dx, head_y + eye_dy), eye_size)
    pygame.draw.circle(screen, black, (head_x - eye_dx, head_y + eye_dy), 1)
    pygame.draw.circle(screen, black, (head_x + eye_dx, head_y + eye_dy), 1)

    pygame.draw.line(screen, red, (head_x, head_y), (head_x + tongue_dx, head_y + tongue_dy), 2)
    pygame.draw.line(screen, red, (head_x + tongue_dx, head_y + tongue_dy),
                     (head_x + tongue_dx - 3, head_y + tongue_dy - 3), 2)
    pygame.draw.line(screen, red, (head_x + tongue_dx, head_y + tongue_dy),
                     (head_x + tongue_dx - 3, head_y + tongue_dy + 3), 2)

    # Draw apples
    for a in apples:
        pygame.draw.circle(screen, red, a, 10)
        pygame.draw.rect(screen, brown, (a[0] - 2, a[1] - 12, 4, 6))
        pygame.draw.polygon(screen, green, [(a[0] - 4, a[1] - 12), (a[0], a[1] - 18), (a[0] + 4, a[1] - 12)])

    # Draw poison
    for p in poison:
        pygame.draw.circle(screen, orange, p, 10)
        pygame.draw.rect(screen, brown, (p[0] - 2, p[1] - 12, 4, 6))
        pygame.draw.polygon(screen, green, [(p[0] - 4, p[1] - 12), (p[0], p[1] - 18), (p[0] + 4, p[1] - 12)])

    # Draw hearts
    for h in hearts:
        x, y = h
        pygame.draw.polygon(screen, red, [(x, y), (x - 5, y - 7), (x - 10, y - 2),
                                          (x - 10, y + 3), (x, y + 12), (x + 10, y + 3),
                                          (x + 10, y - 2), (x + 5, y - 7)])
        pygame.draw.circle(screen, red, (x - 5, y - 5), 3)
        pygame.draw.circle(screen, red, (x + 5, y - 5), 3)

    # -------------------- ENEMY SECTION (Updated) --------------------
    for enemy in enemies:
        ex, ey = enemy["pos"]
        enemy_body = enemy["body"]

        # Move enemy
        ex += enemy["dx"]
        ey += enemy["dy"]
        if ex < 0 or ex > WIDTH:
            enemy["dx"] *= -1
        if ey < 0 or ey > HEIGHT:
            enemy["dy"] *= -1
        enemy["pos"] = [ex, ey]
        enemy["body"].insert(0, [ex, ey])
        if len(enemy["body"]) > 5:
            enemy["body"].pop()

        # Enemy apple eating
        for a in apples[:]:
            if distance([ex, ey], a) < snake_radius + 10:
                apples.remove(a)
                score = max(0, score - 1)
                create_particles(a[0], a[1], red)

        # Enemy body
        for seg in enemy_body:
            pygame.draw.circle(screen, (255, 12, 13), seg, snake_radius)

        # Enemy face (eyes + tongue)
        eye_size = 3
        tongue_len = 6
        if abs(enemy["dx"]) > abs(enemy["dy"]):
            if enemy["dx"] > 0:
                eye_dx, eye_dy = 5, -4
                tongue_dx, tongue_dy = snake_radius, 0
            else:
                eye_dx, eye_dy = -5, -4
                tongue_dx, tongue_dy = -snake_radius, 0
        else:
            if enemy["dy"] > 0:
                eye_dx, eye_dy = -4, 5
                tongue_dx, tongue_dy = 0, snake_radius
            else:
                eye_dx, eye_dy = -4, -5
                tongue_dx, tongue_dy = 0, -snake_radius

        pygame.draw.circle(screen, (255, 0, 0), (ex, ey), snake_radius)
        pygame.draw.circle(screen, white, (ex - eye_dx, ey + eye_dy), eye_size)
        pygame.draw.circle(screen, white, (ex + eye_dx, ey + eye_dy), eye_size)
        pygame.draw.circle(screen, black, (ex - eye_dx, ey + eye_dy), 1)
        pygame.draw.circle(screen, black, (ex + eye_dx, ey + eye_dy), 1)

        pygame.draw.line(screen, red, (ex, ey), (ex + tongue_dx, ey + tongue_dy), 2)
        pygame.draw.line(screen, red, (ex + tongue_dx, ey + tongue_dy),
                         (ex + tongue_dx - 3, ey + tongue_dy - 3), 2)
        pygame.draw.line(screen, red, (ex + tongue_dx, ey + tongue_dy),
                         (ex + tongue_dx - 3, ey + tongue_dy + 3), 2)

        if distance([ex, ey], snake_position) < snake_radius * 2:
            lives -= 1
            create_particles(ex, ey, pink)
            if lives <= 0:
                running = False
    # ----------------------------------------------------------------

    # Draw HUD
    text = font.render(f"Score: {score}  |  Lives: {lives}  |  Level: {level}", True, white)
    screen.blit(text, (20, 20))

    # Borders
    if snake_position[0] < 0 or snake_position[0] > WIDTH or snake_position[1] < 0 or snake_position[1] > HEIGHT:
        lives -= 1
        create_particles(snake_position[0], snake_position[1], pink)
        if lives <= 0:
            running = False
        else:
            snake_position = [400, 400]
            dx, dy = 0, 0

    # Tail management
    if len(snake_body) > score + 1:
        snake_body.pop()

    # Draw particles
    draw_particles()

    pygame.display.update()

# Game Over popup
screen.fill(black)
rect_width, rect_height = 400, 200
popup_rect = pygame.Rect(WIDTH // 2 - rect_width // 2, HEIGHT // 2 - rect_height // 2, rect_width, rect_height)
pygame.draw.rect(screen, gray, popup_rect, border_radius=20)
game_over_font = pygame.font.SysFont("Arial", 64, bold=True)
game_over_text = game_over_font.render("GAME OVER", True, red)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
screen.blit(game_over_text, game_over_rect)
score_font = pygame.font.SysFont("Arial", 36)
final_score_text = score_font.render(f"Final Score: {score}", True, white)
final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
screen.blit(final_score_text, final_score_rect)
pygame.display.update()
pygame.time.wait(5000)
pygame.quit()
sys.exit()