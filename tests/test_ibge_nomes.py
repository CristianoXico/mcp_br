import unittest
from tools.ibge_nomes import pesquisar_nomes, ranking_nomes, frequencia_nome

class TestIbgeNomesHandlers(unittest.TestCase):
    def test_pesquisar_nomes(self):
        resultado = pesquisar_nomes("João")
        self.assertIsInstance(resultado, list)
        self.assertTrue(len(resultado) > 0)
        self.assertIn("nome", resultado[0] if resultado else {"nome": "João"})

    def test_ranking_nomes(self):
        resultado = ranking_nomes(localidade="BR", sexo="M")
        self.assertIsInstance(resultado, list)
        self.assertTrue(len(resultado) > 0)
        self.assertIn("nome", resultado[0] if resultado else {"nome": "João"})

    def test_frequencia_nome(self):
        resultado = frequencia_nome("Maria")
        self.assertIsInstance(resultado, list)
        self.assertTrue(len(resultado) > 0)
        self.assertIn("nome", resultado[0] if resultado else {"nome": "Maria"})

if __name__ == "__main__":
    unittest.main()
