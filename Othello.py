import pygame
from time import sleep

INFINITY = 100000


class Board:
    def __init__(self, size, rows):
        self.size = size
        self.boardSize = rows
        self.projectTile = [["o" for _ in range(self.size)] for _ in range(self.size)]

    def grid(self, window):
        distanceRows = self.boardSize // self.size
        x = 0
        y = 0

        for _ in range(self.size):
            x += distanceRows
            y += distanceRows

            # draw the grid with the color
            pygame.draw.line(window, (6, 17, 60), (x, 0), (x, self.boardSize))
            pygame.draw.line(window, (6, 17, 60), (0, y), (self.boardSize, y))

    def makeBoard(self):
        if self.size % 2 != 0:
            self.projectTile[self.size // 2][self.size // 2] = "W"
            self.projectTile[self.size // 2][(self.size // 2) + 1] = "B"
            self.projectTile[(self.size // 2) + 1][self.size // 2] = "B"
            self.projectTile[(self.size // 2) + 1][(self.size // 2) + 1] = "W"
        else:
            self.projectTile[(self.size // 2) - 1][(self.size // 2) - 1] = "W"
            self.projectTile[(self.size // 2) - 1][self.size // 2] = "B"
            self.projectTile[self.size // 2][(self.size // 2) - 1] = "B"
            self.projectTile[self.size // 2][self.size // 2] = "W"

    def markBoard(self, row, col, player):
        self.projectTile[row][col] = player

    def availableBoard(self, row, col):
        return self.projectTile[row][col] == "o"

    def isBoardFull(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.projectTile[row][col] == "o":
                    return False
        return True

    def calculate(self):
        w, b = 0, 0
        for row in range(self.size):
            for col in range(self.size):
                if self.projectTile[row][col] == "W":
                    w += 1
                else:
                    b += 1
        print(f"W: {w}, B: {b}")
        if w > b:
            return "White Win"
        else:
            return "Black Win"

    def drawProjectTile(self, window):
        for row in range(self.size):
            for col in range(self.size):
                if self.projectTile[row][col] == "W":
                    pygame.draw.circle(window, (255, 255, 255), (
                        int(col * (self.boardSize // self.size) + (self.boardSize // self.size) / 2),
                        int(row * (self.boardSize // self.size) + (self.boardSize // self.size) / 2)),
                                       (self.boardSize // self.size) // 2, 0)
                elif self.projectTile[row][col] == "B":
                    pygame.draw.circle(window, (6, 17, 60), (
                        int(col * (self.boardSize // self.size) + (self.boardSize // self.size) / 2),
                        int(row * (self.boardSize // self.size) + (self.boardSize // self.size) / 2)),
                                       (self.boardSize // self.size) // 2, 0)

    def printBoard(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.projectTile[i][j], end=" ")
            print("")
        print("")

    def flip_projectTile(self, row, col, color):
        ROWS, COLS = len(self.projectTile), len(self.projectTile[0])

        def flip(row, col, color, direc):
            dr, dc = direc
            row, col = row + dr, col + dc
            if (row < 0) or (row >= ROWS):
                return False
            if (col < 0) or (col >= COLS):
                return False
            if self.projectTile[row][col] == "o":
                return False
            if self.projectTile[row][col] == color:
                return True
            else:
                if flip(row, col, color, direc):
                    self.projectTile[row][col] = color
                    return True
                else:
                    return False

        flip(row, col, color, [1, 0])
        flip(row, col, color, [-1, 0])
        flip(row, col, color, [0, 1])
        flip(row, col, color, [0, -1])
        flip(row, col, color, [1, 1])
        flip(row, col, color, [-1, -1])
        flip(row, col, color, [1, -1])
        flip(row, col, color, [-1, 1])

    def opponentColor(self, color):
        if color == "B":
            return "W"
        else:
            return "B"

    def checkMove(self, row, col, color):
        ROWS, COLS = len(self.projectTile), len(self.projectTile[0])
        direction = [[1, 0], [-1, 0], [0, 1], [0, -1],
                     [1, 1], [-1, -1], [1, -1], [-1, 1]]

        def legal(row, col, color, direc):
            if self.projectTile[row][col] == color:
                return False
            elif self.projectTile[row][col] == self.opponentColor(color):
                return False
            else:
                dr, dc = direc
                row, col = row + dr, col + dc
                length = 1

                while 0 <= row < ROWS and 0 <= col < COLS:
                    length += 1
                    if self.projectTile[row][col] == "o":
                        return False
                    if self.projectTile[row][col] == color:
                        return length >= 3
                    row, col = row + dr, col + dc
                return False

        for d in direction:
            while legal(row, col, color, d):
                return True

    def graindingStrategy(self, boardSize):
        dictionary = {
            5: [[100, -20, 10, -20, 100],
                [-20, -50, -2, -50, 100],
                [10, -2, 1, -2, 10],
                [-20, -50, -2, -50, -20],
                [100, -20, 10, -20, 100]],
            6: [[100, -20, 10, 10, -20, 100],
                [-20, -50, -2, -2, -50, -20],
                [10, -2, -1, -1, -2, 10],
                [10, -2, -1, -1, -2, 10],
                [-20, -50, -2, -2, -50, -20],
                [100, -20, 10, 10, -20, 100]],
            7: [[100, -20, 10, 5, 10, -20, 100],
                [-20, -50, -2, -2, -2, -50, -20],
                [10, -2, -1, -1, -1, -2, 10],
                [5, -2, -1, -1, -1, -2, 5],
                [10, -2, -1, -1, -1, -2, 10],
                [-20, -50, -2, -2, -2, -50, -20],
                [100, -20, 10, 5, 10, -20, 100]],
            8: [[100, -20, 10, 5, 5, 10, -20, 100],
                [-20, -50, -2, -2, -2, -2, -50, -20],
                [10, -2, -1, -1, -1, -1, -2, 10],
                [5, -2, -1, -1, -1, -1, -2, 5],
                [5, -2, -1, -1, -1, -1, -2, 5],
                [10, -2, -1, -1, -1, -1, -2, 10],
                [-20, -50, -2, -2, -2, -2, -50, -20],
                [100, -20, 10, 5, 5, 10, -20, 100]],
            9: [[100, -20, 10, 5, 5, 5, 10, -20, 100],
                [-20, -50, -2, -2, -2, -2, -2, -50, -20],
                [10, -2, -1, -1, -1, -1, -1, -2, 10],
                [5, -2, -1, -1, -1, -1, -1, -2, 5],
                [5, -2, -1, -1, -1, -1, -1, -2, 5],
                [5, -2, -1, -1, -1, -1, -1, -2, 5],
                [10, -2, -1, -1, -1, -1, -1, -2, 10],
                [-20, -50, -2, -2, -2, -2, -2, -50, -20],
                [100, -20, 10, 5, 5, 5, 10, -20, 100]],
            10: [[100, -20, 10, 5, 5, 5, 5, 10, -20, 100],
                 [-20, -50, -2, -2, -2, -2, -2, -2, -50, -20],
                 [10, -2, -1, -1, -1, -1, -1, -1, -2, 10],
                 [5, -2, -1, -1, -1, -1, -1, -1, -2, 5],
                 [5, -2, -1, -1, -1, -1, -1, -1, -2, 5],
                 [5, -2, -1, -1, -1, -1, -1, -1, -2, 5],
                 [5, -2, -1, -1, -1, -1, -1, -1, -2, 5],
                 [10, -2, -1, -1, -1, -1, -1, -1, -2, 10],
                 [-20, -50, -2, -2, -2, -2, -2, -2, -50, -20],
                 [100, -20, 10, 5, 5, 5, 5, 10, -20, 100]]
        }
        return dictionary.get(boardSize, 0)

    def evaluation(self, color):
        point = 0
        arr = self.graindingStrategy(self.size)
        opponent_color = self.opponentColor(color)
        for row in range(self.size):
            for col in range(self.size):
                if self.projectTile[row][col] == color:
                    point -= arr[row][col]
                elif self.projectTile[row][col] == opponent_color:
                    point += arr[row][col]
        return point

    def minimax(self, depth, color, board):
        if depth == 0:
            return self.evaluation(color)
        best_val = -INFINITY
        best_move = None
        opponent_color = self.opponentColor(color)
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.checkMove(row, col, color):
                    moves.append((row, col))

        if color == "B":
            if len(moves) == 0:
                return self.minimax(depth - 1, "W", self.projectTile)
            for move in moves:
                newBoard = board
                newBoard[move[0]][move[1]] = color
                val = self.minimax(depth - 1, "W", newBoard)
                newBoard[move[0]][move[1]] = "o"
                if val > best_val:
                    best_val = val
            return best_val

        if color == "W":
            if len(moves) == 0:
                return self.minimax(depth - 1, "B", self.projectTile)
            for move in moves:
                newBoard = board
                newBoard[move[0]][move[1]] = color
                val = self.minimax(depth - 1, "B", newBoard)
                newBoard[move[0]][move[1]] = "o"
                if val > best_val:
                    best_val = val
            return best_val

    def opponentNextMove(self, color):
        best_val = -INFINITY
        best_move = None
        score = None
        for row in range(self.size):
            for col in range(self.size):
                if self.checkMove(row, col, color):
                    self.projectTile[row][col] = color
                    score = self.minimax(3, color, self.projectTile)
                    self.projectTile[row][col] = "o"
                    if score > best_val:
                        best_val = score
                        best_move = [row, col]
                    # print(f"row: {row} col: {col}")
        print(f"best move[0]: {best_move[0]} & best move[1]: {best_move[1]}")
        return best_move[0], best_move[1]

    def isThereAnyMove(self, color):
        for row in range(self.size):
            for col in range(self.size):
                if self.checkMove(row, col, color):
                    return True
        return False


def main():
    player = "W"
    boardSize = int(input("Input the size of board (min. 5)\n"))
    window_size = 500
    board = Board(boardSize, window_size)
    board.makeBoard()
    board.printBoard()

    # Set size of window
    window = pygame.display.set_mode((window_size, window_size))
    window.fill((180, 255, 159))
    board.drawProjectTile(window)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = int(mouseY // (window_size // boardSize))
                clicked_col = int(mouseX // (window_size // boardSize))
                if board.isThereAnyMove(player):
                    if board.availableBoard(clicked_row, clicked_col):
                        if player == "W":
                            if board.checkMove(clicked_row, clicked_col, player):
                                board.markBoard(clicked_row, clicked_col, player)
                                board.flip_projectTile(clicked_row, clicked_col, player)
                                board.printBoard()
                                board.drawProjectTile(window)
                                player = "B"
                                if board.isBoardFull():
                                    print(f"Result:\n{board.calculate()}")
                                else:
                                    if player == "B":
                                        row, col = board.opponentNextMove(player)
                                        board.markBoard(row, col, player)
                                        sleep(0.5)
                                        board.flip_projectTile(row, col, player)
                                        board.printBoard()
                                        board.drawProjectTile(window)
                                        player = "W"
                else:
                    player = "B"
                    if board.isThereAnyMove(player):
                        row, col = board.opponentNextMove(player)
                        board.markBoard(row, col, player)
                        sleep(0.5)
                        board.flip_projectTile(row, col, player)
                        board.printBoard()
                        board.drawProjectTile(window)
                        player = "W"
                    else:
                        player = "W"

            if board.isBoardFull():
                print(f"Result:\n{board.calculate()}")

        board.grid(window)
        pygame.display.update()


main()
