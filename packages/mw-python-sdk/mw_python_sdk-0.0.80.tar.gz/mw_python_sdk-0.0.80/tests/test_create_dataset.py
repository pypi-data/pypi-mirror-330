import unittest
from mw_python_sdk import (
    create_dataset,
    delete_dataset,
    upload_file,
    DatasetConstructor,
)
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class TestCreateDataset(unittest.TestCase):
    def test_dataset_create(self):
        try:
            dataset = create_dataset(
                "llama3chinese", "downloads", "", "llama3 are cool"
            )
            print(dataset.title)
            assert dataset.title == "llama3chinese"
            upload_file("README.md", "test/README.md", dataset)
            delete_dataset(dataset)
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_dataset_constructor(self):
        try:
            dsctr = DatasetConstructor(
                title="llama3chinese", short_description="llama3 are cool"
            )
            dsctr.add_dir("downloads", "")
            dsctr.add_file("README.md", "test/README.md")
            dataset = dsctr.push_dataset()
            print(dataset)
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
