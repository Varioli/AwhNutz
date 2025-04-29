import pygame
import sys
import random
import levelComplete
import pauseMenu

# Initialize pygame
pygame.init()

def start_game(screen):
    # Screen dimensions
    screen_width, screen_height = screen.get_size()

    # Game state variables
    running = True
    paused = False
    clock = pygame.time.Clock()
    timer_started = False
    level_start_time = 0
    level_end_time = 0

    # Audio variables
    sfx_volume = 0.6
    bgm_volume = 0.6
    coin_sound = pygame.mixer.Sound("coin.wav")
    jump_sound = pygame.mixer.Sound("jump.wav")
    bg_music = pygame.mixer.Sound("mainMusic.wav")
    coin_sound.set_volume(sfx_volume)
    jump_sound.set_volume(sfx_volume)
    bg_music.set_volume(bgm_volume)
    bg_music.play(-1)

    # Load assets
    background_image = pygame.image.load("background.png")
    background_width = 5000
    background_image = pygame.transform.scale(background_image, (background_width, screen_height))

    sprite_image = pygame.image.load("gopher.png")
    sprite_width, sprite_height = 50, 75
    sprite_image = pygame.transform.scale(sprite_image, (sprite_width, sprite_height))
    sprite_rect = pygame.Rect(100, screen_height - 175, sprite_width, sprite_height)

    coin_image = pygame.Surface((20, 20))
    coin_image.fill((255, 223, 0))  # Gold for regular coins
    final_coin_image = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.ellipse(final_coin_image, (0, 0, 255), (0, 0, 20, 20))  # Blue for final coin

    # Platforms and walls generation
    platforms = [pygame.Rect(0, screen_height - 100, background_width, 100)]  # Ground

    platform_spacing = 300
    for i in range(5):  # Create 5 floating platforms
        while True:
            x = random.randint(300, background_width - 200)
            y = random.randint(screen_height - 200, screen_height - 185)
            new_platform = pygame.Rect(x, y, 150, 20)
            if all(abs(new_platform.x - platform.x) > platform_spacing for platform in platforms):
                platforms.append(new_platform)
                break

    walls = []
    wall_spacing = 400
    for i in range(6):  # Create 6 walls
        while True:
            x = random.randint(300, background_width - 200)
            y = screen_height - random.randint(100, 175)
            new_wall = pygame.Rect(x, y, 50, 75)
            if all(abs(new_wall.x - wall.x) > wall_spacing for wall in walls) and not any(
                new_wall.colliderect(platform) for platform in platforms
            ):
                walls.append(new_wall)
                break

    # Generate coins
    coins = []
    while len(coins) < 14:
        coin_x = random.randint(100, background_width - 100)
        coin_y = random.randint(screen_height - 150, screen_height - 50)
        new_coin = pygame.Rect(coin_x, coin_y, 20, 20)
        if not any(new_coin.colliderect(obj) for obj in platforms + walls):
            coins.append(new_coin)

    final_coin = pygame.Rect(background_width - 100, screen_height - 150, 20, 20)

    # Game variables
    gravity = 0.7
    jump_strength = -15
    sprite_velocity_y = 0
    is_jumping = False
    sprite_direction = "right"
    health = 100
    money = 0

    font = pygame.font.Font(None, 36)
    camera_x = 0

    # Main game loop
    while running:
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.pause()
                    paused = pauseMenu.pause_menu(screen, clock, screen_width, screen_height, coin_sound, jump_sound, bg_music, bgm_volume)
                    pygame.mixer.unpause()
                elif event.key == pygame.K_SPACE and not is_jumping:
                    sprite_velocity_y = jump_strength
                    is_jumping = True
                    jump_sound.play()

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and sprite_rect.left > 0:
                sprite_rect.x -= 5
                sprite_direction = "left"
                moved = True
            if keys[pygame.K_RIGHT] and sprite_rect.right < background_width:
                sprite_rect.x += 5
                sprite_direction = "right"
                moved = True

            if moved and not timer_started:
                timer_started = True
                level_start_time = pygame.time.get_ticks()

            sprite_velocity_y += gravity
            sprite_rect.y += sprite_velocity_y

            for platform in platforms:
                if sprite_rect.colliderect(platform) and sprite_velocity_y > 0:
                    sprite_rect.bottom = platform.top
                    sprite_velocity_y = 0
                    is_jumping = False

            if sprite_rect.bottom > screen_height - 100:
                sprite_rect.bottom = screen_height - 100
                sprite_velocity_y = 0
                is_jumping = False

            for wall in walls:
                if sprite_rect.colliderect(wall):
                    if sprite_rect.right > wall.left and sprite_rect.left < wall.left:
                        sprite_rect.right = wall.left
                    elif sprite_rect.left < wall.right and sprite_rect.right > wall.right:
                        sprite_rect.left = wall.right

            for coin in coins[:]:
                if sprite_rect.colliderect(coin):
                    coins.remove(coin)
                    money += 10
                    coin_sound.play()

            if sprite_rect.colliderect(final_coin):
                money += 50
                running = False
                level_end_time = pygame.time.get_ticks()
                levelComplete.level_complete(screen)

            camera_x = max(0, min(sprite_rect.centerx - screen_width // 2, background_width - screen_width))

            screen.fill((0, 0, 0))
            screen.blit(background_image, (-camera_x, 0))

            for platform in platforms:
                pygame.draw.rect(screen, (85, 107, 47), (platform.x - camera_x, platform.y, platform.width, platform.height))
            for wall in walls:
                pygame.draw.rect(screen, (101, 67, 33), (wall.x - camera_x, wall.y, wall.width, wall.height))
            for coin in coins:
                screen.blit(coin_image, (coin.x - camera_x, coin.y))
            screen.blit(final_coin_image, (final_coin.x - camera_x, final_coin.y))

            sprite_image_flipped = pygame.transform.flip(sprite_image, True, False) if sprite_direction == "left" else sprite_image
            screen.blit(sprite_image_flipped, (sprite_rect.x - camera_x, sprite_rect.y))

            pygame.draw.rect(screen, (255, 0, 0), (105, 573, 200, 20))
            pygame.draw.rect(screen, (0, 255, 0), (105, 573, 200 * health // 100, 20))

            health_text = font.render(f"Health: ", True, (255, 255, 255))
            money_text = font.render(f"Money: ${money}", True, (255, 255, 255))
            screen.blit(health_text, (10, 570))
            screen.blit(money_text, (10, 610))

            if timer_started:
                elapsed_time = (pygame.time.get_ticks() - level_start_time) / 1000
                timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, (255, 255, 255))
                screen.blit(timer_text, (10, 100))

            pygame.display.flip()
            clock.tick(60)

    save_stats(level_end_time, level_start_time, money)

def save_stats(end_time, start_time, money):
    elapsed_time = (end_time - start_time) / 1000
    stats = {"time": elapsed_time, "money": money}
    try:
        with open("stats.json", "r") as file:
            all_stats = json.load(file)
    except FileNotFoundError:
        all_stats = []
    all_stats.append(stats)
    with open("stats.json", "w") as file:
        json.dump(all_stats, file, indent=4)

if __name__ == "__main__":
    screen_width, screen_height = 650, 650
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ahh, Nutz...")
    start_game(screen)
