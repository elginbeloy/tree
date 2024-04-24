## Directory Tree Printer

This script prints out a file tree starting from a specified path.
The output includes directories, regular files, and optionally hidden files.
Files and directories are color-coded for easy identification.

### Usage

Run the script with the following command:

```bash
python3 file_tree_printer.py --path [path]
```

or add it as an alias to your `.bashrc`, `.zshrc`, or other `.rc` for 
quick usage in your cli as the default path is the current directory.

```bash
alias tree="python3 ~/tree/main.py"
```

### Arguments

- `--path`: The path to start the tree from. Default is the current directory.
- `--exclude_hidden`: Exclude .hidden files. Default is False.
- `--sleep`: Determines how much time to sleep after each directory is printed. It's a float value. Default is None I.E no sleep.
- `--exclude_names`: Exclude files with the names. Provide a space-separated list. Default is an empty list.
- `--verbose`: Verbose output like if hidden files were omitted. Default is False.

### Output

The script prints out the file tree, with directories and files color-coded. If `--verbose` is set to True, it also prints out messages about hidden and excluded files.

### Dependencies

This script requires the `os`, `argparse`, `time`, and `termcolor` modules.
