import unittest
from src.qr_generator.generator import generate_qr_code

class TestQRGenerator(unittest.TestCase):
    def test_generate_qr_code(self):
        data = "https://example.com"
        img_path, qr_id = generate_qr_code(data)
        self.assertTrue(img_path.endswith('.png'))
        self.assertIsNotNone(qr_id)

if __name__ == '__main__':
    unittest.main()
