import pygame
import sys
import audioSettings
import gameState

def pause_menu(screen, clock, screen_width, screen_height, coin_sound, jump_sound, bg_music):
    pygame.init()
    audio_settings = gameState.audio_settings
    menu_font = pygame.font.Font(None, 48)
    menu_options = ["Audio Settings", "Resume", "Exit"]
    selected_option = 0
    paused = True

    # Colors
    HIGHLIGHT_COLOR = (255, 255, 255)
    DEFAULT_COLOR = (100, 100, 100)

    # Background music for the pause menu
    pause_music = pygame.mixer.Sound("pauseMenu.wav")
    pause_music.set_volume(audio_settings["bgm_volume"])
    pause_music.play(-1)

    while paused:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == "Resume":
                        paused = False
                    elif menu_options[selected_option] == "Audio Settings":
                        updated_sfx, updated_bgm = audioSettings.audio_settings_menu(
                            screen, screen_width, screen_height, clock, 
                            coin_sound, jump_sound, bg_music, audio_settings["bgm_volume"]
                        )
                        audio_settings["sfx_volume"] = updated_sfx
                        audio_settings["bgm_volume"] = updated_bgm
                    elif menu_options[selected_option] == "Exit":
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
                mouse_click = True

        # Render menu
        screen.fill((0, 0, 0))  # Black background
        for i, option in enumerate(menu_options):
            color = DEFAULT_COLOR
            if i == selected_option or pygame.Rect(
                screen_width // 2 - 100, 200 + i * 60, 200, 50
            ).collidepoint(mouse_pos):
                color = HIGHLIGHT_COLOR

            text = menu_font.render(option, True, color)
            screen.blit(
                text, (screen_width // 2 - text.get_width() // 2, 200 + i * 60)
            )

            if mouse_click and color == HIGHLIGHT_COLOR:
                if option == "Resume":
                    paused = False
                elif option == "Audio Settings":
                    updated_sfx, updated_bgm = audioSettings.audio_settings_menu(
                        screen, screen_width, screen_height, clock, 
                        coin_sound, jump_sound, bg_music, audio_settings["bgm_volume"]
                    )
                    audio_settings["sfx_volume"] = updated_sfx
                    audio_settings["bgm_volume"] = updated_bgm
                elif option == "Exit":
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

    # Stop pause menu music and resume game music
    pause_music.stop()
    bg_music.play(-1)

    return audio_settings["sfx_volume"], audio_settings["bgm_volume"]
