"""
Stores known information of maze
Has methods to get and set maze information
"""

# bit layout per cell: 0b000VWSEN (V=Visited)
N, E, S, W = 0, 1, 2, 3
VISITED = 16

class Memory:
    def __init__(self, width=9, height=9):
        self.width = width
        self.height = height
        self.cells = bytearray(width*height)
        self.flood = bytearray(width*height)
        # potentially prefill boarder walls

    def _index(self, x, y):
        return y * self.width + x

    def set_wall(self, x, y, direction):
        i = self._index(x, y)
        self.cells[i] |= (1<<direction)

    def has_wall(self, x, y, direction):
        i = self._index(x, y)
        return bool(self.cells[i] & (1<<direction))

    def mark_visited(self, x, y):
        self.cells[self._index(x, y)] |= VISITED

    def is_visited(self, x, y):
        return bool(self.cells[self._index(x, y)] & VISITED)

    def get_flood(self, x, y):
        return self.flood[self._index(x, y)]

    def set_flood(self, x, y, value):
        self.flood[self._index(x, y)] = value

    def block_unvisited(self):
        all_walls = (1<<N) | (1<<E) | (1<<S) | (1<<W)
        for y in range(self.height):
            for x in range(self.width):
                if not self.is_visited(x, y):
                    self.cells[self._index(x, y)] |= all_walls
