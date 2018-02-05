# ============================================================================
# FILE: standalone.py
# AUTHOR: David Johansson
# License: MIT license
# ============================================================================

import curses
from bolt_tui.tui import tui

def print_panes(stdscr, bolt):
    buffer = bolt.get_panes()
    for i in range(0, len(buffer)):
        stdscr.addstr(i, 0, buffer[i])

def main(stdscr):
    # calculate width & height
    width = curses.COLS
    height = curses.LINES - 1

    # init bolt
    bolt = tui(width, height)

    # Clear screen
    stdscr.clear()

    # print the panes
    print_panes(stdscr, bolt)
    
    debug_line = curses.LINES - 1

    while True:

        c = stdscr.getkey()
        stdscr.clear()

        if c == 'q':
            break
        elif c == '\t':
            bolt.cmd_tab()
            stdscr.addstr(debug_line, 1, 'tab      ')
        elif c == 'KEY_UP':
            bolt.cmd_up()
            stdscr.addstr(debug_line, 1, 'up       ')
        elif c == 'KEY_DOWN':
            bolt.cmd_down()
            stdscr.addstr(debug_line, 1, 'down     ')
        elif c == '\x7f':
            stdscr.addstr(debug_line, 1, 'backspace')
        elif c == '\x0a' or c == '\x0d':
            stdscr.addstr(debug_line, 1, 'enter    ')
        else:
            stdscr.addstr(debug_line, 1, c)

        print_panes(stdscr, bolt)
        stdscr.addstr(debug_line,15, str(curses.LINES) + ' x ' + str(curses.COLS))


curses.wrapper(main)
