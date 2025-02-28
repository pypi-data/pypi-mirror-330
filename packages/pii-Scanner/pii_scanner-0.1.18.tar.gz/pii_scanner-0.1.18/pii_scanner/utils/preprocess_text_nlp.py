

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


async def preprocess_text(text: str) -> str:
    """
    Clean and preprocess text by removing stopwords, unnecessary characters, and extra spaces.
    """
    # Strip leading and trailing whitespace
    text = text.strip()
    
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Reconstruct text
    preprocessed_text = ' '.join(filtered_tokens)
    
    return preprocessed_text