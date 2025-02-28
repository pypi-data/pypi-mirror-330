
import unittest
from passim.core import Passim


class TestPassim(unittest.TestCase):
    def setUp(self):
        self.passim = Passim()
        self.custom_passim = Passim(n_gram_size=4, similarity_threshold=0.9, num_ngrams_to_store=3)
        
    def test_password_similarity_default_settings(self):
        """Test similarity checking with default settings"""
        _, sketch = self.passim.store_password("Password123")
        
        # Same or similar passwords should be detected as similar
        self.assertTrue(self.passim.check_similarity(sketch, "Password123"))
        self.assertTrue(self.passim.check_similarity(sketch, "Password124"))
        self.assertTrue(self.passim.check_similarity(sketch, "Password123!"))
        
        # Different passwords should not be detected as similar
        self.assertFalse(self.passim.check_similarity(sketch, "TotallyNew"))
        self.assertFalse(self.passim.check_similarity(sketch, "CompletelyDifferent"))
    
    def test_password_similarity_custom_settings(self):
        """Test similarity checking with custom settings"""
        _, sketch = self.custom_passim.store_password("Password123")
        
        # With higher threshold and n_gram_size, slightly different passwords might still be detected as similar
        # So we need an even more different password to fall below the threshold
        self.assertFalse(self.custom_passim.check_similarity(sketch, "supersecret789"))
        
        # Same password should still be detected as similar
        self.assertTrue(self.custom_passim.check_similarity(sketch, "Password123"))
        
        # Very similar passwords should still be detected
        self.assertTrue(self.custom_passim.check_similarity(sketch, "Password123!"))

    def test_password_change(self):
        """Test password change functionality"""
        old_hash, old_sketch = self.passim.store_password("Password123")
        
        # Similar password change should be rejected
        success, result = self.passim.change_password(old_hash, old_sketch, "Password124")
        self.assertFalse(success)
        self.assertEqual(result, (None, None))
        
        # Different password change should be accepted
        success, (new_hash, new_sketch) = self.passim.change_password(old_hash, old_sketch, "TotallyNew")
        self.assertTrue(success)
        self.assertIsNotNone(new_hash)
        self.assertNotEqual(new_hash, old_hash)
        self.assertIsNotNone(new_sketch)
    
    def test_ngram_generation(self):
        """Test n-gram generation"""
        # For short passwords
        ngrams = self.passim._generate_ngrams("ab")
        self.assertEqual(ngrams, ["ab"])
        
        # For regular passwords
        ngrams = self.passim._generate_ngrams("password")
        self.assertEqual(len(ngrams), 6)  # "pas", "ass", "ssw", "swo", "wor", "ord"
        self.assertEqual(ngrams[0], "pas")
        self.assertEqual(ngrams[-1], "ord")


if __name__ == "__main__":
    unittest.main()