import math
import random
import pygame


with open("words.txt", "r") as file:
    allwords = file.read()
    splitwords = allwords.split()
word = random.choice(splitwords)

# setup display
# random word
pygame.init()
WIDTH, HEIGHT = 1000, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!") #name of the game window

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH-(RADIUS*2 + GAP)*13)/2)
starty = 400
A = 65

for i in range(26):
    x = startx + GAP*2 + ((RADIUS*2+GAP)*(i%13))
    y = starty + (i//13*(GAP+RADIUS*2))
    letters.append([x,y, chr(A+i), True])

# game variables
hangman_status = 0
#word = "DEVELOPER"
guessed = ["D", "E"]

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans',30)
WORD_FONT = pygame.font.SysFont('comicsans', 45)
TITLE_FOND = pygame.font.SysFont('comicsans', 40)

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman"+str(i)+".png")
    images.append(image)


def draw():
    win.fill((WHITE))

    #draw title
    text = TITLE_FOND.render("Guess the word, and the man lives... ", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2,20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text,(400,200))

    #drawing buttons
    for letter in letters:
        x,y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win,BLACK,(x,y), RADIUS, 3) #(draw where, color, coordinates, radius, line thickness)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text,(x-text.get_width()/2,y - text.get_height()/2))
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    global hangman_status
    # setup game loop
    FPS = 60
    clock = pygame.time.Clock()  # our pygame will work at this speed
    run = True

    while run:
        clock.tick(FPS) #to make sure that our while loop runs at the FPS = 60

        draw()

        for event in pygame.event.get(): #all the events are stored in pygame.event.get()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: #this line allows us to detect coordinates of the mouseclick
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2+(y-m_y)**2) # HERE WE ARE CHECKING FOR COLLISION. I DON'T REALLY UNDERSTAND IT
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

            won = True
            for letter in word:
                if letter not in guessed:
                    won = False
                    break
            if won:
                display_message("YOU WON")

            if hangman_status == 6:
                display_message("YOU LOST")
while True:
    main()
pygame.quit()
