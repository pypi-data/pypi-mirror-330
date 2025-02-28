from pathlib import Path
import os
import re

def get_txt_path(filename, extend=""):
    """
    Create the file path for the report files (.txt)
    Reports have the same filename as the Python code of students.
    """
    dir_ = Path(filename).parents[0]
    path = dir_ / Path(filename).stem
    if extend:
        path = path.with_name(f"{path.stem}_{extend}")
    return path.with_suffix('.txt')

def find_relative_import(import_file):
    """
    This finds the common parent of two file paths.
    Next, it determines the import path for import_file depending on main_file.
    :type import_file: str or Path
    :rtype: Path
    """
    main_file, import_file = Path(os.getcwd()), Path(import_file)

    for parent in main_file.parents:
        try:
            path = import_file.relative_to(parent)
        except ValueError:
            continue
        return path.with_suffix('').as_posix().replace("/", ".").split(".", 1)[1]
    raise ValueError(f"No common parent directory could be found for {main_file} and {import_file}!")

class StudentDict(dict):
    """
    This dictionary only excepts student numbers, either starting with an "s" or not.
    """
    def __init__(self, student_n_format, *args, **kwargs):
        self.student_n_format = student_n_format
        super(StudentDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not re.search(f"{self.student_n_format}$", key, flags=re.IGNORECASE):
            return
        super(StudentDict, self).__setitem__(key, value)

    def __getitem__(self, item):
        try:
            return super(StudentDict, self).__getitem__(item)
        except KeyError as exception:
            print(f"Student number {item} was not found in the Brightspace grade list!")
            return None
