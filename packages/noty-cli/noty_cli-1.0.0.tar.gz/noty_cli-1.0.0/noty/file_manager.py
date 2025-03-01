import os
import re
import logging
from datetime import datetime

class FileManager:
    def __init__(self, notes_dir):
        self.notes_dir = notes_dir

    def get_files(self):
        """Returns a list of note files in the notes directory"""
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)
        files = [f for f in os.listdir(self.notes_dir) 
                if os.path.isfile(os.path.join(self.notes_dir, f))
                and f.endswith('.txt')]
        logging.debug(f"Found files: {files}")
        return sorted(files)

    def create_note(self):
        """Creates a new note with a timestamp-based name"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"note_{timestamp}.txt"
        filepath = os.path.join(self.notes_dir, filename)
        with open(filepath, 'w') as f:
            f.write("")
        logging.debug(f"Created new note: {filename}")
        return filename

    def read_note(self, filename):
        """Reads content of a note file"""
        try:
            filepath = os.path.join(self.notes_dir, filename)
            with open(filepath, 'r') as f:
                content = f.read().splitlines()
            logging.debug(f"Read note {filename}: {content}")
            return content
        except FileNotFoundError:
            logging.error(f"File not found: {filename}")
            return []

    def write_note(self, filename, content):
        """Writes content to a note file"""
        filepath = os.path.join(self.notes_dir, filename)
        with open(filepath, 'w') as f:
            f.write('\n'.join(content))
        logging.debug(f"Wrote to {filename}: {content}")

    def delete_note(self, filename):
        """Deletes a note file"""
        try:
            filepath = os.path.join(self.notes_dir, filename)
            os.remove(filepath)
            logging.debug(f"Deleted note: {filename}")
        except FileNotFoundError:
            logging.error(f"File not found for deletion: {filename}")
            pass

    def rename_note(self, old_filename, new_filename):
        """Renames a note file"""
        old_path = os.path.join(self.notes_dir, old_filename)
        new_path = os.path.join(self.notes_dir, new_filename)
        try:
            os.rename(old_path, new_path)
            logging.debug(f"Renamed {old_filename} to {new_filename}")
        except FileNotFoundError:
            logging.error(f"File not found for rename: {old_filename}")
            pass

    def generate_filename(self, title):
        """Generates a filename from the note's first line"""
        # Clean the title to create a valid filename
        clean_title = re.sub(r'[^\w\s-]', '', title.lower())
        clean_title = re.sub(r'[-\s]+', '-', clean_title).strip('-')
        if len(clean_title) > 50:
            clean_title = clean_title[:50]
        if not clean_title:
            clean_title = "untitled"
        return f"{clean_title}.txt"