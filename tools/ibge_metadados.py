"""
Módulo para acesso à API de Metadados Estatísticos do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/metadados-estatisticos
"""

from .ibge_base import *

def listar_fontes() -> List[Dict]:
    """Lista todas as fontes de dados disponíveis"""
    cache_key = "fontes"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/fontes"
        fontes = make_request(url)
        return save_to_cache(cache_key, fontes)
    except Exception as e:
        logger.error(f"Erro ao listar fontes: {e}")
        return [{"erro": str(e)}]

def listar_pesquisas() -> List[Dict]:
    """Obtém as pesquisas com metadados associados"""
    cache_key = "pesquisas"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas"
        pesquisas = make_request(url)
        return save_to_cache(cache_key, pesquisas)
    except Exception as e:
        logger.error(f"Erro ao listar pesquisas: {e}")
        return [{"erro": str(e)}]

def listar_periodos_pesquisa(pesquisa: str) -> List[Dict]:
    """
    Obtém os períodos disponíveis para uma pesquisa
    
    Args:
        pesquisa: ID da pesquisa
    """
    cache_key = f"periodos_pesquisa_{pesquisa}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos"
        periodos = make_request(url)
        return save_to_cache(cache_key, periodos)
    except Exception as e:
        logger.error(f"Erro ao listar períodos da pesquisa {pesquisa}: {e}")
        return [{"erro": str(e)}]

def obter_metadados_pesquisa_periodo(pesquisa: str, periodo: str) -> Dict:
    """
    Obtém os metadados de uma pesquisa para um período específico
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
    """
    cache_key = f"metadados_pesquisa_{pesquisa}_periodo_{periodo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}"
        metadados = make_request(url)
        return save_to_cache(cache_key, metadados)
    except Exception as e:
        logger.error(f"Erro ao obter metadados da pesquisa {pesquisa} período {periodo}: {e}")
        return {"erro": str(e)}

