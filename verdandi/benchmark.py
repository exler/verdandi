class Benchmark:
    prefix_benchmark: str = "bench_"

    def setUp(self):
        """Hook method for setting up the test before running it"""
        pass

    def tearDown(self):
        """Hook method for deconstructing the test after running it"""
        pass

    @classmethod
    def setUpClass(cls):
        """Hook method for setting up class fixture before running tests in the class."""
        pass

    @classmethod
    def tearDownClass(cls):
        """Hook method for deconstructing the class fixture after running all tests in the class."""
        pass

    def discover(self) -> None:
        """
        Get all functions that begin with `prefix_benchmark`
        """
        pass

    def run(self) -> None:
        pass
