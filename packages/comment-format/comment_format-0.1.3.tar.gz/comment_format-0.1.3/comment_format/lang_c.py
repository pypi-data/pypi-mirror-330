import os
import re
import fnmatch

from . import utils

def check_comment_spelling(directory):
    """
    Check for spelling mistakes in comments found in C source files (.c and .h).

    Parameters:
        directory (str): The directory to scan for comments.

    Returns:
        int: The number of spelling mistakes found in comments.
    """

    utils.log(f'Checking comment spelling...')

    err = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.c', '.h')):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r') as f:
                    lines = f.readlines()

                comments = []  # Aggregate all comments here

                for i, line in enumerate(lines):
                    # Find single-line comments
                    if '//' in line:
                        comment_index = line.find('//')
                        comment_text = line[comment_index+2:].strip()
                        comments.append(comment_text)
                    
                    # Find multi-line C-style comments
                    elif '/*' in line:
                        start_index = line.find('/*')
                        end_index = line.find('*/', start_index)
                        if end_index != -1:
                            # Single-line C-style comment
                            comment_text = line[start_index+2:end_index].strip()
                            comments.append(comment_text)
                        else:
                            # Multi-line C-style comment
                            comment_lines = [line[start_index+2:].strip()]
                            i += 1
                            while i < len(lines) and '*/' not in lines[i]:
                                comment_lines.append(lines[i].strip())
                                i += 1
                            if i < len(lines):
                                end_index = lines[i].find('*/')
                                comment_lines.append(lines[i][:end_index].strip())
                            comment_text = ' '.join(comment_lines)
                            comments.append(comment_text)

                # Join all comments into a single string separated by newlines
                aggregated_comments = '\n'.join(comments)

                # Check spelling for all comments at once
                err += utils.check_spelling(aggregated_comments, file_path)
                
    return err


def check_comment_style(directory, ignore_patterns, replace=False, target_style=None):
    """
    Scan files for C-style comments and optionally replace them with C++-style comments.
    If file matches any pattern in ignore_patterns, then no check is performed on that file.

    Parameters:
        directory (str): The directory to scan for comments.
        ignore_patterns (list): List of regex patterns to ignore.
        replace (bool): Whether to replace comments with the target style.
        target_style (str): The desired comment style ('c' or 'cpp').

    Returns:
        int: The number of C-style comments found.
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
                i = 0
                while i < len(lines):
                    line = lines[i]
                    if '/*' in line:
                        start_index = line.find('/*')
                        end_index = line.find('*/', start_index)
                        if end_index != -1:
                            # Single-line C-style comment
                            if replace and target_style == 'cpp':
                                # Replace C-style comment with C++-style comment
                                line = line[:start_index] + '//' + line[start_index+2:end_index].strip() + '\n'
                                modified = True
                            elif not replace:
                                utils.log_error(f"C-style comment found: {os.path.abspath(file_path)}:{i + 1}")
                                err += 1
                        else:
                            # Multi-line C-style comment
                            comment_lines = [line[start_index:]]
                            i += 1
                            while i < len(lines) and '*/' not in lines[i]:
                                comment_lines.append(lines[i])
                                i += 1
                            if i < len(lines):
                                comment_lines.append(lines[i][:lines[i].find('*/') + 2])
                                if replace and target_style == 'cpp':
                                    # Convert multi-line C-style comment to C++-style
                                    for j, comment_line in enumerate(comment_lines):
                                        if j == 0:
                                            new_lines.append(line[:start_index] + '//' + comment_line[2:].strip() + '\n')
                                        elif j == len(comment_lines) - 1:
                                            new_lines.append('//' + comment_line[:-2].strip() + '\n')
                                        else:
                                            new_lines.append('//' + comment_line.strip() + '\n')
                                    modified = True
                                elif not replace:
                                    utils.log_error(f"Multi-line C-style comment found: {os.path.abspath(file_path)}:{i + 1}")
                                    err += 1
                            continue
                    new_lines.append(line)
                    i += 1

                if replace and modified:
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)

    if err == 0 and not replace:
        utils.log_info(f"No C-style comments found")
    return err
