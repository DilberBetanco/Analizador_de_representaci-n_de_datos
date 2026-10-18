from django.test import TestCase, Client
from django.urls import reverse

class AnalizadorTests(TestCase):
    def setUp(self):
        self.client = Client()

    # 1. Conversión válida
    def test_conversion_valida(self):
        response = self.client.post(reverse('index'), {'form_numero': '1', 'numero': '2AF', 'base': '16'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('687', response.content.decode('utf-8'))

    # 2. Error de dígitos inválidos según la base
    def test_error_digitos_invalidos(self):
        response = self.client.post(reverse('index'), {'form_numero': '1', 'numero': '1021', 'base': '2'})
        self.assertIn('inválidos', response.content.decode('utf-8'))

    # 3. Error de valor fuera de rango (> 65535)
    def test_error_rango_excedido(self):
        response = self.client.post(reverse('index'), {'form_numero': '1', 'numero': '70000', 'base': '10'})
        self.assertIn('65,535', response.content.decode('utf-8'))

    # 4. Error de número negativo
    def test_error_numero_negativo(self):
        response = self.client.post(reverse('index'), {'form_numero': '1', 'numero': '-15', 'base': '10'})
        self.assertIn('negativos', response.content.decode('utf-8'))

    # 5. Entrada vacía
    def test_error_entrada_vacia_texto(self):
        response = self.client.post(reverse('index'), {'form_texto': '1', 'texto': ''})
        self.assertIn('Entrada vacía', response.content.decode('utf-8'))

    # 6. Prueba UTF-8 con la letra 'ñ'
    def test_analisis_utf8_con_enie(self):
        response = self.client.post(reverse('index'), {'form_texto': '1', 'texto': 'Año'})
        self.assertIn('U+00F1', response.content.decode('utf-8'))