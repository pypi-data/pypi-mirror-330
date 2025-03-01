import subprocess
import os

# ANSI escape codes for colored text
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def log(message):
    print(f'{message}')

def log_error(message):
    print(f'{RED}{message}{RESET}')

def log_info(message):
    print(f'{GREEN}{message}{RESET}')

def check_spelling(comment_text, file_path) -> int:
    """
    Use codespell to check for spelling mistakes in a given comment text.

    Parameters:
        comment_text (str): The comment text to check.
        file_path (str): The path of the file containing the comment.
    """

    result = subprocess.run(
        ['codespell', '-'],
        input=comment_text,
        text=True,
        capture_output=True
    )

    if result.stdout:
        log_error(f"Spelling mistake in {os.path.abspath(file_path)}\n{result.stdout}")
        return 1
    else:
        log_info(f'{file_path} OK')
        return 0