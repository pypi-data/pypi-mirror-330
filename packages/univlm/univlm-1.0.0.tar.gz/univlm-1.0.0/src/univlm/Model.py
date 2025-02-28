from .Model_utils import HFModelSearcher,HFProcessorSearcher, reference_table 
from transformers import AutoModelForCausalLM, AutoModelForVision2Seq, AutoModelForSeq2SeqLM, AutoModelForMaskedLM
from vllm import LLM, SamplingParams 
import torch

class unify:
    def __init__(self, model_name, Feature_extractor=False, Image_processor=False, Config_Name = None):
        self.model = None
        self.model_type = None  
        self.Processor = None  
        self.model_name = model_name
        self.Feature_extractor = Feature_extractor
        self.Image_processor =  Image_processor
        self.Config_Name = Config_Name 
        self.map = None

    def load(self):
        """Determine model type loads it."""

        try: 
            self.model = LLM(model=self.model_name,
                             gpu_memory_utilization=0.9,
                             max_model_len=2048,trust_remote_code=True)
            self.model_type = "VLLM"
            print("VLLM model Loaded")
            return "Loaded"  
        except Exception as e:
            print(f"Not supported on VLLM: {e}")

        # Try loading as an HF model
        try:
            placeholder = HFModelSearcher()
            results = placeholder.search(self.model_name,self.Config_Name)

            if not results:
                raise ValueError("No HF model found.")
            if self.Config_Name is not None:
                print(0)
                placeholder2 = results[0]
                print(placeholder2)
                print(1)
                self.model = reference_table[placeholder2]
            else:
                if len(results) > 1:
                    print("Multiple use cases found for the same backbone model")
                    print(results)
                    index = int(input("Write the index of the model you want to use: ")) 
                    placeholder2 = results[index][0]  # Assuming it's a tuple/list
                    print(reference_table[placeholder2])
                    self.model = reference_table[placeholder2]
                    
                else:
                    placeholder2 = results[0][0]
                    self.model = reference_table[placeholder2]
                
            self.map = self.model
            self.model = self.model.from_pretrained(self.model_name)
            self.model_type = "HF"
            print("HF model Loaded")
            return "Loaded"  
        except Exception as e:
            print(f"Not supported on HF: {e}")

        # Try loading as an exclusive model
        try:
            model_class = reference_table[self.model_name]
            self.model = model_class()
            self.model.env_setup()
            self.model.download_checkpoints()
            self.model.load_model()
            self.model_type = "Exclusive"
            print("Exclusive model Loaded")
            return "Loaded"  
        except Exception as e:
            print(f"Not supported by Athena as of this moment: {e}")

        return "Failed to Load"  # Return failure if all methods fail

    def Proccessor(self):
        """
        Determines the appropriate processor (Tokenizer or Processor) for the model
        Args:
            model_name: Name of the model to process
        Returns:
            str: Type of processor selected ('Processor' or 'Tokenizer')
        """

        if self.model_type == "VLLM":
            pass
        elif self.model_type == "HF":
            Placeholder = HFProcessorSearcher()
            self.Processor, temp = Placeholder.search(self.model_name,self.Feature_extractor,self.Image_processor)
            self.Processor = self.Processor.from_pretrained(self.model_name)
        elif self.model_type == "Exclusive":
            self.Processor = self.model.processor()
        else: 
            raise ValueError("Model not loaded")
        
        return "Processor Loaded"

    def _standardize_payload(self, payload):
        """
        Standardize input payload keys to work with both VLLM and HF.
        Handles both single inputs and batches.
        """
        standard_keys = {
            "prompt": ["prompt", "text", "input_text", "inputs"],
            "images": ["images", "image", "pixel_values", "pixel_vals", "visual_input"]
        }
        
        standardized = {}
        
        def find_matching_key(key_options):
            return next((k for k in key_options if k in payload), None)
        
        text_key = find_matching_key(standard_keys["prompt"])
        if text_key:
            text_input = payload[text_key]
            if not isinstance(text_input, list):
                text_input = [text_input]
            standardized["text"] = text_input

        image_key = find_matching_key(standard_keys["images"])
        if image_key:
            image_input = payload[image_key]
            if not isinstance(image_input, list):
                image_input = [image_input]
            standardized["pixel_values"] = image_input

        # Determine if it's a batch operation
        is_batch = any(isinstance(v, list) and len(v) > 1 for v in standardized.values())
        
        return standardized, is_batch

    def _get_processor_input_names(self, processor):
        """
        Determine the correct input parameter names for different processor types
        """
        # Check processor type and return appropriate parameter names
        processor_class = processor.__class__.__name__.lower()
        
        if 'processor' in processor_class:
            # Multi-modal processors typically use these names
            return {
                "text": "text",
                "image": "images"
            }
        elif 'tokenizer' in processor_class:
            # Tokenizers only handle text
            return {
                "text": "text",
                "image": None
            }
        elif 'imageprocessor' in processor_class or 'featureextractor' in processor_class:
            # Image processors only handle images
            return {
                "text": None,
                "image": "pixel_values"
            }
        else:
            # Default fallback
            return {
                "text": "text",
                "image": "pixel_values"
            }

    def inference(self, payload):
        """
        Perform inference on single or batch inputs
        """
        if self.model_type != "Exclusive":
            # Standardize input format
            standardized_payload, is_batch = self._standardize_payload(payload)
            if not standardized_payload:
                raise ValueError("No valid input keys found in payload")

            if self.model_type == "VLLM":
                if "text" not in standardized_payload:
                    raise ValueError("VLLM requires text input")
                
                # Get prompts and ensure they're in list format
                prompts = standardized_payload["text"]
                if not isinstance(prompts, list):
                    prompts = [prompts]
                    
                # Configure sampling parameters
                sampling_params = SamplingParams(
                    temperature=0.8,
                    max_tokens=128,
                    stop=["</s>", "[/INST]", "Assistant:", "Human:"]
                )
                
                try:
                    # Generate outputs using VLLM's batch API
                    outputs = self.model.generate(prompts, sampling_params)
                    
                    # Process outputs maintaining batch order
                    responses = []
                    for output in outputs:
                        # Extract the generated text, removing any leading/trailing whitespace
                        generated_text = output.outputs[0].text.strip()
                        responses.append(generated_text)
                        
                    return responses if is_batch else responses[0]
                    
                except Exception as e:
                    print(f"VLLM generation error: {e}")
                    raise
            elif self.model_type == "HF":
                try:
                    self.Proccessor()
                except:
                    raise ValueError("Processor not loaded")

                processor = self.Processor
                input_names = self._get_processor_input_names(processor)
                batch_size = len(next(iter(standardized_payload.values())))
                
                # Process each input separately first to get their sizes
                processed_inputs = []
                max_length = 0
                for i in range(batch_size):
                    current_input = {}
                    
                    if "text" in standardized_payload and input_names["text"]:
                        current_input[input_names["text"]] = standardized_payload["text"][i]
                    
                    if "pixel_values" in standardized_payload and input_names["image"]:
                        current_input[input_names["image"]] = standardized_payload["pixel_values"][i]
                    
                    # Process the input
                    processed = processor(**current_input, return_tensors="pt")
                    processed_inputs.append(processed)
                    
                    # Track maximum sequence length for text inputs
                    if 'input_ids' in processed:
                        max_length = max(max_length, processed['input_ids'].shape[1])

                # Pad all inputs to the same length
                padded_inputs = []
                for processed in processed_inputs:
                    padded = {}
                    for key, value in processed.items():
                        if key == 'input_ids' or key == 'attention_mask':
                            # Pad text inputs
                            current_length = value.shape[1]
                            if current_length < max_length:
                                padding = torch.zeros(value.shape[0], max_length - current_length, 
                                                dtype=value.dtype, device=value.device)
                                if key == 'input_ids':
                                    padding = padding.fill_(processor.pad_token_id if hasattr(processor, 'pad_token_id') else 0)
                                padded[key] = torch.cat([value, padding], dim=1)
                            else:
                                padded[key] = value
                        else:
                            # Copy other inputs as is
                            padded[key] = value
                    padded_inputs.append(padded)

                # Combine into batch
                batched_inputs = {
                    k: torch.cat([inp[k] for inp in padded_inputs]) 
                    for k in padded_inputs[0].keys()
                }

                # Generate outputs
                if self.map in [AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoModelForVision2Seq, AutoModelForMaskedLM]:
                    outputs = self.model.generate(**batched_inputs)
                    responses = []
                    for output in outputs:
                        if hasattr(outputs, 'sequences'):
                            generated_ids = output
                        else:
                            generated_ids = output
                        responses.append(processor.decode(generated_ids, skip_special_tokens=True))
                    return responses if is_batch else responses[0]
                else:
                    try:
                        with torch.no_grad():
                            outputs = self.model(**batched_inputs)
                            return [outputs] if not is_batch else outputs
                    except Exception as e:
                        outputs = self.model.generate(**batched_inputs)
                        responses = []
                        for output in outputs:
                            responses.append(processor.decode(output, skip_special_tokens=True))
                        return responses if is_batch else responses[0]

        else:  # Exclusive
            outputs = []
            for i in range(len(next(iter(standardized_payload.values())))):
                single_payload = {
                    k: v[i] if v is not None else None 
                    for k, v in standardized_payload.items()
                }
                self.model.processor(single_payload)
                outputs.append(self.model.infer())
            return outputs if is_batch else outputs[0]