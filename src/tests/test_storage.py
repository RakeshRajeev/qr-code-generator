import unittest
import asyncio
from src.storage.storage import QRCodeStorage
from src.db.session import get_db

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.db = next(get_db())
        self.storage = QRCodeStorage()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def test_save_and_get_qr_code(self):
        qr_id = "test_id"
        qr_code_path = "/tmp/test.png"
        original_data = "test_data"
        
        # Test saving
        self.loop.run_until_complete(
            self.storage.save_qr_code(qr_id, qr_code_path, original_data)
        )
        
        # Test retrieval
        retrieved_path = self.loop.run_until_complete(
            self.storage.get_qr_code(qr_id)
        )
        self.assertEqual(retrieved_path, qr_code_path)

    def tearDown(self):
        self.db.close()
        self.loop.close()

if __name__ == '__main__':
    unittest.main()
