import random
import pygame as pg
from pygame import *

pg.init()
screen = pg.display.set_mode((600, 700))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
COLORS = {
    "W": WHITE,
    "R": RED,
    "G": GREEN,
    "B": BLUE,
    "O": ORANGE,
    "Y": YELLOW
}
FONT = pg.font.SysFont('Comic Sans MS', 32)
SCRAMBLE_FONT = pg.font.SysFont('Comic Sans MS', 20)
IMAGE_NORMAL = pg.Surface((100, 32))
IMAGE_NORMAL.fill((WHITE))
IMAGE_HOVER = pg.Surface((100, 32))
IMAGE_HOVER.fill((20, 20, 20))
IMAGE_DOWN = pg.Surface((100, 32))
IMAGE_DOWN.fill((40, 40, 40))
invalid_cases = {
    "U": ["U", "D"],
    "D": ["U", "D"],
    "R": ["R", "L"],
    "L": ["R", "L"],
    "F": ["F", "B"],
    "B": ["F", "B"]
}

class Cube:
    def __init__(self):
        self.top = [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"]]
        self.bottom = [["Y", "Y", "Y"], ["Y", "Y", "Y"], ["Y", "Y", "Y"]]
        self.front = [["R", "R", "R"], ["R", "R", "R"], ["R", "R", "R"]]
        self.back = [["O", "O", "O"], ["O", "O", "O"], ["O", "O", "O"]]
        self.left = [["G", "G", "G"], ["G", "G", "G"], ["G", "G", "G"]]
        self.right = [["B", "B", "B"], ["B", "B", "B"], ["B", "B", "B"]]
        self.lines = [[" "] * 12, [" "] * 12, [" "] * 12, [" "] * 12, [" "] * 12, [" "] * 12, [" "] * 12, [" "] * 12, [" "] * 12]

    def is_solved(self):
        return all([
            len(set("".join(["".join(row) for row in self.top]))) == 1,
            len(set("".join(["".join(row) for row in self.front]))) == 1,
            len(set("".join(["".join(row) for row in self.back]))) == 1,
            len(set("".join(["".join(row) for row in self.bottom]))) == 1,
            len(set("".join(["".join(row) for row in self.left]))) == 1,
            len(set("".join(["".join(row) for row in self.right]))) == 1
        ])

    def scramble(self):
        moveset = ["R", "L", "U", "D", "B", "F", "R'", "L'", "U'", "D'", "B'", "F'", "R2", "L2", "U2", "D2", "B2", "F2"]
        movements = []
        movements.append(random.choice(moveset))
        while len(movements) < 20:
            move = random.choice(moveset)
            valid = False
            i = len(movements) - 1
            while movements[i][0] != move[0] and i >= 0:
                if movements[i][0] not in invalid_cases[move[0]]:
                    valid = True
                    break
                i -= 1
            if valid:
                movements.append(move)
        for move in movements:
            self.move(move)
        return " ".join(movements)

    def rotate(self, lst):
        lst = [[row[i] for row in lst][::-1] for i in range(3)]
        return lst

    def move(self, rotation):
        if rotation == "R":
            self.right = self.rotate(self.right)
            tmp = [row[2] for row in self.top][::-1]
            self.top = [self.top[i][:-1] + [self.front[i][2]] for i in range(3)]
            self.front = [self.front[i][:-1] + [self.bottom[i][2]] for i in range(3)]
            self.bottom = [self.bottom[i][:-1] + [self.back[2-i][0]] for i in range(3)]
            self.back = [[tmp[i]] + self.back[i][1:] for i in range(3)]
        elif rotation == "L":
            self.left = self.rotate(self.left)
            tmp = [row[0] for row in self.top]
            self.top = [[self.back[2-i][2]] + self.top[i][1:] for i in range(3)]
            self.back = [self.back[i][:-1] + [self.bottom[2-i][0]] for i in range(3)]
            self.bottom = [[self.front[i][0]] + self.bottom[i][1:]  for i in range(3)]
            self.front = [[tmp[i]] + self.front[i][1:] for i in range(3)]
        elif rotation == "U":
            self.top = self.rotate(self.top)
            tmp = self.front[0]
            self.front[0] = self.right[0]
            self.right[0] = self.back[0]
            self.back[0] = self.left[0]
            self.left[0] = tmp
        elif rotation == "D":
            self.bottom = self.rotate(self.bottom)
            tmp = self.front[2]
            self.front[2] = self.left[2]
            self.left[2] = self.back[2]
            self.back[2] = self.right[2]
            self.right[2] = tmp
        elif rotation == "F":
            self.front = self.rotate(self.front)
            tmp = self.top[2]
            self.top[2] = [row[2] for row in self.left][::-1]
            self.left = [self.left[i][:-1] + [self.bottom[0][i]] for i in range(3)]
            self.bottom[0] = [row[0] for row in self.right][::-1]
            self.right = [[tmp[i]] + self.right[i][1:] for i in range(3)]
        elif rotation == "B":
            self.back = self.rotate(self.back)
            tmp = self.top[0]
            self.top[0] = [row[2] for row in self.right]
            self.right = [self.right[i][:-1] + [self.bottom[2][2-i]] for i in range(3)]
            self.bottom[2] = [row[0] for row in self.left]
            self.left = [[tmp[2-i]] + self.left[i][1:] for i in range(3)]
        elif rotation == "R'":
            for _ in range(3):
                self.move("R")
        elif rotation == "L'":
            for _ in range(3):
                self.move("L")
        elif rotation == "U'":
            for _ in range(3):
                self.move("U")
        elif rotation == "D'":
            for _ in range(3):
                self.move("D")
        elif rotation == "B'":
            for _ in range(3):
                self.move("B")
        elif rotation == "F'":
            for _ in range(3):
                self.move("F")
        elif rotation == "R2":
            for _ in range(2):
                self.move("R")
        elif rotation == "L2":
            for _ in range(2):
                self.move("L")
        elif rotation == "U2":
            for _ in range(2):
                self.move("U")
        elif rotation == "D2":
            for _ in range(2):
                self.move("D")
        elif rotation == "B2":
            for _ in range(2):
                self.move("B")
        elif rotation == "F2":
            for _ in range(2):
                self.move("F")

    def __str__(self):
        for i, colors in enumerate(self.top):
            for j, color in enumerate(colors):
                self.lines[3+i][3+j] = color

        for i, colors in enumerate(self.back):
            for j, color in enumerate(colors):
                self.lines[2-i][5-j] = color

        for i, colors in enumerate(self.left):
            for j, color in enumerate(colors):
                self.lines[3+j][2-i] = color

        for i, colors in enumerate(self.right):
            for j, color in enumerate(colors):
                self.lines[5-j][6+i] = color

        for i, colors in enumerate(self.bottom):
            for j, color in enumerate(colors):
                self.lines[5-i][11-j] = color

        for i, colors in enumerate(self.front):
            for j, color in enumerate(colors):
                self.lines[6+i][3+j] = color

        return "\n".join([" ".join(line) for line in self.lines])

class Button(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                 font=FONT, text='', text_color=(0, 0, 0),
                 image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                 image_down=IMAGE_DOWN):
        super().__init__()
        self.active = True

        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover, (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_center = self.image.get_rect().center

        self.text = text
        text_surf = font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.image_center)

        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.active:
            if self.rect.collidepoint(event.pos):
                self.button_down = True
        elif event.type == pg.MOUSEBUTTONUP and self.active:
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback(self.text)
            if self.active:
                self.image = self.image_normal
            self.button_down = False
        elif event.type == pg.MOUSEMOTION and self.active:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal

class Game:
    def __init__(self, screen):
        self.solved = False
        self.quit = False
        self.screen = screen
        self.cube = Cube()
        self.scramble = self.cube.scramble()
        self.lines = [[""] * 12, [""] * 12, [""] * 12, [""] * 12, [""] * 12, [""] * 12, [""] * 12, [""] * 12, [""] * 12]
        self.base = ["U", "D", "R", "L", "F", "B"]
        self.power = ["", "'", "2"]
        self.all_sprites = pg.sprite.Group()
        for j in range(502, 700, 66):
            for i in range(0, 600, 100):
                self.all_sprites.add(
                    Button(
                        i, j, 60, 60, self.cube.move, text=self.base[i//100]+self.power[(j-502)//66]
                    )
                )

    def check(self):
        self.solved = self.cube.is_solved()

    def play_again(self):
        done = True
        while done:
            msg = "CONGRATULATIONS!!!"
            msg = FONT.render(f"{msg}", True, (0, 0, 0))
            text_rect = msg.get_rect(center=(300, 225))
            screen.blit(msg, text_rect)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = False

    def run(self):
        while not self.quit:
            self.handle_events()
            self.run_logic()
            self.draw()
            self.check()
            if self.solved:
                self.quit = True
        if self.solved:
            self.play_again()
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit = True
            if event.type == pg.KEYDOWN:
                key = chr(event.key).upper()
                self.cube.move(key)
            for button in self.all_sprites:
                button.handle_event(event)

    def run_logic(self):
        for i, colors in enumerate(self.cube.top):
            for j, color in enumerate(colors):
                self.lines[3+i][3+j] = color

        for i, colors in enumerate(self.cube.back):
            for j, color in enumerate(colors):
                self.lines[2-i][5-j] = color

        for i, colors in enumerate(self.cube.left):
            for j, color in enumerate(colors):
                self.lines[3+j][2-i] = color

        for i, colors in enumerate(self.cube.right):
            for j, color in enumerate(colors):
                self.lines[5-j][6+i] = color

        for i, colors in enumerate(self.cube.bottom):
            for j, color in enumerate(colors):
                self.lines[5-i][11-j] = color

        for i, colors in enumerate(self.cube.front):
            for j, color in enumerate(colors):
                self.lines[6+i][3+j] = color

    def draw(self):
        self.screen.fill((30, 30, 30))
        msg = SCRAMBLE_FONT.render(f"{self.scramble}", True, (255, 255, 255))
        text_rect = msg.get_rect(center=(300, 25))
        screen.blit(msg, text_rect)
        self.all_sprites.draw(self.screen)
        for i, colors in enumerate(self.lines):
            for j, color in enumerate(colors):
                if color:
                    pg.draw.rect(self.screen, COLORS[color], (j * 50, i * 50 + 50, 50, 50))
                    pg.draw.rect(self.screen, (0, 0, 0), (j * 50, i * 50 + 50, 50, 50), 1)
        pg.display.flip()

if __name__ == "__main__":
    Game(screen).run()
    pg.quit()