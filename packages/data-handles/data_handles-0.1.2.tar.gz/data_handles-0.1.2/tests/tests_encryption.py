import unittest
import base64
from packages.encryption import crypto

class TestCryptoFunctions(unittest.TestCase):
    
    def test_hash_sha256(self):
        result = crypto("hash", "hello", b"", "SHA-256")
        self.assertEqual(result, "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
    
    def test_hash_sha512(self):
        result = crypto("hash", "hello", b"", "SHA-512")
        self.assertEqual(result, "9b71d224bd62f3785d96d46ad3ea3d73319b3a3b7763ed9e1d1308e6f14acad7"
                                   "f5ecb469d2d9b07108d4e8b6a7e5c8bf793fcd5d5e51de4da6b3473a27c5df7a")
    
    def test_hash_md5(self):
        result = crypto("hash", "hello", b"", "MD5")
        self.assertEqual(result, "5d41402abc4b2a76b9719d911017c592")
    
    def test_encrypt_decrypt_aes(self):
        key = b"secretkey"
        text = "Hello, World!"
        encrypted = crypto("encrypt", text, key, "AES")
        decrypted = crypto("decrypt", encrypted, key, "AES")
        self.assertEqual(decrypted, text)
    
    def test_encrypt_decrypt_des(self):
        key = b"secretkey"
        text = "Hello, World!"
        encrypted = crypto("encrypt", text, key, "DES")
        decrypted = crypto("decrypt", encrypted, key, "DES")
        self.assertEqual(decrypted, text)
    
    def test_encrypt_decrypt_3des(self):
        key = b"secretkey"
        text = "Hello, World!"
        encrypted = crypto("encrypt", text, key, "3DES")
        decrypted = crypto("decrypt", encrypted, key, "3DES")
        self.assertEqual(decrypted, text)
    
    def test_encrypt_decrypt_blowfish(self):
        key = b"secretkey"
        text = "Hello, World!"
        encrypted = crypto("encrypt", text, key, "Blowfish")
        decrypted = crypto("decrypt", encrypted, key, "Blowfish")
        self.assertEqual(decrypted, text)
    
    def test_encrypt_decrypt_rc4(self):
        key = b"secretkey"
        text = "Hello, World!"
        encrypted = crypto("encrypt", text, key, "RC4")
        decrypted = crypto("decrypt", encrypted, key, "RC4")
        self.assertEqual(decrypted, text)
    
    def test_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            crypto("encrypt", "test", b"key", "InvalidAlgo")
    
    def test_invalid_action(self):
        with self.assertRaises(ValueError):
            crypto("invalid", "test", b"key", "AES")

if __name__ == "__main__":
    unittest.main()
