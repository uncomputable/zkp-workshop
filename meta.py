from typing import Callable, TypeVar
import os
import re
import sys

T = TypeVar("T")


def update_variable(file_path: str, pattern: Callable[[T], str], updated_value: T):
    """
    Updates the variable inside the given file to the given updated value.

    **The variable should occur exactly once in the file!**

    :param file_path: Python file
    :param pattern: Function that takes a value and returns the string of the form `name = value` that defines the variable
    :param updated_value: New value for the variable
    """
    if not os.path.exists(file_path):
        print(f"{file_path} does not exist. Make sure to run this script from the root directory of this repo.")
        sys.exit(1)

    regex = re.compile(re.escape(pattern("できれば現れない文字")).replace("できれば現れない文字", ".*"))
    update = pattern(updated_value)

    apply = input(f"Do you want to apply the update to {file_path}? y/n: ")
    if apply.lower() == "y":
        with open(file_path, "r") as f:
            file_data = f.read()
        if not regex.search(file_data):
            print(f"Variable not found in {file_path}. Wrong file name?")

        file_data = regex.sub(update, file_data)
        with open(file_path, "w") as f:
            f.write(file_data)

        print(f"Successfully updated {file_path}")
    else:
        do_print = input("Print updated value? y/n: ")
        if do_print.lower() == "y":
            print(update)

        print("No file update")
