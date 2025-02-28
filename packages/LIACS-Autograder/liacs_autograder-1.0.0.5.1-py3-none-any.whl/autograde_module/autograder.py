from pathlib import Path
import time
import re
from yaml import safe_load
import os
import pandas as pd

# tmp solution, search for the overall autograding directory and add it to path.
# try:
#     import sys
#     main_folder_name = "autograding"  # This could be in the overall .yml file
#     sys.path.append(re.search(f".*/{main_folder_name}(?=/)", Path(__file__).as_posix()).group(0))
# except AttributeError:
#     pass

# These two lines make it possible to use relative imports, when working in the autograde module
# import relative_import
# relative_import.enable_relative()

from .multiproccessing_extended import UnittestProcess
from . import subprocess_controller, utils

class ProcessManager():
    def __init__(self, dir_, config):
        self.processes = []
        self.dir = dir_
        self.config = config
        self.student_files_name_suite = []
        self.student_number_to_file = {}

        # if exclude string exists add to regex otherwise leave it out
        if self.config["exclude_strings"]:
            self.student_n_regex = fr'(?<={self.config["filename_format"]})_?\d*_?[s|S]?(?P<digits>{self.config["student_n_format"]})((?!{self.config["exclude_strings"]}).)*$'
        else:
            self.student_n_regex = fr'(?<={self.config["filename_format"]})_?\d*_?[s|S]?(?P<digits>{self.config["student_n_format"]}).*$'

        self.init_test_configs()

    def init_test_configs(self):
        """Loads test config yaml file."""
        # Get relative path of assignment config folder
        config_folder = self.dir / "config"
        crt_folder = Path.cwd()
        config_folder = config_folder.relative_to(crt_folder)

        # Read and store assignment config
        with open(config_folder / "test_config.yaml") as config_file:
            self.test_config = safe_load(config_file)

    def start(self):
        # Go through all the student files.
        for file in self.dir.rglob("*.py"):
            file = file.resolve()  # create absolute file path

            # incorrect file format
            if not re.search(self.student_n_regex, str(file), flags=re.IGNORECASE):
                continue

            # skip files not in the student folder
            if not re.search(str(self.dir.as_posix()), str(file.as_posix()), flags=re.IGNORECASE):
                continue

            # skip files that are actually a notebook but disguised themselves as python files
            with open(file) as f:
                if f.read()[0] == "{":
                    continue

            self.student_number_to_file[re.search(self.student_n_regex, str(file), flags=re.IGNORECASE).group('digits')] = file
            self.start_process(file)

            # delay the start of the next process
            self.control_number_of_current_processes()

    def control_number_of_current_processes(self):
        # Manage the amount of processes
        open_processes = sum(1 for p in self.processes if p.is_alive())
        if open_processes > self.config["max_concurrent_process"]:
            time.sleep(0.05)  # Give the process some time to finish.
            for p in self.processes[:-self.config["max_concurrent_process"]]:  # Only terminate old processes
                self.terminate_process_after_n_seconds(p)

    def close_all(self):
        # close all processes, thus unittests
        while len(self.processes):
            # check if tests for a student is done
            self.terminate_process_after_n_seconds(self.processes[0])

    def start_process(self, file):
        for file_num in range(self.test_config["n_files"]):
            # Start a new process for each students such that the unittest file can import a different student "module/script".
            p = UnittestProcess(name=str(file),
                                target=subprocess_controller.run_student_code,
                                kwargs={"dir_": self.dir,
                                        "file": file,
                                        "suite": self.test_config["files"][file_num]["name"],
                                        "n_unittests": self.test_config["files"][file_num]["n_tests"],
                                        "max_unittest_code_lines_4_report": self.config.get("max_unittest_code_lines_4_report", 0),
                                        "print_variables": self.config.get("print_variables", True)},
                                config=self.config,
                                suite_config=self.test_config["files"][file_num])
            self.processes.append(p)
            self.student_files_name_suite.append((p.name, p.suite, p.n_unittests))
            p.start()
            if not self.config["run_parallel"]:
                self.terminate_process_after_n_seconds(p)

    def terminate_process_after_n_seconds(self, p):
        # check if tests for a student is done
        if p.is_alive():
            # Give the test MAX_RUNTIME seconds to finish running
            p.join(p.suite_config["max_runtime"])

            # force the tests to stop running, if still running
            if p.is_alive():
                print(f"TERMINATE PROCESS {p}")  # Can be helpful to see which student codes have a timeout error
                p.terminate()
                p.join()  # make sure the process is terminate this can take a while but terminate itself is not blocking

        # release resources and remove from self.processes
        p.close()
        self.processes.remove(p)

