'''
# Games with Python #
## Breakout ##
## Aouther: Omar Tamer #
'''

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breakout Game ")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the paddle
paddle_width = 100
paddle_height = 10
paddle_speed = 10
paddle = pygame.Rect(350, 550, paddle_width, paddle_height)

# Set up the ball
ball_size = 10
ball_speed = [5, -5]
ball = pygame.Rect(395, 540, ball_size, ball_size)

# Set up the bricks
brick_width = 70
brick_height = 20
brick_padding = 10  # Space between bricks
brick_offset_x = 35  # Offset from the left edge
brick_offset_y = 45  # Offset from the top edge


def create_bricks(level):
    brick_rows = 4 + level
    brick_cols = 9
    bricks = []
    for i in range(brick_rows):
        for j in range(brick_cols):
            if random.choice([True, False]):
                brick_x = brick_offset_x + j * (brick_width + brick_padding)
                brick_y = brick_offset_y + i * (brick_height + brick_padding)
                bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))
    return bricks


# Set up the score, lives, and level
score = 0
lives = 3
level = 1
font = pygame.font.SysFont(None, 36)


def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(
        game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 200)
    )
    screen.blit(
        score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 250)
    )
    screen.blit(
        restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 300)
    )
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
    return False


def level_up_screen():
    screen.fill(BLACK)
    level_up_text = font.render(f"Level {level} Complete!", True, WHITE)
    continue_text = font.render("Press SPACE to Continue", True, WHITE)
    screen.blit(
        level_up_text, (screen.get_width() // 2 - level_up_text.get_width() // 2, 250)
    )
    screen.blit(
        continue_text, (screen.get_width() // 2 - continue_text.get_width() // 2, 300)
    )
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Main game loop
def main():
    global score, lives, level, ball_speed, ball, paddle

    score = 0
    lives = 3
    level = 1
    paddle = pygame.Rect(350, 550, paddle_width, paddle_height)
    ball = pygame.Rect(395, 540, ball_size, ball_size)
    ball_speed = [5, -5]
    bricks = create_bricks(level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Get the set of keys pressed
        keys = pygame.key.get_pressed()

        # Move the paddle
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < screen.get_width():
            paddle.left += paddle_speed

        # Move the ball
        ball.left += ball_speed[0]
        ball.top += ball_speed[1]

        # Ball collision with the walls & paddle
        if ball.left <= 0 or ball.right >= screen.get_width():
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        # Ball collision with the bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove(brick)
                score += 10  # Increase score for each brick hit

        # Check for level completion
        if not bricks:
            level_up_screen()  # waiting...Press SPACE to Continue or Quit
            level += 1
            bricks = create_bricks(level)  # Start new level
            # Reset ball & paddle positions and directions
            ball.left = 395
            ball.top = 540
            ball_speed = [5, -5]
            paddle.left = 350

        # Check for game over
        if ball.top >= screen.get_height():
            lives -= 1  # Decrease lives
            if lives == 0:
                running = False  # End game if no lives left
            else:
                # Reset ball and paddle position
                ball.left = 395
                ball.top = 540
                ball_speed = [5, -5]
                paddle.left = 350

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw the paddle
        pygame.draw.rect(screen, WHITE, paddle)

        # Draw the ball
        pygame.draw.ellipse(screen, WHITE, ball)

        # Draw the bricks
        for brick in bricks:
            pygame.draw.rect(screen, RED, brick)

        # Display score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (20, 10))
        screen.blit(lives_text, (700, 10))
        screen.blit(level_text, (360, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    if game_over_screen():  # waiting...Press R to Restart or Q to Quit
        main()


main()
pygame.quit()
