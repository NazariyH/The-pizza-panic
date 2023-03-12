# main file game
# create interface

import pygame
import random
import pan_move as pm

display_width = 1920  # Display width
display_height = 1080  # Display height

sky_width = display_width  # Sky width
sky_height = 300  # Sky height

pan_width = 140  # Pan width
pan_height = 70  # Pan height

mouse_x = (display_width - pan_width) / 2  # Default mouse X position
mouse_y = (display_height - pan_height) / 2  # Default mouse Y position

scores = 0  # Start scores
scores_x = 1700  # Scores position x
scores_y = 70  # Scores position y

heart_size = (50, 50)  # Heart size
heart_margin = 0  # Heart margin
heart_x = 100  # Heart position x
heart_y = 70  # Heart position y

pizza_in_game = []  # Pizza in game
pizza_speed = 5  # Pizza move speed
pizza_speed_spawn = 1000  # Pizza speed spawn
pizza_size = (150, 150)  # Pizza size
pizza_x = 0  # Pizza default x position
pizza_y = 70  # Pizza y position

cola_size = (150, 150)  # Cola size
cola_speed = pizza_speed  # Cola move speed
cola_in_game = []  # Cola in game
cola_x = 0  # Cola default x position
cola_y = 70  # Cola y position

def change_fast_game():
    """Speeding up the game"""
    global pizza_speed, cola_speed
    if scores >= 500 and scores < 900:
        pizza_speed = 10
        cola_speed = 10
    elif scores >= 900:
        if pizza_speed != 9:
            pygame.time.set_timer(pizza_timer, 0)  # Delete old timer
            pygame.time.set_timer(pizza_timer, 300)  # Create new timer

        pizza_speed = 9
        cola_speed = 9



def scores_update():
    """Scores update"""
    global scores
    scores_text = scores_fonts.render(f"{int(scores)}", True, (255, 255, 255))  # Create text
    screen.blit(scores_text, (scores_x, scores_y))  # Set text on display
    scores += 0.1

def show_health():
    """Draw heart on screen"""
    global health, heart_margin

    if health:
        for (i, el) in enumerate(health):
            heart_margin += 100
            if heart_margin == len(health) * 100:
                heart_margin = 0

            screen.blit(heart_image, (heart_x + heart_margin, heart_y))
    else:
        finish_sound.play(-1)  # Play finish sound
        end_game()

def create_pizza(pan_rect):
    """Create pizza and check collision with pan"""
    if pizza_in_game:
        for (i, el) in enumerate(pizza_in_game):
            screen.blit(pizza, el)  # Set pizza in display
            el.y += pizza_speed  # Pizza falls to the bottom

            if el.y > 1080:
                lost_sound.play()  # Play lost sound
                health.pop(-1)  # Remove one health when pizza fall to the bottom
                pizza_in_game.pop(i)  # Remove pizza which fall to the bottom

            if pan_rect.colliderect(el):
                eating_sound.play()  # Play eating sound
                pizza_in_game.pop(i)  # Remove pizza which collision with pan
    if cola_in_game:
        for (i, el) in enumerate(cola_in_game):
            screen.blit(cola, el)  # Set cola in display
            el.y += cola_speed  # Cola falls to the bottom

            if el.y > 1080:
                lost_sound.play()  # Play lost sound
                health.pop(-1)  # Remove one health when cola fall to the bottom
                cola_in_game.pop(i)  # Remove cola which fall to the bottom

            if pan_rect.colliderect(el):
                drinking_sound.play()  # Play drinking sound
                if len(health) < 10:
                    health.append(heart_image)  # Add one health when cola collision with pan
                cola_in_game.pop(i)  # Remove cola which collision with pan

def pan_move():
    """Move pan"""
    the_pan = pm.Pan(mouse_x, mouse_y, screen, pan)
    move_x, move_y = the_pan.move()
    screen.blit(pan, (move_x - pan_width / 2,move_y - pan_height / 2))  # Set pan
    pan_rect = pan.get_rect(topleft=(move_x - pan_width / 2, move_y - pan_height / 2))  # Create pan rect

    return pan_rect

def end_game():
    """End Game"""
    global gameplay

    gameplay = False
    pygame.mixer.music.stop()  # stop play background sound
    screen.blit(game_over, (display_width / 2 - 220, display_height / 2 - 100))  # Set text on display
    screen.blit(restart, (display_width / 2 - 220, display_height / 2))  # Set text on display
    player_control()  # Check on restart, when player press space

