import pygame, main
#---------PROPS-----------#
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

#------INITIALISATION-----#
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
pygame.display.set_caption('Test')
clock = pygame.time.Clock()
greet='Enter your name: '
name=''
font = pygame.font.Font(None, 30)
done = False

#-------LOAD-MUSIC--------#
#pygame.mixer.music.load("mus_library/rave.wav")
#pygame.mixer.music.play()

#-------MAIN-LOOP---------#
while not done:
    screen.fill(WHITE)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                name += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            elif event.key == pygame.K_RETURN:
                main.login(name)
        elif event.type == pygame.QUIT:
            done = True
    block1 = font.render(greet, True, BLUE)
    block2 = font.render(name, True, BLACK)
    screen.blit(block1,(40,40))
    screen.blit(block2, (220, 40))
    pygame.display.flip()
    clock.tick(7)