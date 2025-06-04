# protocol/handlers.py
import logging
from tools import ibge, transparencia, cnpj
from tools.vulnerabilidade_social import obter_vulnerabilidade_social

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def call_tool(tool_name, params):
    """
    Coordena a chamada às ferramentas do MCP com base no nome da ferramenta e parâmetros.
    
    Args:
        tool_name: Nome da ferramenta a ser chamada
        params: Parâmetros para a ferramenta
        
    Returns:
        Resultado da chamada à ferramenta
    """
    logger.info(f"Chamando ferramenta: {tool_name} com parâmetros: {params}")
    
    try:
        if tool_name == "buscar_populacao":
            return ibge.buscar_populacao(params["municipio"])
        elif tool_name == "gastos_publicos":
            return transparencia.gastos(params["orgao"])
        elif tool_name == "dados_cnpj":
            return cnpj.buscar(params["cnpj"])
        elif tool_name == "vulnerabilidade_social":
            municipio = params.get("municipio")
            ano = params.get("ano", None)
            return await obter_vulnerabilidade_social(municipio, ano)
        else:
            raise ValueError(f"Ferramenta desconhecida: {tool_name}")
    except Exception as e:
        logger.error(f"Erro ao chamar a ferramenta {tool_name}: {e}")
        raise