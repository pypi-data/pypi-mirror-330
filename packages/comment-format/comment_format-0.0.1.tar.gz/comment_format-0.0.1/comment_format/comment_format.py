"""
Script Name: Comment Checker and Replacer
Description: This script scans source files in a given directory for code comments.
             It can optionally replace them to ensure all comments are of a specified style.

Usage and arguments:
    python script_name.py --help

Author: Alex Fabre
"""

import os
import argparse
import re
import sys

# ANSI escape codes for colored text
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

def find_cpp_comment_style(directory, ignore_patterns, replace=False, target_style=None):
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
    err = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.c', '.cpp', '.h', '.hpp')):
                file_path = os.path.join(root, file)

                # Check if file matches any ignore pattern
                if any(re.match(pattern, file) for pattern in ignore_patterns):
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
                            print(f"{RED}C++-style comment found: {os.path.abspath(file_path)}:{i + 1}{RESET}")
                            err += 1
                    new_lines.append(line)

                if replace and modified:
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)

    if err == 0 and not replace:
        print(f"{GREEN}No C++-style comments found{RESET}")
    return err

def find_c_comment_style(directory, ignore_patterns, replace=False, target_style=None):
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
    err = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.c', '.cpp', '.h', '.hpp')):
                file_path = os.path.join(root, file)

                # Check if file matches any ignore pattern
                if any(re.match(pattern, file) for pattern in ignore_patterns):
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
                                print(f"{RED}C-style comment found: {os.path.abspath(file_path)}:{i + 1}{RESET}")
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
                                    print(f"{RED}Multi-line C-style comment found: {os.path.abspath(file_path)}:{i + 1}{RESET}")
                                    err += 1
                            continue
                    new_lines.append(line)
                    i += 1

                if replace and modified:
                    with open(file_path, 'w') as f:
                        f.writelines(new_lines)

    if err == 0 and not replace:
        print(f"{GREEN}No C-style comments found{RESET}")
    return err

def main():
    parser = argparse.ArgumentParser(description='Check for C++-style and C-style comments in source files.')
    parser.add_argument('style', choices=['c', 'cpp', 'c++'], help='Specify the desired comment style: "c" for C-style or "cpp" for C++-style.')
    parser.add_argument('directory', type=str, help='The directory to scan for comments.')
    parser.add_argument('-r', '--replace', action='store_true', help='Replace comments to match the specified style.')
    parser.add_argument('-i', '--ignore', nargs='+', default=[], help='Regex pattern(s) of file(s) to ignore. (ex: -i \'test_.*\\.cpp\' or -i \'test_.*\\.cpp\' \'.*_backup\\.c\' \'old_.*\\.h\')')
    args = parser.parse_args()

    error_count = 0
    if args.style == 'cpp' or args.style == 'c++':
        error_count = find_c_comment_style(args.directory, args.ignore, args.replace, target_style='cpp')
    elif args.style == 'c':
        error_count = find_cpp_comment_style(args.directory, args.ignore, args.replace, target_style='c')
    
    sys.exit(error_count)

if __name__ == '__main__':
    main()
