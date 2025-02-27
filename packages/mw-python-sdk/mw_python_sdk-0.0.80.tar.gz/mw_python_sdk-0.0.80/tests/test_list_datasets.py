import unittest
from mw_python_sdk import list_datasets,list_all_datasets
import logging


# Configure logging

logging.basicConfig(level=logging.DEBUG)


class TestListDatasets(unittest.TestCase):
    def test_dataset_create(self):
        try:
            dataset_iter = list_datasets("llama3chinese")
            for dataset in dataset_iter:
                print(dataset)
            datasets = list_all_datasets("llama3chinese")
            print(datasets)
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
