import curses
from enum import Enum
import os
import logging

# Configure logging
logging.basicConfig(filename='noty_debug.log', level=logging.DEBUG)

class Mode(Enum):
    NORMAL = 1
    INSERT = 2

class Editor:
    def __init__(self, file_manager, ui):
        self.file_manager = file_manager
        self.ui = ui
        self.mode = Mode.NORMAL
        self.current_note = None
        self.clipboard = None
        self.cursor_y = 0
        self.cursor_x = 0
        self.scroll_offset = 0
        self.files = []
        self.selected_idx = 0
        self.content = []

    def refresh(self):
        self.files = self.file_manager.get_files()
        if self.current_note:
            if self.current_note not in self.files:
                self.current_note = None
                self.content = []
            elif self.mode != Mode.INSERT:  # Only reload content if not in insert mode
                self.content = self.file_manager.read_note(self.current_note)
                logging.debug(f"Refreshed content from file: {self.content}")
        self.ui.draw(self)

    def handle_input(self, key):
        if key == ord('q') and self.mode == Mode.NORMAL:
            return False

        if self.mode == Mode.NORMAL:
            return self._handle_normal_mode(key)
        else:
            return self._handle_insert_mode(key)

    def _handle_normal_mode(self, key):
        if key == ord('i'):
            self.mode = Mode.INSERT
            self.cursor_x = 0
            self.cursor_y = 0
        elif key == ord('j'):
            self.selected_idx = min(self.selected_idx + 1, len(self.files) - 1)
        elif key == ord('k'):
            self.selected_idx = max(0, self.selected_idx - 1)
        elif key == ord('\n'):
            if self.selected_idx < len(self.files):
                self.current_note = self.files[self.selected_idx]
                self.content = self.file_manager.read_note(self.current_note)
                self.cursor_x = 0
                self.cursor_y = 0
        elif key == ord('n'):
            new_note = self.file_manager.create_note()
            self.files.append(new_note)
            self.selected_idx = len(self.files) - 1
            self.current_note = new_note
            self.mode = Mode.INSERT
            self.cursor_x = 0
            self.cursor_y = 0
            self.content = []
        elif key == ord('d'):
            next_key = self.ui.stdscr.getch()
            if next_key == ord('d'):
                if self.selected_idx < len(self.files):
                    to_delete = self.files[self.selected_idx]
                    self.file_manager.delete_note(to_delete)
                    if to_delete == self.current_note:
                        self.current_note = None
                        self.content = []
                    self.files = self.file_manager.get_files()
                    if self.selected_idx >= len(self.files):
                        self.selected_idx = max(0, len(self.files) - 1)
        elif key == ord('y'):
            next_key = self.ui.stdscr.getch()
            if next_key == ord('y') and self.current_note:
                self.clipboard = self.content.copy()
        elif key == ord('p') and self.clipboard:
            self.content.extend(self.clipboard)
            if self.current_note:
                self.file_manager.write_note(self.current_note, self.content)
        return True

    def _handle_insert_mode(self, key):
        if key == 27:  # ESC
            self.mode = Mode.NORMAL
            if self.current_note and self.content:
                logging.debug(f"Saving content on ESC: {self.content}")
                self.file_manager.write_note(self.current_note, self.content)
                # Update filename based on first line
                if self.content:
                    new_name = self.file_manager.generate_filename(self.content[0])
                    if new_name != self.current_note:
                        self.file_manager.rename_note(self.current_note, new_name)
                        self.current_note = new_name
        elif key == curses.KEY_BACKSPACE or key == 127:
            if self.cursor_x > 0:
                if len(self.content) <= self.cursor_y:
                    self.content.append("")
                line = self.content[self.cursor_y]
                self.content[self.cursor_y] = line[:self.cursor_x-1] + line[self.cursor_x:]
                self.cursor_x -= 1
                if self.current_note:
                    self.file_manager.write_note(self.current_note, self.content)
        elif key == 10:  # Enter
            if len(self.content) <= self.cursor_y:
                self.content.append("")
            line = self.content[self.cursor_y]
            self.content[self.cursor_y] = line[:self.cursor_x]
            self.content.insert(self.cursor_y + 1, line[self.cursor_x:])
            self.cursor_y += 1
            self.cursor_x = 0
            if self.current_note:
                self.file_manager.write_note(self.current_note, self.content)
        elif 32 <= key <= 126:  # Printable characters
            if len(self.content) <= self.cursor_y:
                self.content.append("")
            line = self.content[self.cursor_y]
            self.content[self.cursor_y] = line[:self.cursor_x] + chr(key) + line[self.cursor_x:]
            self.cursor_x += 1
            logging.debug(f"Added character {chr(key)} at ({self.cursor_y}, {self.cursor_x-1}), content: {self.content}")
            # Save content after each character input
            if self.current_note:
                self.file_manager.write_note(self.current_note, self.content)
        return True