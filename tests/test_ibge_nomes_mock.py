import unittest
from unittest.mock import patch
from tools import ibge_nomes_handlers

class TestIbgeNomesHandlersMock(unittest.TestCase):
    @patch('tools.ibge_nomes_handlers.api_get_nomes')
    def test_pesquisar_nomes_mock(self, mock_api):
        mock_api.return_value = [{"nome": "João", "frequencia": 123}]
        resultado = ibge_nomes_handlers.pesquisar_nomes("João")
        self.assertIsInstance(resultado, list)
        self.assertTrue(len(resultado) > 0)
        self.assertIn("nome", resultado[0])

    @patch('tools.ibge_nomes_handlers.api_get_nomes')
    def test_ranking_nomes_mock(self, mock_api):
        mock_api.return_value = [{"nome": "Maria", "frequencia": 456}]
        resultado = ibge_nomes_handlers.ranking_nomes(localidade="BR", sexo="F")
        self.assertIsInstance(resultado, list)
        self.assertTrue(len(resultado) > 0)
        self.assertIn("nome", resultado[0])

    @patch('tools.ibge_nomes_handlers.api_get_nomes')
    def test_frequencia_nome_mock(self, mock_api):
        mock_api.return_value = [{"nome": "Ana", "frequencia": 789}]
        resultado = ibge_nomes_handlers.frequencia_nome("Ana")
        self.assertIsInstance(resultado, list)
        self.assertTrue(len(resultado) > 0)
        self.assertIn("nome", resultado[0])

if __name__ == "__main__":
    unittest.main()
