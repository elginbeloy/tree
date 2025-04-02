import os
from time import sleep
from argparse import ArgumentParser


vert = "│"
vert_with_horz = "├"
horz = "─"

connector = f"{vert_with_horz}{horz}{horz} "
indent_str = f"{vert}   "


def get_size_str(file_size_bytes):
  if file_size_bytes >= 1000000000:
    file_size_gigabytes = file_size_bytes / (1000 * 1000 * 1000)
    file_size_gigabytes = round(file_size_gigabytes * 100) / 100
    return str(file_size_gigabytes) + "GB"
  elif file_size_bytes >= 1000000:
    file_size_megabytes = file_size_bytes / (1000 * 1000)
    file_size_megabytes = round(file_size_megabytes * 100) / 100
    return str(file_size_megabytes) + "MB"
  elif file_size_bytes >= 1000:
    file_size_kilobytes = file_size_bytes / 1000
    file_size_kilobytes = round(file_size_kilobytes * 100) / 100
    return str(file_size_kilobytes) + "KB"
  else:
    return str(file_size_bytes) + "B"


def colored(text, color):
  colors = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
  }

  color_code = colors.get(color.lower())
  return f"{color_code}{text}\033[0m"


def print_files_in_path(
  path="/", prefix="", exclude_hidden=False,
  sleep_time=None, exclude_names=[], current_depth=0, max_depth=None):
  total_size = 0

  if max_depth is not None and current_depth > max_depth:
    return total_size

  next_prefix = prefix + indent_str

  for file in sorted(os.listdir(path) or []):
    if file.startswith("."):
      if exclude_hidden:
        hidden_messages.append("Not showing hidden file: " + file)
        continue

    if file in exclude_names:
      hidden_messages.append("Not showing excluded file: " + file)
      continue

    file_path = f"{path}/{file}"

    # Handle symbolic links
    if os.path.islink(file_path):
      link_target = readlink(file_path)
      if os.path.exists(file_path):
        file_size_bytes = os.path.getsize(file_path)
        total_size += file_size_bytes
        print(prefix + connector + colored(file + " -> " + link_target, "magenta"), end="")
        print("  [" + colored(get_size_str(file_size_bytes), "blue") + "]")
      else:
        print(prefix + connector + colored(file + " -> " + link_target, "red") + "  [BROKEN LINK]")
      continue

    file_size_bytes = os.path.getsize(file_path)

    if file.startswith("_") and not os.path.isdir(file_path):
      print(prefix + connector + colored(file, "yellow"), end="")
      print("  [" + colored(get_size_str(file_size_bytes), "blue") + "]")
      continue

    if os.path.isdir(file_path):
      if sleep_time is not None:
        sleep(sleep_time)
      print(prefix + connector + colored(file, "green"))
      dir_size = print_files_in_path(
        path=file_path,
        prefix=next_prefix,
        exclude_hidden=exclude_hidden,
        sleep_time=sleep_time,
        exclude_names=exclude_names,
        current_depth=current_depth+1,
        max_depth=max_depth)
      total_size += dir_size
      print(next_prefix + "[" + colored("TOTAL DIR SIZE: " + get_size_str(dir_size), "blue") + "]")
    else:
      total_size += file_size_bytes
      print(prefix + connector + file, end="")
      print("  [" + colored(get_size_str(file_size_bytes), "blue") + "]")

  return total_size


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument(
    "--path",
    default="./",
    help="The path to start the tree from")
  parser.add_argument(
    "--exclude_hidden",
    action="store_true",
    default=False,
    help="Exclude .hidden files")
  parser.add_argument(
    "--sleep",
    type=float,
    default=None,
    help="Number of seconds to sleep after each directory is printed. Default is 0.")
  parser.add_argument(
    "--exclude_names",
    nargs="*",
    default=[],
    help="Exclude files with the names")
  parser.add_argument(
    "--max_depth",
    type=int,
    default=None,
    help="Limit how many directories deep the search goes. Default is no limit.")
  parser.add_argument(
    "--verbose",
    action="store_true",
    help="Verbose output like hidden files")
  args = parser.parse_args()

  hidden_messages = []
  print(colored("Running Tree: ", "green"), end="")
  print(f"verbose={args.verbose} ", end="| ")
  print(f"exclude_hidden={args.exclude_hidden} ", end="| ")
  print(f"exclude_names={args.exclude_names} ", end="| ")
  print(f"max_recursion_depth={args.max_depth}")
  print_files_in_path(
    args.path,
    exclude_hidden=args.exclude_hidden,
    sleep_time=args.sleep,
    exclude_names=args.exclude_names,
    max_depth=args.max_depth)

  if args.verbose:
    for msg in hidden_messages:
      print(colored(msg, "red"))
