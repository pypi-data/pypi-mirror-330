import unittest
from mw_python_sdk import download_dir


class TestDownloadFile(unittest.TestCase):
    def test_download(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:
            download_dir("638456025305bf4b57c4a244", local_dir="downloads")
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_redownload(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:
            print(download_dir(dataset_id_tmp))
            print(download_dir(dataset_id_tmp))
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_download_local_dir(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:
            print(download_dir(dataset_id_tmp, local_dir="downloads"))
            print(download_dir(dataset_id_tmp, local_dir="downloads"))
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
