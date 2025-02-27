import unittest
from mw_python_sdk import get_dataset


class TestGetDataset(unittest.TestCase):
    def test_dataset_create(self):
        try:
            dataset = get_dataset("66b08ec9898e74a8232bb2d1")
            print(dataset.files)
            print(dataset.commits)
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
