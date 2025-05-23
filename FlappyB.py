#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pygame
from sys import exit
import random

# Initialize Pygame and sound mixer
pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("assets/background_music.mp3")  
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1)  
clock = pygame.time.Clock()

# Window
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

# Images
# Load Bird Images
bird_images1 = [pygame.image.load("assets/bird1_down.png"),
                pygame.image.load("assets/bird1_mid.png"),
                pygame.image.load("assets/bird1_up.png")]

bird_images2 = [pygame.image.load("assets/bird2_down.png"),
                pygame.image.load("assets/bird2_mid.png"),
                pygame.image.load("assets/bird2_up.png")]

bird_images3 = [pygame.image.load("assets/bird3_down.png"),
                pygame.image.load("assets/bird3_mid.png"),
                pygame.image.load("assets/bird3_up.png")]

bird_images4 = [pygame.image.load("assets/bird4_down.png"),
                pygame.image.load("assets/bird4_mid.png"),
                pygame.image.load("assets/bird4_up.png")]

bird_images5 = [pygame.image.load("assets/bird5_down.png"),
                pygame.image.load("assets/bird5_mid.png"),
                pygame.image.load("assets/bird5_up.png")]

bird_images6 = [pygame.image.load("assets/bird6_down.png"),
                pygame.image.load("assets/bird6_mid.png"),
                pygame.image.load("assets/bird6_up.png")]

# Create a list of all bird image sets for easier selection
bird_image_sets = [bird_images1, bird_images2, bird_images3, bird_images4, bird_images5, bird_images6]



skyline_image = pygame.image.load("assets/background.png")
ground_image = pygame.image.load("assets/ground.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")

# Game
scroll_speed = 1
bird_start_position = (100, 250)
score = 0
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True

    def update(self, user_input):
        # Animate Bird
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        # Gravity and Flap
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Rotate Bird
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        # User Input
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        # Move Pipe
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

        # Score
        global score
        if self.pipe_type == 'bottom':
            if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        # Move Ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()


def quit_game():
    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# Game Main Method
def main():
    global score, game_stopped

    # Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    # Setup Pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))

    run = True
    while run:
        # Quit
        quit_game()

        # Reset Frame
        window.fill((0, 0, 0))

        # User Input
        user_input = pygame.key.get_pressed()

        # Draw Background
        window.blit(skyline_image, (0, 0))

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))

        # Draw - Pipes, Ground and Bird
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        # Show Score
        score_text = font.render('Score: ' + str(score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20))

        # Update - Pipes, Ground and Bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            # Display Game Over Screen
            window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                          win_height // 2 - game_over_image.get_height() // 2))
            pygame.display.update()  # Update the display to show the game over image
            # Wait for user input to restart
            while True:
                quit_game()  # Allow the player to quit
                user_input = pygame.key.get_pressed()
                if user_input[pygame.K_r]:  # Restart if 'R' is pressed
                    score = 0
                    game_stopped = True
                    menu()  # Go back to the main menu
                clock.tick(60)  # Limit the frame rate

        # Spawn Pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()



# Menu
def menu():
    global game_stopped
    
    bird_selection_menu()
        
def bird_selection_menu():
    global bird_images, game_stopped

    selected_bird = 0  # Default selected bird

    while game_stopped:
        quit_game()

        # Draw Menu
        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, (0, 520))

        # Display each bird option
        for i, bird_set in enumerate(bird_image_sets):
            x_pos = 50 + i * 80
            window.blit(bird_set[1], (x_pos, win_height // 2 - bird_set[1].get_height() // 2))
            if selected_bird == i:
                pygame.draw.rect(window, (255, 255, 0), (x_pos - 5, win_height // 2 - bird_set[1].get_height() // 2 - 5, bird_set[1].get_width() + 10, bird_set[1].get_height() + 10), 2)

        # Instructions
        instructions = font.render("Press Left/Right to select bird, Space to start", True, pygame.Color(255, 255, 255))
        window.blit(instructions, (win_width // 2 - instructions.get_width() // 2, 20))

        # User Input
        user_input = pygame.key.get_pressed()

        if user_input[pygame.K_LEFT]:
            selected_bird = (selected_bird - 1) % len(bird_image_sets)
            pygame.time.delay(200)  # Delay to prevent fast cycling
        if user_input[pygame.K_RIGHT]:
            selected_bird = (selected_bird + 1) % len(bird_image_sets)
            pygame.time.delay(200)

        if user_input[pygame.K_SPACE]:
            bird_images = bird_image_sets[selected_bird]  # Set the selected bird
            game_stopped = False
            main()  # Start the main game

        pygame.display.update()



menu()


# In[ ]:





# In[ ]:





# In[ ]:




