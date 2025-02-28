# autograding
Autograder and custommagics for python

# How to run
```
conda create -n autograding_env
conda init
conda activate autograding_env

pip install -r requirements.txt

python main.py
```

# How to make unittest

Example:

```python
from autograde_module import ExtendTestCase  # Adds extra tests

"""
Student code can be accessed using the module student which is dynamically import by the autograder.
Do not add the code "import student"
"""

class Test1Basics(ExtendTestCase):
    def test_add(self):
        self.assertEqual(3+5, student.add(3, 5))
```

Make sure that in the assignment .yml file contains:
 - SUITES_AND_UNITTESTS
 - Where the first input is the name of the unittest without "unit_test_"
 - And the second input is the number of unittests
 - The name of the unittest must be unique within each assignments.