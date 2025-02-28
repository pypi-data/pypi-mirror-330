from multiprocessing import Process
import inspect
import importlib
import re

from . import utils

class UnittestProcess(Process):
    """
    A subclass of multiprocessing to make sure that each unittest report start with the number of test passed.
    """
    def __init__(self, config, suite_config, *args, **kwargs):
        super(UnittestProcess, self).__init__(*args, **kwargs)
        self.config = config
        self.suite_config = suite_config
        self.update_file = False  # signal if the file is update with the number of passed tests
        self.daemon = True
        self.n_unittests = kwargs['kwargs']['n_unittests']
        self.suite = kwargs['kwargs']['suite']

    def terminate(self):
        """
        Terminate process; sends SIGTERM signal or uses TerminateProcess()

        Extend by making update_unittest_report blocking
        """
        self._check_closed()
        if not self.update_file:  # Do not terminate if the function called by run is already done
            self._popen.terminate()  # terminate the process

            # Check if the file is "new", aka does not already contain unnittest passed. Could happen if tests are rerun.
            path = utils.get_txt_path(self.name, self.suite)
            if path.exists():
                with open(path, "r") as log_file:
                    if "Unittests passed" in log_file.readline():
                        self.update_file = True
                        return

            # update report with timeout error and number of passed tests
            self.update_unittest_report()
            self.add_timeout_error_to_report()
            self.update_file = True

    def run(self):
        """
        This method is run in the new process
        """
        if self._target:
            # run the tests
            self._target(*self._args, **self._kwargs)

            # update the reports
            self.update_file = True
            self.update_unittest_report()

    def update_unittest_report(self):
        """
        Update the unittest report.txt by adding the number of passed tests.
        The number of correct (ok) tests is read from the file.
        return the number of correct tests.
        """
        path = utils.get_txt_path(self.name, self.suite)

        # Check if a report exist otherwise create one (this happens if no unittest run because of e.g. import error)
        if not path.exists():
            with open(path, "w") as log_file:
                log_file.write(f"Unittests passed 0/{self.n_unittests}\n\n")
                log_file.write("----------------------------------------------------------------------\n\n")
                log_file.write("Your file contains syntax error and could not be tested!\n\n")
            return

        # Count total good tests
        with open(path, "r") as log_file:
            file = log_file.read()
            correct = len(list(re.finditer(r"\) ... ok", file, re.IGNORECASE)))

        # Log the total good tests
        with open(path, "w") as log_file:
            log_file.write(f"Unittests passed {correct}/{self.n_unittests}\n\n")
            log_file.write("----------------------------------------------------------------------\n\n")
            log_file.write(file)

    def add_timeout_error_to_report(self):
        """
        This method makes sure that the report is complete in a case of a timeout.
        A timeout can occur when the student code takes longer then "x" seconds to run,
        which can be caused by for example suboptimal code or infinite loops.

        The report is complete with a message stating that the code took to long to run and
        show the unittest code that was running when this process got terminated.
        """
        path = utils.get_txt_path(self.name, self.suite)
        with open(path, "r+") as log_file:
            # find source code
            last_line = log_file.read().split("\n")[-1]
            if last_line[:4] == "test":  # This is specific to the unittest module
                unittest_object = last_line.split(" ")[1][1:-1]
                # find which test went wrong (module, class, method)
                *unittest_module_name, unittest_class_name, unittest_method_name = unittest_object.split(".")
                # import the unittest
                unittest_module_name = ".".join(unittest_module_name)
                unittest_name = importlib.import_module(unittest_module_name)
                # get the method object from unittest
                unittest_method = getattr(getattr(unittest_name, unittest_class_name), unittest_method_name)
                # get the source code of the unittest that was last run before the timeout error occurred
                source_code = "\n".join(inspect.getsource(unittest_method).split("\n")[1:self.config["timeout_error_lines"]])
                log_file.write(f"ERROR\nUnittest code that exceeded the maximum runtime:\n{source_code}")
            else:  # Should only happen if there is a script in the student code (no test are running)
                log_file.write("\n")
            log_file.write(f'...\n\nThe rest of the unittests are terminated due to exceeding the maximum runtime of {self.suite_config["max_runtime"]} seconds.')
