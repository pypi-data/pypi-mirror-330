import unittest
import logging
# Configure logging

logging.basicConfig(level=logging.DEBUG)


class TestRAGSearch(unittest.TestCase):
    def test_rag_search(self):
        try:
            from mw_python_sdk import rag_search
            results = rag_search("67be81cc230239527e919ef8", "llama", 0.3, 2)
            self.assertIsNotNone(results)
            print(results)
        except Exception as err:
            print(f"An error occurred: {err}")
            
if __name__ == "__main__":
    unittest.main()
