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

    def run(self) -> None:
        pass
