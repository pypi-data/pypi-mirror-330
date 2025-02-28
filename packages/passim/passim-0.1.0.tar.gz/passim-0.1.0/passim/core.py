import bcrypt
import hashlib
from typing import Set, Tuple


class Passim:
    """A class for secure password similarity checking using n-grams."""

    def __init__(self, n_gram_size: int = 3, similarity_threshold: float = 0.5, num_ngrams_to_store: int = 5):
        """
        Initialize Passim with configurable parameters.
        
        Args:
            n_gram_size (int): Size of n-grams (default: 3 for trigrams).
            similarity_threshold (float): Threshold for similarity (0 to 1, default: 0.5).
            num_ngrams_to_store (int): Max number of n-grams to store in sketch (default: 5).
        """
        self.n_gram_size = n_gram_size
        self.similarity_threshold = similarity_threshold
        self.num_ngrams_to_store = num_ngrams_to_store

    def _generate_ngrams(self, password: str) -> list[str]:
        """Generate n-grams from a password."""
        if len(password) < self.n_gram_size:
            return [password]
        return [password[i:i + self.n_gram_size] for i in range(len(password) - self.n_gram_size + 1)]

    def _hash_ngram(self, ngram: str) -> str:
        """Hash an n-gram using SHA-256, truncated for efficiency."""
        return hashlib.sha256(ngram.encode('utf-8')).hexdigest()[:8]

    def _create_similarity_sketch(self, password: str) -> Set[str]:
        """Create a similarity sketch from hashed n-grams."""
        ngrams = self._generate_ngrams(password)
        hashed_ngrams = [self._hash_ngram(ngram) for ngram in ngrams]
        return set(hashed_ngrams[:self.num_ngrams_to_store])

    def hash_password(self, password: str) -> bytes:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def store_password(self, password: str) -> Tuple[bytes, Set[str]]:
        """Store a password's hash and similarity sketch."""
        password_hash = self.hash_password(password)
        sketch = self._create_similarity_sketch(password)
        return password_hash, sketch

    def check_similarity(self, old_sketch: Set[str], new_password: str) -> bool:
        """
        Check if a new password is too similar to the old one.
        
        Args:
            old_sketch (Set[str]): Similarity sketch of the old password.
            new_password (str): New password to check.
        
        Returns:
            bool: True if too similar, False otherwise.
        """
        new_sketch = self._create_similarity_sketch(new_password)
        if not old_sketch or not new_sketch:
            return False
        common_ngrams = old_sketch.intersection(new_sketch)
        similarity_score = len(common_ngrams) / \
            min(len(old_sketch), len(new_sketch))
        return similarity_score >= self.similarity_threshold

    def change_password(self, old_sketch: Set[str], new_password: str) -> Tuple[bool, Tuple[bytes, Set[str]]]:
        """
        Attempt to change a password, checking similarity.
        
        Returns:
            Tuple[bool, Tuple[bytes, Set[str]]]: (success, (new_hash, new_sketch) or (None, None)).
        """
        if self.check_similarity(old_sketch, new_password):
            return False, (None, None)
        new_hash, new_sketch = self.store_password(new_password)
        return True, (new_hash, new_sketch)
