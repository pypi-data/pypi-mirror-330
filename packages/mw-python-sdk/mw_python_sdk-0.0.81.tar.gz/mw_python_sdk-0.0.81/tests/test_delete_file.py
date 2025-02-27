import unittest
import os
import json
from dataclasses import asdict
from mw_python_sdk import download_file, get_dataset, delete_file
import logging

logging.basicConfig(level=logging.DEBUG)
class TestDeleteFile(unittest.TestCase):
    def test_download(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:  # Example assertion
            dataset = get_dataset(dataset_id_tmp)
            print(dataset.files)
            delete_file(dataset_id_tmp, "a_folder/README.md")
            delete_file(dataset_id_tmp, "a_folder/config_4.json")
            delete_file(dataset_id_tmp, "a_folder/config_3.json")
            delete_file(dataset_id_tmp, "a.txt")
            delete_file(dataset_id_tmp, "b.txt")
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
