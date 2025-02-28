import os


def count_lines_in_file(filepath, comment_prefixes=None):
    """
    Counts the number of code and comment lines in a file.
    A line is considered a comment if, after stripping whitespace, it starts with any of the prefixes in comment_prefixes.
    Empty lines are not counted as code or comment, but are included in the total line count.
    Returns a tuple: (number of code lines, number of comment lines, total number of lines)
    """
    if comment_prefixes is None:
        comment_prefixes = ["#"]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        code_lines = 0
        comment_lines = 0
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if any(stripped.startswith(prefix) for prefix in comment_prefixes):
                comment_lines += 1
            else:
                code_lines += 1
        return code_lines, comment_lines, len(lines)
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return 0, 0, 0


def count_lines_in_directory(directory, file_extensions=('.py',), show_file=False, ignore_dirs=None,
                             comment_prefixes=None):
    """
    Recursively scans the directory and analyzes files with the specified extensions.
    The ignore_dirs parameter is a list of folder names to exclude.
    Returns:
        files_by_extension — a dictionary where the key is the file extension and the value is a list of the form
                             [number of files, total number of lines, number of code lines, number of comment lines].
    """
    comment_prefixes = comment_prefixes or ['#']
    files_by_extension = {}

    if ignore_dirs is None:
        ignore_dirs = []
    else:
        ignore_dirs = [d.strip() for d in ignore_dirs if d.strip()]

    for root, dirs, files in os.walk(directory):
        # Exclude directories that should be skipped
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(file_extensions):
                file_ext = os.path.splitext(file)[1]
                extension_stat = files_by_extension.get(file_ext, [0, 0, 0, 0])  # [files, total lines, code, comments]

                filepath = os.path.join(root, file)
                if show_file:
                    print(filepath)
                code, comments, lines = count_lines_in_file(filepath, comment_prefixes)
                extension_stat[0] += 1
                extension_stat[1] += lines
                extension_stat[2] += code
                extension_stat[3] += comments

                files_by_extension[file_ext] = extension_stat

    return files_by_extension


def print_summary(files_by_extension, show_stats=False, raw=False, quiet=False):
    """
    Prints a summary of the code analysis.
      - If raw mode is enabled, prints only the total number of lines without breaking them down into code/comments.
      - If quiet mode is enabled, prints only the final total number of lines.
      - Otherwise, prints detailed statistics.
    """
    total_files = 0
    total_code = 0
    total_comments = 0
    total_lines = 0

    for ext, stats in files_by_extension.items():
        files, lines, code_lines, comment_lines = stats
        total_files += files
        total_lines += lines
        total_code += code_lines
        total_comments += comment_lines

    if quiet:
        # Print only the final total number of lines
        print(total_lines)
        return

    if raw:
        # Raw mode: print only the line count for each extension and the overall total
        print("\n=== Raw Lines Count ===")
        for ext, stats in files_by_extension.items():
            files, lines, _, _ = stats
            print(f"{ext}: {lines} lines in {files} file(s)")
        print(f"\nTotal number of lines: {total_lines}")
    else:
        if show_stats:
            print("\n=== Code Analysis Results ===")
            print(f"| {'File Extension':<20} | {'Code':<10} | {'Code %':<10} | {'Comments':<12} | {'Comment %':<10} |")
            print(f"|{'-' * 22}|{'-' * 12}|{'-' * 12}|{'-' * 14}|{'-' * 12}|")
            for ext, stats in files_by_extension.items():
                files, lines, code_lines, comment_lines = stats
                file_total = code_lines + comment_lines
                code_pct = (code_lines / file_total * 100) if file_total > 0 else 0
                comment_pct = (comment_lines / file_total * 100) if file_total > 0 else 0
                print(f"| {ext:<20} | {code_lines:<10} | {round(code_pct,2):<10} | {comment_lines:<12} | {round(comment_pct,2):<10} |")
            overall_total = total_code + total_comments
            overall_code_pct = (total_code / overall_total * 100) if overall_total > 0 else 0
            overall_comment_pct = (total_comments / overall_total * 100) if overall_total > 0 else 0
            print(f"|{'-' * 22}|{'-' * 12}|{'-' * 12}|{'-' * 14}|{'-' * 12}|")
            print(f"| {'Total':<20} | {total_code:<10} | {round(overall_code_pct,2):<10} | {total_comments:<12} | {round(overall_comment_pct,2):<10} |")
            print(f"|{'-' * 22}|{'-' * 12}|{'-' * 12}|{'-' * 14}|{'-' * 12}|")
        else:
            print(f"Total number of lines: {total_lines}")
            total_nonempty = total_code + total_comments
            code_pct = round(total_code / total_nonempty * 100, 2) if total_nonempty > 0 else 0
            comment_pct = round(total_comments / total_nonempty * 100, 2) if total_nonempty > 0 else 0
            print(f"Code lines: {total_code} ({code_pct}%)")
            print(f"Comment lines: {total_comments} ({comment_pct}%)")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Count code lines in a project")
    parser.add_argument("directory", type=str, help="Path to the project directory")
    parser.add_argument("-e", "--extensions", type=str, default=".py",
                        help="File extensions to analyze, separated by commas. Example: .py,.js")
    parser.add_argument("-i", "--ignore", type=str, default="",
                        help="Directories to ignore, separated by commas. Example: __pycache__,venv")
    parser.add_argument("-show", "--show-files", action="store_true",
                        help="Show paths of the analyzed files")
    parser.add_argument("-s", "--stats", action="store_true",
                        help="Show detailed statistics per file")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Quiet mode: print only the final total number of lines")
    parser.add_argument("-r", "--raw", action="store_true",
                        help="Raw mode: count all lines without splitting into code and comments")
    parser.add_argument("-c", "--comm", type=str, default="#",
                        help="Custom comment prefixes, separated by commas. Default is '#'")

    args = parser.parse_args()

    # Process file extensions
    extensions = tuple(ext.strip() for ext in args.extensions.split(",") if ext.strip())
    ignore_dirs = [d.strip() for d in args.ignore.split(",") if d.strip()]

    # Process custom comment prefixes
    comment_prefixes = [p.strip() for p in args.comm.split(",") if p.strip()]

    files_by_extension = count_lines_in_directory(
        args.directory,
        file_extensions=extensions,
        show_file=args.show_files,
        ignore_dirs=ignore_dirs,
        comment_prefixes=comment_prefixes
    )
    print_summary(files_by_extension, show_stats=args.stats, raw=args.raw, quiet=args.quiet)
