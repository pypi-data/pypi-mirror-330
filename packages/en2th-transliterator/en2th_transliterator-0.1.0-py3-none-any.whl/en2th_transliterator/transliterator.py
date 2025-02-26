from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch


class En2ThTransliterator:

    def __init__(self,
                 model_path=None,
                 max_length=100,
                 num_beams=4,
                 length_penalty=1.0,
                 verbose=False,
                 fp16=True):
        """
        Initialize the English to Thai transliterator.
        
        Args:
            model_path (str, optional): Path to a local model. If None, will use the HF model.
            max_length (int): Maximum length of generated sequence.
            num_beams (int): Number of beams for beam search.
            length_penalty (float): Length penalty for generation.
            verbose (bool): Whether to print verbose output.
            fp16 (bool): Whether to use mixed precision (fp16) for inference.
        """
        # Model parameters
        self.max_length = max_length
        self.num_beams = num_beams
        self.length_penalty = length_penalty
        self.verbose = verbose
        self.fp16 = fp16

        # Use either custom path or default HF model
        if model_path:
            if self.verbose:
                print(f"Loading model from {model_path}")
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        else:
            if self.verbose:
                print("Loading model from Hugging Face Hub")
            # Use the yacht/byt5-base-en2th-transliterator model
            hf_model_name = "yacht/byt5-base-en2th-transliterator"
            self.model = AutoModelForSeq2SeqLM.from_pretrained(hf_model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(hf_model_name)

        # Move model to GPU if available
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        # Enable fp16 if requested and available
        self.amp_enabled = self.fp16 and self.device.type == "cuda"
        if self.amp_enabled and self.verbose:
            print("Using mixed precision (fp16) for inference")

        if self.verbose:
            print(f"Model loaded and running on {self.device}")

    def transliterate(self, text, temperature=1.0, top_k=None, top_p=None):
        """
        Transliterate English text to Thai.
        
        Args:
            text (str): English text to transliterate.
            temperature (float): Sampling temperature.
            top_k (int, optional): Top-k sampling parameter.
            top_p (float, optional): Top-p sampling parameter.
            
        Returns:
            str: Thai transliteration of the input text.
        """
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        # Configure generation parameters
        gen_kwargs = {
            "max_length": self.max_length,
            "num_beams": self.num_beams,
            "length_penalty": self.length_penalty,
        }

        # Add sampling parameters if specified
        if temperature != 1.0:
            gen_kwargs["temperature"] = temperature
            gen_kwargs["do_sample"] = True

        if top_k is not None:
            gen_kwargs["top_k"] = top_k
            gen_kwargs["do_sample"] = True

        if top_p is not None:
            gen_kwargs["top_p"] = top_p
            gen_kwargs["do_sample"] = True

        # Generate transliteration with mixed precision if enabled
        with torch.amp.autocast(device_type=self.device.type,
                                enabled=self.amp_enabled):
            outputs = self.model.generate(**inputs, **gen_kwargs)

        # Decode and return
        thai_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return thai_text

    def batch_transliterate(self, texts, batch_size=8, **kwargs):
        """
        Transliterate a batch of English texts to Thai.
        
        Args:
            texts (list): List of English texts to transliterate.
            batch_size (int): Batch size for processing.
            **kwargs: Additional arguments to pass to transliterate().
            
        Returns:
            list: List of Thai transliterations.
        """
        results = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]

            if self.verbose:
                print(
                    f"Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}"
                )

            # Process each text in the batch
            batch_results = [
                self.transliterate(text, **kwargs) for text in batch
            ]
            results.extend(batch_results)

        return results
