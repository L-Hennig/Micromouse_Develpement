"""
Stores known information of maze
Has methods to get and set maze information
"""

# bit layout per cell: 0b000VNESW (V=Visited)
W, S, E, N = 1, 2, 4, 8
VISITED = 16

class Memory:
    def __init__(self, width=9, height=9):
        self.width = width
        self.height = height
        self.cells = bytearray(width*height)
        self.flood = bytearray(width*height)

    def _index(self, x, y):
        return y * self.width + x

    def set_wall(self, x, y, direction):
        i = self._index(x, y)
        self.cells[i] |= direction

    def has_wall(self, x, y, direction):
        i = self._index(x, y)
        return bool(self.cells[i] & direction)

    def mark_visited(self, x, y):
        self.cells[self._index(x, y)] |= VISITED

    def is_visited(self, x, y):
        return bool(self.cells[self._index(x, y)] & VISITED)

    def get_flood(self, x, y):
        return self.flood[self._index(x, y)]

    def set_flood(self, x, y, value):
        self.flood[self._index(x, y)] = value