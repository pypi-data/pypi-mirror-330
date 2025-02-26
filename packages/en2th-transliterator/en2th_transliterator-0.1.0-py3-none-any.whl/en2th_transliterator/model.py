"""Core English-to-Thai transliteration model implementation."""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the environment variable to avoid tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class En2ThTransliterator:
    """Class for English-to-Thai transliteration using ByT5."""

    def __init__(self,
                 model_path="en2th_transliterator/model",
                 max_length=100,
                 num_beams=4,
                 length_penalty=1.0,
                 verbose=False):
        """
        Initialize the English-to-Thai transliterator.
        
        Args:
            model_path: Path to the model directory or HuggingFace model name
            max_length: Maximum length of generated text
            num_beams: Number of beams for beam search
            length_penalty: Length penalty for generation
            verbose: Whether to print detailed logs
        """
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')

        if not verbose:
            # Disable most logging
            logging.getLogger("transformers").setLevel(logging.ERROR)
            logger.setLevel(logging.WARNING)

        logger.info(f"Loading model from {model_path}")
        logger.info(f"Using device: {self.device}")

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()

        # Generation parameters
        self.max_length = max_length
        self.num_beams = num_beams
        self.length_penalty = length_penalty
        self.verbose = verbose

        logger.info("Model loaded successfully")

    def transliterate(self,
                      text,
                      temperature=0.7,
                      top_k=50,
                      top_p=0.9,
                      prefix=""):
        """
        Transliterate English text to Thai.
        
        Args:
            text: English text to transliterate
            temperature: Sampling temperature (0 for deterministic)
            top_k: Top-k sampling parameter
            top_p: Top-p sampling parameter
            prefix: Optional prefix to add before the input text
            
        Returns:
            Thai transliteration of the input text
        """
        # Add prefix if provided
        if prefix:
            input_text = f"{prefix}: {text}"
        else:
            input_text = text

        if self.verbose:
            logger.info(f"\nInput text: {input_text}")
            logger.info(f"Input length: {len(input_text)}")

        # Tokenize
        input_ids = self.tokenizer(input_text,
                                   return_tensors="pt").to(self.device)

        if self.verbose:
            logger.info(
                f"Input token length: {len(input_ids['input_ids'][0])}")
            logger.info(
                f"Input tokens: {self.tokenizer.convert_ids_to_tokens(input_ids['input_ids'][0])}"
            )

        # Generate
        with torch.no_grad():
            if temperature > 0 and temperature != 1.0:
                # Use sampling
                outputs = self.model.generate(
                    input_ids=input_ids["input_ids"],
                    max_length=self.max_length,
                    do_sample=True,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    early_stopping=True,
                )
            else:
                # Use beam search
                outputs = self.model.generate(
                    input_ids=input_ids["input_ids"],
                    max_length=self.max_length,
                    num_beams=self.num_beams,
                    length_penalty=self.length_penalty,
                    early_stopping=True,
                )

        # Decode
        output_text = self.tokenizer.decode(outputs[0],
                                            skip_special_tokens=True)

        if self.verbose:
            logger.info(f"Output text: {output_text}")
            logger.info(f"Output length: {len(output_text)}")
            logger.info(f"Output token length: {len(outputs[0])}")
            logger.info(
                f"Output tokens: {self.tokenizer.convert_ids_to_tokens(outputs[0])}"
            )

        return output_text

    def batch_transliterate(self, texts, batch_size=16, **kwargs):
        """
        Transliterate a batch of English texts to Thai.
        
        Args:
            texts: List of English texts to transliterate
            batch_size: Batch size for processing
            **kwargs: Additional arguments to pass to transliterate()
            
        Returns:
            List of Thai transliterations
        """
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_results = [
                self.transliterate(text, **kwargs) for text in batch
            ]
            results.extend(batch_results)
        return results
