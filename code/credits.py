import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption('End credits')
screen = pygame.display.set_mode((1200, 704))
screen_r = screen.get_rect()
font = pygame.font.Font('graphics/ui/ARCADEPI.TTF',40)
clock = pygame.time.Clock()

def main():

    credit_list = ["CREDITS - CoinSurfer's Chronicles"," "," ","Abdullah Abu Hamad - The Big Orange Cat"," ","Amjad Al-Sayyed   - The Moustache Cat"," ", "Nawras Albibi     - The Shawarma Man"," ", "Mohammad AlGhanim   - The Tiger           "," ", "Yazan Abu Shhab   - The Head Hunter   "]

    texts = []
    # we render the text once, since it's easier to work with surfaces
    # also, font rendering is a performance killer
    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (10, 10, 10))
        # we also create a Rect for each Surface. 
        # whenever you use rects with surfaces, it may be a good idea to use sprites instead
        # we give each rect the correct starting position 
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        screen.fill((40, 120, 60))

        for r, s in texts:
            # now we just move each rect by one pixel each frame
            r.move_ip(0, -1)
            # and drawing is as simple as this
            screen.blit(s, r)

        # if all rects have left the screen, we exit
        if not screen_r.collidelistall([r for (r, _) in texts]):
            return

        # only call this once so the screen does not flicker
        pygame.display.flip()

        # cap framerate at 60 FPS
        clock.tick(60)

if __name__ == '__main__': 
    main()