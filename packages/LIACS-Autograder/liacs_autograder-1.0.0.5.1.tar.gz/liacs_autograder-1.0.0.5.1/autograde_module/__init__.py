# this helps to access the content of the module from a module level
# for example, autograde_module.autograder.main()
from . import autograder, utils, unittest_extensions

# This imports autograder into the top level module namespace which makes this possible autograde_module.main()
from .autograder import main
from .unittest_extensions import ExtendTestCase

