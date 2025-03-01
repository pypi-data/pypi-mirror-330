import os
import re
import fnmatch
import subprocess

from . import utils

def check_comment_style(directory, ignore_patterns, replace=False, target_style=None):
    """
    Scan files for C++-style comments and optionally replace them with C-style comments.
    If file matches any pattern in ignore_patterns, then no check is performed on that file.

    Parameters:
        directory (str): The directory to scan for comments.
        ignore_patterns (list): List of regex patterns to ignore.
        replace (bool): Whether to replace comments with the target style.
        target_style (str): The desired comment style ('c' or 'cpp').

    Returns:
        int: The number of C++-style comments found.
    """

    utils.log(f'Checking comment style...')


    err = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.c', '.cpp', '.h', '.hpp')):
                file_path = os.path.join(root, file)

                # Convert shell-style wildcards to regex patterns
                regex_patterns = [re.compile(fnmatch.translate(pattern)) for pattern in ignore_patterns]

                # Check if file_path matches any ignore pattern
                if any(regex_pattern.fullmatch(file_path) for regex_pattern in regex_patterns):
                    continue

                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                modified = False
                new_lines = []
                for i, line in enumerate(lines):
                    # Check for '//' not preceded by ':' (to avoid URLs like http://)
                    if '//' in line and not line.strip().startswith('http'):
                        comment_index = line.find('//')
                        if replace and target_style == 'c':
                            # Replace C++-style comment with C-style comment
                            line = line[:comment_index] + '/*' + line[comment_index+2:].rstrip() + ' */\n'
                            modified = True
                        elif not replace:
                            utils.log_error(f"C++-style comment found: {os.path.abspath(file_path)}:{i + 1}")
                            err += 1
                    new_lines.append(line)

                if replace and modified:
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)

    if err == 0 and not replace:
        utils.log_info(f"No C++-style comments found")
    return err
