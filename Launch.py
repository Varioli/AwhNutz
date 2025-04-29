import pygame
import sys
import playGame  # Import the game module

# Initialize pygame
pygame.init()
pygame.font.init()  # Initialize the font module

# Screen settings
screen_width = 650
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ahh, Nutz...')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main_menu():
    # Load game menu image
    try:
        background_image = pygame.image.load("load.png")
        custom_width = int(screen_width * 1.4)
        custom_height = screen_height
        background_image = pygame.transform.scale(background_image, (custom_width, custom_height))
    except pygame.error:
        print("Error: Unable to load the image 'load.png'. Make sure it exists in the directory.")
        pygame.quit()
        sys.exit()

    # Fonts
    font = pygame.font.Font(None, 72)
    small_font = pygame.font.Font(None, 48)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Start the game when 'R' is pressed
                    running = False
                    playGame.start_game(screen)  # Call the start_game function

        # Draw background and menu options
        screen.blit(background_image, (-100, 0))  # Display the background
        title_text = font.render("Ahh, Nutz...", True, WHITE)
        play_text = small_font.render("Press 'R' to Play", True, WHITE)

        # Center the text on the screen
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 550))
        screen.blit(play_text, (screen_width // 2 - play_text.get_width() // 2, 600))

        pygame.display.flip()

# Run the main menu
if __name__ == "__main__":
    main_menu()

pygame.quit()
sys.exit()
