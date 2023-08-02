from typing import Callable, TypeVar, Tuple
import os
import re

T = TypeVar("T")


def update_variables(file_path: str, patterns: Tuple[Callable[[T], str], ...], updated_values: Tuple[T, ...]):
    """
    Updates the variables inside the given file to the given updated values.

    **Each variable should occur exactly once in the file!**

    :param file_path: Python file
    :param patterns: For each variable, function that takes a value and returns the string of the form `name = value` that defines the variable
    :param updated_values: For each variable, new value for the variable
    """
    if not os.path.exists(file_path):
        raise ValueError(f"{file_path} does not exist. Run this script from the root directory of this repo.")
    if len(patterns) != len(updated_values):
        raise ValueError("Need as many patterns as updated values")

    updates = [patterns[i](updated_values[i]) for i in range(len(patterns))]
    apply = input(f"Do you want to apply the update to {file_path}? y/n: ")

    if apply.lower() == "y":
        with open(file_path, "r") as f:
            file_data = f.read()

        for i in range(len(patterns)):
            regex = re.compile(re.escape(patterns[i]("できれば現れない文字")).replace("できれば現れない文字", ".*"))

            if not regex.search(file_data):
                print(f"Variable not found in {file_path}. Wrong file name?")

            file_data = regex.sub(updates[i], file_data)

        with open(file_path, "w") as f:
            f.write(file_data)

        print(f"Successfully updated {file_path}")
    else:
        do_print = input("Print updated values? y/n: ")
        if do_print.lower() == "y":
            for update in updates:
                print(update)

        print("No file update")


def update_variable(file_path: str, pattern: Callable[[T], str], updated_value: T):
    """
    Updates the variable inside the given file to the given updated value.

    **The variable should occur exactly once in the file!**

    :param file_path: Python file
    :param pattern: Function that takes a value and returns the string of the form `name = value` that defines the variable
    :param updated_value: New value for the variable
    """
    update_variables(file_path, (pattern,), (updated_value,))
