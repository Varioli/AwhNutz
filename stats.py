import pygame
import sys
import json

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 650, 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Stats")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Clock for managing frame rate
clock = pygame.time.Clock()

def show_stats():
    # Load stats from file
    try:
        with open("stats.json", "r") as file:
            top_stats = json.load(file)
    except FileNotFoundError:
        top_stats = []  # No stats available

    # Fonts
    stats_font = pygame.font.Font(None, 36)
    back_font = pygame.font.Font(None, 48)

    running_stats = True  # Keep the stats menu running
    while running_stats:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse button press for the "Back" button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):
                    running_stats = False  # Exit stats menu

        # Clear the screen
        screen.fill(BLACK)

        # Display the stats
        y = 100
        for i, stat in enumerate(top_stats[:5]):  # Show top 5 stats
            text = stats_font.render(f"#{i + 1} - Time: {stat['time']} sec, Coins: {stat['coins']}", True, WHITE)
            screen.blit(text, (50, y))
            y += 40

        # Draw the "Back" button
        back_text = back_font.render("Back", True, WHITE)
        back_rect = back_text.get_rect(center=(screen_width // 2, 450))  # Center the button
        pygame.draw.rect(screen, WHITE, back_rect, width=2)  # Draw button outline
        screen.blit(back_text, back_rect.topleft)  # Draw button text

        # Update the display
        pygame.display.flip()
        clock.tick(60)

# Prevent auto-run on import
if __name__ == "__main__":
    show_stats()
    pygame.quit()
    sys.exit()