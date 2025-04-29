import pygame
import sys
import pauseMenu
import stats
import levelComplete
import playGame
import gameState

def audio_settings_menu(screen, screen_width, screen_height, clock, coin_sound, jump_sound, bg_music):
    audio_settings = gameState.audio_settings
    sfx_volume = audio_settings["sfx_volume"]
    bgm_volume = audio_settings["bgm_volume"]
    
    # Adjust sliders and save changes back to gameState
    gameState.audio_settings["sfx_volume"] = sfx_volume
    gameState.audio_settings["bgm_volume"] = bgm_volumeslider_width = 400
    slider_height = 10

    coin_sound.set_volume(sfx_slider_value)  # Adjust coin sound volume
    jump_sound.set_volume(sfx_slider_value)  # Adjust jump sound volume

    # Volumes
    sfx_volume = coin_sound.get_volume()  # Use current sound settings
    bgm_volume = bg_music.get_volume()
    
    # Adjust BGM slider logic
    bg_music.set_volume(bgm_slider_value)

    return sfx_slider_value, bgm_slider_value  # Return updated slider values
    
    dragging_sfx = False
    dragging_bgm = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sfx_slider_rect.collidepoint(event.pos):
                    dragging_sfx = True
                if bgm_slider_rect.collidepoint(event.pos):
                    dragging_bgm = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_sfx = dragging_bgm = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging_sfx:
                    sfx_volume = adjust_slider(event.pos[0], slider_width, sfx_slider_rect)
                    coin_sound.set_volume(sfx_volume)
                    jump_sound.set_volume(sfx_volume)
                if dragging_bgm:
                    bgm_volume = adjust_slider(event.pos[0], slider_width, bgm_slider_rect)
                    bg_music.set_volume(bgm_volume)

        # Render sliders and buttons here
        pygame.display.flip()
        clock.tick(60)

    return sfx_volume, bgm_volume


        # Render sliders
    screen.fill((0, 0, 0))  # Black background
    draw_slider(screen, slider_x_start, coin_slider_y, slider_width, slider_height, coin_volume, "Coin Volume")
    draw_slider(screen, slider_x_start, jump_slider_y, slider_width, slider_height, jump_volume, "Jump Volume")
    draw_slider(screen, slider_x_start, bgm_slider_y, slider_width, slider_height, bgm_volume, "Music Volume")

        # Add Save and Cancel Buttons
    save_button, cancel_button = draw_buttons(screen, screen_width)

        # Handle button clicks
    if pygame.mouse.get_pressed()[0]:  # Left mouse button
        mouse_pos = pygame.mouse.get_pos()
        if save_button.collidepoint(mouse_pos):
            return
        if cancel_button.collidepoint(mouse_pos):
            return

def draw_slider(screen, x, y, width, height, value, label):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height))  # Slider background
    pygame.draw.rect(screen, (0, 255, 0), (x, y, value * width, height))  # Slider fill
    pygame.draw.circle(screen, (255, 255, 255), (int(x + value * width), y + height // 2), 15)
    font = pygame.font.Font(None, 36)
    text = font.render(f"{label}: {int(value * 100)}%", True, (255, 255, 255))
    screen.blit(text, (x, y - 40))

pygame.display.flip()