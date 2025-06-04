"""
Façade do domínio Agregados do IBGE.

Este módulo serve apenas como ponto de entrada padronizado para o domínio Agregados.

- Funções utilitárias de acesso à API: ibge_agregados_api.py
- Handlers MCP: ibge_agregados_handlers.py
- Logger e utilitários centralizados: logger.py, cache_utils.py, api_config.py

Importe as funções/handlers do módulo ibge_agregados_handlers.py.
"""

from .ibge_agregados_handlers import *

# O bloco abaixo estava fora de função/classe e causava erro de indentação.
# Se for uma função utilitária, deve estar dentro de uma função. Caso contrário, manter comentado.

# """
# Lista as localidades disponíveis para um agregado
# 
# Args:
#     id_agregado: ID do agregado
# """
# cache_key = f"localidades_agregado_{id_agregado}"
# cached_data = get_cached_data(cache_key)
# if cached_data:
#     return cached_data
# try:
#     url = f"{BASE_URL_AGREGADOS}/{id_agregado}/localidades"
#     localidades = make_request(url)
#     return save_to_cache(cache_key, localidades)
# except Exception as e:
#     logger.error(f"Erro ao listar localidades do agregado {id_agregado}: {e}")
#     return [{"erro": str(e)}]

def listar_niveis_territoriais_agregado(id_agregado: str) -> List[Dict]:
    """
    Lista os níveis territoriais disponíveis para um agregado
    
    Args:
        id_agregado: ID do agregado
    """
    cache_key = f"niveis_territoriais_agregado_{id_agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_AGREGADOS}/{id_agregado}/metadados/niveis"
        niveis = make_request(url)
        return save_to_cache(cache_key, niveis)
    except Exception as e:
        logger.error(f"Erro ao listar níveis territoriais do agregado {id_agregado}: {e}")
        return [{"erro": str(e)}]

def obter_metadados_agregado(id_agregado: str) -> Dict:
    """
    Obtém os metadados de um agregado
    
    Args:
        id_agregado: ID do agregado
    """
    cache_key = f"metadados_agregado_{id_agregado}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        url = f"{BASE_URL_AGREGADOS}/{id_agregado}/metadados"
        metadados = make_request(url)
        return save_to_cache(cache_key, metadados)
    except Exception as e:
        logger.error(f"Erro ao obter metadados do agregado {id_agregado}: {e}")
        return {"erro": str(e)}

def consultar_agregado(
    id_agregado: str, 
    variaveis: List[str], 
    localidades: List[str] = None,
    classificacoes: Dict[str, List[str]] = None,
    periodo: List[str] = None
) -> Dict:
    """
    Consulta os dados de um agregado
    
    Args:
        id_agregado: ID do agregado
        variaveis: Lista de IDs das variáveis
        localidades: Lista de IDs das localidades
        classificacoes: Dicionário com IDs das classificações e suas categorias
        periodo: Lista de períodos
    """
    # Constrói a chave de cache baseada nos parâmetros
    vars_str = "_".join(variaveis)
    locs_str = "_".join(localidades) if localidades else ""
    period_str = "_".join(periodo) if periodo else ""
    class_str = ""
    if classificacoes:
        for k, v in classificacoes.items():
            class_str += f"{k}_{'_'.join(v)}_"
    
    cache_key = f"consulta_agregado_{id_agregado}_vars_{vars_str}_locs_{locs_str}_period_{period_str}_class_{class_str}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        # Constrói a URL base
        url = f"{BASE_URL_AGREGADOS}/{id_agregado}/resultados"
        
        # Adiciona as variáveis
        vars_param = "/".join(variaveis)
        url += f"/{vars_param}"
        
        # Parâmetros da consulta
        params = {}
        
        # Adiciona as localidades se fornecidas
        if localidades:
            params["localidades"] = "|".join(localidades)
        
        # Adiciona as classificações se fornecidas
        if classificacoes:
            for classif_id, categorias in classificacoes.items():
                params[f"classificacao[{classif_id}]"] = "|".join(categorias)
        
        # Adiciona o período se fornecido
        if periodo:
            params["periodo"] = "|".join(periodo)
        
        # Faz a requisição
        resultado = make_request(url, params)
        return save_to_cache(cache_key, resultado)
    except Exception as e:
        logger.error(f"Erro ao consultar agregado {id_agregado}: {e}")
        return {"erro": str(e)}
