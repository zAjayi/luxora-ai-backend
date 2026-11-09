import unittest
from datetime import timedelta
from uuid import uuid4

from app.core.security import create_access_token, get_password_hash, verify_password


class AuthSecurityTests(unittest.TestCase):
    def test_password_hashing_round_trip(self):
        password = "secret123"
        hashed = get_password_hash(password)

        self.assertNotEqual(hashed, password)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong-password", hashed))

    def test_create_access_token_returns_string(self):
        token = create_access_token({"sub": str(uuid4())}, expires_delta=timedelta(minutes=5))
        self.assertIsInstance(token, str)
        self.assertTrue(token)


if __name__ == "__main__":
    unittest.main()
