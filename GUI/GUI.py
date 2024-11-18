# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
HIGHLIGHT_BLUE = (40, 40, 255)

def draw_alu(surface, color, x, y, width, height):
    # Define the points of the ALU shape
    points = [
        (x, y),  # Top-left
        (x + width * 0.8, y),  # Top-right
        (x + width, y + height * 0.5),  # Middle-right
        (x + width * 0.8, y + height),  # Bottom-right
        (x, y + height),  # Bottom-left
        (x + width * 0.2, y + height * 0.5)  # Middle-left
    ]
    # Draw the shape
    pygame.draw.polygon(surface, color, points)

# Function to draw a rectangle
def draw_rectangle(surface, color, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))

# Function to draw a circle
def draw_circle(surface, color, center, radius):
    pygame.draw.circle(surface, color, center, radius)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    #draw_rectangle(screen, BLUE, 200, 150, 400, 300)
    #draw_circle(screen, BLUE, (400, 300), 50)
    draw_alu(screen, BLUE, 300, 200, 200, 300)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()



