import pygame
import os
import sys
import random

pygame.init()
pygame.display.set_caption('Frog')
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
bricks = pygame.sprite.Group()

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def check_rect(rect1, rect2):
    #rect = [x, w] or [y, h]
    rect1, rect2 = sorted([rect1, rect2], key=lambda r: r[0])
    if rect1[0] + rect1[1] >= rect2[0]:
        return True
    return False


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
    

class Frog(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        image = load_image("frog.jpg", -1)
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 3
        self.vy = 2
        
    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
            self.image = pygame.transform.flip(self.image, False, True)
            
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
            self.image = pygame.transform.flip(self.image, True, False)

            
        cat = False
        for e in bricks:
            if check_rect([self.rect.x, self.rect.width], [e.rect.x, e.rect.width]):
                if check_rect([self.rect.y, self.rect.height], [e.rect.y, e.rect.height]):
                    if e.exist:
                        e.exist = False
                        cat = True
        if cat:
            self.vy = -self.vy
            self.image = pygame.transform.flip(self.image, False, True)
            
        if pygame.sprite.spritecollideany(self, platforms):
            self.vy = -self.vy
            if self.vx > 0:
                if platform.rect.x + 25 < self.rect.x + self.radius // 2:
                    self.vx = -self.vx
                    self.image = pygame.transform.flip(self.image, True, True)
                else:
                    self.image = pygame.transform.flip(self.image, False, True)
            else:
                if platform.rect.x + 25 > self.rect.x + self.radius // 2:
                    self.vx = -self.vx
                    self.image = pygame.transform.flip(self.image, True, True)
                else:
                    self.image = pygame.transform.flip(self.image, False, True)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(platforms)
        image = load_image("platform1.jpg", 'black')
        self.image = pygame.transform.scale(image, (60, 41))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = 60
        self.rect.height = 41
        
    def update(self, x):
        self.rect.x = x


class Brick(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(bricks)
        image = load_image("dragonfly.jpg", 'black')
        self.image = pygame.transform.scale(image, (63, 35))
        self.rect = self.image.get_rect()
        self.exist = True
        

        def check_pos(x, y):
            for e in bricks:
                if check_rect([x, 63], [e.rect.x, 63]) and check_rect([y, 35], [e.rect.y, 35]):
                    return False
            return True

            
        x = random.randrange(800 - 63)
        y = random.randrange(600 - 325)
        while not check_pos(x, y):
            x = random.randrange(800 - 63)
            y = random.randrange(600 - 325)
        self.rect.x, self.rect.y = x, y
        self.rect.width = 63
        self.rect.height = 35
        
    def update(self):
        pass             

n_of_win = 0
Border(5, 5, width - 5, 5)
#Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)
#Ball(5, 200, 200)
platform = Platform(375, 560)
frog = None
for _ in range(5 + n_of_win):
    Brick()




start = True
size = (800, 600)
green = (0, 150, 0)

button_pos = (250, 400)
button_size = (325, 40)
button_txt = "Начать новую игру"

basic_txt = "Симулятор голодной лягушки"
basic_pos = (120, 20)

win_pos = (250, 200)
win_txt = ["", "Вы победили!", "Вы проиграли :c"]
win_or_loss = 0



def start_screen(screen): ##отрисовка
    font = pygame.font.Font(None, 50)
    screen.fill(green)
    pygame.draw.rect(screen, "white", (*button_pos, *button_size), 0)
    text1 = font.render(basic_txt, True, "white")
    text2 = font.render(win_txt[win_or_loss], True, "white")
    text3 = font.render(button_txt, True, green)
    screen.blit(text1, basic_pos)
    screen.blit(text2, win_pos)
    screen.blit(text3, button_pos)




n = 0
dx = 0
touch = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start:
                st = True
                for i in range(2):
                    if event.pos[i] < button_pos[i] or event.pos[i] > button_pos[i] + button_size[i]:
                        st = False
                if st:
                    start = False
            elif event.pos[0] >= 375 and  event.pos[0] <= 425 and not frog:
                dx = event.pos[0] - platform.rect.x
                touch = True
                frog = Frog(5, 400, 300)
        if event.type == pygame.MOUSEMOTION:
            if touch:
                x = event.pos[0] - dx
                platform.update(x)
            
    screen.fill('white')
    if start:
        start_screen(screen)
    for e in all_sprites:
        if not e:
            del e
        else:
            e.update()
    cat = False
    for e in bricks:
        if e.exist:
            screen.blit(e.image, (e.rect.x, e.rect.y))
            cat = True
    if not cat:
        for e in all_sprites:
            e = None
        all_sprites = pygame.sprite.Group()
        bricks = pygame.sprite.Group()
        frog = None
        touch = False
        platforms = pygame.sprite.Group()
        platform = Platform(375, 560)
        start = True
        win_or_loss = 1
        n_of_win = (n_of_win + 5) % 30
        for _ in range(5 + n_of_win):
            Brick()
    if frog:
        if frog.rect.y >= 600:
            start = True
            win_or_loss = 2
            frog = None
            touch = False
            platform.rect.x = 375
            platform.rect.y = 560
            for e in bricks:
                e.exist = True
    platforms.draw(screen)
    for e in all_sprites:
        if e:
            screen.blit(e.image, (e.rect.x, e.rect.y))
    if start:
        start_screen(screen)
    clock.tick(100)
    pygame.display.flip()
pygame.quit()
    
