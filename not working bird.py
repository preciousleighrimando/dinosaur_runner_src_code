import pygame
import os
import random

# Initialize pygame mixer with lower latency
pygame.mixer.pre_init(44100, -16, 2, 512)  # Frequency, size, channels, buffer size
pygame.init()

# Constants
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Assets
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

small_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
large_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

bird_img= [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))


background = pygame.image.load(os.path.join("BackG/", "bg-night.gif"))
ground = pygame.image.load(os.path.join("Assets/Other", "ground1.png"))

# Load and scale the animated background frames
background_frames = [
    pygame.transform.scale(
        pygame.image.load(os.path.join("BackG/", f"a{i}.png")), (SCREEN_WIDTH, SCREEN_HEIGHT)
    ) for i in range(1, 21)
]

# Load the sound effect
button_click_sound = pygame.mixer.Sound('Sound/S1.mp3')  # Ensure S1.mp3 is in the correct path

# Function to play the sound effect
def play_button_sound():
    button_click_sound.play()

class Dinosaur:
    X_POS = 80
    Y_POS = SCREEN_HEIGHT - 263  # Move Dino higher
    Y_POS_DUCK = SCREEN_HEIGHT - 224  # Move ducking position higher
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect(x=self.X_POS, y=self.Y_POS)

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect(x=SCREEN_WIDTH)

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image, random.randint(0, 2))
        self.rect.y = SCREEN_HEIGHT - 240  # Move small cactus higher


class LargeCactus(Obstacle):
    def __init__(self, image):
        super().__init__(image, random.randint(0, 2))
        self.rect.y = SCREEN_HEIGHT - 260  # Move large cactus higher


