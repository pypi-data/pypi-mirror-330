import unittest
from unittest.mock import patch
from Model_utils import  HFProcessorSearcher

class TestHFProcessorSearcher(unittest.TestCase):

    def test_extract_processor_family(self):
        test_cases = [
            ("bert-base-uncased", "bert"),
            ("facebook/wav2vec2-base-960h", "wav2vec2"),
            ("google/vit-base-patch16-224", "vit"),
            ("openai/clip-vit-base-patch32", "clip"),
        ]
        searcher = HFProcessorSearcher()
        for model_path, expected in test_cases:
            with self.subTest(model_path=model_path):
                self.assertEqual(searcher.extract_model_family(model_path), expected)



if __name__ == '__main__':
    unittest.main()
