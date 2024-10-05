import unittest
import cv2
import numpy as np
from etapa1 import filtro_passa_baixa, filtro_media, filtro_mediana, filtro_passa_alta, filtro_laplaciano, filtro_sobel

class TestImageFilters(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a sample image for testing
        cls.img_original = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.rectangle(cls.img_original, (25, 25), (75, 75), (255, 255, 255), -1)
        global img_original
        img_original = cls.img_original

    def test_filtro_passa_baixa(self):
        filtro_passa_baixa()
        self.assertIsNotNone(img_original)
        self.assertEqual(img_original.shape, (100, 100, 3))

    def test_filtro_media(self):
        filtro_media()
        self.assertIsNotNone(img_original)
        self.assertEqual(img_original.shape, (100, 100, 3))

    def test_filtro_mediana(self):
        filtro_mediana()
        self.assertIsNotNone(img_original)
        self.assertEqual(img_original.shape, (100, 100, 3))

    def test_filtro_passa_alta(self):
        filtro_passa_alta()
        self.assertIsNotNone(img_original)
        self.assertEqual(img_original.shape, (100, 100, 3))

    def test_filtro_laplaciano(self):
        filtro_laplaciano()
        self.assertIsNotNone(img_original)
        self.assertEqual(img_original.shape, (100, 100, 3))

    def test_filtro_sobel(self):
        filtro_sobel()
        self.assertIsNotNone(img_original)
        self.assertEqual(img_original.shape, (100, 100, 3))

if __name__ == '__main__':
    unittest.main()