def player_control():
    """Check on pressed key"""
    global gameplay, scores, health, pizza_speed, cola_speed
    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        finish_sound.stop()  # Stop play finish sound
        pygame.mixer.music.play()  # Play play background sound
        gameplay = True  # Duration of the game
        pizza_in_game.clear() 
        scores = 0  # Scores counter
        health = [heart_image] * 5  # Health player
        pizza_speed = 5
        cola_speed = 5


clock = pygame.time.Clock()  # Create clock
pygame.init()  # Initialization game

screen = pygame.display.set_mode((display_width, display_height))  # Set display size
pygame.display.set_caption("Panic In The Pizzerla")  # Set title
pygame.mouse.set_visible(False)  # Hide cursor

bg = pygame.image.load("images/wall.jpg").convert()  # Load background image
bg = pygame.transform.scale(bg, (display_width, display_height)) # Set background image display size

sky = pygame.image.load("images/sky.jpg").convert()  # Load sky image
sky = pygame.transform.scale(sky, (sky_width, sky_height))  # Set sky size

pan = pygame.image.load("images/pan.png").convert_alpha()  # Load pan
pan = pygame.transform.scale(pan, (pan_width, pan_height))  # Set pan size

heart_image = pygame.image.load("images/heart.png").convert_alpha()  # Load heart image
heart_image = pygame.transform.scale(heart_image, heart_size)  # Change size image heart
health = [heart_image] * 5  # Number of lives

pizza = pygame.image.load("images/pizza.png").convert_alpha()  # Load pizza image
pizza = pygame.transform.scale(pizza, pizza_size)  # Change pizza size

cola = pygame.image.load("images/cola.png").convert_alpha()  # Load cola image
cola = pygame.transform.scale(cola, cola_size)  # Change cola size

pygame.mixer.music.load("sound/bgSound.mp3")  # Load background music
pygame.mixer.music.play(-1)  # Infinite play background music

finish_sound = pygame.mixer.Sound("sound/finish.mp3")  # Load finish sound
eating_sound = pygame.mixer.Sound("sound/eating.mp3")  # Load eating sound
drinking_sound = pygame.mixer.Sound("sound/drinking.mp3")  # Load drinking sound
lost_sound = pygame.mixer.Sound("sound/lost.mp3")  # Load lost sound


finish_font = pygame.font.Font("fonts/GolosText-VariableFont_wght.ttf", 100)  # Load font
restart_font = pygame.font.Font("fonts/GolosText-VariableFont_wght.ttf", 50)  # Load font
scores_fonts = pygame.font.Font("fonts/GolosText-VariableFont_wght.ttf", 50)  # Load font

game_over = finish_font.render("Game Over", True, (0, 0, 0))  # Create text
restart = restart_font.render("Press space to restart", True, (0, 0, 0))  # Create text



gameplay = True  # Duration of the game

pizza_timer = pygame.USEREVENT + 1  # Creatr timer
pygame.time.set_timer(pizza_timer, 1000)  # Set timer

running = True

def updates():
    """Updates game"""
    global mouse_x, mouse_y, running

    while running:
        screen.blit(bg, (0, 0))  # Set background image
        screen.blit(sky, (0, 0))  # Set sky image

        if gameplay:
            scores_update()  # Call scores update
            show_health()  # Show heart
            pan_rect = pan_move()  # Move pan
            create_pizza(pan_rect)  # Create pizza and check collision with pan
            change_fast_game()  # Call speeding up the game
        else:
            end_game()  # Call end game
            
        pygame.display.update()  # Update game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Stop game
                pygame.quit()  # Quit game
            if event.type == pizza_timer:
                random_value = random.randint(0, 20)  # if random_value is equal to 0, create cola 
                if random_value != 0:
                    pizza_x = random.randint(0, display_width - pizza_size[0])  # Randint random position X for pizza
                    pizza_in_game.append(pizza.get_rect(topleft=(pizza_x, pizza_y)))  # Creatr rect model for pizza
                else:
                    cola_x = random.randint(0, display_width - pizza_size[0])  # Randint random position X for cola
                    cola_in_game.append(cola.get_rect(topleft=(cola_x, cola_y)))  # Creatr rect model for cola

        clock.tick(90)


updates()  # Call game
