import numpy as np


class Move:
    LEFT = (False, False)
    RIGHT = (False, True)
    UP = (True, False)
    DOWN = (True, True)


class Square:
    def __init__(self, pos):
        self.head = False
        self.apple = False
        self.length = 0
        self.turn_protection = False

    def change_turn(self):
        if (not self.apple) and (self.length != 0) and (not self.turn_protection):
            self.length -= 1
        if self.head:
            self.head = False
        self.turn_protection = True

    def undo_protection(self):
        self.turn_protection = False

    def __str__(self):
        if self.head:
            return "X"
        elif self.apple:
            return "O"
        elif self.length >= 10:
            return "*"
        elif self.length > 0:
            return str(self.length)
        else:
            return " "


v_square = np.vectorize(Square)


class Board:
    def __init__(self, width: int = 8, height: int = 8, start_pos: (int, int) = (0, 0), start_length: int = 3):
        self.score = start_length

        self.board = np.empty((width, height), dtype=object)
        self.board[:, :] = v_square(np.arange(width * height).reshape((width, height)))
        self.board[start_pos[0], start_pos[1]].head = True
        self.board[start_pos[0], start_pos[1]].length = start_length

        self.head_pos = start_pos

        self.width = width
        self.height = height
        self.__add_apple__()

    def __add_apple__(self):
        while True:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            if not self.board[x, y].apple and self.board[x, y].length == 0:
                self.board[x, y].apple = True
                break

    def next_board(self, move: Move):
        if move == Move.LEFT:
            self.head_pos = (self.head_pos[0], self.head_pos[1] - 1)
        elif move == Move.RIGHT:
            self.head_pos = (self.head_pos[0], self.head_pos[1] + 1)
        elif move == Move.UP:
            self.head_pos = (self.head_pos[0] - 1, self.head_pos[1])
        elif move == Move.DOWN:
            self.head_pos = (self.head_pos[0] + 1, self.head_pos[1])

        if self.head_pos[0] < 0 or \
                self.head_pos[0] >= self.width or \
                self.head_pos[1] < 0 or \
                self.head_pos[1] >= self.height or \
                self.board[self.head_pos[0], self.head_pos[1]].length > 1:
            return False

        v_change = np.vectorize(lambda x: x.change_turn())
        v_change(self.board)

        v_undo = np.vectorize(lambda x: x.undo_protection())
        v_undo(self.board)

        # Increase score if apple is eaten
        if self.board[self.head_pos[0], self.head_pos[1]].apple:
            self.score += 1
            self.board[self.head_pos[0], self.head_pos[1]].apple = False
            self.__add_apple__()

        self.board[self.head_pos[0], self.head_pos[1]].head = True
        self.board[self.head_pos[0], self.head_pos[1]].length = self.score

        return True

    def __str__(self):

        return "\n".join(["|".join([str(x) for x in row]) for row in self.board])


if __name__ == "__main__":
    print("start")
    board = Board()
    test = True
    while test:
        print(board)

        move = input("Enter move: ")
        if move == "q":
            break
        elif move == "a":
            test = board.next_board(Move.LEFT)
        elif move == "d":
            test = board.next_board(Move.RIGHT)
        elif move == "w":
            test = board.next_board(Move.UP)
        elif move == "s":
            test = board.next_board(Move.DOWN)
        else:
            print("Invalid move")
        print("\n")
    print("end")
