import os
import argparse
import time
from termcolor import colored

def get_size_str(file_size_bytes):
  if file_size_bytes >= 1000000000:  # 1GB
    file_size_gigabytes = file_size_bytes / (1000 * 1000 * 1000)
    file_size_gigabytes = round(file_size_gigabytes * 100) / 100
    return str(file_size_gigabytes) + "GB"
  elif file_size_bytes >= 1000000: # 1MB
    file_size_megabytes = file_size_bytes / (1000 * 1000)
    file_size_megabytes = round(file_size_megabytes * 100) / 100
    return str(file_size_megabytes) + "MB"
  elif file_size_bytes >= 1000:  # 1KB
    file_size_kilobytes = file_size_bytes / 1000
    file_size_kilobytes = round(file_size_kilobytes * 100) / 100
    return str(file_size_kilobytes) + "KB"
  else:
    return str(file_size_bytes) + "B"

def print_files_in_path(
  path="/", indent=0, exclude_hidden=False, sleep=None, exclude_names=[], current_depth=0, max_depth=None):
  total_size = 0
  if max_depth is not None and current_depth > max_depth:
    return total_size

  for file in sorted(os.listdir(path) or []):
    if file.startswith("."):
      if exclude_hidden:
        hidden_messages.append("Not showing hidden file: " + file)
        continue

    if file in exclude_names:
      hidden_messages.append("Not showing excluded file: " + file)
      continue

    file_path = f"{path}/{file}"
    file_size_bytes = os.path.getsize(file_path)

    if file.startswith("_") and not os.path.isdir(file_path):
      print((" "*indent) + colored(file, "yellow"), end="")
      print("  [" + colored(get_size_str(file_size_bytes) + "KB", "blue") + "]")
      continue

    if os.path.isdir(file_path):
      if sleep is not None:
        time.sleep(sleep)
      print((" "*indent) + colored(file, "green", attrs=["bold", "reverse"]) + " {")
      dir_size = print_files_in_path(
        path=file_path,
        indent=indent+4,
        exclude_hidden=exclude_hidden,
        sleep=sleep,
        exclude_names=exclude_names,
        current_depth=current_depth+1,
        max_depth=max_depth)
      total_size += dir_size
      print((" "*indent) + "}" + "  [" + colored("TOTAL DIR SIZE: " + get_size_str(dir_size), "blue", attrs=["reverse"]) + "]")
    else:
      total_size += file_size_bytes
      print((" "*indent) + file, end="")
      print("  [" + colored(get_size_str(file_size_bytes), "blue") + "]")

  return total_size

parser = argparse.ArgumentParser()
parser.add_argument("--path", default="./", help="The path to start the tree from")
parser.add_argument("--exclude_hidden", action="store_true", default=False, help="Exclude .hidden files")
parser.add_argument("--sleep", type=float, default=None, help="How much time to sleep after each directory is printed. Default is None I.E no sleep.")
parser.add_argument("--exclude_names", nargs="*", default=[], help="Exclude files with the names")
parser.add_argument("--max_depth", type=int, default=None, help="Limit how many directories deep the search goes. Default is no limit.")
parser.add_argument("--verbose", action="store_true", help="Verbose output like hidden files")
args = parser.parse_args()

hidden_messages = []
print(colored("Running Tree: ", "green", attrs=["bold"]), end="")
print(f"verbose={args.verbose} ", end="| ")
print(f"exclude_hidden={args.exclude_hidden} ", end="| ")
print(f"exclude_names={args.exclude_names} ", end="| ")
print(f"max_recursion_depth={args.max_depth}")
print_files_in_path(
  args.path,
  exclude_hidden=args.exclude_hidden,
  sleep=args.sleep,
  exclude_names=args.exclude_names,
  max_depth=args.max_depth)

if args.verbose:
  for msg in hidden_messages:
    print(colored(msg, "red", attrs=["bold"]))
