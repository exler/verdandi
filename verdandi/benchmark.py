import inspect
from typing import Callable, List


class Benchmark:
    def setUp(self):
        """Hook method for setting up the bench before running it"""
        pass

    def tearDown(self):
        """Hook method for deconstructing the bench after running it"""
        pass

    def setUpIter(self):
        """Hook method for setting up the bench iteration before running it"""
        pass

    def tearDownIter(self):
        """Hook method for deconstructing the bench iteration after running it"""
        pass

    @classmethod
    def setUpClass(cls):
        """Hook method for setting up class before running all benches in the class"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Hook method for deconstructing the class after running all benches in the class"""
        pass

    def collect_bench_methods(self, method_prefix: str = "bench_") -> List[Callable[..., None]]:
        bench_methods: List[Benchmark] = []

        for name, attr in inspect.getmembers(self):
            if name.startswith(method_prefix):
                bench_methods.append(attr)

        return bench_methods
