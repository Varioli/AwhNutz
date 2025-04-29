import pygame
import sys
import os

# Initialize pygame
pygame.init()

def level_complete(screen):
    # Game state variables
    running = True
    clock = pygame.time.Clock()

    # Screen dimensions
    screen_width, screen_height = screen.get_size()

    # Load assets
    background_color = (0, 0, 0)
    gif_image = pygame.image.load("endOfLevel.gif")
    gif_image = pygame.transform.scale(gif_image, (screen_width, screen_height))

    # Fonts
    font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)

    # Buttons
    next_level_button = pygame.Rect(screen_width // 4 - 100, screen_height - 100, 200, 50)
    main_menu_button = pygame.Rect(3 * screen_width // 4 - 100, screen_height - 100, 200, 50)

    # Button colors
    button_color = (0, 128, 0)
    button_hover_color = (0, 255, 0)
    text_color = (255, 255, 255)

    # Main loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if next_level_button.collidepoint(mouse_pos):
                    # Placeholder for the next level
                    os.system("python level2.py")  # Assumes level2.py exists in the same directory
                    pygame.quit()
                    sys.exit()
                elif main_menu_button.collidepoint(mouse_pos):
                    # Return to the main menu
                    os.system("python launch.py")  # Assumes launch.py exists in the same directory
                    pygame.quit()
                    sys.exit()

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw background
        screen.fill(background_color)
        screen.blit(gif_image, (0, 0))

        # Draw buttons
        pygame.draw.rect(screen, button_hover_color if next_level_button.collidepoint(mouse_pos) else button_color, next_level_button)
        pygame.draw.rect(screen, button_hover_color if main_menu_button.collidepoint(mouse_pos) else button_color, main_menu_button)

        # Draw button text
        next_level_text = button_font.render("Next Level", True, text_color)
        main_menu_text = button_font.render("Main Menu", True, text_color)
        screen.blit(next_level_text, (next_level_button.centerx - next_level_text.get_width() // 2, next_level_button.centery - next_level_text.get_height() // 2))
        screen.blit(main_menu_text, (main_menu_button.centerx - main_menu_text.get_width() // 2, main_menu_button.centery - main_menu_text.get_height() // 2))

        # Update display
        pygame.display.flip()
        clock.tick(30)

# Prevent auto-run on import
if __name__ == "__main__":
    screen_width, screen_height = 650, 650
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Level Complete!")
    level_complete(screen)
