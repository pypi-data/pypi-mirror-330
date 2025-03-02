import time
import logging
import random
import asyncio
from typing import Dict, List, Union
from pii_scanner.regex_patterns.presidio_patterns import patterns
from presidio_analyzer.nlp_engine.spacy_nlp_engine import SpacyNlpEngine
from pii_scanner.check_digit_warehouse.validate_entity_type import validate_entity_check_digit
from presidio_analyzer import AnalyzerEngine, PatternRecognizer

logger = logging.getLogger(__name__)

class LoadedSpacyNlpEngine(SpacyNlpEngine):
    def __init__(self, loaded_spacy_model):
        super().__init__()
        self.nlp = {"en": loaded_spacy_model}

class SpacyNERScanner:
    """
    Optimized NER Scanner using Presidio's AnalyzerEngine with SpaCy.
    """
    SPACY_EN_MODEL = "en_core_web_lg"

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.analyzer = None
        self.nlp_engine = None
        self.initialized = False
        self.region = None

    def _initialize(self):
        """Lazy initialization of the SpaCy model and Presidio Analyzer."""
        if self.initialized:
            return

        import spacy
        try:
            self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)
        except OSError:
            self.logger.warning("Downloading en_core_web_lg model for SpaCy.")
            from spacy.cli import download
            download(self.SPACY_EN_MODEL)
            self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)

        loaded_nlp_engine = LoadedSpacyNlpEngine(loaded_spacy_model=self.nlp_engine)
        self.analyzer = AnalyzerEngine(nlp_engine=loaded_nlp_engine)

        combined_patterns = {**patterns.get("GLOBAL", {}), **patterns.get(self.region.value, {})}
        recognizers = [PatternRecognizer(supported_entity=entity, patterns=[pattern]) for entity, pattern in combined_patterns.items()]
        
        for recognizer in recognizers:
            self.analyzer.registry.add_recognizer(recognizer)

        self.initialized = True

    async def _process_with_analyzer(self, text: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """Processes text using the Presidio Analyzer."""
        self._initialize()
        analyzer_results = self.analyzer.analyze(text, language="en")

        if not analyzer_results:
            return {"text": text, "entity_detected": []}

        entity_type = analyzer_results[0].entity_type
        return await validate_entity_check_digit(text, entity_type, self.region.value)

    async def _process_batch_async(self, texts: List[str]) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
        """Processes a batch of texts concurrently using asyncio."""
        return await asyncio.gather(*(self._process_with_analyzer(text) for text in texts))

    def _sample_data(self, sample_data: List[str], sample_size: Union[int, float]) -> List[str]:
        """Samples the data based on the given size (integer or percentage)."""
        total = len(sample_data)
        if isinstance(sample_size, float) and 0 < sample_size <= 1:
            sample_size = int(total * sample_size)
        return random.sample(sample_data, min(sample_size, total))

    async def scan(self, sample_data: List[str], sample_size: Union[int, float], region: str) -> Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
        """Performs an asynchronous scan on the given data."""
        start_time = time.time()
        self.region = region

        if sample_size:
            sample_data = self._sample_data(sample_data, sample_size)
        # print(len(sample_data), "lengh of sample data")
        results = await self._process_batch_async(sample_data)

        self.logger.info(f"Processing completed in {time.time() - start_time:.2f} seconds.")
        return {"results": results}
