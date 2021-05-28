import random

class Piece:
    pieces = [
        # piece layout is stored as 4 numbers, which correspond to:
        # 1  2  3  4
        # 5  6  7  8
        # 9 10 11 12
        #13 14 15 16
        # all rotations are also stored
        # I piece
        [[4, 5, 6, 7], [1, 5, 9, 13], [4, 5, 6, 7], [2, 6, 10, 14]],
        # J piece
        [[0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10], [1, 2, 5, 9]],
        # L piece
        [[3, 5, 6, 7], [1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11]],
        # S piece
        [[2, 3, 5, 6], [1, 5, 6, 10], [2, 3, 5, 6], [2, 6, 7, 11]],
        # Z piece
        [[1, 2, 6, 7], [2, 5, 6, 9], [1, 2, 6, 7], [3, 6, 7, 10]],
        # T piece
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        # O piece
        [[1, 2, 5, 6]]
    ]

    # initialize with position, type of piece, and rotation
    def __init__(self, x, y, piece_type):
        self.x = x
        self.y = y
        self.rotation = 0
        self.type = piece_type

    # rotate, either clockwise or counterclockwise
    def rotate(self, direction):
        if(direction == 1):
            self.rotation = (self.rotation + 1) % len(self.pieces[self.type])
        else:
            self.rotation = (self.rotation + 3) % len(self.pieces[self.type])

    # returns the position of each square of the piece, useful for drawing    
    def return_positions(self):
        return self.pieces[self.type][self.rotation]
