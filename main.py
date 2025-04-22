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

dead_dino = pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png"))
small_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
large_cactus = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

bird_img= [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "cloud1.png"))


background = pygame.image.load(os.path.join("BackG/", "bg-night.gif"))
ground = pygame.image.load(os.path.join("Assets/Other", "ground1.png"))

# Load and scale the animated background frames
home_bg_frames = [
    pygame.transform.scale(
        pygame.image.load(os.path.join("BackG/", f"a{i}.png")), (SCREEN_WIDTH, SCREEN_HEIGHT)
    ) for i in range(1, 21)
]

ongame_bg_frames = [pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert() for _ in [None] * 1]
for frame in ongame_bg_frames:
    frame.fill((180, 225, 236))  # Fill each frame with sky blue color

# Load the sound effect
button_click_sound = pygame.mixer.Sound('Sound/S1.mp3')  # Ensure S1.mp3 is in the correct path

# Function to play the sound effect
def play_button_sound():
    button_click_sound.play()

class Dinosaur:
    X_POS = 80
    Y_POS = SCREEN_HEIGHT - 263  # Move Dino higher
    Y_POS_DUCK = SCREEN_HEIGHT - 224  # Move ducking position higher
    JUMP_VEL = 7

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = dead_dino

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.dino_dead = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect(x=self.X_POS, y=self.Y_POS)
        self.dino_rect.inflate_ip(-30, -20)  # Shrink the hitbox by 20px width and 10px height

    def update(self, userInput):
        if self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_dead:
            self.dead()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_DOWN]:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL  # Reset jump velocity to stop jumping immediately
        elif userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif not (self.dino_jump or userInput[pygame.K_DOWN] or userInput[pygame.K_UP]):
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

    def dead(self):
        self.image = self.dead_img  # Use the correct dead image
        # Align the dinosaur with the ground or obstacle
        self.dino_rect.y = self.Y_POS
        self.dino_rect = self.image.get_rect(center=self.dino_rect.center)
        self.dino_duck = False
        self.dino_run = False
        self.dino_jump = False

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(-10, 300)
        self.y = random.randint(-50, 200)
        self.image = pygame.transform.scale(CLOUD, (450, 200))  # Resize the cloud image to 100x50
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(-10, 300)
            self.y = random.randint(-50, 200)

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
        self.rect.y = SCREEN_HEIGHT - 320  # Move bird higher above the dinosaur
        self.step_index = 0  # To track the animation frame

    def draw(self, SCREEN):
        # Alternate between Bird1 and Bird2 based on the step_index
        self.image = bird_img[self.step_index // 5]  # Switch frame every 5 steps
        SCREEN.blit(self.image, self.rect)
        self.step_index += 1
        if self.step_index >= 10:  # Reset step_index after both frames
            self.step_index = 0



class OnGameBackground:
    def __init__(self, z_index=0):
        self.frame_index = 0  # To track the current frame of the background animation
        self.frame_delay = 5  # Number of frames to wait before updating the background frame
        self.frame_counter = 0  # Counter to control the frame delay
        self.z_index = z_index  # zIndex to determine the drawing order

    def update(self):
        self.frame_counter = (self.frame_counter + 1) % self.frame_delay
        if self.frame_counter == 0:
            self.frame_index = (self.frame_index + 1) % len(ongame_bg_frames)

    def draw(self, SCREEN):
        SCREEN.blit(ongame_bg_frames[self.frame_index], (0, 0))

    


# Modify the main game loop to use the updated layering system
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    max_speed = 30
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    levels = 1  # Initialize levels
    obstacles = []

    font = pygame.font.Font('freesansbold.ttf', 20)

    def score():
        global points, game_speed, levels
        points += 1
        levels = points // 500  # Update levels dynamically based on points

        if points % 200 == 0 and game_speed < max_speed:
            game_speed += 1

        # Display level and points
        text_level = font.render(f"Level: {levels + 1}", True, (0, 0, 0))
        SCREEN.blit(text_level, (10, 20))
        text_score = font.render(f"Points: {points}", True, (0, 0, 0))
        SCREEN.blit(text_score, (10, 40))

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

        # Add obstacles based on levels
        if not obstacles:
            if levels == 0:  # Level 1: Only small cacti
                obstacles.append(BirdIndex(bird_img))
            elif levels == 1:  # Level 2: Small cacti and birds
                if random.choice([True, False]):
                    obstacles.append(SmallCactus(small_cactus))
                else:
                    obstacles.append(BirdIndex(bird_img))
            elif levels == 2:  # Level 3: Small, large cacti, and birds
                choice = random.randint(0, 2)
                if choice == 0:
                    obstacles.append(SmallCactus(small_cactus))
                elif choice == 1:
                    obstacles.append(LargeCactus(large_cactus))
                else:
                    obstacles.append(BirdIndex(bird_img))
            elif levels == 3:  # Level 4: Faster spawning
                choice = random.randint(0, 2)
                if choice == 0:
                    obstacles.append(SmallCactus(small_cactus))
                elif choice == 1:
                    obstacles.append(LargeCactus(large_cactus))
                else:
                    obstacles.append(BirdIndex(bird_img))
            elif levels >= 4:  # Level 5: Spawn objects side by side
                choice = random.randint(0, 2)
                if choice == 0:
                    obstacles.append(SmallCactus(small_cactus))
                    obstacles.append(SmallCactus(small_cactus))
                elif choice == 1:
                    obstacles.append(LargeCactus(large_cactus))
                    obstacles.append(LargeCactus(large_cactus))
                else:
                    obstacles.append(BirdIndex(bird_img))
                    obstacles.append(BirdIndex(bird_img))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                player.dead()  # Trigger the dead state
                pygame.time.delay(1500)
                run = False  # Stop the game loop immediately
                break  # Exit the obstacle loop

        background()
        cloud.draw(SCREEN)
        cloud.update()
        score()

        clock.tick(30)
        pygame.display.update()

    game_over("main")

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
        if frame_counter == 0:
            frame_index = (frame_index + 1) % len(home_bg_frames)
        frame_counter = (frame_counter + 1) % frame_delay
        SCREEN.blit(home_bg_frames[frame_index], (0, 0))

        # Render the "Difficulty" title
        text = title_font.render("Difficulty", True, (255, 255, 255))  # Render the text in white
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3.9))  # Center the title

        # Draw buttons in a column
        button_easy = pygame.Rect(button_x, start_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_easy, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_easy, border_radius=10, width=2)  # Border
        button_text_easy = button_font.render("EASY", True, (0, 0, 0))  # Black text
        SCREEN.blit(button_text_easy, (button_x + (button_width - button_text_easy.get_width()) // 2,
                                       start_y + (button_height - button_text_easy.get_height()) // 2))

        button_medium = pygame.Rect(button_x, start_y + button_height + spacing, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_medium, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_medium, border_radius=10, width=2)  # Border
        button_text_medium = button_font.render("MEDIUM", True, (0, 0, 0))  # Black text
        SCREEN.blit(button_text_medium, (button_x + (button_width - button_text_medium.get_width()) // 2,
                                         start_y + button_height + spacing + (button_height - button_text_medium.get_height()) // 2))

        button_hard = pygame.Rect(button_x, start_y + 2 * (button_height + spacing), button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_hard, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_hard, border_radius=10, width=2)  # Border
        button_text_hard = button_font.render("HARD", True, (0, 0, 0))  # Black text
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
                    meduim_mode()  # Call medium_mode() when the button is clicked
                elif button_hard.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    menu()

        clock.tick(30)  # Adjust the frame rate (30 FPS for the game loop)

def easy_mode():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, levels
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
    levels = 0
    gameBG = OnGameBackground()  # Create an instance of the OnGameBackground class

    

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
        elif points < 300:
            levels = 1

        # Increase speed every 200 points (up to max speed)
        if points % 200 == 0 and game_speed < max_speed:
            game_speed += 1

        # Display Level
        text_level = font.render(f"Level: {levels}", True, (0, 0, 0))
        SCREEN.blit(text_level, (10, 20))
       #text_speed = font.render(f"Game Speed: {game_speed}", True, (0, 0, 0))
        # SCREEN.blit(text_speed, (10, 80))

        # Display Points
        if points > 4250:
            points = 4250  # Cap the points at 4250
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

        gameBG.draw(SCREEN)
        gameBG.update()
        player.draw(SCREEN)
        player.update(userInput)

          # Add obstacles based on levels
        if not obstacles:
            if levels == 1:  # Level 1: Only small cacti
                obstacles.append(SmallCactus(small_cactus))
                
            elif levels == 2:  # Level 2: Small cacti and birds
                choice = random.randint(0, 1)
                obstacles.append([SmallCactus, BirdIndex][choice]([small_cactus, bird_img][choice]))

            elif levels >= 3:  # Level 3: 2 obstacles

                choice = random.randint(0, 2)
                obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                obstacles[-1].rect.x += 0 # Adjust x-axis for spacing

                chances = random.randint(0, 4)
                if chances == 0:
                    pass
                else:
                    choice1 = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                    obstacles[-1].rect.x += 650 # Adjust x-axis for spacing
                    if levels >= 4 and chances > 0: 
                        # Level 4: Chances of spawning 3 obstacles
                        choice1 = random.randint(0, 4)
                        if choice1 == 0:  # 1/4 chance to spawn no obstacle
                            pass
                        else:
                            choice1 = random.randint(0, 2)
                            obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                            obstacles[-1].rect.x += 1300# Adjust x-axis for spacing

                    elif levels >= 5 and chances > 0:
                        # Level 5: Chances of spawning 4 obstacles or 3 obstacles with 1pair of obstacles
                        
                        choice1 = random.randint(0, 5)
                        if choice1 == 0:
                            pass
                        elif choice1 >= 1 :
                            if random.choice([True, False, False]):
                                # 2 obstacles

                                choice1 = random.randint(0, 2)
                                obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                                obstacles[-1].rect.x += 1800# Adjust x-axis for spacing
                                choice2 = random.randint(0, 2)
                                obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice2]([small_cactus, large_cactus, bird_img][choice2]))
                                obstacles[-1].rect.x += 2600# Adjust x-axis for spacing
                        elif choice1 >= 4:
                            choice = random.randint(0, 4)
                            if choice >= 3:

                                # 1pair of obstacle + single obstacle

                                obs_chances = random.randint(0, 2)
                                obstacles.append([SmallCactus, LargeCactus][obs_chances]([small_cactus, large_cactus][obs_chances]))
                                obstacles[-1].rect.x += 1800
                                obstacles.append([SmallCactus, LargeCactus][obs_chances]([small_cactus, large_cactus][obs_chances]))
                                obstacles[-1].rect.x += 1875

                                choice1 = random.randint(0, 2)
                                obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                                obstacles[-1].rect.x += 2600
                            
                              

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
        game_over("easy")

def meduim_mode():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, levels
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 30
    max_speed = 50
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    complete = False
    levels = 0
    gameBG = OnGameBackground()  # Create an instance of the OnGameBackground class

    font = pygame.font.Font('Font/monogram.ttf', 50)  # Adjusted font size for better visibility
    obstacles = []

    def score():
        global points, game_speed, levels

        points += 1

        # Define levels at specific points
        if points >= 5300:
            levels = 5
        elif points >= 3800:
            levels = 4
        elif points >= 2500:
            levels = 3
        elif points >= 1250:
            levels = 2
        elif points < 500:
            levels = 1

        # Increase speed every 200 points (up to max speed)
        if points % 200 == 0 and game_speed < max_speed:
            game_speed += 1

        # Display Level
        text_level = font.render(f"Level: {levels}", True, (0, 0, 0))
        SCREEN.blit(text_level, (10, 20))
        # text_difficulty = font.render(f"Difficulty: Medium", True, (0, 0, 0))
        # SCREEN.blit(text_difficulty, (800, 20))
        # text_speed = font.render(f"Game Speed: {game_speed}", True, (0, 0, 0))
        # SCREEN.blit(text_speed, (10, 80))

        # Display Points
        if points > 7000:
            points = 7000  # Cap the points at 7000
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

        gameBG.draw(SCREEN)
        gameBG.update()
        player.draw(SCREEN)
        player.update(userInput)

        # Add obstacles based on levels
        if not obstacles:
            if levels == 1:  
                # Level 1:
                # 1/8 chances of no obstacles
                
                chances = random.randint(0, 4)

                if chances == 0:
                    pass
                elif chances >= 1:
                    choice = random.randint(0, 2)  
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                    obstacles[-1].rect.x += 50 # Adjust x-axis for spacing
                    choice1 = random.randint(0, 2)  
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                    obstacles[-1].rect.x += 600 # Adjust x-axis for spacing
                    choice2 = random.randint(0, 2)  
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice2]([small_cactus, large_cactus, bird_img][choice2]))
                    obstacles[-1].rect.x += 1200 # Adjust x-axis for spacing

                    chances1 = random.randint(0, 5)
                    if chances1 >= 1: 
                        pass
                    else:
                        choice = random.randint(0, 2)  
                        obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                        obstacles[-1].rect.x += 1800 # Adjust x-axis for spacing


            elif levels >= 2:  # Level 2: Spawn objects side by side

                    chances = random.randint(0, 6)

                    if chances == 0:
                        pass
                    elif chances >= 1:
                        choice = random.randint(0, 2)  
                        obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                        obstacles[-1].rect.x += 50 # Adjust x-axis for spacing
                        choice1 = random.randint(0, 2)  
                        obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                        obstacles[-1].rect.x += 600 # Adjust x-axis for spacing
                        choice2 = random.randint(0, 2)  
                        obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice2]([small_cactus, large_cactus, bird_img][choice2]))
                        obstacles[-1].rect.x += 1200 # Adjust x-axis for spacing
                    if choice1 == 0: 
                        pass
                    else:
                        choice = random.randint(0, 2)  
                        obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                        obstacles[-1].rect.x += 1800 # Adjust x-axis for spacing


            elif levels >= 3:  # Level 3: Spawn objects side by side
                # Pass 1/6 || 3 obsacles 3/6 || 4 obstacles 2/6
                choice1 = random.randint(0, 7)
                if choice1 == 0:
                    pass
                elif choice1 >= 1:
                    choice = random.randint(0, 1)
                    # choice3 = random.randint(0, 2)
                    if choice == 0:
                        choice = random.randint(0, 1)
                        choice1 = random.randint(0, 1)
                        choice2 = random.randint(0, 2)
                        obstacles.append([SmallCactus, LargeCactus][choice]([small_cactus, large_cactus][choice]))
                        obstacles[-1].rect.x += 50 # Adjust x-axis for spacing
                        obstacles.append([SmallCactus, LargeCactus][choice1]([small_cactus, large_cactus][choice1]))
                        obstacles[-1].rect.x += 75 # Adjust x-axis for spacing
                        obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice2]([small_cactus, large_cactus, bird_img][choice2]))
                        obstacles[-1].rect.x += random.randint(800, 900)  # Adjust x-axis for spacing
                    else:
                        choice = random.randint(0, 2)
                        choice1 = random.randint(0, 1)
                        choice2 = random.randint(0, 1)
                        obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                        obstacles[-1].rect.x += random.randint(50, 100)  # Adjust x-axis for spacing
                        obstacles.append([SmallCactus, LargeCactus][choice1]([small_cactus, large_cactus][choice1]))
                        obstacles[-1].rect.x += random.randint(750, 900)  # Adjust x-axis for spacing
                        obstacles.append([SmallCactus, LargeCactus][choice2]([small_cactus, large_cactus][choice2]))
                        obstacles[-1].rect.x += random.randint(800, 900)  # Adjust x-axis for spacing
                elif choice1 >= 5:
                    choice = random.randint(0, 2)
                    choice1 = random.randint(0, 1)
                    choice2 = random.randint(0, 1)
                    choice3 = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus][choice]))
                    obstacles[-1].rect.x += random.randint(50, 70)  # Adjust x-axis for spacing
                    obstacles.append([SmallCactus, LargeCactus][choice1]([small_cactus, large_cactus][choice1]))
                    obstacles[-1].rect.x += random.randint(75, 100)  # Adjust x-axis for spacing
                    obstacles.append([SmallCactus, LargeCactus][choice2]([small_cactus, large_cactus][choice2]))
                    obstacles[-1].rect.x += random.randint(800, 900)  # Adjust x-axis for spacing
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice3]([small_cactus, large_cactus, bird_img][choice3]))
                    obstacles[-1].rect.x += random.randint(825, 900)  # Adjust x-axis for spacing


                        # if choice3 >= 1:
                        #     choice = random.randint(0, 2)
                        #     choice1 = random.randint(0, 2)
                        #     choice2 = random.randint(0, 2)
                        #     if choice == 0:
                        #         obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                        #         obstacles[-1].rect.x += random.randint(50, 100)  # Adjust x-axis for spacing
                        #         obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                        #         obstacles[-1].rect.x += random.randint(500, 600)  # Adjust x-axis for spacing
                        #         obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice2]([small_cactus, large_cactus, bird_img][choice2]))
                        #         obstacles[-1].rect.x += random.randint(1300, 1400)  # Adjust x-axis for spacing

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(0)
                run = False  # Stop the game loop immediately
                break  # Exit the obstacle loop
            elif points >= 7000:
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
        game_over("medium")  # Pass "medium" mode to game_overmedium")

