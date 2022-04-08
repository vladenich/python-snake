import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# рисует квадратик - часть змейки
# изначально создаёт первый квадратик - голову змейки с глазами
class Cube (object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255, 0, 0)):
        self.pos = start  # (10, 10) количество квадратиков по осям
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]  # координата x (квадратик)
        j = self.pos[1]  # координата y (квадратик)

        pygame.draw.rect(surface, self.color, (i*dis + 1, j*dis + 1, dis-2, dis-2))  # из-за сетки прибавляем 1

        if eyes:  # если True, тогда рисует глаза
            center = dis // 2
            radius = 3
            circleMiddle = (i*dis + center - radius, j*dis + 8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class Snake (object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)  # добавляет голову змейки в список body
        # направление стартовой змейки
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    # меняет направление змейки и записиывает в словарь turns позицию x и y (ключ) и напрвление (знач.)
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:  # ставим elif чтобы считалось одно нажатие
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]  # позиция квадратика (x, y)
            if p in self.turns:
                turn = self.turns[p]  # записывает в turn движение змейки (dirnx, dirny)
                c.move(turn[0], turn[1])  # c.move(dirnx, dirny) вызывается метод объекта Cube - змейка поворачивает до тех пор пока не дойдет до последнего квадратика
                if i == len(self.body) - 1:  # вычитается 1, так как i начинается с 0
                    self.turns.pop(p)  # если дошли до последнего квадратика, то змейка прекращает поворачивать
            else:
                # если дошли до границы, то рисуем змейку с противоположной границы
                if c.dirnx == -1 and c.pos[0] <= 0:  # c.pos[0] = x
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:  # если же змейка не врезается в границу, то
                    c.move(c.dirnx, c.dirny)  # змейка просто движется в том же направлении


    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):  # добавляет квадратик к телу змейки
        tail = self.body[-1]  # присваивается хвост змейки (последний квадратик)
        dx, dy = tail.dirnx, tail.dirny  # фиксирууется направление движения змейки

        if dx == 1 and dy == 0:  # если змейка движется вправо
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))  # то добавляем квадратик по оси х перед хвостом
        elif dx == -1 and dy == 0:  # и так далее
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        # теперь новому хвосту (последнему квадратику) присвоим такое же направление, как и у всей змейки
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:  # если True, тогда рисует первому квадратику (голове) глаза
                c.draw(surface, True)  # eyes == True
            else:  # для остальной части тела змейки глаза не рисуем
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))  # рисует вертикальную линию
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))  # рисует горизонтальную линию

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(item):
    global rows
    positions = item.body  # записывает координаты змейки

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # если координаты змейки соответсвуют координате кусочка
            continue  # то создаем кусочек с новыми координатами, чтобы он не был создан на теле змейки
        else:
            break
    return (x, y)  # когда такой кусочек создался, возвращаем его координаты

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(randomSnack(s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.display.set_caption('Змейка')
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:  # если позиция головы змейки равна позиции кусочка
            s.addCube()  # то прибавляем к змейке квадратик
            snack = Cube(randomSnack(s), color=(0, 255, 0))  # и создаем новый рандомный кусочек

        for x in range(len(s.body)):
            # если какой-то квадратик змейки совпадет с остальными
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print("Score: ", len(s.body))
                message_box("Вы проиграли!", f"Ваш результат: {len(s.body)}. Попробуйте снова...")
                s.reset((10, 10))
                break

        redrawWindow(win)


main()