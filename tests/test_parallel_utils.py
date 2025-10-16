import unittest
from utils_library.parallel_utils import run_parallel_list, run_parallel_stream


def square(x):
    return x * x

def add(x, y):
    return x + y


class TestParallelUtils(unittest.TestCase):

    def test_run_parallel_list_single_arg(self):
        data = [1, 2, 3, 4]
        res = run_parallel_list(square, data, workers=2, backend="thread")
        self.assertEqual(res, [1, 4, 9, 16])

    def test_run_parallel_list_multi_arg(self):
        data = [(1, 2), (3, 4), (5, 6)]
        res = run_parallel_list(add, data, workers=2, backend="process")
        self.assertEqual(res, [3, 7, 11])

    def test_run_parallel_stream_single_arg(self):
        data = (i for i in range(5))
        res = list(run_parallel_stream(square, data, workers=2))
        self.assertEqual(sorted(res), [0, 1, 4, 9, 16])

    def test_run_parallel_stream_multi_arg(self):
        data = ((i, i+1) for i in range(3))
        res = list(run_parallel_stream(add, data, workers=2))
        self.assertEqual(sorted(res), [1, 3, 5])


if __name__ == "__main__":
    unittest.main()
