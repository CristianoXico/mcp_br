"""
Testes automatizados para o módulo de vulnerabilidade social.
Valida a integração, coleta e formatação dos dados.
"""

import sys
import os
import unittest
import asyncio
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.vulnerabilidade_social import obter_vulnerabilidade_social
from tools import cadunico, sus, educacao, snis, seguranca, cnpj
from tools.vulnerabilidade_social import _obter_dados_cadunico, _obter_dados_saude, _obter_dados_educacao, _obter_dados_saneamento, _obter_dados_seguranca, _obter_dados_emprego

# Função auxiliar para executar corrotinas em testes
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper


class TestVulnerabilidadeSocial(unittest.TestCase):
    """Testes para o módulo de vulnerabilidade social."""

    def setUp(self):
        """Configura o ambiente de teste."""
        # Limpa os caches para garantir testes isolados
        cadunico._cache = {}
        sus._cache = {}
        educacao._cache = {}
        snis._cache = {}
        seguranca._cache = {}
        cnpj._cache = {}

    @patch('tools.vulnerabilidade_social._obter_dados_cadunico')
    @patch('tools.vulnerabilidade_social._obter_dados_saude')
    @patch('tools.vulnerabilidade_social._obter_dados_educacao')
    @patch('tools.vulnerabilidade_social._obter_dados_saneamento')
    @patch('tools.vulnerabilidade_social._obter_dados_seguranca')
    @patch('tools.vulnerabilidade_social._obter_dados_emprego')
    @async_test
    async def test_obter_vulnerabilidade_social(
        self, mock_emprego, mock_seguranca, mock_saneamento, 
        mock_educacao, mock_saude, mock_cadunico
    ):
        """Testa a função principal de obtenção de vulnerabilidade social."""
        # Configura os mocks para retornar dados simulados
        mock_cadunico.return_value = {
            "familias_vulneraveis": 10000,
            "extrema_pobreza": 2000,
            "familias_beneficiadas": 5000,
            "valor_medio": 450.0
        }
        
        mock_saude.return_value = {
            "cobertura_aps": 75.5,
            "estabelecimentos_saude": 50,
            "leitos_sus": 200,
            "medicos_1000_habitantes": 1.8
        }
        
        mock_educacao.return_value = {
            "taxa_analfabetismo": 8.5,
            "escolaridade_media": 9.2,
            "ideb": 5.4,
            "escolas": 45
        }
        
        mock_saneamento.return_value = {
            "agua_encanada": 85.5,
            "coleta_esgoto": 65.2,
            "coleta_lixo": 90.1
        }
        
        mock_seguranca.return_value = {
            "homicidios_ano": 250,
            "violencia_domestica": 350,
            "roubos": 450
        }
        
        mock_emprego.return_value = {
            "desemprego": 12.1,
            "taxa_informalidade": 43.2,
            "microempresas_ativas": 10241
        }

        # Chama a função com parâmetros de teste
        resultado = await obter_vulnerabilidade_social("São Paulo", 2023)
        
        # Verifica se o resultado contém todas as seções esperadas
        self.assertIn("municipio", resultado)
        self.assertIn("ano", resultado)
        self.assertIn("familias_vulneraveis", resultado)
        self.assertIn("extrema_pobreza", resultado)
        self.assertIn("bolsa_familia", resultado)
        self.assertIn("saude_basica", resultado)
        self.assertIn("educacao", resultado)
        self.assertIn("saneamento", resultado)
        self.assertIn("seguranca", resultado)
        self.assertIn("emprego", resultado)
        
        # Verifica valores específicos
        self.assertEqual(resultado["municipio"], "São Paulo")
        self.assertEqual(resultado["ano"], 2023)
        
        # Verifica se os dados das APIs foram incorporados corretamente
        self.assertEqual(resultado["bolsa_familia"]["familias_beneficiadas"], 5000)
        self.assertEqual(resultado["saude_basica"]["cobertura_aps"], 75.5)
        self.assertEqual(resultado["educacao"]["taxa_analfabetismo"], 8.5)
        self.assertEqual(resultado["saneamento"]["coleta_esgoto"], 65.2)
        self.assertEqual(resultado["seguranca"]["violencia_domestica"], 350)
        self.assertEqual(resultado["emprego"]["taxa_informalidade"], 43.2)

    @patch('tools.cadunico.obter_dados_cadunico')
    @async_test
    async def test_integracao_cadunico(self, mock_cadunico):
        """Testa a integração com o módulo CadÚnico."""
        # Configura o mock para retornar dados simulados
        mock_cadunico.return_value = {
            "familias_vulneraveis": 10000,
            "extrema_pobreza": 2000,
            "familias_beneficiadas": 5000,
            "valor_medio": 450.0
        }
        
        # Chama a função do módulo
        resultado = await _obter_dados_cadunico("São Paulo", 2023)
        
        # Verifica os resultados
        self.assertIsNotNone(resultado)
        self.assertIn("familias_vulneraveis", resultado)
        self.assertIn("extrema_pobreza", resultado)
        self.assertIn("familias_beneficiadas", resultado)
        self.assertIn("valor_medio", resultado)

    @patch('tools.cadunico.obter_dados_cadunico')
    @async_test
    async def test_integracao_com_erro(self, mock_cadunico):
        """Testa o comportamento quando a API retorna erro."""
        # Configura o mock para simular um erro na API
        mock_cadunico.side_effect = Exception("Erro de conexão")
        
        # Chama a função do módulo
        resultado = await _obter_dados_cadunico("São Paulo", 2023)
        
        # Verifica se foram retornados dados simulados em caso de erro
        self.assertIsNotNone(resultado)
        self.assertIn("familias_vulneraveis", resultado)
        self.assertIn("extrema_pobreza", resultado)
        self.assertIn("familias_beneficiadas", resultado)
        self.assertIn("valor_medio", resultado)


if __name__ == '__main__':
    # Configura o loop de eventos para testes assíncronos
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Executa os testes
    unittest.main()