def game_over(difficulty):  # Remove x_pos_bg and y_pos_bg arguments
    button_width = 200
    button_height = 50
    spacing = 20  # Space between buttons
    total_width = 3 * button_width + 2 * spacing  # Total width of all buttons and spacing
    start_x = (SCREEN_WIDTH - total_width) // 2  # Starting x-coordinate for the first button
    button_y = (SCREEN_HEIGHT - button_height) // 2  # Center the button vertically

    # Load the custom font
    title_font = pygame.font.Font('Font/monogram.ttf', 80)  # Larger font size for "Game Over"
    button_font = pygame.font.Font('Font/monogram.ttf', 40)  # Smaller font size for buttons

    clock = pygame.time.Clock()  # Define clock to control the frame rate

    while True:
        # Stop the background at the exact position where the dino bumped
        image_width = ground.get_width()
        text = title_font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.5))
        SCREEN.blit(text, text_rect)

        # Draw "LEVEL" button
        button_level = pygame.Rect(start_x, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_level, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_level, border_radius=10, width=2)  # Border
        button_text_level = button_font.render("LEVEL", True, (0, 0, 0))  # Black text
        SCREEN.blit(button_text_level, (start_x + (button_width - button_text_level.get_width()) // 2,
                                        button_y + (button_height - button_text_level.get_height()) // 2))

        # Draw "HOME" button
        button_home = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_home, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_home, border_radius=10, width=2)  # Border
        button_text_home = button_font.render("HOME", True, (0, 0, 0))  # Black text
        SCREEN.blit(button_text_home, (start_x + button_width + spacing + (button_width - button_text_home.get_width()) // 2,
                                       button_y + (button_height - button_text_home.get_height()) // 2))

        # Draw "RESTART" button
        button_restart = pygame.Rect(start_x + 2 * (button_width + spacing), button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_restart, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_restart, border_radius=10, width=2)  # Border
        button_text_restart = button_font.render("RESTART", True, (0, 0, 0))  # Black text
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
                    if difficulty == "easy":
                        easy_mode()
                    elif difficulty == "medium":
                        meduim_mode()
                    else:
                        main()
                elif button_home.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    menu()  # Go back to the main menu
                elif button_level.collidepoint(mouse_x, mouse_y):
                    play_button_sound()  # Play sound effect
                    difficulty_menu()  # Go to the difficulty menu

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

        font = pygame.font.Font('Font/monogram.ttf', 80)  # Font size for "Well Done!"
        button_font = pygame.font.Font('Font/monogram.ttf', 40)  # Smaller font size for buttons

        text = font.render("Well Done!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        SCREEN.blit(text, text_rect)

        # Draw "LEVEL" button
        button_level = pygame.Rect(start_x, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_level, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_level, border_radius=10, width=2)  # Border
        button_text_level = button_font.render("LEVEL", True, (0, 0, 0))  # Black text
        SCREEN.blit(button_text_level, (start_x + (button_width - button_text_level.get_width()) // 2,
                        button_y + (button_height - button_text_level.get_height()) // 2))

        # Draw "HOME" button
        button_home = pygame.Rect(start_x + button_width + spacing, button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_home, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_home, border_radius=10, width=2)  # Border
        button_text_home = button_font.render("HOME", True, (0, 0, 0))  # Black text
        SCREEN.blit(button_text_home, (start_x + button_width + spacing + (button_width - button_text_home.get_width()) // 2,
                           button_y + (button_height - button_text_home.get_height()) // 2))

        # Draw "RESTART" button
        button_restart = pygame.Rect(start_x + 2 * (button_width + spacing), button_y, button_width, button_height)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_restart, border_radius=10)  # White background
        pygame.draw.rect(SCREEN, (255, 255, 255), button_restart, border_radius=10, width=2)  # Border
        button_text_restart = button_font.render("RESTART", True, (0, 0, 0))  # Black text
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
    font = pygame.font.Font('Font/monogram.ttf', 100)  # Font size for "Dinosaur Runner"
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
            frame_index = (frame_index + 1) % len(home_bg_frames)
        frame_counter = (frame_counter + 1) % frame_delay
        SCREEN.blit(home_bg_frames[frame_index], (0, 0))

        # Render the title text using the custom font
        text = font.render("Dinosaur Runner", True, (255, 255, 255))  # Render the text in white
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

        # Fill the button background with a color (e.g., white)
        pygame.draw.rect(SCREEN, (255, 255, 255), button_border, border_radius=10)

        # Draw the border for the button
        pygame.draw.rect(SCREEN, (255, 255, 255), button_border, width=2, border_radius=10)

        # Render the "Start" button text
        button_font = pygame.font.Font('Font/monogram.ttf', 40)  # Smaller font size for the "Start" button
        button_text = button_font.render("Start", True, (0, 0, 0))  # Render the button text in white
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

