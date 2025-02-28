# hmlines

This Python package is designed to show **how many** lines of code and comments your project. 
## Features
- **Quiet mode** : Get only line number without any information with `--quiet` or `-q` flag
- **Custom Comments** : Add your own prefixes for comments. with `--comm` or `-c` flag
- **Raw Input** : Get count of all lines in files with `--raw`  or `-r` flag
- **Ignore Specific Directories**: Exclude directories like `__pycache__` or `venv` to avoid analyzing irrelevant files.
- **File Extension Filtering**: Analyze only files with specific extensions (e.g., `.py`, `.js`).
- **Show File Paths**: Option to print paths of the files being analyzed.
- **Detailed Statistics**: Provides detailed stats for each file, including the count of code and comment lines, as well as percentages.
- **Summarized Results**: Outputs a summary of total lines, code lines, comment lines, and their percentages.

## Installation

### Requirements

- Python 3.x
- No external dependencies are required, the script uses standard Python libraries.
```bash
! pip install hmlines 
```


### Usage
```bash
python hmlines <project-name> [options]
```

### Arguments

- `directory`: Path to the directory you want to analyze.


- `-e`, `--extensions`: Specify which file extensions to analyze. Default is `.py`.

  ```bash
  python hmlines /path/to/project -e ".py,.js"
  ```

- `-i`, `--ignore`: Specify directories to ignore (e.g., `__pycache__`, `venv`). Directories should be separated by commas.

  ```bash
  python hmlines /path/to/project -i "__pycache__,venv"
  ```

- `-show`, `--show-files`: Show the paths of the files being analyzed.

  ```bash
  python hmlines /path/to/project -show
  ```

- `-s`, `--stats`: Show detailed statistics per file (code and comment lines, percentages).
  ```bash
  python hmlines /path/to/project -s
  ```

### Example Command

To analyze all `.py` files in a project while ignoring `__pycache__` and `venv` directories, and show detailed statistics:

```bash
python hmlines /path/to/project -e ".py" -i __pycache__,venv -s
```

### Output Example

#### With `-s` (Detailed Statistics)

```
=== Code Analysis Results ===
| File Extension       | Code      | Code %    | Comments  | Comment % |
|----------------------|-----------|-----------|-----------|-----------|
| .py                  | 100       | 85.0      | 15        | 15.0      |
|----------------------|-----------|-----------|-----------|-----------|
| Total 200 in (2)     | 180       | 90.0      | 20        | 10.0      |
|----------------------|-----------|-----------|-----------|-----------|
```

#### Without `-s` (Summary)

```
Total Lines: 200
Code: 180 (90.0%)
Comment: 20 (10.0%)
```

#### With `-q` (Quiet mode)
```
200
```

## Functions

#### `count_lines_in_file(filepath)`
Counts the number of code and comment lines in a file. It returns a tuple with:
- Number of code lines
- Number of comment lines
- Total number of lines

#### `count_lines_in_directory(directory, file_extensions=('.py',), show_file=False, ignore_dirs=None)`
Recursively scans the directory and analyzes files with the specified extensions. Returns a dictionary containing file statistics per extension:
- Number of files
- Total lines
- Code lines
- Comment lines

### `print_summary(files_by_extension, show_stats=False)`
Prints a summary of the code analysis:
- Total number of files and lines
- Number of code and comment lines with percentage
- Breakdown of files by extension

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

