from random import randint

class Board():
    def __init__(self, dims, no_of_bombs):
        if no_of_bombs > dims[0]*dims[1]:
            raise GenerationError

        self.dims = dims
        self.no_of_bombs = no_of_bombs
        self.generateBombBoard()
        self.generateNumberBoard()

    def generateBombBoard(self):
        self.bomb_board = [[0 for _ in range(self.dims[1])] for _ in range(self.dims[0])]
        for _ in range(self.no_of_bombs):
            pos = [randint(0,self.dims[0]-1), randint(0,self.dims[1]-1)]

            while self.bomb_board[pos[0]][pos[1]] == 1:
                pos = [randint(0,self.dims[0]-1), randint(0,self.dims[1]-1)]
            self.bomb_board[pos[0]][pos[1]] = 1
        
    def generateNumberBoard(self):
        self.number_board = [[0 for i in range(self.dims[1])] for j in range(self.dims[0])]
        for i, row in enumerate(self.bomb_board):
            for j, value in enumerate(row):
                if value == 1:
                    for z in range(3):
                        self.bombAroundTile(i,j,-1,z-1)
                        self.bombAroundTile(i,j,1,z-1)
                    self.bombAroundTile(i,j,0,-1)
                    self.bombAroundTile(i,j,0,1)

    def bombAroundTile(self,i,j,x,y):
        if (i+x) < 0 or (j+y) < 0 or (i+x) >= self.dims[0] or (j+y) >= self.dims[1]:
            return
        self.number_board[i+x][j+y] += 1
        


class GenerationError(Exception):
    def __init__(self):
        self.message = "More bombs than positions on board"
        super().__init__(self.message)