def listar_agregados_pesquisa_periodo(pesquisa: str, periodo: str) -> List[Dict]:
    """
    Lista os agregados de uma pesquisa para um período específico
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
    """
    cache_key = f"agregados_pesquisa_{pesquisa}_periodo_{periodo}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados"
        agregados = make_request(url)
        return save_to_cache(cache_key, agregados)
    except Exception as e:
        logger.error(f"Erro ao listar agregados da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]

def obter_agregado(pesquisa: str, periodo: str, agregado: str) -> Dict:
    """
    Obtém informações detalhadas de um agregado específico
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
        agregado: ID do agregado
    """
    cache_key = f"agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}"
        info_agregado = make_request(url)
        return save_to_cache(cache_key, info_agregado)
    except Exception as e:
        logger.error(f"Erro ao obter agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return {"erro": str(e)}

def listar_variaveis_agregado(pesquisa: str, periodo: str, agregado: str) -> List[Dict]:
    """
    Lista as variáveis de um agregado específico
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
        agregado: ID do agregado
    """
    cache_key = f"variaveis_agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/variaveis"
        variaveis = make_request(url)
        return save_to_cache(cache_key, variaveis)
    except Exception as e:
        logger.error(f"Erro ao listar variáveis do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]

def obter_variavel(pesquisa: str, periodo: str, agregado: str, variavel: str) -> Dict:
    """
    Obtém informações detalhadas de uma variável específica
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
        agregado: ID do agregado
        variavel: ID da variável
    """
    cache_key = f"variavel_{pesquisa}_periodo_{periodo}_agregado_{agregado}_variavel_{variavel}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/variaveis/{variavel}"
        info_variavel = make_request(url)
        return save_to_cache(cache_key, info_variavel)
    except Exception as e:
        logger.error(f"Erro ao obter variável {variavel} do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return {"erro": str(e)}

def listar_classificacoes_agregado(pesquisa: str, periodo: str, agregado: str) -> List[Dict]:
    """
    Lista as classificações de um agregado específico
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
        agregado: ID do agregado
    """
    cache_key = f"classificacoes_agregado_{pesquisa}_periodo_{periodo}_agregado_{agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes"
        classificacoes = make_request(url)
        return save_to_cache(cache_key, classificacoes)
    except Exception as e:
        logger.error(f"Erro ao listar classificações do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]

def listar_niveis_classificacao(pesquisa: str, periodo: str, agregado: str, classificacao: str) -> List[Dict]:
    """
    Lista os níveis de uma classificação específica
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
        agregado: ID do agregado
        classificacao: ID da classificação
    """
    cache_key = f"niveis_classificacao_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis"
        niveis = make_request(url)
        return save_to_cache(cache_key, niveis)
    except Exception as e:
        logger.error(f"Erro ao listar níveis da classificação {classificacao} do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]

def listar_categorias_nivel(pesquisa: str, periodo: str, agregado: str, classificacao: str, nivel: str) -> List[Dict]:
    """
    Lista as categorias de um nível específico de classificação
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
        agregado: ID do agregado
        classificacao: ID da classificação
        nivel: ID do nível
    """
    cache_key = f"categorias_nivel_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}_nivel_{nivel}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis/{nivel}/categorias"
        categorias = make_request(url)
        return save_to_cache(cache_key, categorias)
    except Exception as e:
        logger.error(f"Erro ao listar categorias do nível {nivel} da classificação {classificacao} do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return [{"erro": str(e)}]

def obter_categoria(pesquisa: str, periodo: str, agregado: str, classificacao: str, nivel: str, categoria: str) -> Dict:
    """
    Obtém informações detalhadas de uma categoria específica
    
    Args:
        pesquisa: ID da pesquisa
        periodo: ID do período
        agregado: ID do agregado
        classificacao: ID da classificação
        nivel: ID do nível
        categoria: ID da categoria
    """
    cache_key = f"categoria_{pesquisa}_periodo_{periodo}_agregado_{agregado}_classificacao_{classificacao}_nivel_{nivel}_categoria_{categoria}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/pesquisas/{pesquisa}/periodos/{periodo}/agregados/{agregado}/classificacoes/{classificacao}/niveis/{nivel}/categorias/{categoria}"
        info_categoria = make_request(url)
        return save_to_cache(cache_key, info_categoria)
    except Exception as e:
        logger.error(f"Erro ao obter categoria {categoria} do nível {nivel} da classificação {classificacao} do agregado {agregado} da pesquisa {pesquisa} período {periodo}: {e}")
        return {"erro": str(e)}

def listar_dominios() -> List[Dict]:
    """Lista todos os domínios disponíveis"""
    cache_key = "dominios"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/dominios"
        dominios = make_request(url)
        return save_to_cache(cache_key, dominios)
    except Exception as e:
        logger.error(f"Erro ao listar domínios: {e}")
        return [{"erro": str(e)}]

def listar_variaveis() -> List[Dict]:
    """Lista todas as variáveis disponíveis"""
    cache_key = "variaveis"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/variaveis"
        variaveis = make_request(url)
        return save_to_cache(cache_key, variaveis)
    except Exception as e:
        logger.error(f"Erro ao listar variáveis: {e}")
        return [{"erro": str(e)}]

def listar_unidades_medida() -> List[Dict]:
    """Lista todas as unidades de medida disponíveis"""
    cache_key = "unidades_medida"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/unidades-medida"
        unidades = make_request(url)
        return save_to_cache(cache_key, unidades)
    except Exception as e:
        logger.error(f"Erro ao listar unidades de medida: {e}")
        return [{"erro": str(e)}]

def listar_conceitos() -> List[Dict]:
    """Lista todos os conceitos disponíveis"""
    cache_key = "conceitos"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_METADADOS}/conceitos"
        conceitos = make_request(url)
        return save_to_cache(cache_key, conceitos)
    except Exception as e:
        logger.error(f"Erro ao listar conceitos: {e}")
        return [{"erro": str(e)}]
