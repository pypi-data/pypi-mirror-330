import importlib
import unittest
import traceback
import sys
from . import unittest_formatter
from . import utils
from pathlib import Path

def run_student_code(dir_, file, suite, max_unittest_code_lines_4_report, print_variables, *args, **kwargs):
    # Append local path for student file imports
    sys.path.append(str(Path(file).parents[0]))

    # Create the relative student module import path
    student_module_path = utils.find_relative_import(file)

    # Create the relative unit_test module import path
    unittest_module_path = utils.find_relative_import(next(dir_.rglob(f"unit_test_{suite}.py")))

    # Run the tests
    run_tests(file, student_module_path, unittest_module_path, utils.get_txt_path(file, suite), max_unittest_code_lines_4_report, print_variables)

def run_tests(file, student_module, unittest_module, report_path, max_unittest_code_lines_4_report, print_variables):
    # Check if the file can be imported if not catch the error and write to file
    try:
        student = importlib.import_module(student_module)
    except:
        # Create an error report for the student that gives feedback where the import crashed.
        with open(report_path, "w") as log_file:
            log_file.write(f"The student file could not be imported due to the following error:\n{traceback.format_exc(-1)}\n\n")
            log_file.write(f"\nThe student file that is tested is: {student_module.rsplit('.', 1)[1]}")
        return

    unit_test = importlib.import_module(unittest_module)
    unit_test.student = student  # dynamically import the student code in the unit_test module

    # Run the tests
    with open(report_path, "w") as log_file:
        for tests in [obj for obj in dir(unit_test) if obj[:4] == "Test"]:
            suite = unittest.TestLoader().loadTestsFromTestCase(vars(unit_test)[tests])
            unittest_formatter.MyTextTestRunner(stream=log_file,
                                                verbosity=2,
                                                resultclass=unittest_formatter.MyTextTestResult,
                                                max_unittest_code_lines_4_report=max_unittest_code_lines_4_report,
                                                print_variables=print_variables,
                                                tb_locals=True).run(suite)
        log_file.write(f"\nThe student file that is tested is: {student.__name__}")