class BrightspaceHandler():
    """
    This class handles the brightspace grade file.
    """
    def __init__(self, dir_, config):
        """
        Read student numbers from file to dict and set grades to zero
        """
        self.dir = dir_
        self.config = config
        self.grades = utils.StudentDict(self.config["student_n_format"])

        self.init_grade_configs()
        self.load()

    def init_grade_configs(self):
        """Loads test config yaml file."""
        # Get relative path of assignment config folder
        config_folder = self.dir / "config"
        crt_folder = Path.cwd()
        config_folder = config_folder.relative_to(crt_folder)

        # Read and store assignment config
        with open(config_folder / "grade_config.yaml") as config_file:
            self.grade_config = safe_load(config_file)
            if "deadline" in self.grade_config:
                self.grade_config["deadline"] = pd.to_datetime(self.grade_config["deadline"], format="%d-%m-%Y %H:%M")

    def get_student_number(self, row):
        """
        Retrieve the student number from the brightspace grades csv file.
        The regex works as follows:
         - each student number should start with a "s"
         - Followed by the STUDENT_N_FORMAT which is group 0 (the student number)
         - after the student number we expect a BRIGHTSPACE_DELIMITER
        """
        try:
            return re.search(f"(?<=s){self.config['student_n_format']}(?={self.grade_config['brightspace_delimiter']})", row, flags=re.IGNORECASE).group(0)
        except AttributeError:
            print(f"The following row did not contain a student number: {row}!")
        return ""

    def get_student_grade(self, row):
        """
        Retrieve the student grade from the brightspace grades csv file.
        The regex works as follows:
         - each student number should start with a "s" + STUDENT_N_FORMAT + delimiter: (?<=s{self.config['student_n_format']}{self.grade_config['brightspace_delimiter']})
         - Followed a grade which is group 0: \d+
         - after the grade we expect again a delimiter: (?={self.grade_config['brightspace_delimiter']})
        """
        try:
            return re.search(f"(?<=s{self.config['student_n_format']}{self.grade_config['brightspace_delimiter']})\d+(\.\d+)?(?={self.grade_config['brightspace_delimiter']})", row, flags=re.IGNORECASE).group(0)
        except AttributeError:
            print(f"The following row did not contain a grade: {row}!")
        return 0

    def load(self):
        """
        Load the brightspace file and set grades to zero
        """
        with open(self.dir / self.grade_config["brightspace_grade_file"], "r") as grade_file:
            for row in grade_file.read().split("\n")[1:]:
                self.grades[self.get_student_number(row)] = 0 if self.grade_config["reset_grade"] else self.get_student_grade(row)

    def set_submitted_student_grades_to_zero(self, process_manager):
        """
        Set all grades from students that handed in a file to zero.
        """
        for student_number in process_manager.student_number_to_file:
            if self.grades[student_number] is not None:
                self.grades[student_number] = 0

    def update_successful_unittests(self, process_manager):
        """
        Update the grade file with the number of unittest passed per student over multiple unittest suites
        """
        for file, suite, n_tests in process_manager.student_files_name_suite:
            # Make the file path to store the results, which should already exists
            path = utils.get_txt_path(file, suite)

            # update grade, if the file does not exist. There is an error in handling feedback files often due to a syntax error in the student file.
            with open(path, "r") as log_file:
                file = log_file.read()
                grade = int(re.search("(?<=Unittests passed )\d+(?=/\d+)" , file).group(0))  # If this crashes there is a mistake in the logic, each file should have this text line.

            student_number = re.search(process_manager.student_n_regex, str(path), flags=re.IGNORECASE).group('digits')
            if self.grades[student_number] is not None:
                # extra test do not count for ITP grades
                if self.grade_config["grading_scheme"] == "ITP" and "extra" in suite:
                    continue
                self.grades[student_number] += grade

    def calculate_grades(self, process_manager):
        """
        Calculate the final grade of each student
        """
        # Calculate total number of unittest if needed
        if self.grade_config["grading_scheme"] in ["pass/fail", "ML"]:
            total = sum(test["n_tests"] for _, test in process_manager.test_config["files"].items())
        elif self.grade_config["grading_scheme"] == "ITP":
            total = sum(test["n_tests"] for _, test in process_manager.test_config["files"].items() if "extra" not in test["name"])

        # Calculate new grade for students that handed in something
        for student_number in process_manager.student_number_to_file:
            if self.grades[student_number] is None:
                continue

            if self.grade_config["grading_scheme"] == "sum":
                pass
            elif self.grade_config["grading_scheme"] == "ML":
                path = process_manager.student_number_to_file[student_number].as_posix()
                hand_in_timestamp = pd.to_datetime(re.search(r"\b\d{1,2} \w+ \d{4} \d{4}\b", path).group(0), format="%d %B %Y %H%M")
                greece_period_days = min(0, (self.grade_config["deadline"] - hand_in_timestamp).floor("d").days)  # 0 is before the deadline
                self.grades[student_number] = max(1, round(self.grades[student_number] / total * 9 + 1 + greece_period_days, 2))  # TODO: Adjust for late submission
            elif self.grade_config["grading_scheme"] in ["pass/fail", "ITP"]:
                self.grades[student_number] //= total
            else:
                raise ValueError("You typed an invalid grading scheme in the 'grade_config.yaml'.")

    def save_grades(self):
        """
        Save grades to the brightspace file by replacing grades
        """
        # read file and create the updated csv string
        with open(self.dir / self.grade_config["brightspace_grade_file"], "r") as grade_file:
            lines = grade_file.read().split("\n")
            new_file = [lines[0]]
            for row in lines[1:]:
                new_grade = self.grades[self.get_student_number(row)]
                if new_grade is None:  # empty line or not a student line in the csv
                    continue

                new_grade = str(new_grade)
                # This regex substitutes the old grade with the new grade (this should be the second column after the student number)
                row = re.sub(f"(?<=s{self.config['student_n_format']}{self.grade_config['brightspace_delimiter']})\d*(\.\d+)?(?={self.grade_config['brightspace_delimiter']})", new_grade, row, flags=re.IGNORECASE)
                new_file.append(row)

        # overwrite the old csv with the new csv string
        with open(self.dir / self.grade_config["brightspace_grade_file"], "w") as grade_file:
            grade_file.write("\n".join(new_file))

    def __repr__(self):
        return repr(self.grades)

