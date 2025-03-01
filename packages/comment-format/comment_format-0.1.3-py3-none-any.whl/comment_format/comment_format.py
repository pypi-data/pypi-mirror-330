"""
Script Name: Comment Checker and Replacer
Description: This script scans source files in a given directory for code comments.
             It can optionally replace them to ensure all comments are of a specified style.

Usage and arguments:
    python script_name.py --help

Author: Alex Fabre
"""

import argparse
import sys

from . import lang_c as C
from . import lang_cpp as CPP

TOOL_VERSION = "0.1.3"

def main():
    parser = argparse.ArgumentParser(description='Check for C++-style and C-style comments in source files.')
    parser.add_argument('style', choices=['c', 'cpp', 'c++'], help='Specify the desired comment style: "c" for C-style or "cpp" for C++-style.')
    parser.add_argument('directory', type=str, help='The directory to scan for comments.')
    parser.add_argument('-r', '--replace', action='store_true', help='Replace comments to match the specified style.')
    parser.add_argument('-i', '--ignore', nargs='+', default=[], help='Regex pattern(s) of file(s) to ignore. (ex: -i \'*/objdict/*\'  or -i \'*CO_OD.[c,h]\' or -i \'*CO_OD.c\' \'*CO_OD.h\')')
    parser.add_argument('--version', action='version', version=f'%(prog)s {TOOL_VERSION}', help='Show the version of the tool and exit.')
    args = parser.parse_args()

    error_count = 0
    if args.style == 'cpp' or args.style == 'c++':
        error_count = C.check_comment_style(args.directory, args.ignore, args.replace, target_style='cpp')
        error_count += C.check_comment_spelling(args.directory)
    elif args.style == 'c':
        error_count = CPP.check_comment_style(args.directory, args.ignore, args.replace, target_style='c')
        error_count += C.check_comment_spelling(args.directory)
    
    sys.exit(error_count)

if __name__ == '__main__':
    main()
