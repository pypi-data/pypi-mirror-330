import unittest
from unittest.mock import patch
from Model_utils import HFModelSearcher

class TestHFModelSearcher(unittest.TestCase):
    def setUp(self):
        self.searcher = HFModelSearcher()
        
        # Mock the ordered_dicts_mapping for all tests
        self.searcher.ordered_dicts_mapping = {
            "MODEL_FOR_CAUSAL_LM_MAPPING_NAMES": {
                "gpt2": "GPT2Config",
                "bert": "BertConfig"
            },
            "MODEL_FOR_IMAGE_CLASSIFICATION_MAPPING_NAMES": {
                "vit": "ViTConfig"
            }
        }

    def test_extract_model_family(self):
        test_cases = [
            ("bert-base-uncased", "bert"),
            ("facebook/bart-large", "bart"),
            ("t5-small", "t5"),
            ("wav2vec2-base", "wav2vec2"),
        ]
        for model_path, expected in test_cases:
            with self.subTest(model_path=model_path):
                result = self.searcher.extract_model_family(model_path)
                self.assertEqual(result, expected)

    def test_search_with_config(self):
        result = self.searcher.search(config="GPT2Config")
        self.assertEqual(result, ("MODEL_FOR_CAUSAL_LM_MAPPING_NAMES", "gpt2"))

    def test_search_with_invalid_config(self):
        result = self.searcher.search(config="InvalidConfig")
        self.assertIsNone(result)

    def test_exact_match_search(self):
        results = self.searcher.search("bert")
        self.assertEqual(results, [["MODEL_FOR_CAUSAL_LM_MAPPING_NAMES", "BertConfig"]])

    def test_fuzzy_match_search(self):
        results = self.searcher.search("beer")  # Fuzzy match for "bert"
        self.assertIsNotNone(results)
        self.assertEqual(results[0][0], "MODEL_FOR_CAUSAL_LM_MAPPING_NAMES")
        self.assertEqual(results[0][1], "BertConfig")

if __name__ == '__main__':
    unittest.main()