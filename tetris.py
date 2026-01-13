import pygame
import random
import math
from pygame.locals import *

orange = (255, 136, 0)
blue = (68, 255, 255)
dblue = (0, 0, 200)
green = (68, 255, 68)
pink = (255, 68, 255)
yellow = (255, 255, 68)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
collision = False
new_blocks = []
score = 0
tetris = 0
drop = False
hold_piece = None
next_piece = None
hold_used = False
movedL = False
movedR = False
lines_cleared = 0
level = 1
speedsave = 500
last_level = 1
lines_req = 10
speed_increase = 1
size= 20
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((size*26, size*30))
pygame.display.set_caption("Tetris")
square = [
    [1, 1],
    [1, 1],
    yellow
]
line = [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    blue
]
tBlock = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0],
    pink
]
jBlock = [
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 0],
    dblue
]
lBlock = [
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 0],
    orange
]
zBlock = [
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 0],
    red
]
sBlock = [
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 0],
    green
]
floor = pygame.Rect(size*8, size*25, size*10, size/4)
wall1 = pygame.Rect(size*7.75, size*5, size/4, size*20.25)
wall2 = pygame.Rect(size*18, size*5, size/4, size*20.25)
hold_bottom = pygame.Rect(size*2, size*10.5, size*5, size/4)
hold_top = pygame.Rect(size*2, size*5.5, size*5, size/4)
hold_side = pygame.Rect(size*1.75, size*5.5, size/4, size*5.25)
hold_side2 = pygame.Rect(size*7, size*5.5, size/4, size*5.25)
next_bottom = pygame.Rect(size*19, size*10.5, size*5, size/4)
next_top = pygame.Rect(size*19, size*5.5, size*5, size/4)
next_side = pygame.Rect(size*23.75, size*5.5, size/4, size*5.25)
next_side2 = pygame.Rect(size*18.75, size*5.5, size/4, size*5.25)
bagsave = [square, line, tBlock, jBlock, lBlock, zBlock, sBlock]
bag = [square, line, tBlock, jBlock, lBlock, zBlock, sBlock]
bag_index = 0
random.shuffle(bag)
blocks = []
score_font = pygame.font.SysFont('Avenir Book', int(size*2.5))
color = bag[bag_index][-1]

def rotate(shape):
    shape = bag[bag_index][:-1]
    color = bag[bag_index][-1]
    rotated_shape = [
        [shape[j][i] for j in range(len(shape))] for i in range(len(shape[0]))
    ]
    rotated_shape = rotated_shape[::-1]
    return rotated_shape + [color]

def get_ghost_y(xpos, ypos, piece, blocks, floor):
    ghost_y = ypos
    while True:
        collision = False
        for row_index, row in enumerate(piece[:-1]):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    x = xpos + col_index * size
                    y = ghost_y + row_index * size
                    if floor.colliderect(pygame.Rect(x, y, size, size)):
                        collision = True
                        break
                    for block_x, block_y, _ in blocks:
                        if pygame.Rect(x, y, size, size).colliderect(pygame.Rect(block_x, block_y, size, size)):
                            collision = True
                            break
            if collision:
                break
        if collision:
            ghost_y -= size
            break
        else:
            ghost_y += size
    return ghost_y