def main():
    """
    The main flow of the autograder script.
    """
    global_config_path = next(Path(os.getcwd()).rglob("global_config.yaml"))
    global_config_path = global_config_path.resolve()
    with open(global_config_path) as config_file:
        config = safe_load(config_file)

    # Test if at least one folder matches the student_folder regex
    try:
        Path(os.getcwd()).glob(config["student_folder"]).__next__()
    except StopIteration:
        raise ValueError(f'{config["student_folder"]}, this directory/sub-path can not be found in the assignment folder!')

    # Search for exercise folder (in parent directory) giving in global config
    for dir_ in Path(os.getcwd()).glob(config["student_folder"]):
        # check if it is a folder
        if not dir_.is_dir():
            continue

        dir_ = dir_.resolve()
        # check if it is a folder that contains a test_config.yaml
        try:
            process_manager = ProcessManager(dir_, config)
        except (NotADirectoryError, FileNotFoundError):
            continue

        # Check if grades need to be calculated
        if config["grades"]:
            try:
                brightspace_grades = BrightspaceHandler(dir_, config)
            except (NotADirectoryError, FileNotFoundError):
                raise FileNotFoundError("The global config is set to track grades, but no grade_config.yaml was found!")

        process_manager.start()
        process_manager.close_all()

        if config["grades"]:
            brightspace_grades.set_submitted_student_grades_to_zero(process_manager)
            brightspace_grades.update_successful_unittests(process_manager)
            brightspace_grades.calculate_grades(process_manager)
            brightspace_grades.save_grades()

if __name__ == "__main__":
    main()
