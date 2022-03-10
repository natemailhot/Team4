import pygame
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PitchPerfect.io")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont('comicsansms', 64)
startText = FONT.render('PitchPerfect.io', False, WHITE)
centerRect = startText.get_rect(center=(WIDTH/2, HEIGHT/2))

FPS = 60

def draw_window():
    WIN.fill(BLACK)
    WIN.blit(startText, centerRect)
    pygame.display.update()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
