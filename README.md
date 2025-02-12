## Directory Tree Printer

This script prints out a file tree starting from a specified path.
The output includes directories, files, bytes for each, and 
optionally hidden files as well. Files and directories are color-coded 
for easy identification. You can limit the recursion depth and make it
print out at a custom speed for a cool visual all using flags.

### Usage

Run the python script with the following command:

```bash
python main.py --path [path]
```

Use the `--help` flag for a list of options and usage information.

### As A Command

You can add it as an alias to your `.bashrc`, `.zshrc`, etc... for 
quick usage in your cli as the default path is the current directory.

```bash
alias tree="python3 ~/tree/main.py"
```

### Dependencies

This script requires the `os`, `argparse`, `time`, and `termcolor` modules.
