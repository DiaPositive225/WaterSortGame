#!/usr/bin/python3

import sys

import pygame
from pygame.locals import *

from bottles import Bottles

# initial setup
pygame.init()
SIZE = 480,640
FPS = 30
screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# loading "level" in colors.setup and colorscheme from colors.codes
b = None
with open("colors.setup", "r") as f:
    lines = []
    for i in f.readlines():
        lines.append(i.strip())
    num = int(lines[0])
    b = Bottles(num, lines[1].split())
if b is None:
    raise TypeError

colors = []
with open("colors.codes", "r") as f:
    for line in f.readlines():
        colors.append(pygame.Color(line.strip()))
if len(colors) < b.length - 2:
    raise ValueError

class bot_animator:
    def __init__(self, frames : int = 20) -> None:
        self.active = False
        self.frame_lim = frames
        self.frame = 0
        self.a = None
        self.ra = None
        self.m = None
        self.rm = None
        self.t = None
        self.rt = None
        self.vec = (0, 0)
        self.block = ((False, -1), (False, -1))
        self.target_angle = 90
        self.current_angle = 0
        self.angle_quantum = self.target_angle / self.frame_lim

    def start(self, bot_m : tuple[pygame.Surface, pygame.Rect, pygame.Surface], bot_t : tuple[pygame.Surface, pygame.Rect, pygame.Surface], mov : tuple[tuple[bool, int], tuple[bool, int]], offset : tuple[int, int] = (30, -30)) -> None:
        self.active = True
        self.block = mov
        self.m = bot_m[0]
        self.t = bot_t[0]
        self.nm = bot_m[2]
        self.nt = bot_t[2]
        self.rm = bot_m[1]
        self.rt = bot_t[1]
        r1 = bot_m[1].midtop
        r2 = bot_t[1].midtop
        self.vec = (r2[0] - r1[0] + offset[0]) / self.frame_lim, (r2[1] - r1[1] + offset[1]) / self.frame_lim

    def update(self) -> None:
        if self.active:
            self.frame += 1
            if self.frame < self.frame_lim:
                if type(self.rm) is pygame.Rect and type(self.rt) is pygame.Rect and type(self.t) is pygame.Surface and type(self.m) is pygame.Surface:
                    screen.blit(self.t, self.rt)
                    r = self.rm.copy()
                    self.m.set_colorkey("0x000000")
                    mer = pygame.transform.rotate(self.m, self.frame * self.angle_quantum)
                    r.midtop = r.midtop[0] + int(self.vec[0] * self.frame), r.midtop[1] + int(self.vec[1] * self.frame)
                    screen.blit(mer, r)
                    # pygame.draw.line(screen, "red", self.rm.midtop, (self.rm.midtop[0] + self.vec[0] * self.frame_lim, self.rm.midtop[1] + self.vec[1] * self.frame_lim), 5)
            elif self.frame == self.frame_lim:
                if type(self.rm) is pygame.Rect and type(self.rt) is pygame.Rect and type(self.t) is pygame.Surface and type(self.m) is pygame.Surface:
                    screen.blit(self.t, self.rt)
                    r = self.rm.copy()
                    self.m.set_colorkey("0x000000")
                    mer = pygame.transform.rotate(self.m, self.frame * self.angle_quantum)
                    r.midtop = r.midtop[0] + int(self.vec[0] * self.frame), r.midtop[1] + int(self.vec[1] * self.frame)
                    screen.blit(mer, r)
                self.t = self.nt
                self.m = self.nm
            elif self.frame_lim < self.frame < 2 * self.frame_lim:
                if type(self.rm) is pygame.Rect and type(self.rt) is pygame.Rect and type(self.t) is pygame.Surface and type(self.m) is pygame.Surface:
                    fram = self.frame- self.frame_lim
                    screen.blit(self.t, self.rt)
                    r = self.rm.copy()
                    self.m.set_colorkey("0x000000")
                    mer = pygame.transform.rotate(self.m, self.target_angle - fram * self.angle_quantum)
                    r.midtop = r.midtop[0] + int( self.vec[0] * (self.frame_lim - fram)), r.midtop[1] + int(self.vec[1] * (self.frame_lim - fram))
                    screen.blit(mer, r)
            elif 2 * self.frame_lim == self.frame:
                if type(self.rm) is pygame.Rect and type(self.rt) is pygame.Rect and type(self.t) is pygame.Surface and type(self.m) is pygame.Surface:
                    screen.blit(self.m, self.rm)
                    screen.blit(self.t, self.rt)
                self.frame = 0
                self.active = False
                self.a = None
                self.ra = None
                self.m = None
                self.rm = None
                self.t = None
                self.rt = None
                self.vec = (0, 0)
                self.block = ((False, -1), (False, -1))