xpos = size*12
ypos = size*5
fallspeed = 500 
last_fall_time = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_UP:
                bag[bag_index] = rotate(bag[bag_index])
            if event.key == K_DOWN:
                fallspeed /= 8
            if event.key == K_LEFT:
                xpos -= size
                movedL = True
            if event.key == K_RIGHT:
                xpos += size
                movedR = True
            if event.key == K_RCTRL:
                if not hold_used:
                    current_piece = bag[bag_index]
                    if hold_piece is None:
                        hold_piece = current_piece
                        bag_index += 1
                        if bag_index >= len(bag):
                            bag = bagsave[:]
                            random.shuffle(bag)
                            bag_index = 0
                    else:
                        bag[bag_index] = hold_piece
                        hold_piece = current_piece
                    xpos = size*12
                    ypos = size*5
                    hold_used = True
            if event.key == K_SPACE:
                drop_distance = 0
                while True:
                    ypos += size
                    drop_distance += size
                    collision = False
                    for row_index, row in enumerate(bag[bag_index]):
                        for col_index, cell in enumerate(row):
                            if cell == 1:
                                x = xpos + col_index * size
                                y = ypos + row_index * size
                                if floor.colliderect(pygame.Rect(x, y, size, size)):
                                    collision = True
                                    break
                                for block_x, block_y, block_color in blocks:
                                    falling_block_rect = pygame.Rect(x, y, size, size)
                                    static_block_rect = pygame.Rect(block_x, block_y, size, size)
                                    if falling_block_rect.colliderect(static_block_rect):
                                        collision = True
                                        break
                        if collision:
                            break
                    if collision:
                        drop = True
                        ypos -= size
                        drop_distance -= size
                        break
                for row_index, row in enumerate(bag[bag_index]):
                    for col_index, cell in enumerate(row):
                        if cell == 1:
                            x = xpos + col_index * size
                            y = ypos + row_index * size
                            blocks.append((x, y, color))                  
                score += (drop_distance // size) * 2
        if event.type == KEYUP:
                 if event.key == K_DOWN:
                    fallspeed = speedsave
    collision = False
    color = bag[bag_index][-1]

    if lines_cleared >= lines_req:
        lines_req += 10
        level += 1
    if level >= speed_increase + 5:
        speed_increase += 5
        fallspeed /= 2
        speedsave /= 2


    current_time = pygame.time.get_ticks()
    if current_time - last_fall_time > fallspeed:
        ypos += size
        last_fall_time = current_time
        score += int(math.fabs(fallspeed / 100 - 5)/5)

    for row_index, row in enumerate(bag[bag_index]):
        for col_index, cell in enumerate(row):
            if cell == 1:
                x = xpos + col_index * size
                y = ypos + row_index * size
                if floor.colliderect(pygame.Rect(x, y, size, size)):
                    collision = True
                    break
                for block_x, block_y, block_color in blocks:
                    falling_block_rect = pygame.Rect(x, y, size, size)
                    static_block_rect = pygame.Rect(block_x, block_y, size, size)
                    if falling_block_rect.colliderect(static_block_rect):
                        collision = True
                        break
        if collision:
            break

    if collision and not drop and not movedL and not movedR:
        ypos -= size
        for row_index, row in enumerate(bag[bag_index]):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    x = xpos + col_index * size
                    y = ypos + row_index * size
                    blocks.append((x, y, color))
    if collision and not movedL and not movedR:
        bag_index +=1
        if bag_index >= len(bag):
            bag = bagsave[:]
            random.shuffle(bag)
            bag_index = 0
        xpos = size*12
        ypos = size*5
        drop = False
        hold_used = False

        lines_to_clear = []
        for y in range(size*25, size*5-1, -size):
            line_blocks = [block for block in blocks if block[1] == y]
            if len(line_blocks) == 10:
                lines_to_clear.append(y)
                tetris += 1
                lines_cleared += 1
        
        if lines_to_clear:
            lines_to_clear.sort(reverse=True)
            new_blocks = []
            if tetris == 4:
                score += 800 * level
            else:
                score += (200 * tetris - 100) * level
            for block in blocks:
                block_x, block_y, block_color = block
                if block_y not in lines_to_clear:
                    new_y = block_y
                    for cleared_y in lines_to_clear:
                        if block_y < cleared_y:
                            new_y += size
                    new_blocks.append((block_x, new_y, block_color))
    if collision and movedL:
        xpos += size
    elif collision and movedR:
        xpos -= size

    tetris = 0
    blocks = new_blocks
    if bag_index + 1 >= len(bag):
        bag = bagsave[:]
        random.shuffle(bag)
        bag_index = 0
    next_piece = bag[bag_index + 1]
    movedL = False
    movedR = False

    screen.fill(black)

    score_surface = score_font.render("SCORE: " + str(score), False, white)
    screen.blit(score_surface, (size/2,size/2))
    hold_surface = score_font.render("HOLD", False, white)
    screen.blit(hold_surface, (size*2, size*3.75))
    hold_surface = score_font.render("NEXT", False, white)
    screen.blit(hold_surface, (size*19, size*3.75))
    level_surface = score_font.render("LEVEL " + str(level), False, white)
    screen.blit(level_surface, (size*17.5, size/2))

    pygame.draw.rect(screen, white, (floor))
    pygame.draw.rect(screen, white, (wall1))
    pygame.draw.rect(screen, white, (wall2))
    pygame.draw.rect(screen, white, (hold_bottom))
    pygame.draw.rect(screen, white, (hold_top))
    pygame.draw.rect(screen, white, (hold_side))
    pygame.draw.rect(screen, white, (next_bottom))
    pygame.draw.rect(screen, white, (next_top))
    pygame.draw.rect(screen, white, (next_side))
    pygame.draw.rect(screen, white, (next_side2))
    pygame.draw.rect(screen, white, (hold_side2))

    for row_index, row in enumerate(bag[bag_index]):
        for col_index, cell in enumerate(row):
            if cell == 1:
                x = xpos + col_index * size
                y = ypos + row_index * size
                if wall1.colliderect(pygame.Rect(x, y, size, size)):
                    xpos += size
                if wall2.colliderect(pygame.Rect(x, y, size, size)):
                    xpos -= size
                x = xpos + col_index * size
                pygame.draw.rect(screen, color, (x, y, size, size))

    for block_x, block_y, block_color in blocks:
        pygame.draw.rect(screen, block_color, (block_x, block_y, size, size))

    ghost_y = get_ghost_y(xpos, ypos, bag[bag_index], blocks, floor)
    ghost_color = [min(255, c + 100) for c in color]
    for row_index, row in enumerate(bag[bag_index][:-1]):
        for col_index, cell in enumerate(row):
            if cell == 1:
                x = xpos + col_index * size
                y = ghost_y + row_index * size
                pygame.draw.rect(screen, ghost_color, (x, y, size, size), 1)
    
    for row_index, row in enumerate(next_piece[:-1]):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, next_piece[-1], (size*19.5 + col_index * size, size*7 + row_index * size, size, size))

    if hold_piece:
        for row_index, row in enumerate(hold_piece[:-1]):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, hold_piece[-1], (size*3 + col_index * size, size*7 + row_index * size, size, size))

    pygame.display.flip()
pygame.quit()