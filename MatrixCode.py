import time
import curses
import numpy as np
import string
import sys

stdscr = curses.initscr()

rows = curses.LINES - 2
cols = curses.COLS - 2
health = rows
health_limit = rows / 2
health_pad = rows / 8
duration = int(sys.argv[1]) if len(sys.argv) > 1 else 100
delay = 0.05

def decay(matrix):
    matrix = np.vectorize(lambda x: x-1 if x > -health_pad else health+np.random.randint(0, health_limit))(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            curr = matrix[i][j]

            if curr == health - 1 and i+1 < rows:
                matrix[i+1][j] = health
    return matrix
            

def main(stdscr):
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    chars = np.random.choice(list(string.ascii_lowercase), size=(rows, cols))
    charsTime = np.zeros(chars.shape)
    charsTime[0] = np.floor(np.random.rand(cols) * health)

    for col in range(len(charsTime[0])):
        curr = charsTime[0][col] + 1
        row = 1
        while (curr <= health and row < rows):
            charsTime[row][col] = curr
            curr += 1
            row += 1   

    i = 0
    while i < duration:
        for j in range(len(chars)):
            for k in range(len(chars[0])):
                if charsTime[j][k] == health:
                    stdscr.addstr(j, k, chars[j][k], curses.color_pair(2))
                elif charsTime[j][k] > health_limit:
                    stdscr.addstr(j, k, chars[j][k], curses.color_pair(1))
                else:
                    stdscr.addstr(j, k, " ")
        time.sleep(delay)
        charsTime = decay(charsTime)
        stdscr.refresh()
        i += 1



    stdscr.getkey()

curses.wrapper(main)