class B_display:
    def __init__(self, b : Bottles, width : int = 30, height : int = 40, sep : int = 20) -> None:
        self.b = b
        self.width = width
        self.height = height
        self.separation = sep
        self.anim = bot_animator()

    def draw(self, s : int = -1, mov : tuple[int, int] = (-1, -1)) -> None:
        # define the middle with x, y and determine how many bottles per row
        x = SIZE[0] // 2
        y = SIZE[1] // 2
        row1 = self.b.length // 2
        row2 = self.b.length - row1

        # used to determine which bottle is selected when drawing
        r = s >= row1
        if r:
            s -= row1

        # when moved
        move_set = ((mov[0] >= row1,
                (mov[0] - row1) if mov[0] >= row1 else mov[0]),
               (mov[1] >= row1,
                (mov[1] - row1) if mov[1] >= row1 else mov[1]))
        surf = [pygame.Surface((0,0)), pygame.Rect((0,0,0,0)), pygame.Surface((0,0)), pygame.Rect((0,0,0,0)),pygame.Surface((0,0)),pygame.Surface((0,0))]

        # bottom left corners of both rows
        base1 = x - (row1 * self.width + (row1 - 1) * self.separation) // 2, y - self.separation // 2
        base2 = x - (row2 * self.width + (row2 - 1) * self.separation) // 2, y + self.separation // 2 + 4 * self.height
        for i, bot in enumerate(self.b.bottles[:row1]):
            # curr_bot is filled and populated, bottom_bit is there to produce rounded bottom
            curr_bot = pygame.Surface((self.width, 4*self.height))
            curr_bot.fill("darkgray")
            for j, c in enumerate(bot):
                pygame.draw.rect(curr_bot, colors[int(c) - 1], (0, (3 - j) * self.height, self.width, self.height))
            bottom_bit = pygame.Surface((self.width, self.width))
            bottom_bit.fill("0x000000")
            pygame.draw.rect(bottom_bit, "0xffffff", (0,0,self.width,self.width // 2))
            pygame.draw.circle(bottom_bit, "0xffffff", (self.width // 2, self.width // 2), self.width // 2)
            bottom_bit.set_colorkey("0xffffff")
            rec = bottom_bit.get_rect()
            rec.bottomleft = 0, 4 * self.height
            curr_bot.blit(bottom_bit, rec)
            rec = curr_bot.get_rect()
            rec.bottomleft = base1[0] + i * (self.separation + self.width), base1[1] + (- self.separation // 2 if not r and i == s else 0)
            if not move_set[0][0] and move_set[0][1] == i:
                surf[0] =  curr_bot
                surf[1] = rec
            elif not move_set[1][0] and move_set[1][1] == i:
                surf[2] =  curr_bot
                surf[3] = rec
            elif not (not self.anim.block[0][0] and self.anim.block[0][1] == i or not self.anim.block[1][0] and self.anim.block[1][1] == i): 
                screen.blit(curr_bot, rec)
        for i, bot in enumerate(self.b.bottles[row1:]):
            # idem
            curr_bot = pygame.Surface((self.width, 4*self.height))
            curr_bot.fill("darkgray")
            for j, c in enumerate(bot):
                pygame.draw.rect(curr_bot, colors[int(c) - 1], (0, (3 - j) * self.height, self.width, self.height))
            bottom_bit = pygame.Surface((self.width, self.width))
            bottom_bit.fill("0x000000")
            pygame.draw.rect(bottom_bit, "0xffffff", (0,0,self.width,self.width // 2))
            pygame.draw.circle(bottom_bit, "0xffffff", (self.width // 2, self.width // 2), self.width // 2)
            bottom_bit.set_colorkey("0xffffff")
            rec = bottom_bit.get_rect()
            rec.bottomleft = 0, 4 * self.height
            curr_bot.blit(bottom_bit, rec)
            rec = curr_bot.get_rect()
            rec.bottomleft = base2[0] + i * (self.separation + self.width), base2[1] + (- self.separation // 2 if  r and i == s else 0)
            if  move_set[0][0] and move_set[0][1] == i:
                surf[0] =  curr_bot
                surf[1] = rec
            elif  move_set[1][0] and move_set[1][1] == i:
                surf[2] =  curr_bot
                surf[3] = rec
            elif not ( self.anim.block[0][0] and self.anim.block[0][1] == i or  self.anim.block[1][0] and self.anim.block[1][1] == i): 
                screen.blit(curr_bot, rec)
        if mov != (-1, -1):
            self.b.move(mov[0], mov[1])
            for i in range(2):
                curr_bot = pygame.Surface((self.width, 4*self.height))
                curr_bot.fill("darkgray")
                for j, c in enumerate(self.b.bottles[(row1 if move_set[i][0] else 0) + move_set[i][1]]):
                    pygame.draw.rect(curr_bot, colors[int(c) - 1], (0, (3 - j) * self.height, self.width, self.height))
                bottom_bit = pygame.Surface((self.width, self.width))
                bottom_bit.fill("0x000000")
                pygame.draw.rect(bottom_bit, "0xffffff", (0,0,self.width,self.width // 2))
                pygame.draw.circle(bottom_bit, "0xffffff", (self.width // 2, self.width // 2), self.width // 2)
                bottom_bit.set_colorkey("0xffffff")
                rec = bottom_bit.get_rect()
                rec.bottomleft = 0, 4 * self.height
                curr_bot.blit(bottom_bit, rec)
                surf[4+i] = curr_bot.copy()
            self.anim.start((surf[0], surf[1], surf[4]), (surf[2], surf[3], surf[5]), move_set)
        self.anim.update()

    def click_lands(self, mPos : tuple[int,int]) -> int:
        x = SIZE[0] // 2
        y = SIZE[1] // 2
        row1 = self.b.length // 2
        row2 = self.b.length - row1
        base1 = x - (row1 * self.width + (row1 - 1) * self.separation) // 2, y - self.separation // 2
        base2 = x - (row2 * self.width + (row2 - 1) * self.separation) // 2, y + self.separation // 2 + 4 * self.height
        # determine if mPos is in the horizontal strips and then vertical
        if base1[1] >= mPos[1] >= base1[1] - 4 * self.height:
            for i in range(row1):
                if base1[0] + i * (self.width + self.separation) <= mPos[0] <= base1[0] + i * (self.width + self.separation) + self.width:
                    return i
        elif base2[1] >= mPos[1] >= base2[1] - 4 * self.height:
            for i in range(row2):
                if base2[0] + i * (self.width + self.separation) <= mPos[0] <= base2[0] + i * (self.width + self.separation) + self.width:
                    return row1 + i
        return -1

B = B_display(b)
done = False
selection = -1
move_set = (-1, -1)
while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                c = B.click_lands(pygame.mouse.get_pos())
                if selection == c or c == -1:
                    selection = -1
                elif selection == -1:
                    selection = c
                elif not B.anim.active:
                    # B.b.move(selection, c)
                    move_set = (selection, c)
                    selection = -1
    screen.fill("black")
    SIZE = pygame.display.get_window_size()
    B.draw(selection, move_set)
    move_set = (-1, -1)
    # pygame.draw.circle(screen, "red", (SIZE[0]//2,SIZE[1]//2), 10)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