class BirdIndex(Obstacle):
    def __init__(self, image):
        super().__init__(image, 0)
        self.rect.y = SCREEN_HEIGHT - 320  # Move bird_img higher above the dinosaur
        self.index = 0  # Initialize the index attribute

    def draw(self, SCREEN):
        self.index = (self.index + 1) % 10  # Update the index for animation
        SCREEN.blit(self.image[self.index // 5], self.rect)


# Modify the main game loop to use the updated layering system
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    MAX_SPEED = 30
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []

    def score():
        global points, game_speed
        points += 1
        if points % 200 == 0 and game_speed < MAX_SPEED:
            game_speed += 1
        text = font.render(f"Points: {points}", True, (0, 0, 0))
        SCREEN.blit(text, (1000, 40))

    def background():
        global x_pos_bg
        image_width = ground.get_width()
        SCREEN.blit(ground, (x_pos_bg, SCREEN_HEIGHT - 200))  # Move background higher
        SCREEN.blit(ground, (image_width + x_pos_bg, SCREEN_HEIGHT - 200))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if not obstacles:
            choice = random.randint(0, 2)
            obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1500)
                break  # Stop the game loop immediately

        background()
        cloud.draw(SCREEN)
        cloud.update()
        score()

        clock.tick(30)
        pygame.display.update()

    game_over()

def difficulty_menu():  # Accept x_pos_bg and y_pos_bg as arguments
    button_width = 200
    button_height = 50
    spacing = 20  # Space between buttons
    button_x = (SCREEN_WIDTH - button_width) // 2  # Center the buttons horizontally
    start_y = (SCREEN_HEIGHT - (3 * button_height + 2 * spacing)) // 2  # Center the column vertically

    # Load the custom fonts
    title_font = pygame.font.Font('Font/monogram.ttf', 80)  # Larger font size for "Difficulty"
    button_font = pygame.font.Font('Font/monogram.ttf', 40)  # Smaller font size for buttons

    frame_index = 0  # To track the current frame of the background animation
    frame_delay = 5  # Number of frames to wait before updating the background frame
    frame_counter = 0  # Counter to control the frame delay
    clock = pygame.time.Clock()  # To control the frame rate

    while True:
        frame_counter = (frame_counter + 1) % frame_delay
        SCREEN.blit(background_frames[frame_index], (0, 0))

        # Render the "Difficulty" title
        text = title_font.render("Difficulty", True, (255, 255, 255))  # Render the text in white
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3.9))  # Center the title

        # Draw buttons in a column
        button_easy = pygame.Rect(button_x, start_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_easy, border_radius=10, width=2)  # Border only
        button_text_easy = button_font.render("EASY", True, (255, 255, 255))  # Render the button text in white
        SCREEN.blit(button_text_easy, (button_x + (button_width - button_text_easy.get_width()) // 2,
                                       start_y + (button_height - button_text_easy.get_height()) // 2))

        button_medium = pygame.Rect(button_x, start_y + button_height + spacing, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_medium, border_radius=10, width=2)  # Border only
        button_text_medium = button_font.render("MEDIUM", True, (255, 255, 255))  # Render the button text in white
        SCREEN.blit(button_text_medium, (button_x + (button_width - button_text_medium.get_width()) // 2,
                                         start_y + button_height + spacing + (button_height - button_text_medium.get_height()) // 2))

        button_hard = pygame.Rect(button_x, start_y + 2 * (button_height + spacing), button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_hard, border_radius=10, width=2)  # Border only
        button_text_hard = button_font.render("HARD", True, (255, 255, 255))  # Render the button text in white
        SCREEN.blit(button_text_hard, (button_x + (button_width - button_text_hard.get_width()) // 2,
                                       start_y + 2 * (button_height + spacing) + (button_height - button_text_hard.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the program cleanly
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_easy.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    easy_mode()  # Call easy_mode() when the button is clicked
                elif button_medium.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    menu()
                elif button_hard.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    menu()

        clock.tick(30)  # Adjust the frame rate (30 FPS for the game loop)


def easy_mode():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 25
    max_speed = 40
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    complete = False
    levels = 1
    last_spawned_type = None  # Track the last spawned obstacle type
    spawn_count = 0  # Count consecutive spawns of the same type

    font = pygame.font.Font('Font/monogram.ttf', 50)  # Adjusted font size for better visibility
    obstacles = []

    def score():
        global points, game_speed, levels

        points += 1

        # Define levels at specific points
        if points >= 3000:
            levels = 5
        elif points >= 1800:
            levels = 4
        elif points >= 800:
            levels = 3
        elif points >= 300:
            levels = 2
        else:
            levels = 1

        # Increase speed every 200 points (up to max speed)
        if points % 200 == 0 and game_speed < max_speed:
            game_speed += 1

        # Display Level
        text_level = font.render(f"Level: {levels}", True, (0, 0, 0))
        SCREEN.blit(text_level, (10, 20))

        # Display Points
        text_score = font.render(f"Points: {points}", True, (0, 0, 0))
        SCREEN.blit(text_score, (10, 60))

    def background():
        global x_pos_bg
        image_width = ground.get_width()
        SCREEN.blit(ground, (x_pos_bg, SCREEN_HEIGHT - 200))  # Move background higher
        SCREEN.blit(ground, (image_width + x_pos_bg, SCREEN_HEIGHT - 200))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if not obstacles:
            # Spawn obstacles based on the current level
            obstacle_classes = [SmallCactus, LargeCactus, BirdIndex]
            obstacle_images = [small_cactus, large_cactus, bird_img]

            if levels == 1:  # Level 1: Only small cacti
                selected_class = SmallCactus
                selected_image = small_cactus
            elif levels == 2:  # Level 2: Small cacti and birds
                choice = random.randint(0, 1)
                selected_class = [SmallCactus, BirdIndex][choice]
                selected_image = [small_cactus, bird_img][choice]
            elif levels == 3:  # Level 3: Small, large cacti, and birds
                choice = random.randint(0, 2)
                selected_class = obstacle_classes[choice]
                selected_image = obstacle_images[choice]
            elif levels == 4:  # Level 4: Faster spawning
                choice = random.randint(0, 2)
                selected_class = obstacle_classes[choice]
                selected_image = obstacle_images[choice]
            elif levels == 5:  # Level 5: Same as level 4 but spawn objects side by side
                choice = random.randint(0, 2)
                selected_class = obstacle_classes[choice]
                selected_image = obstacle_images[choice]
                obstacles.append(selected_class(selected_image))  # Spawn the first object
                obstacles.append(selected_class(selected_image))  # Spawn the second object side by side

            # Update the last spawned type and reset or increment the spawn count
            if levels < 5:  # Levels 1-4
                if selected_class == last_spawned_type:
                    spawn_count += 1
                else:
                    spawn_count = 1
                    last_spawned_type = selected_class

                # Append the new obstacle
                obstacles.append(selected_class(selected_image))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(0)
                run = False  # Stop the game loop immediately
                break  # Exit the obstacle loop
            elif points >= 4250:
                complete = True
                run = False  # Stop the game loop immediately
                break  # Exit the obstacle loop

        background()
        cloud.draw(SCREEN)
        cloud.update()
        score()

        clock.tick(30)
        pygame.display.update()
    if complete:
        level_completed()  # Pass the current background position to game_over()
    else:
        game_over()

def game_over():  # Remove x_pos_bg and y_pos_bg arguments
    button_width = 200
    button_height = 50
    spacing = 20  # Space between buttons
    total_width = 3 * button_width + 2 * spacing  # Total width of all buttons and spacing
    start_x = (SCREEN_WIDTH - total_width) // 2  # Starting x-coordinate for the first button
    button_y = (SCREEN_HEIGHT - button_height) // 2  # Center the button vertically

    clock = pygame.time.Clock()  # Define clock to control the frame rate

    while True:
        # Stop the background at the exact position where the dino bumped
        image_width = ground.get_width()

        font = pygame.font.Font('Font/monogram.ttf', 100)  # Font size for "Dino Game"
        text = font.render("Game Over", True, (255, 0, 0))
        SCREEN.blit(text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))

        # Draw "LEVEL" button
        button_level = pygame.Rect(start_x, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_level, border_radius=25)
        button_text_level = font.render("LEVEL", True, (0, 0, 0))
        SCREEN.blit(button_text_level, (start_x + (button_width - button_text_level.get_width()) // 2,
                                          button_y + (button_height - button_text_level.get_height()) // 2))

        # Draw "HOME" button
        button_home = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_home, border_radius=25)
        button_text_home = font.render("HOME", True, (0, 0, 0))
        SCREEN.blit(button_text_home, (start_x + button_width + spacing + (button_width - button_text_home.get_width()) // 2,
                                       button_y + (button_height - button_text_home.get_height()) // 2))

        # Draw "RESTART" button
        button_restart = pygame.Rect(start_x + 2 * (button_width + spacing), button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_restart, border_radius=25)
        button_text_restart = font.render("RESTART", True, (0, 0, 0))
        SCREEN.blit(button_text_restart, (start_x + 2 * (button_width + spacing) + (button_width - button_text_restart.get_width()) // 2,
                                        button_y + (button_height - button_text_restart.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the program cleanly
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_restart.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    main()
                elif button_home.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    menu()
                elif button_level.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    difficulty_menu()  # Pass the background position

        clock.tick(30)  # Adjust the frame rate (30 FPS for the game loop)

def level_completed():  # Remove x_pos_bg and y_pos_bg arguments
    button_width = 200
    button_height = 50
    spacing = 20  # Space between buttons
    total_width = 3 * button_width + 2 * spacing  # Total width of all buttons and spacing
    start_x = (SCREEN_WIDTH - total_width) // 2  # Starting x-coordinate for the first button
    button_y = (SCREEN_HEIGHT - button_height) // 2  # Center the button vertically

    clock = pygame.time.Clock()  # Define clock to control the frame rate

    while True:
        # Stop the background at the exact position where the dino bumped
        image_width = ground.get_width()

        font = pygame.font.Font('Font/monogram.ttf', 100)  # Font size for "Dino Game"
        text = font.render("Well Done!", True, (255, 0, 0))
        SCREEN.blit(text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))

        # Draw "LEVEL" button
        button_level = pygame.Rect(start_x, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_level, border_radius=25)
        button_text_level = font.render("LEVEL", True, (0, 0, 0))
        SCREEN.blit(button_text_level, (start_x + (button_width - button_text_level.get_width()) // 2,
                                          button_y + (button_height - button_text_level.get_height()) // 2))

        # Draw "HOME" button
        button_home = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_home, border_radius=25)
        button_text_home = font.render("HOME", True, (0, 0, 0))
        SCREEN.blit(button_text_home, (start_x + button_width + spacing + (button_width - button_text_home.get_width()) // 2,
                                       button_y + (button_height - button_text_home.get_height()) // 2))

        # Draw "RESTART" button
        button_restart = pygame.Rect(start_x + 2 * (button_width + spacing), button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_restart, border_radius=25)
        button_text_restart = font.render("RESTART", True, (0, 0, 0))
        SCREEN.blit(button_text_restart, (start_x + 2 * (button_width + spacing) + (button_width - button_text_restart.get_width()) // 2,
                                        button_y + (button_height - button_text_restart.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the program cleanly
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_restart.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    main()
                elif button_home.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    menu()
                elif button_level.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    difficulty_menu()  # Pass the background position

        clock.tick(30)  # Adjust the frame rate (30 FPS for the game loop)

def menu():
    button_width = 100  # Width of the "Start" button
    button_height = 30  # Height of the "Start" button
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = (SCREEN_HEIGHT - button_height) // 2  # Center the button vertically

    # Load the custom font
    font = pygame.font.Font('Font/monogram.ttf', 100)  # Font size for "Dino Game"
    font.set_bold(True)  # Enable bold text

    frame_index = 0  # To track the current frame of the background animation
    frame_delay = 5  # Number of frames to wait before updating the background frame
    frame_counter = 0  # Counter to control the frame delay
    clock = pygame.time.Clock()  # To control the frame rate

    while True:
        # Clear the screen to avoid overlay issues
        SCREEN.fill((255, 255, 255))

        # Draw the animated background
        if frame_counter == 0:
            frame_index = (frame_index + 1) % len(background_frames)
        frame_counter = (frame_counter + 1) % frame_delay
        SCREEN.blit(background_frames[frame_index], (0, 0))

        # Render the title text using the custom font
        text = font.render("Dino Game", True, (255, 255, 255))  # Render the text in white
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.4))  # Adjust position for larger text
        SCREEN.blit(text, text_rect)

        # Reset bold if needed for other text
        font.set_bold(False)

        # Draw the larger white border for the "Start" button
        border_width = button_width + 70  # Increase the border width
        border_height = button_height + 10  # Increase the border height
        border_x = button_x - 38 # Adjust the x position to center the larger border
        border_y = button_y - 2  # Adjust the y position to center the larger border
        button_border = pygame.Rect(border_x, border_y, border_width, border_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_border, width=2, border_radius=10)  # Border only

        # Render the "Start" button text
        button_font = pygame.font.Font('Font/monogram.ttf', 40)  # Smaller font size for the "Start" button
        button_text = button_font.render("Start", True, (255, 255, 255))  # Render the button text in white
        SCREEN.blit(button_text, (button_x + (button_width - button_text.get_width()) // 2,
                                  button_y + (button_height - button_text.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the program cleanly
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    play_button_sound()  # Play sound effect
                    difficulty_menu()  # Call the difficulty menu when the button is clicked

        clock.tick(30)  # Adjust the frame rate (30 FPS for the game loop)

menu()

