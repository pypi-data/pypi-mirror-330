import curses
import logging
from .editor import Mode

class UI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.sidebar_width = 30

    def draw(self, editor):
        self.stdscr.clear()
        self.height, self.width = self.stdscr.getmaxyx()
        logging.debug(f"Terminal dimensions: {self.height}x{self.width}")

        # Calculate available height for content (excluding status bar)
        content_height = self.height - 1
        logging.debug(f"Content height: {content_height}")

        # Draw sidebar
        for y in range(content_height):
            try:
                self.stdscr.addstr(y, self.sidebar_width, "│")
            except curses.error:
                pass

        # Draw files list
        visible_files = editor.files[:content_height]
        for idx, filename in enumerate(visible_files):
            if idx == editor.selected_idx:
                self.stdscr.attron(curses.color_pair(2))
            try:
                self.stdscr.addstr(idx, 0, filename[:self.sidebar_width].ljust(self.sidebar_width))
            except curses.error:
                pass
            if idx == editor.selected_idx:
                self.stdscr.attroff(curses.color_pair(2))

        # Draw editor content
        editor_x = self.sidebar_width + 1
        editor_width = self.width - editor_x - 1  # Leave one column margin
        logging.debug(f"Editor width: {editor_width}")

        if editor.current_note:
            # Ensure content list has enough lines
            while len(editor.content) <= editor.cursor_y:
                editor.content.append("")

            visible_content = editor.content[:content_height]
            logging.debug(f"Drawing content: {visible_content}")
            for idx, line in enumerate(visible_content):
                # Ensure we don't write beyond the screen width
                truncated_line = line[:editor_width]
                try:
                    self.stdscr.addstr(idx, editor_x, truncated_line)
                except curses.error:
                    pass  # Ignore errors from writing at screen boundaries

        # Draw help text and status bar
        status = f" {'INSERT' if editor.mode == Mode.INSERT else 'NORMAL'} | "
        if editor.mode == Mode.NORMAL:
            status += "n:new dd:delete yy:copy p:paste j/k:navigate q:quit | "
        else:
            status += "ESC:normal mode | "
        status += f"{'No File' if not editor.current_note else editor.current_note}"

        # Ensure status line doesn't exceed screen width
        status = status[:self.width - 1]
        try:
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(self.height-1, 0, status)
            # Fill the rest of the status line
            remaining_width = self.width - len(status) - 1
            if remaining_width > 0:
                self.stdscr.addstr(self.height-1, len(status), " " * remaining_width)
            self.stdscr.attroff(curses.color_pair(1))
        except curses.error:
            pass  # Ignore errors from writing at screen boundaries

        # Position cursor
        try:
            if editor.mode == Mode.INSERT and editor.current_note:
                curses.curs_set(1)  # Show cursor in insert mode
                cursor_y = min(editor.cursor_y, content_height - 1)
                cursor_x = min(editor_x + editor.cursor_x, self.width - 2)
                logging.debug(f"Setting cursor to ({cursor_y}, {cursor_x})")
                self.stdscr.move(cursor_y, cursor_x)
            else:
                curses.curs_set(0)  # Hide cursor in normal mode
        except curses.error:
            pass  # Ignore cursor positioning errors

        self.stdscr.refresh()