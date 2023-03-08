import unittest
from Disk_analyser import Disk_analyser
from pathlib import Path
import datetime
class TestSum(unittest.TestCase):
    def setUp(self):
        pass

    def test_is_right_extensions(self):
        analyser=Disk_analyser(Path("test_files"), 10**10, [".txt"], False, None, False, None)
        self.assertEqual(2,len(analyser.files))
        expected_result=["test_files\\test.txt","test_files\\test1\\test.txt"]
        self.assertTrue(str(analyser.files[0].path) in expected_result)

    def test_is_right_maxdeep(self):
        analyser=Disk_analyser(Path("test_files"), 1, None, False, None, False, None)
        self.assertEqual(2,len(analyser.files))
        expected_result = ["test_files\\test.txt", "test_files\\test.py"]
        self.assertTrue(str(analyser.files[0].path) in expected_result)
        self.assertTrue(str(analyser.files[1].path) in expected_result)
    def test_is_right_time(self):
        date=datetime.datetime.strptime('17.11.2022', '%d.%m.%Y').date()
        analyser=Disk_analyser(Path("test_files"), 10**10, None, False,[date], False, None)
        self.assertEqual(3,len(analyser.files))
        expected_result = ["test_files\\test.txt", "test_files\\test.py","test_files\\test1\\test.txt"]
        self.assertTrue(str(analyser.files[0].path) in expected_result)
        self.assertTrue(str(analyser.files[1].path) in expected_result)
        self.assertTrue(str(analyser.files[2].path) in expected_result)
    def test_is_right_time_maxdeep_time(self):
        date = datetime.datetime.strptime('17.11.2022', '%d.%m.%Y').date()
        analyser = Disk_analyser(Path("test_files"),1, [".txt"], False, [date], False, None)
        self.assertEqual(1, len(analyser.files))
        self.assertEqual("test_files\\test.txt",str(analyser.files[0].path))
