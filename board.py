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
        self.on_body = False

    def change_turn(self):
        if self.length == 0 and self.on_body:
            self.on_body = False
        if (self.length != 0) and (not self.turn_protection):
            self.length -= 1
        if self.head:
            self.head = False
        self.turn_protection = True

    def get_apple(self):
        if self.on_body and (not self.turn_protection):
            self.length += 1
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


class Board:
    def __init__(self, apple_func: callable, width: int = 8, height: int = 8, start_pos: (int, int) = (0, 0), start_length: int = 3):
        self.score = start_length

        self.state = np.empty((width, height), dtype=object)
        v_square = np.vectorize(Square)
        self.state[:, :] = v_square(np.arange(width * height).reshape((width, height)))
        self.state[start_pos[0], start_pos[1]].head = True
        self.state[start_pos[0], start_pos[1]].length = start_length

        self.head_pos = start_pos

        self.width = width
        self.height = height

        self.__add_apple__ = apple_func

        self.__add_apple__(self)


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
                self.state[self.head_pos[0], self.head_pos[1]].length > 1:
            return False

        v_change = np.vectorize(lambda x: x.change_turn())
        v_change(self.state)

        v_undo = np.vectorize(lambda x: x.undo_protection())
        v_undo(self.state)

        self.state[self.head_pos[0], self.head_pos[1]].head = True
        self.state[self.head_pos[0], self.head_pos[1]].on_body = True

        self.state[self.head_pos[0], self.head_pos[1]].length = self.score

        # Increase score if apple is eaten
        if self.state[self.head_pos[0], self.head_pos[1]].apple:
            self.score += 1
            self.state[self.head_pos[0], self.head_pos[1]].apple = False
            v_get_apple = np.vectorize(lambda x: x.get_apple())
            v_get_apple(self.state)
            v_undo(self.state)
            self.__add_apple__(self)



        return True

    def __str__(self):

        return "\n".join(["|".join([str(x) for x in row]) for row in self.state])


def random_apples(board):
    while True:
        x = np.random.randint(0, board.width)
        y = np.random.randint(0, board.height)
        if not board.state[x, y].apple and board.state[x, y].length == 0:
            board.state[x, y].apple = True
            break


if __name__ == "__main__":
    print("start")
    board = Board(apple_func=random_apples)
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
