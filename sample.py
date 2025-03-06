import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((600, 600)) #Set window

icon = pygame.image.load('uic_logo.png')
pygame.display.set_icon(icon)

running=True  #set game loop
playing = True

upFacing = True
downFacing = False
rightFacing = False
leftFacing = False

numPellets = 1
pelletX = [0, 600, 300, 300] #for the four possible positions of the pellets
pelletY = [300, 300, 0, 600]
pelletX_change = [0.06, -0.06, 0, 0]
pelletY_change = [0, 0, 0.06, -0.06]
pellet_direction = ['right', 'left', 'down', 'up']

userRect = pygame.Rect(270, 270, 60, 60)

pellet_add_delay = False
add_pellet_time = 0  # Store the time to add the next pellet
delay_duration = 1000  # Delay in milliseconds (1 second)
x=1

play_score = 0
font = pygame.font.Font('freesansbold.ttf', 30)
over_font = pygame.font.Font('freesansbold.ttf', 50)

def player():
    global upFacing, downFacing, rightFacing, leftFacing
    if (upFacing):
        pygame.draw.polygon(screen, (255, 0, 0), [(270, 270), (300, 300), (330, 270)])
    elif (downFacing):
        pygame.draw.polygon(screen, (255, 0, 0), [(270, 330), (300, 300), (330, 330)])
    elif (leftFacing):
        pygame.draw.polygon(screen, (255, 0, 0), [(270, 330), (300, 300), (270, 270)])
    elif (rightFacing):
        pygame.draw.polygon(screen, (255, 0, 0), [(330, 270), (300, 300), (330, 330)])

class pellet:
    def __init__(self, x, y, xChange, yChange, direction):
        self.x = x
        self.y = y
        self.xChange = xChange
        self.yChange = yChange
        self.direction = direction

    def displayPelt(pellet):
        pygame.draw.circle(screen, (255, 0, 0), (pellet.x, pellet.y), 15)

    def update(pellet):
        pellet.x += pellet.xChange
        pellet.y += pellet.yChange
    
    def reassign(self):
        random_numb = random.randint(0, 3)
        self.x = pelletX[random_numb]
        self.y = pelletY[random_numb]
        self.xChange = pelletX_change[random_numb]
        self.yChange = pelletY_change[random_numb]
        self.direction = pellet_direction[random_numb]

pellets = []
for i in range(numPellets):
    random_number = random.randint(0, 3)
    myPelt = pellet(pelletX[random_number], pelletY[random_number], pelletX_change[random_number], pelletY_change[random_number], pellet_direction[random_number])
    pellets.append(myPelt)

def addPellet():
    global numPellets
    numPellets+=1
    random_number = random.randint(0, 3)
    myPelt = pellet(pelletX[random_number], pelletY[random_number], pelletX_change[random_number], pelletY_change[random_number], pellet_direction[random_number])
    pellets.append(myPelt)

def showScore(x, y):
    score = font.render("Score: " + str(play_score), True, (255, 50, 10)) #render text
    screen.blit(score, (x,y)) #draw the rendered text


def rect_circle_collision(rect, circle_x, circle_y, circle_radius):
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    
    distance = math.sqrt((closest_x - circle_x) ** 2 + (closest_y - circle_y) ** 2)
    
    if distance <= circle_radius:
        return True
    else:
        return False

def gameOverText():
    over_text = over_font.render("GAME OVER", True, (255, 0,  0))
    screen.blit(over_text, (170, 200)) #draw the rendered text

def start_screen():
    title_text = font.render("Use w a s d to catch the orbs", True, (255, 0, 0))
    instruction_text = font.render("Press any key to start...", True, (255, 0, 0))
    
    # Draw the title and instructions
    screen.blit(title_text, (100, 200))
    screen.blit(instruction_text, (130, 300))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

start_screen()
while running:

    screen.fill((0,0,0))

    for event in pygame.event.get(): #Event loop
        if event.type == pygame.QUIT:
            running=False

        if event.type== pygame.KEYDOWN and playing:
            if event.key == pygame.K_a:
                leftFacing = True
                rightFacing = downFacing = upFacing = False 
                upFacing = False
            elif event.key == pygame.K_d:
                rightFacing = True
                leftFacing = downFacing = upFacing = False
            elif event.key == pygame.K_s:
                downFacing = True
                leftFacing = rightFacing = upFacing = False
            elif event.key == pygame.K_w:
                upFacing=True   
                leftFacing = rightFacing = downFacing = False

    player()
    showScore(10, 10)
    for i in range(numPellets):
        pellets[i].displayPelt()
        pellets[i].update()
        if rect_circle_collision(userRect, pellets[i].x, pellets[i].y, 15):
            if pellets[i].direction == 'right' and leftFacing:
                play_score += 1
                pellets[i].reassign()
            elif pellets[i].direction == 'left' and rightFacing:
                play_score += 1
                pellets[i].reassign()
            elif pellets[i].direction == 'down' and upFacing:
                play_score += 1
                pellets[i].reassign()
            elif pellets[i].direction == 'up' and downFacing:
                play_score += 1
                pellets[i].reassign()
            else:
                gameOverText()
                pellets[i].x = 300
                pellets[i].y = 300
                playing = False
            if play_score % (10+x) ==0:
                pellet_add_delay = True
                add_pellet_time = pygame.time.get_ticks()  # Record the time for delay

    # Handle delay for adding a new pellet
    if pellet_add_delay:
        if pygame.time.get_ticks() - add_pellet_time >= delay_duration:
            pellet_add_delay = False  
            addPellet() 
            x+= 15

    pygame.display.update()
            
pygame.quit()