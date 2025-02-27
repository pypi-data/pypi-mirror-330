import unittest
from mw_python_sdk import create_commit


class TestCreateCommit(unittest.TestCase):
    def test_create_commit(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:  # Example assertion
            commit = create_commit(dataset_id_tmp, "This is a test commit message")
            print(commit)
        except Exception as err:
            print(f"An error occurred: {err}")

if __name__ == "__main__":
    unittest.main()
