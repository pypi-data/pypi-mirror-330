import time
import logging
import random
import asyncio
import spacy
from spacy.matcher import Matcher
from typing import Dict, List, Union
from pii_scanner.regex_patterns.matcher_patterns import patterns
from pii_scanner.check_digit_warehouse.validate_entity_type import validate_entity_check_digit

logger = logging.getLogger(__name__)

class SpacyMatchScanner:
    """
    SpacyMatch Scanner for Named Entity Recognition (NER) and Regex-based entity detection.
    """

    SPACY_EN_MODEL = "en_core_web_lg"

    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize variables for lazy loading
        self.matcher = None
        self.nlp_engine = None
        self.initialized = False
        self.region = None

    def _initialize(self, region: str):
        """Lazy initialization of the SpaCy model and Matcher with region-specific patterns."""
        if not self.initialized:
            try:
                self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)
            except OSError:
                self.logger.warning("Downloading en_core_web_lg language model for SpaCy")
                from spacy.cli import download
                download(self.SPACY_EN_MODEL)
                self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)

            # Create matcher and add patterns
            self.matcher = Matcher(self.nlp_engine.vocab)
            self.region = region  # Set the region

            # Fetch region-specific patterns
            global_patterns = patterns.get("GLOBAL", {})
            region_patterns = patterns.get(self.region.value, {})
            if not global_patterns and not region_patterns:
                self.logger.warning(f"No patterns found for region: {self.region}")

            combined_patterns = {}
            combined_patterns.update(global_patterns)
            combined_patterns.update(region_patterns)
            # print(combined_patterns)
            for label, pattern in combined_patterns.items():
                try:
                    self.matcher.add(label, [[{"TEXT": {"REGEX": pattern}}]])
                except Exception as e:
                    self.logger.error(f"Failed to add pattern for {label}: {e}")

            self.initialized = True

    def _chunk_text(self, text: str, chunk_size: int = 512) -> List[str]:
        """
        Splits the text into smaller chunks for processing.
        """
        words = text.split()
        chunks, chunk = [], []

        for word in words:
            if len(" ".join(chunk) + " " + word) <= chunk_size:
                chunk.append(word)
            else:
                chunks.append(" ".join(chunk))
                chunk = [word]

        if chunk:
            chunks.append(" ".join(chunk))
        return chunks

    async def _scan_text_async(self, data: str) -> List[Dict[str, Union[str, List[Dict[str, Union[str, int, float]]]]]]:
        """Asynchronously process a single text chunk using SpaCy and Matcher."""
        doc = self.nlp_engine(data)

        matched_patterns = []

        # Apply SpaCy NER detection
        for ent in doc.ents:
            matched_patterns.append({
                'text': ent.text,
                'entity_detected': [{
                    'type': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'score': 0.95  # Fixed confidence score for demonstration
                }]
            })

        # Apply custom regex patterns using the pre-configured matcher
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            pattern_id = self.nlp_engine.vocab.strings[match_id]
            entity = doc[start:end].text

            matched_patterns.append({
                'text': entity,
                'entity_detected': [{
                    'type': pattern_id,
                    'start': start,
                    'end': end,
                    'score': round(random.uniform(0.8, 1.0), 2)  # Random confidence score
                }]
            })

        return matched_patterns

    async def scan_async(self, data: str, region: str) -> List[Dict[str, Union[str, List[Dict[str, Union[str, int, float]]]]]]:
        """
        Asynchronously processes large text by splitting it into chunks and processing each chunk in parallel.
        """
        self._initialize(region)
        start_time = time.time()

        # Chunk the text
        text_chunks = self._chunk_text(data)

        # Process each text chunk asynchronously
        tasks = [self._scan_text_async(chunk) for chunk in text_chunks]
        chunk_results = await asyncio.gather(*tasks)

        # Combine results
        final_results = [item for sublist in chunk_results for item in sublist]

        # Validate detected entities using check digit logic
        validation_tasks = []
        for entity in final_results:
            analyzer_result = entity.get("entity_detected", [])
            if analyzer_result:
                analyzer_result = analyzer_result[0]
                entity_type = analyzer_result.get("type")
                text = entity.get("text", "")
                validation_tasks.append(
                    validate_entity_check_digit(text, entity_type, region)
                )

        validation_results = await asyncio.gather(*validation_tasks)

        # Attach validation results
        for entity, validation_result in zip(final_results, validation_results):
            entity["validated"] = {
                "entity_detected": entity.get("entity_detected", []),
                "check_digit": validation_result.get("check_digit", False)
            }

        end_time = time.time()
        self.logger.info(f"Processing completed in {end_time - start_time:.2f} seconds.")

        return final_results
