"""
Módulo para acesso à API de Malhas do IBGE
Documentação: https://servicodados.ibge.gov.br/api/docs/malhas
"""

from .ibge_base import *

def obter_malha(
    localidade: str, 
    resolucao: str = None, 
    formato: str = "application/vnd.geo+json", 
    qualidade: str = None
) -> Dict:
    """
    Obtém a malha de uma localidade
    
    Args:
        localidade: ID da localidade (BR para Brasil, UF para estados, etc.)
        resolucao: Resolução da malha (1, 2, 3, 4, 5)
        formato: Formato de saída (application/vnd.geo+json, application/json, application/vnd.google-earth.kml+xml, etc.)
        qualidade: Qualidade da malha (1, 2, 3, 4, 5)
    """
    cache_key = f"malha_localidade_{localidade}_resolucao_{resolucao}_formato_{formato}_qualidade_{qualidade}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_MALHAS}/{localidade}"
        
        params = {}
        if resolucao:
            params["resolucao"] = resolucao
        if formato:
            params["formato"] = formato
        if qualidade:
            params["qualidade"] = qualidade
        
        # Para malhas, precisamos usar o cliente httpx diretamente para lidar com diferentes formatos
        response = httpx.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        
        # O retorno depende do formato solicitado
        if formato == "application/vnd.geo+json" or formato == "application/json":
            resultado = response.json()
        else:
            # Para outros formatos, retornamos o conteúdo como string
            resultado = {"conteudo": response.text, "formato": formato}
        
        return save_to_cache(cache_key, resultado)
    except Exception as e:
        logger.error(f"Erro ao obter malha da localidade {localidade}: {e}")
        return {"erro": str(e)}

def obter_malha_por_ano(
    ano: str,
    localidade: str, 
    divisao: str = None,
    subdivisao: str = None,
    resolucao: str = None, 
    formato: str = "application/vnd.geo+json", 
    qualidade: str = None
) -> Dict:
    """
    Obtém a malha de uma localidade por ano específico
    
    Args:
        ano: Ano de referência da malha
        localidade: ID da localidade (BR para Brasil, UF para estados, etc.)
        divisao: Divisão territorial (municipio, mesorregiao, microrregiao, etc.)
        subdivisao: Subdivisão territorial
        resolucao: Resolução da malha (1, 2, 3, 4, 5)
        formato: Formato de saída (application/vnd.geo+json, application/json, application/vnd.google-earth.kml+xml, etc.)
        qualidade: Qualidade da malha (1, 2, 3, 4, 5)
    """
    cache_key = f"malha_ano_{ano}_localidade_{localidade}_divisao_{divisao}_subdivisao_{subdivisao}_resolucao_{resolucao}_formato_{formato}_qualidade_{qualidade}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        # Constrói a URL base
        url = f"{BASE_URL_MALHAS}/{ano}"
        
        # Adiciona localidade
        if localidade:
            url += f"/{localidade}"
        
        # Adiciona divisão
        if divisao:
            url += f"/{divisao}"
            
        # Adiciona subdivisão
        if subdivisao:
            url += f"/{subdivisao}"
        
        # Parâmetros
        params = {}
        if resolucao:
            params["resolucao"] = resolucao
        if formato:
            params["formato"] = formato
        if qualidade:
            params["qualidade"] = qualidade
        
        # Para malhas, precisamos usar o cliente httpx diretamente para lidar com diferentes formatos
        response = httpx.get(url, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        
        # O retorno depende do formato solicitado
        if formato == "application/vnd.geo+json" or formato == "application/json":
            resultado = response.json()
        else:
            # Para outros formatos, retornamos o conteúdo como string
            resultado = {"conteudo": response.text, "formato": formato}
        
        return save_to_cache(cache_key, resultado)
    except Exception as e:
        logger.error(f"Erro ao obter malha do ano {ano} para localidade {localidade}: {e}")
        return {"erro": str(e)}
