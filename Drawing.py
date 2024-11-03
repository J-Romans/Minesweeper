import pygame

pygame.init()
WIDTH,HEIGHT = 400,400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.Font(None, 20)

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (211,211,211)
DARK_GREY = (100,100,100)
RED = (255,0,0)
GREEN = (0,255,0)
text_colours = {1:(0,0,255), 2:(0,100,220), 3:(0,150,190), 4:(40,150,150), 5:(100,100,100), 6:(150,40,40), 7:(170,0,0), 8:(255,0,0)}

board_dims = [16,16]
SCALE = WIDTH/board_dims[0]

def drawNumbers(board):
    for i,row in enumerate(board.number_board):
        for j,value in enumerate(row):
                if board.bomb_board[i][j] == 1:
                    pygame.draw.rect(win, RED,(SCALE*i, SCALE*j, SCALE, SCALE))
                elif value != 0:
                    text = font.render(str(value), True, text_colours[value])
                    centre_coords = text.get_rect(center = (SCALE*(i+1/2),SCALE*(j+1/2)))
                    win.blit(text, centre_coords)

def drawSquares(tiles, colour):
    for i,row in enumerate(tiles):
        for j,value in enumerate(row):
            if value == 1:
                pygame.draw.rect(win, colour,(i*SCALE,j*SCALE, SCALE, SCALE))

def drawLines():
    for i in range(board_dims[0]):
        pygame.draw.line(win,BLACK,(i*SCALE,0), (i*SCALE,HEIGHT))
    for i in range(board_dims[1]):
        pygame.draw.line(win,BLACK,(0,i*SCALE), (WIDTH,i*SCALE))