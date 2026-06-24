#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   solver.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: zo-rakot <zo-rakot@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/23 05:52:48 by zo-rakot            #+#    #+#            #
#   Updated: 2026/06/23 08:27:22 by zo-rakot           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import time

def clear():
    print("\033[H\033[J", end="")


def solve(maze, delay=0.04):
    maze.reset_visited()

    stack = []
    parent = {}

    start = maze.start
    end = maze.end

    current = start
    current.visited = True

    while True:
        clear()
        maze.display()
        time.sleep(delay)

        if current == end:
            break

        x, y = current.x, current.y

        neighbors = []

        if not current.coord["N"]:
            n = maze.getCell(x, y - 1)
            if n and not n.visited:
                neighbors.append(n)

        if not current.coord["S"]:
            s = maze.getCell(x, y + 1)
            if s and not s.visited:
                neighbors.append(s)

        if not current.coord["E"]:
            e = maze.getCell(x + 1, y)
            if e and not e.visited:
                neighbors.append(e)

        if not current.coord["W"]:
            w = maze.getCell(x - 1, y)
            if w and not w.visited:
                neighbors.append(w)

        if neighbors:
            stack.append(current)
            nxt = neighbors[0]   #FIX : déterministe (au lieu de random)
            parent[nxt] = current
            current = nxt
            current.visited = True

        elif stack:
            current = stack.pop()
        else:
            return None

    # =========================
    # reconstruction du path
    # =========================
    path = []
    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    # =========================
    # animation finale propre
    # =========================
    for i in range(len(path)):
        clear()
        maze.display(path=path[:i + 1])
        time.sleep(delay)

    return path