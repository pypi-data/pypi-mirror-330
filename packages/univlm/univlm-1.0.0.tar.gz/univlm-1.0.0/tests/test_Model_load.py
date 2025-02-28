import unittest
from unittest.mock import patch, MagicMock
import torch
from Model import Yggdrasil, reference_table
from Model_utils import HFModelSearcher, HFProcessorSearcher

class TestYggdrasilInitialization(unittest.TestCase):
    def test_init_with_valid_parameters(self):
        y = Yggdrasil("nlptown/bert-base-multilingual-uncased-sentiment", 
                      Feature_extractor=False, 
                      Image_processor=False,
                      Config_Name='BertForSequenceClassification')
        self.assertEqual(y.model_name, "nlptown/bert-base-multilingual-uncased-sentiment")
        self.assertFalse(y.Feature_extractor)
        self.assertFalse(y.Image_processor)

class TestYggdrasilLoad(unittest.TestCase):
    @patch('Model_utils.HFModelSearcher')
    @patch('transformers.AutoModelForSequenceClassification.from_pretrained')
    def test_load_hf_success(self, mock_from_pretrained, mock_searcher):
        mock_searcher_instance = MagicMock()
        mock_searcher.return_value = mock_searcher_instance
        mock_searcher_instance.search.return_value = [["MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES", "bert"]]
        
        y = Yggdrasil("nlptown/bert-base-multilingual-uncased-sentiment", 
                     False, False,
                     Config_Name='BertForSequenceClassification')
        result = y.load()
        
        self.assertEqual(result, "Loaded")
        self.assertEqual(y.model_type, "HF")
        mock_from_pretrained.assert_called_once_with("nlptown/bert-base-multilingual-uncased-sentiment")

class TestYggdrasilProcessor(unittest.TestCase):
    @patch('Model_utils.HFProcessorSearcher')
    def test_hf_processor_loading(self, mock_searcher):
        mock_processor = MagicMock()
        mock_searcher_instance = MagicMock()
        mock_searcher.return_value = mock_searcher_instance
        mock_searcher_instance.search.return_value = (MagicMock(), "nlptown/bert-base-multilingual-uncased-sentiment")
        
        y = Yggdrasil("nlptown/bert-base-multilingual-uncased-sentiment", False, False)
        y.model_type = "HF"
        result = y.Proccessor()
        
        self.assertEqual(result, "Processor Loaded")
        self.assertIsNotNone(y.Processor)

class TestYggdrasilInference(unittest.TestCase):
    def setUp(self):
        self.mock_hf_model = MagicMock()
        self.mock_hf_processor = MagicMock()

    # In test_Model_load.py - Fix sentiment inference test
    def test_sentiment_model_inference(self):
        y = Yggdrasil("nlptown/bert-base-multilingual-uncased-sentiment", 
                    False, False,
                    Config_Name='BertForSequenceClassification')
        y.model_type = "HF"
        
        # Create real tensor with comparison logic
        mock_logits = torch.tensor([[2.1, -0.5, 1.8, 0.3, -1.2]])  # 5-class sentiment
        mock_output = MagicMock()
        mock_output.logits = mock_logits
        y.model = MagicMock(return_value=mock_output)
        
        # Mock processor
        y.Processor = MagicMock()
        y.Processor.return_value = {
            "input_ids": torch.tensor([[101, 2023, 2003, 3782, 102]]),
            "attention_mask": torch.tensor([[1, 1, 1, 1, 1]])
        }
        
        result = y.inference({"text": "This is great!"})
        output = result[0]  
        logits = output.logits  

        self.assertEqual(logits.argmax().item(), 0)  # Verify highest score at index 0

class TestHelperMethods(unittest.TestCase):
    def test_processor_input_names(self):
        y = Yggdrasil("nlptown/bert-base-multilingual-uncased-sentiment", False, False)
        
        # Test tokenizer
        mock_tokenizer = MagicMock()
        mock_tokenizer.__class__.__name__ = "BertTokenizer"
        names = y._get_processor_input_names(mock_tokenizer)
        self.assertIsNone(names["image"])
        self.assertEqual(names["text"], "text")

    def test_standardize_payload(self):
        y = Yggdrasil("nlptown/bert-base-multilingual-uncased-sentiment", False, False)
        
        # Test text standardization
        payload = {"input_text": "This is awesome!"}
        standardized, _ = y._standardize_payload(payload)
        self.assertEqual(standardized["text"], ["This is awesome!"])

class TestHFModelSearcher(unittest.TestCase):
    def setUp(self):
        self.searcher = HFModelSearcher()
        self.searcher.ordered_dicts_mapping = {
            "MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES": {
                "bert": "BertConfig"
            }
        }

    def test_extract_model_family(self):
        test_cases = [
            ("nlptown/bert-base-multilingual-uncased-sentiment", "bert"),
            ("bert-base-uncased", "bert"),
            ("bert-large-uncased", "bert")
        ]
        for model_path, expected in test_cases:
            with self.subTest(model_path=model_path):
                result = self.searcher.extract_model_family(model_path)
                self.assertEqual(result, expected)

    def test_search_with_config(self):
        result = self.searcher.search(query=None, config="BertConfig")
        self.assertEqual(result, ("MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES", "bert"))

    def test_search_with_invalid_config(self):
        result = self.searcher.search(query=None, config="InvalidConfig")
        self.assertIsNone(result)

    def test_exact_match_search(self):
        results = self.searcher.search("bert")
        self.assertEqual(results, [["MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES", "BertConfig"]])

    def test_fuzzy_match_search(self):
        results = self.searcher.search("beer")  # Fuzzy match for "bert"
        self.assertIsNotNone(results)
        self.assertEqual(results[0][0], "MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING_NAMES")
        self.assertEqual(results[0][1], "BertConfig")

if __name__ == '__main__':
    unittest.main()