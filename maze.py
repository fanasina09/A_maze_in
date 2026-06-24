#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   maze.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: zo-rakot <zo-rakot@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/17 19:23:00 by zo-rakot            #+#    #+#            #
#   Updated: 2026/06/23 08:12:03 by zo-rakot           ###   ########.fr      #
#                                                                             #
# ########################################################################### #


import time

# ==========================
# Colors ANSI
# ==========================

WALL  = "\033[38;5;99m"      # Violet néon
PATH  = "\033[38;5;51m"      # Cyan lumineux
START = "\033[38;5;46m"      # Vert néon
END   = "\033[38;5;196m"     # Rouge vif
RESET = "\033[0m"

class Cell():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visited = False
        self.coord = {
            "N": True,
            "S": True,
            "E": True,
            "W": True
        }

    def markVisited(self) -> None:
        self.visited = True


class Maze():
    def __init__(self, width: int, height: int, entry: tuple[int, int], exiting: tuple[int, int]) -> None:
        self.width = width
        self.height = height

        self.grid = self.createGrid()
        self.stack = []
        self.current = None
        self.entry = entry
        self.exit = exiting
        self.start = self.getCell(entry[0], entry[1])
        self.end = self.getCell(exiting[0], exiting[1])

    def createGrid(self) -> list[list[Cell]]:
        grid = []

        for y in range(self.height):
            row = []

            for x in range(self.width):
                row.append(Cell(x, y))
            grid.append(row)

        return (grid)

    def getCell(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            return None

    def reset_visited(self):
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def getNeighbors(self, cell: Cell) -> list[str, int]:
        x, y = cell.x, cell.y
        neighbors = []
        directions = [
            ("N", (x, y - 1)),
            ("S", (x, y + 1)),
            ("E", (x + 1, y)),
            ("W", (x - 1, y))
        ]

        for direction, (nx, ny) in directions:
            neighbor = self.getCell(nx, ny)

            if neighbor and not neighbor.visited:
                neighbors.append((direction, neighbor))

        return (neighbors)

    def removeWall(self, current: Cell, nextCell: Cell, directions: str) -> None:
        if directions == "N":
            current.coord["N"] = False
            nextCell.coord["S"] = False

        elif directions == "S":
            current.coord["S"] = False
            nextCell.coord["N"] = False

        elif directions == "E":
            current.coord["E"] = False
            nextCell.coord["W"] = False

        elif directions == "W":
            current.coord["W"] = False
            nextCell.coord["E"] = False

    def print_title(self):
        title = [
    " █████╗ ███╗   ███╗ █████╗ ███████╗██╗███╗  ██╗██████╗     ██████╗  █████╗ ██████╗ ██╗   ██╗",
    "██╔══██╗████╗ ████║██╔══██╗╚══███╔╝██║████╗ ██║██╔════╝    ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝",
    "███████║██╔████╔██║███████║  ███╔╝ ██║██╔██╗██║██║  ███╗   ██████╔╝███████║██████╔╝ ╚████╔╝ ",
    "██╔══██║██║╚██╔╝██║██╔══██║ ███╔╝  ██║██║╚████║██║   ██║   ██╔══██╗██╔══██║██╔══██╗  ╚██╔╝  ",
    "██║  ██║██║ ╚═╝ ██║██║  ██║███████║██║██║ ╚███║██║   ██║   ██████╔╝██║  ██║███████║   ██║   ",
    "╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚══╝╚█████╔╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝   ╚═╝   ",
    ]

        maze_width = self.width * 4  # approx largeur d'une cellule (3 chars + séparation)

        for line in title:
            line_len = len(line)

            # centre dans la largeur du maze
            padding = max(0, (maze_width // 2) - (line_len // 2))

            print(" " * padding + PATH + line + RESET)

    def display(self, path=None) -> None:
        path_set = set(path) if path else set()
        # top border
        self.print_title()
        print(WALL + "╔" + "═══╦" * self.width + RESET)

        for y in range(self.height):
            line = WALL + "║" + RESET
            bottom = WALL + "╠" + RESET

            for x in range(self.width):
                cell = self.grid[y][x]

                # CONTENT (une seule chose par cellule)
                if cell == self.start:
                    line += START + " ◉ " + RESET

                elif cell == self.end:
                    line += END + " ◎ " + RESET

                elif cell in self.carve_42():
                    line += WALL + "███" + RESET

                elif cell in path_set:
                    line += PATH + " • " + RESET

                else:
                    line += "   "

                # EAST wall
                if cell.coord["E"]:
                    line += WALL + "║" + RESET
                else:
                    line += " "

                # SOUTH wall
                if cell.coord["S"]:
                    bottom += WALL + "═══╩" + RESET
                else:
                    bottom += "   " + WALL + "╬" + RESET

            print(line)
            print(bottom)

    def carve_42(self):
        cx = self.width // 2
        cy = self.height // 2

        pattern = [
            # --- 4 ---
            (0, 0), (0, 1), (0, 2),
            (1, 2),
            (2, 0), (2, 1), (2, 2),
            (2, 3), (2, 4),

            # --- 2 ---
            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4),
        ]

        ox = cx - 4
        oy = cy - 3

        cells = []
        for dx, dy in pattern:
            c = self.getCell(ox + dx, oy + dy)
            if c:
                cells.append(c)

        return set(cells)
