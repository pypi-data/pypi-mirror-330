import unittest
from mw_python_sdk import upload_folder  # , upload_file


class TestUploadFolder(unittest.TestCase):
    def test_upload_folder(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:  # Example assertion
            upload_folder("downloads", "test_upload_folder/", dataset_id_tmp)
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
