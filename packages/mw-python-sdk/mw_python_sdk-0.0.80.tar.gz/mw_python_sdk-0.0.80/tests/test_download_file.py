import unittest
import os
from mw_python_sdk import download_file

import logging
# Set the logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
class TestDownloadFile(unittest.TestCase):
    def test_download_specific_version(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:  # Example assertion
            download_file(
                dataset_id_tmp,
                "b_local_dir/heart_2020_cleaned.csv",
                commit="66b472ea7a15d14beb825911",
            )
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_download(self):
        dataset_id_tmp = "64254cbfb9d501d04418c291"
        try:  # Example assertion
            path = download_file(dataset_id_tmp, "README.md")
            print(path)
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_download_again(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:  # Example assertion
            download_file(dataset_id_tmp, "flask.zip")
            download_file(dataset_id_tmp, "flask.zip")
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_download_local(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:  # Example assertion
            download_file(
                dataset_id_tmp, "flask.zip", local_dir=os.getcwd() + ("/downloads")
            )
            download_file(
                dataset_id_tmp, "flask.zip", local_dir=os.getcwd() + ("/downloads")
            )
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
