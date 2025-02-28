import unittest
import numpy as np
import ast
import inspect

class ExtendTestCase(unittest.TestCase):
    def assertArrayEqual(self, in_, out):
        self.assertIsInstance(out, np.ndarray, f"Expected numpy array.")
        self.assertEqual(in_.shape, out.shape, f"Expected {in_.shape} got {out.shape}.")
        equal = np.isclose(in_, out)
        self.assertTrue(equal.all(), f"Expected {in_} got {out}.")

    def _get_call_name(self, c):
        if isinstance(c.func, ast.Attribute):
            return c.func.attr
        elif isinstance(c.func, ast.Name):
            return c.func.id
        return self._get_call_name(c.func)

    def _call_names(self, source):
        return [self._get_call_name(c)
                for c in ast.walk(ast.parse(inspect.getsource(source).lstrip()))
                if isinstance(c, ast.Call)]

    def call_test_in(self, source, target):
        call_names = self._call_names(source)
        self.assertIn(target.__name__, call_names, msg=f"{target.__qualname__} is not used in {source.__qualname__}!")

    def call_test_not_in(self, source, target):
        call_names = self._call_names(source)
        self.assertNotIn(target.__name__, call_names, msg=f"{target.__qualname__} is not allowed to be used in {source.__qualname__}!")

    def call_test_not_in_partial(self, source, target):
        call_names = self._call_names(source)
        for x in call_names:
            self.assertNotIn(target, x, msg=f"Any functions named *{target}* are not allowed to be used in {source.__qualname__}!")
