import pygame

# Tamanho e carregamento de mapa
width = 800
height = 600
mapa = []
tile = {}

# Configurações do jogador
player = None
player_x = width // 2
player_y = height - 100
player_speed = 5
player_bullet = None
player_alive = True

# Configurações dos inimigos
enemies = []
enemy_speed = 3
enemy_bullets = []
enemy_shoot_timer = 0

# Tamanho dos tiros
bullet_width, bullet_height = 5, 10

# Configuração da animação de explosão
explosion_duration = 20
explosion_image = pygame.image.load("explosion.png")
explosion_image = pygame.transform.scale(explosion_image, (70, 70))

def load_mapa(tilesets):
    global mapa
    with open(tilesets, "r") as file:
        for line in file:
            mapa.append(line.strip())

def load():
    global clock, tile, player
    clock = pygame.time.Clock()
    load_mapa("mapa.txt")
    tile['G'] = pygame.image.load("img1.png")
    player = pygame.image.load("ship.png")
    player = pygame.transform.scale(player, (70, 70))
    enemy_image = pygame.image.load("invader.png")
    enemy_image = pygame.transform.scale(enemy_image, (70, 70))
    for i in range(len(mapa)):
        enemies.append({
            "x": i * 80,
            "y": i * 40 + 50,
            "dir": 1,
            "img": enemy_image,
            "alive": True
        })

def shoot_bullet(source_x, source_y, bullets, direction):
    bullets.append({"x": source_x, "y": source_y, "dir": direction})

def update(keys_pressed):
    global player_x, player_y, player_bullet, player_alive, enemy_bullets, enemy_shoot_timer

    if player_alive:
        if keys_pressed[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys_pressed[pygame.K_RIGHT] and player_x < width - 70:
            player_x += player_speed
        if keys_pressed[pygame.K_SPACE] and player_bullet is None:
            player_bullet = {"x": player_x + 35, "y": player_y, "dir": -1}

    for enemy in enemies:
        if "explosion_timer" in enemy:
            enemy["explosion_timer"] -= 1
            if enemy["explosion_timer"] <= 0:
                enemies.remove(enemy)
        else:
            enemy["x"] += enemy_speed * enemy["dir"]
            if enemy["x"] <= 0 or enemy["x"] >= width - 70:
                enemy["dir"] *= -1

    enemy_shoot_timer += 1
    if enemy_shoot_timer > 300 and enemies:
        shooter = enemies[0]
        shoot_bullet(shooter["x"] + 35, shooter["y"] + 40, enemy_bullets, 1)
        enemy_shoot_timer = 0

    if player_bullet:
        player_bullet["y"] += player_bullet["dir"] * 10
        if player_bullet["y"] < 0:
            player_bullet = None

    for bullet in enemy_bullets[:]:
        bullet["y"] += bullet["dir"] * 5
        if bullet["y"] > height:
            enemy_bullets.remove(bullet)

    check_collisions()

def check_collisions():
    global player_bullet, player_alive, enemies, enemy_bullets

    if player_bullet:
        for enemy in enemies[:]:
            if enemy["x"] < player_bullet["x"] < enemy["x"] + 70 and enemy["y"] < player_bullet["y"] < enemy["y"] + 70:
                enemy["explosion_timer"] = explosion_duration
                enemy["alive"] = False
                player_bullet = None
                break

    for enemy in enemies[:]:
        if not enemy.get("alive") and enemy.get("explosion_timer", 0) <= 0:
            enemies.remove(enemy)

    if player_alive:
        for bullet in enemy_bullets[:]:
            if player_x < bullet["x"] < player_x + 70 and player_y < bullet["y"] < player_y + 70:
                enemy_bullets.remove(bullet)
                player_alive = False

def draw_screen(screen):
    for row_index, row in enumerate(mapa):
        for col_index, tile_char in enumerate(row):
            if tile_char in tile:
                x = col_index * 32
                y = row_index * 32
                screen.blit(tile[tile_char], (x, y))

    if player_alive:
        screen.blit(player, (player_x, player_y))

    for enemy in enemies:
        if "explosion_timer" in enemy:
            screen.blit(explosion_image, (enemy["x"], enemy["y"]))
        else:
            screen.blit(enemy["img"], (enemy["x"], enemy["y"]))

    if player_bullet:
        pygame.draw.rect(screen, (255, 255, 0), (player_bullet["x"], player_bullet["y"], bullet_width, bullet_height))

    for bullet in enemy_bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet["x"], bullet["y"], bullet_width, bullet_height))

def main_loop(screen):
    running = True
    while running:
        keys_pressed = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        update(keys_pressed)
        screen.fill((0, 0, 0))
        draw_screen(screen)
        pygame.display.update()
        clock.tick(60)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")
load()
main_loop(screen)
pygame.quit()
