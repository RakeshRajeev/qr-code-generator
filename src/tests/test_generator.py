import unittest
import os
import shutil
import tempfile
from src.qr_generator.generator import generate_qr_code

class TestQRGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.environ['QR_CODES_DIR'] = self.test_dir

    def test_generate_qr_code(self):
        data = "https://example.com"
        img_path, qr_id = generate_qr_code(data)
        self.assertTrue(img_path.endswith('.png'))
        self.assertIsNotNone(qr_id)
        self.assertTrue(os.path.exists(img_path))

    def tearDown(self):
        # Clean up test directory and its contents
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main()
