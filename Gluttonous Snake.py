import pygame, sys, random, math, os
import pygame.freetype

pygame.init()

icon = pygame.image.load("Snake Head.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Gluttonous Snake")

SPEED = 20
LENGTH = 20

size = width, height = 600, 400
screen = pygame.display.set_mode(size)
bgcolor = pygame.Color("black")
scorecolor = pygame.Color("yellow")
fail = False
failcolor = pygame.Color("red")
failfont = pygame.freetype.Font("C://Windows//Fonts//msyh.ttc", 72)
scorefont = pygame.freetype.Font("C://Windows//Fonts//msyh.ttc", 36)
screen.fill(bgcolor)
direction = {
    "right": 0,
    "up": 90,
    "left": 180,
    "down": 270
}

fps = 2
fclock = pygame.time.Clock()

grow = False


class SnakeHead(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Snake Head.png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 200
        self.direction = "up"

    def turn(self, n_direction):
        self.image = pygame.transform.rotate(self.image, direction[n_direction] - direction[self.direction])
        self.direction = n_direction

    def update(self, *args):
        if self.direction == "up":
            self.rect.move_ip(0, -SPEED)
        elif self.direction == "down":
            self.rect.move_ip(0, SPEED)
        elif self.direction == "right":
            self.rect.move_ip(SPEED, 0)
        elif self.direction == "left":
            self.rect.move_ip(-SPEED, 0)
        self.rect.left = self.rect.left % width
        self.rect.top = self.rect.top % height


class SnakeBody(pygame.sprite.Sprite):
    def __init__(self, body):
        super().__init__()

        self.image = pygame.image.load("Snake Body.png")
        self.rect = body.rect.copy()
        self.BeforeBody = body

    def update(self, *args):
        self.rect.clamp_ip(self.BeforeBody.rect.copy())


class SnakeTail(pygame.sprite.Sprite):
    def __init__(self, body):
        super().__init__()

        self.image = pygame.image.load("Snake Tail.png")
        self.rect = body.rect.copy()
        self.BeforeBody = body
        self.grow = False

    def reblit(self, body):
        self.BeforeBody = body
        self.grow = True

    def update(self, *args):
        if self.grow:
            self.grow = False
            return
        if (self.rect.x == self.BeforeBody.rect.x
            and (self.rect.y - SPEED) % height == self.BeforeBody.rect.y
            and (self.BeforeBody.rect.x - SPEED) % width == self.BeforeBody.BeforeBody.rect.x) \
                or (self.rect.x == self.BeforeBody.rect.x
                    and (self.rect.y + SPEED) % height == self.BeforeBody.rect.y
                    and (self.BeforeBody.rect.x + SPEED) % width == self.BeforeBody.BeforeBody.rect.x) \
                or (self.rect.y == self.BeforeBody.rect.y
                    and (self.rect.x - SPEED) % width == self.BeforeBody.rect.x
                    and (self.BeforeBody.rect.y + SPEED) % height == self.BeforeBody.BeforeBody.rect.y) \
                or (self.rect.y == self.BeforeBody.rect.y
                    and (self.rect.x + SPEED) % width == self.BeforeBody.rect.x
                    and (self.BeforeBody.rect.y - SPEED) % height == self.BeforeBody.BeforeBody.rect.y):
            self.image = pygame.transform.rotate(self.image, 90)
        elif (self.rect.x == self.BeforeBody.rect.x
              and (self.rect.y - SPEED) % height == self.BeforeBody.rect.y
              and (self.BeforeBody.rect.x + SPEED) % width == self.BeforeBody.BeforeBody.rect.x) \
                or (self.rect.x == self.BeforeBody.rect.x
                    and (self.rect.y + SPEED) % height == self.BeforeBody.rect.y
                    and (self.BeforeBody.rect.x - SPEED) % width == self.BeforeBody.BeforeBody.rect.x) \
                or (self.rect.y == self.BeforeBody.rect.y
                    and (self.rect.x - SPEED) % width == self.BeforeBody.rect.x
                    and (self.BeforeBody.rect.y - SPEED) % height == self.BeforeBody.BeforeBody.rect.y) \
                or (self.rect.y == self.BeforeBody.rect.y
                    and (self.rect.x + SPEED) % width == self.BeforeBody.rect.x
                    and (self.BeforeBody.rect.y + SPEED) % height == self.BeforeBody.BeforeBody.rect.y):
            self.image = pygame.transform.rotate(self.image, -90)
        self.rect.clamp_ip(self.BeforeBody.rect.copy())


class SnakeFood(pygame.sprite.Sprite):
    def __init__(self, body):
        super().__init__()

        self.image = pygame.image.load("Food.png")
        self.rect = self.image.get_rect()
        self.overlap = False
        while True:
            self.rect.x = random.randrange(30) * 20
            self.rect.y = random.randrange(20) * 20
            for rect in body.sprites():
                if self.rect == rect.rect:
                    self.overlap = True
            if not self.overlap:
                break


Head = SnakeHead()
Body = SnakeBody(Head)
Tail = SnakeTail(Body)

Bodys = [Body]

Snake = pygame.sprite.Group()

Snake.add(Tail)
Snake.add(Body)
Snake.add(Head)

Food = SnakeFood(Snake)
Snake.add(Food)

Snake.update()
Snake.draw(screen)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif fail:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and Head.direction != "right":
                Head.turn("left")
                break
            elif event.key == pygame.K_RIGHT and Head.direction != "left":
                Head.turn("right")
                break
            elif event.key == pygame.K_DOWN and Head.direction != "up":
                Head.turn("down")
                break
            elif event.key == pygame.K_UP and Head.direction != "down":
                Head.turn("up")
                break

    if fail:
        continue

    screen.fill(bgcolor)

    if grow:
        Body = SnakeBody(Bodys[-1])
        Bodys.append(Body)
        fps = math.floor((len(Bodys) + 5) / 3)
        Tail.reblit(Body)
        Snake.empty()
        Snake.add(Tail)
        for abody in Bodys[::-1]:
            Snake.add(abody)
        Snake.add(Head)
        Snake.add(Food)
        grow = False

    Snake.update()

    for abody in Bodys:
        if Head.rect == abody.rect or Head.rect == Tail.rect:
            fail = True
            break

    if Head.rect == Food.rect:
        Food.kill()
        Food = SnakeFood(Snake)
        Snake.add(Food)
        grow = True

    Snake.draw(screen)

    if fail:
        screen.fill(bgcolor)
        failfont.render_to(screen, [80, 150], "GAME OVER", failcolor)
        scorefont.render_to(screen, [100, 200], "SCORE: %d" % (len(Bodys) - 1), scorecolor)
        pygame.display.update()

    pygame.display.update()
    fclock.tick(fps)