import unittest
from mw_python_sdk import upload_file  # , upload_file


class TestUploadFile(unittest.TestCase):
    def test_upload_file(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:  # Example assertion
            upload_file("README.md", "config_3.json", dataset_id_tmp)
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_reupload_file(self):
        dataset_id_tmp = "66b08ec9898e74a8232bb2d1"
        try:  # Example assertion
            upload_file("README.md", "a_folder/README.md", dataset_id_tmp, overwrite=True)
            upload_file("README.md", "a_folder/config_4.json", dataset_id_tmp)
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
