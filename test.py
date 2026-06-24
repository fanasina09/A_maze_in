#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   test.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: zo-rakot <zo-rakot@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/06/18 02:29:58 by zo-rakot            #+#    #+#            #
#   Updated: 2026/06/18 04:13:02 by zo-rakot           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

#!/usr/bin/env python3
"""
Petit utilitaire CLI pour générer et afficher un labyrinthe à partir de maze.py

Usage exemple:
  python3 maze_cli.py --width 20 --height 10 --seed 42
  python3 maze_cli.py -w 30 -h 15 --save out.png --seed 123
"""
from __future__ import annotations
import argparse
import random
from typing import List, Tuple, Optional
from maze import Maze, Cell

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

def validate_args(width: int, height: int) -> None:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive integers")

def carve_entrance_exit(m: Maze) -> None:
    # Ouvre l'entrée en haut à gauche (N) et la sortie en bas à droite (S)
    start = m.getCell(0, 0)
    end = m.getCell(m.width - 1, m.height - 1)
    if start:
        start.coord["N"] = False
    if end:
        end.coord["S"] = False

def render_ascii(m: Maze, solution: Optional[List[Tuple[int,int]]] = None) -> str:
    w, h = m.width, m.height
    # chaque cellule -> représentée par " _" pour south wall et "|" pour east wall
    out_lines = []
    # top border
    top = "+"
    for x in range(w):
        top += "---+"
    out_lines.append(top)
    for y in range(h):
        line_top = "|"
        line_bottom = "+"
        for x in range(w):
            c = m.getCell(x, y)
            in_solution = solution is not None and (x, y) in solution
            # contenu de la cellule
            if in_solution:
                body = " * "
            else:
                body = "   "
            # Est-ce que le mur Est existe ?
            if c.coord["E"]:
                line_top += body + "|"
            else:
                line_top += body + " "
            # South wall
            if c.coord["S"]:
                line_bottom += "---+"
            else:
                line_bottom += "   +"
        out_lines.append(line_top)
        out_lines.append(line_bottom)
    return "\n".join(out_lines)

def solve_bfs(m: Maze) -> Optional[List[Tuple[int,int]]]:
    from collections import deque
    start = (0, 0)
    goal = (m.width - 1, m.height - 1)
    q = deque([start])
    prev = {start: None}
    while q:
        x, y = q.popleft()
        if (x, y) == goal:
            break
        c = m.getCell(x, y)
        # pour chaque direction sans mur, ajouter voisin
        if not c.coord["N"]:
            nb = (x, y - 1)
            if nb not in prev:
                prev[nb] = (x, y)
                q.append(nb)
        if not c.coord["S"]:
            nb = (x, y + 1)
            if nb not in prev:
                prev[nb] = (x, y)
                q.append(nb)
        if not c.coord["E"]:
            nb = (x + 1, y)
            if nb not in prev:
                prev[nb] = (x, y)
                q.append(nb)
        if not c.coord["W"]:
            nb = (x - 1, y)
            if nb not in prev:
                prev[nb] = (x, y)
                q.append(nb)
    if goal not in prev:
        return None
    # reconstituer le chemin
    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path

def save_png(m: Maze, filename: str, cell_size: int = 20, path: Optional[List[Tuple[int,int]]] = None) -> None:
    if not PIL_AVAILABLE:
        raise RuntimeError("Pillow non disponible. Installe `pip install pillow` pour activer save PNG.")
    w, h = m.width, m.height
    img_w = w * cell_size + 1
    img_h = h * cell_size + 1
    img = Image.new("RGB", (img_w, img_h), "white")
    draw = ImageDraw.Draw(img)
    # dessiner murs
    for y in range(h):
        for x in range(w):
            c = m.getCell(x, y)
            x0 = x * cell_size
            y0 = y * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            if c.coord["N"]:
                draw.line([(x0, y0), (x1, y0)], fill="black")
            if c.coord["S"]:
                draw.line([(x0, y1), (x1, y1)], fill="black")
            if c.coord["W"]:
                draw.line([(x0, y0), (x0, y1)], fill="black")
            if c.coord["E"]:
                draw.line([(x1, y0), (x1, y1)], fill="black")
    # solution en rouge
    if path:
        px = [((x * cell_size + cell_size//2), (y * cell_size + cell_size//2)) for (x,y) in path]
        draw.line(px, fill="red", width=max(1, cell_size//6))
    img.save(filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", type=int, default=20)
    parser.add_argument("-H", "--height", type=int, default=10)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--save", type=str, default=None, help="Fichier PNG de sortie (requiert pillow)")
    parser.add_argument("--show-solution", action="store_true", help="Afficher solution (BFS) dans l'ASCII")
    args = parser.parse_args()

    validate_args(args.width, args.height)
    if args.seed is not None:
        random.seed(args.seed)

    m = Maze(args.width, args.height)
    m.generate()
    carve_entrance_exit(m)

    solution = None
    if args.show_solution:
        solution = solve_bfs(m)

    print(render_ascii(m, solution=solution))

    if args.save:
        save_png(m, args.save, path=solution)
        print(f"Sauvegardé dans {args.save}")

if __name__ == "__main__":
    main()
