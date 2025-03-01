#!/usr/bin/env python3
import curses
import sys
import os
import argparse
from noty.editor import Editor
from noty.ui import UI
from noty.file_manager import FileManager
from noty import __version__

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='A terminal-based note-taking application with vim-like navigation')
    parser.add_argument('--version', action='version', version=f'noty {__version__}')
    parser.parse_args()

    # Initialize curses with proper settings
    os.environ.setdefault('ESCDELAY', '25')  # Reduce ESC key delay
    curses.wrapper(_main_wrapped)

def _main_wrapped(stdscr):
    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Status bar
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE) # Selected item
    curses.init_pair(3, curses.COLOR_YELLOW, -1)  # Directory

    # Hide cursor
    curses.curs_set(0)

    # Initialize components
    notes_dir = os.path.expanduser("~/notes")
    if not os.path.exists(notes_dir):
        os.makedirs(notes_dir)

    file_manager = FileManager(notes_dir)
    ui = UI(stdscr)
    editor = Editor(file_manager, ui)

    # Enable keypad for special keys
    stdscr.keypad(1)

    # Don't wait for enter key
    stdscr.nodelay(0)

    # Main loop
    while True:
        try:
            # Get terminal size on each iteration
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            min_height = 3
            min_width = 10  # Reduced from 20

            if height < min_height or width < min_width:
                message = f"Terminal too small. Minimum size: {min_width}x{min_height}"
                try:
                    stdscr.addstr(0, 0, message[:width-1])  # Ensure message fits
                    stdscr.refresh()
                except curses.error:
                    pass  # If even the error message doesn't fit, just continue
                curses.napms(100)
                continue

            editor.refresh()
            key = stdscr.getch()
            if not editor.handle_input(key):
                break
        except KeyboardInterrupt:
            break
        except curses.error:
            # Handle terminal resize or other curses errors
            stdscr.clear()
            stdscr.refresh()
            continue

if __name__ == "__main__":
    main()