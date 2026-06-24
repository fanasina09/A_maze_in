#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   generate.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: zo-rakot <zo-rakot@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/23 01:04:03 by zo-rakot            #+#    #+#            #
#   Updated: 2026/06/23 09:13:22 by zo-rakot           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import random
import time

def clear():
    print("\033[H\033[J", end="")

def generate(maze, delay=0.009):
    start = maze.getCell(0, 0)
    start.visited = True

    stack = []
    current = start

    while True:
        neighbors = maze.getNeighbors(current)

        if neighbors:
            direction, nxt = random.choice(neighbors)
            maze.removeWall(current, nxt, direction)

            stack.append(current)
            current = nxt
            current.visited = True

        elif stack:
            current = stack.pop()
        else:
            break

        clear()
        maze.display()
        time.sleep(delay)