import os
import argparse
import time
from termcolor import colored

def print_files_in_path(
  path="/", indent=0, exclude_hidden=False, sleep=None, exclude_names=[]):
  for file in os.listdir(path):
    if file.startswith("."):
      if exclude_hidden:
        hidden_messages.append("Not showing hidden file: " + file)
      else:
        print((" "*indent) + colored(file, "blue"))
      continue

    if file in exclude_names:
      hidden_messages.append("Not showing excluded file: " + file)
      continue

    file_path = f"{path}/{file}"
    if file.startswith("_") and not os.path.isdir(file_path):
      print((" "*indent) + colored(file, "yellow"))
      continue

    if os.path.isdir(file_path):
      if sleep is not None:
        time.sleep(sleep)
      print((" "*indent) + colored(file, "green", attrs=["bold", "reverse"]))
      print_files_in_path(
        path=file_path,
        indent=indent+4,
        exclude_hidden=exclude_hidden,
        sleep=sleep,
        exclude_names=exclude_names)
    else:
      print((" "*indent) + file)

parser = argparse.ArgumentParser()
parser.add_argument("--path", default="./", help="The path to start the tree from")
parser.add_argument("--exclude_hidden", action="store_true", default=False, help="Exclude .hidden files")
parser.add_argument("--sleep", type=float, default=None, help="How much time to sleep after each directory is printed. Default is None I.E no sleep.")
parser.add_argument("--exclude_names", nargs="*", default=[], help="Exclude files with the names")
parser.add_argument("--verbose", action="store_true", help="Verbose output like hidden files")
args = parser.parse_args()

hidden_messages = []
print(f"Running Tree: verbose={args.verbose} " + \
  f"| exclude_hidden={args.exclude_hidden} " + \
  f"| exclude_names={args.exclude_names}")
print_files_in_path(
  args.path,
  exclude_hidden=args.exclude_hidden,
  sleep=args.sleep,
  exclude_names=args.exclude_names)

if args.verbose:
  for msg in hidden_messages:
    print(colored(msg, "red", attrs=["bold"]))
