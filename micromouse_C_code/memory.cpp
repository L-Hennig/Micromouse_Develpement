/*
 * Filename: memory.cpp
 * Description: C++ port of memory.py for Arduino IDE (arduino-pico core).
 */
#include "memory.h"
#include <string.h>

Memory::Memory() {
  reset();
}

void Memory::reset() {
  memset(_cells, 0, sizeof(_cells));
  memset(_flood, 0, sizeof(_flood));
}

void Memory::set_wall(uint8_t x, uint8_t y, Direction direction) {
  _cells[_index(x, y)] |= (1 << direction);
}

bool Memory::has_wall(uint8_t x, uint8_t y, Direction direction) const {
  return _cells[_index(x, y)] & (1 << direction);
}

void Memory::mark_visited(uint8_t x, uint8_t y) {
  _cells[_index(x, y)] |= VISITED;
}

bool Memory::is_visited(uint8_t x, uint8_t y) const {
  return _cells[_index(x, y)] & VISITED;
}

uint8_t Memory::get_flood(uint8_t x, uint8_t y) const {
  return _flood[_index(x, y)];
}

void Memory::set_flood(uint8_t x, uint8_t y, uint8_t value) {
  _flood[_index(x, y)] = value;
}

void Memory::block_unvisited() {
  uint8_t all_walls = (1 << NORTH) | (1 << EAST) | (1 << SOUTH) | (1 << WEST);
  for (uint8_t y = 0; y < MAZE_HEIGHT; y++) {
    for (uint8_t x = 0; x < MAZE_WIDTH; x++) {
      if (!is_visited(x, y)) {
        _cells[_index(x, y)] |= all_walls;
      }
    }
  }
}