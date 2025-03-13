import unittest
from storage.storage import save_qr_code, get_qr_code

class TestStorage(unittest.TestCase):
    def test_save_and_get_qr_code(self):
        qr_id = "test_id"
        qr_code_path = "/tmp/test.png"
        save_qr_code(qr_id, qr_code_path)
        retrieved_path = get_qr_code(qr_id)
        self.assertEqual(retrieved_path, qr_code_path)

if __name__ == '__main__':
    unittest.main()
