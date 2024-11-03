from Board import Board
from Drawing import *
from sys import exit
import pygame

pygame.init()

def checkZeros(board, tiles,pos):
    number_board = board.number_board
    checked_tiles = []
    new_tiles = [pos]

    change_made = True
    while change_made:
        for tile in list(new_tiles):
            tiles[tile[0]][tile[1]] = 0
            for z in range(3):
                new_tiles = checkTile(board, checked_tiles, new_tiles, tile, -1, z-1)
                new_tiles = checkTile(board, checked_tiles, new_tiles, tile, 1, z-1)
            new_tiles = checkTile(board, checked_tiles, new_tiles, tile, 0, -1)
            new_tiles = checkTile(board, checked_tiles, new_tiles, tile, 0, 1)
        
            checked_tiles.append(tile)
            new_tiles.remove(tile)
        if new_tiles == []:
             change_made = False
    
    for tile in checked_tiles:
        for z in range(3):
            tiles = setTile(tiles, tile, -1, z-1)
            tiles = setTile(tiles, tile, 1, z-1)
        tiles = setTile(tiles, tile, 0, -1)
        tiles = setTile(tiles, tile, 0, 1)
    
    return tiles          

def checkTile(board,checked_tiles, new_tiles, tile, x, y):
    number_board = board.number_board
    subject_tile = [tile[0]+x,tile[1]+y]
    if  subject_tile in checked_tiles or subject_tile in new_tiles: #Not Already Checked
         return new_tiles
    if subject_tile[0] < 0 or subject_tile[1] < 0 or subject_tile[0] >= len(number_board) or subject_tile[1] >= len(number_board[0]): #Actually Exists
         return new_tiles
    if  board.bomb_board[subject_tile[0]][subject_tile[1]] == 1: #Not a Bomb
         return new_tiles
    if number_board[subject_tile[0]][subject_tile[1]] == 0:
                new_tiles.append(subject_tile)
    return new_tiles

def setTile(tiles, tile, x, y):
    if (tile[0]+x) < 0 or (tile[1]+y) < 0 or (tile[0]+x) >= len(tiles) or (tile[1]+y) >= len(tiles[0]):
         return tiles
    
    tiles[tile[0]+x][tile[1]+y] = 0
    return tiles

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                scaled_pos = [int(pos[0]//SCALE),int(pos[1]//SCALE)]
                running = False

        win.fill(GREY)
        drawSquares([[1 for i in range(board_dims[1])]for j in range(board_dims[0])], DARK_GREY)
        drawLines()
        pygame.display.update()



    NO_OF_BOMBS = 32
    board = Board(board_dims,NO_OF_BOMBS)
    while board.bomb_board[scaled_pos[0]][scaled_pos[1]] == 1 or board.number_board[scaled_pos[0]][scaled_pos[1]] != 0:
        board = Board(board_dims,NO_OF_BOMBS)

    clickable_tiles = [[1 for i in range(board_dims[1])] for j in range(board_dims[0])]
    clickable_tiles = checkZeros(board, clickable_tiles,scaled_pos)

    bomb_guesses = [[0 for i in range(board_dims[1])] for j in range(board_dims[0])]
    result = "..."

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                scaled_pos = [int(pos[0]//SCALE),int(pos[1]//SCALE)]
                if bomb_guesses[scaled_pos[0]][scaled_pos[1]] == 1:
                    pass
                elif board.bomb_board[scaled_pos[0]][scaled_pos[1]] == 1:
                    clickable_tiles[scaled_pos[0]][scaled_pos[1]] = 0
                    result = "LOSE"
                    running = False
                elif board.number_board[scaled_pos[0]][scaled_pos[1]] == 0:
                    clickable_tiles = checkZeros(board, clickable_tiles,scaled_pos)
                    bomb_guesses[scaled_pos[0]][scaled_pos[1]] = 0
                else:
                    clickable_tiles[scaled_pos[0]][scaled_pos[1]] = 0
                    bomb_guesses[scaled_pos[0]][scaled_pos[1]] = 0

                if clickable_tiles == board.bomb_board:
                    result = "WIN"
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos = pygame.mouse.get_pos()
                scaled_pos = [int(pos[0]//SCALE),int(pos[1]//SCALE)]

                if bomb_guesses[scaled_pos[0]][scaled_pos[1]] == 0 and clickable_tiles[scaled_pos[0]][scaled_pos[1]] == 1:
                    bomb_guesses[scaled_pos[0]][scaled_pos[1]] = 1
                else:
                    bomb_guesses[scaled_pos[0]][scaled_pos[1]] = 0

        win.fill(GREY)
        drawNumbers(board)
        drawSquares(clickable_tiles, DARK_GREY)
        drawSquares(bomb_guesses, GREEN)
        drawLines()
        pygame.display.update()


    running = True
    while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                running  = False
            if keys[pygame.K_r]:
                main()

            font2 = pygame.font.Font(None, 50)
            text = font2.render("YOU {}!".format(result), True, BLACK)
            centerer = text.get_rect(center = (int(WIDTH/2),int(HEIGHT/2)))
            win.blit(text, centerer)

            pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()