"""
Módulo para geração de relatórios completos sobre localidades (municípios, cidades, estados, regiões)
integrando dados de múltiplas fontes.
"""

import asyncio
import logging
import json
import os
import datetime
import re
from typing import Dict, List, Any, Optional, Union, Tuple
import argparse
from dateutil.relativedelta import relativedelta

# Importa os módulos de busca de dados
from .busca_localidade import buscar_info_localidade, normalizar_texto
from .transparencia import (
    listar_orgaos,
    buscar_auxilios_por_municipio,
    buscar_bolsa_familia_por_municipio,
    buscar_convenios_por_municipio,
    buscar_transferencias_por_municipio
)

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Diretório para armazenar relatórios
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "relatorios")
os.makedirs(REPORTS_DIR, exist_ok=True)

def calcular_periodo(periodo_tipo: str, data_referencia: Optional[datetime.datetime] = None, 
periodo_valor: Optional[str] = None) -> Tuple[datetime.datetime, datetime.datetime]:
    """
    Calcula o período (data inicial e final) com base no tipo de período e valor específico.
    
    Args:
        periodo_tipo: Tipo de período ('dia', 'mes', 'ano')
        data_referencia: Data de referência para o cálculo (padrão: data atual)
        periodo_valor: Valor específico do período (ex: '2023-06-15' para dia, '2023-06' para mês, '2023' para ano)
        
    Returns:
        Tupla contendo (data_inicial, data_final)
    """
    if data_referencia is None:
        data_referencia = datetime.datetime.now()
    
    # Verifica se foi fornecido um valor específico de período
    if periodo_valor:
        try:
            if periodo_tipo == 'dia' and len(periodo_valor) == 10:  # YYYY-MM-DD
                data = datetime.datetime.strptime(periodo_valor, "%Y-%m-%d")
                data_inicial = datetime.datetime(data.year, data.month, data.day, 0, 0, 0)
                data_final = data_inicial + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
                return data_inicial, data_final
            elif periodo_tipo == 'mes' and len(periodo_valor) == 7:  # YYYY-MM
                data = datetime.datetime.strptime(periodo_valor, "%Y-%m")
                data_inicial = datetime.datetime(data.year, data.month, 1, 0, 0, 0)
                if data.month == 12:
                    data_final = datetime.datetime(data.year + 1, 1, 1, 0, 0, 0) - datetime.timedelta(seconds=1)
                else:
                    data_final = datetime.datetime(data.year, data.month + 1, 1, 0, 0, 0) - datetime.timedelta(seconds=1)
                return data_inicial, data_final
            elif periodo_tipo == 'ano' and len(periodo_valor) == 4:  # YYYY
                ano = int(periodo_valor)
                data_inicial = datetime.datetime(ano, 1, 1, 0, 0, 0)
                data_final = datetime.datetime(ano + 1, 1, 1, 0, 0, 0) - datetime.timedelta(seconds=1)
                return data_inicial, data_final
        except (ValueError, TypeError):
            logging.warning(f"Formato de período inválido: {periodo_valor}. Usando período padrão.")
    
    # Cálculo padrão baseado no tipo de período
    if periodo_tipo == 'dia':
        data_inicial = datetime.datetime(data_referencia.year, data_referencia.month, data_referencia.day, 0, 0, 0)
        data_final = data_inicial + datetime.timedelta(days=1) - datetime.timedelta(seconds=1)
    elif periodo_tipo == 'mes':
        data_inicial = datetime.datetime(data_referencia.year, data_referencia.month, 1, 0, 0, 0)
        if data_referencia.month == 12:
            data_final = datetime.datetime(data_referencia.year + 1, 1, 1, 0, 0, 0) - datetime.timedelta(seconds=1)
        else:
            data_final = datetime.datetime(data_referencia.year, data_referencia.month + 1, 1, 0, 0, 0) - datetime.timedelta(seconds=1)
    elif periodo_tipo == 'ano':
        data_inicial = datetime.datetime(data_referencia.year, 1, 1, 0, 0, 0)
        data_final = datetime.datetime(data_referencia.year + 1, 1, 1, 0, 0, 0) - datetime.timedelta(seconds=1)
    else:  # Padrão: últimos 30 dias
        data_final = data_referencia.replace(hour=23, minute=59, second=59, microsecond=999999)
        data_inicial = data_final - datetime.timedelta(days=30)
    
    return data_inicial, data_final

def formatar_data_api(data: datetime.datetime) -> str:
    """
    Formata uma data para o formato esperado pelas APIs (YYYYMM ou YYYYMMDD).
    
    Args:
        data: Data a ser formatada
        
    Returns:
        String formatada para uso nas APIs
    """
    return data.strftime("%Y%m")

async def gerar_relatorio_municipio(nome_municipio: str, dados: Dict, periodo: str = 'mes') -> Dict:
    """
    Gera um relatório detalhado sobre um município.
    
    Args:
        nome_municipio: Nome do município
        dados: Dados básicos já coletados sobre o município
        
    Returns:
        Relatório completo sobre o município
    """
    municipio = dados["dados_basicos"]
    codigo_ibge = municipio["codigo"]
    
    relatorio = {
        "nome": municipio["nome"],
        "estado": municipio["uf"]["nome"],
        "sigla_estado": municipio["uf"]["sigla"],
        "codigo_ibge": codigo_ibge,
        "data_geracao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dados_demograficos": {},
        "dados_socioeconomicos": {},
        "indicadores": {},
        "auxilios_emergenciais": {},
        "bolsa_familia": {},
        "convenios": {},
        "transferencias": {},
        "estatisticas": {}
    }
    
    # Processa dados demográficos
    dados_demograficos = dados.get("dados_demograficos", {})
    if dados_demograficos:
        relatorio["dados_demograficos"] = dados_demograficos
    
    # Processa dados socioeconômicos
    dados_socioeconomicos = dados.get("dados_socioeconomicos", {})
    if dados_socioeconomicos:
        relatorio["dados_socioeconomicos"] = dados_socioeconomicos
    
    # Processa indicadores municipais
    indicadores = dados.get("indicadores", {})
    if indicadores:
        relatorio["indicadores"] = indicadores
    
    # Processa dados de auxílios emergenciais
    auxilios = dados.get("auxilios_emergenciais", {})
    if "data" in auxilios and auxilios["data"]:
        relatorio["auxilios_emergenciais"] = {
            "dados": auxilios["data"][:5],  # Limita a 5 registros
            "total_registros": auxilios.get("totalRegistros", len(auxilios["data"])),
            "resumo": {
                "total_beneficiarios": sum(item.get("quantidadeBeneficiados", 0) for item in auxilios["data"]),
                "total_valor": sum(item.get("valor", 0) for item in auxilios["data"]),
                "media_valor_por_beneficiario": sum(item.get("valor", 0) for item in auxilios["data"]) / 
                                               sum(item.get("quantidadeBeneficiados", 1) for item in auxilios["data"])
                                               if sum(item.get("quantidadeBeneficiados", 0) for item in auxilios["data"]) > 0 else 0
            }
        }
    
    # Processa dados de bolsa família
    bolsa_familia = dados.get("bolsa_familia", {})
    if "data" in bolsa_familia and bolsa_familia["data"]:
        relatorio["bolsa_familia"] = {
            "dados": bolsa_familia["data"][:5],  # Limita a 5 registros
            "total_registros": bolsa_familia.get("totalRegistros", len(bolsa_familia["data"])),
            "resumo": {
                "total_beneficiarios": sum(item.get("quantidadeBeneficiados", 0) for item in bolsa_familia["data"]),
                "total_valor": sum(item.get("valor", 0) for item in bolsa_familia["data"]),
                "media_valor_por_beneficiario": sum(item.get("valor", 0) for item in bolsa_familia["data"]) / 
                                               sum(item.get("quantidadeBeneficiados", 1) for item in bolsa_familia["data"])
                                               if sum(item.get("quantidadeBeneficiados", 0) for item in bolsa_familia["data"]) > 0 else 0
            }
        }
    
    # Processa dados de convênios
    convenios = dados.get("convenios", {})
    if "data" in convenios and convenios["data"]:
        relatorio["convenios"] = {
            "dados": convenios["data"][:5],  # Limita a 5 registros
            "total_registros": convenios.get("totalRegistros", len(convenios["data"])),
            "resumo": {
                "total_valor": sum(item.get("valor", 0) for item in convenios["data"]),
                "media_valor": sum(item.get("valor", 0) for item in convenios["data"]) / len(convenios["data"]) if convenios["data"] else 0
            }
        }
    
    # Processa dados de transferências
    transferencias = dados.get("transferencias", {})
    if "data" in transferencias and transferencias["data"]:
        relatorio["transferencias"] = {
            "dados": transferencias["data"][:5],  # Limita a 5 registros
            "total_registros": transferencias.get("totalRegistros", len(transferencias["data"])),
            "resumo": {
                "total_valor": sum(item.get("valor", 0) for item in transferencias["data"]),
                "media_valor": sum(item.get("valor", 0) for item in transferencias["data"]) / len(transferencias["data"]) if transferencias["data"] else 0
            }
        }
    
    # Calcula estatísticas gerais
    total_recursos = (
        relatorio.get("auxilios_emergenciais", {}).get("resumo", {}).get("total_valor", 0) +
        relatorio.get("bolsa_familia", {}).get("resumo", {}).get("total_valor", 0) +
        relatorio.get("convenios", {}).get("resumo", {}).get("total_valor", 0) +
        relatorio.get("transferencias", {}).get("resumo", {}).get("total_valor", 0)
    )
    
    relatorio["estatisticas"] = {
        "total_recursos_recebidos": total_recursos,
        "distribuicao_recursos": {
            "auxilios_emergenciais": relatorio.get("auxilios_emergenciais", {}).get("resumo", {}).get("total_valor", 0) / total_recursos if total_recursos > 0 else 0,
            "bolsa_familia": relatorio.get("bolsa_familia", {}).get("resumo", {}).get("total_valor", 0) / total_recursos if total_recursos > 0 else 0,
            "convenios": relatorio.get("convenios", {}).get("resumo", {}).get("total_valor", 0) / total_recursos if total_recursos > 0 else 0,
            "transferencias": relatorio.get("transferencias", {}).get("resumo", {}).get("total_valor", 0) / total_recursos if total_recursos > 0 else 0
        }
    }
    
    return relatorio

async def gerar_relatorio_estado(nome_estado: str, dados: Dict, periodo: str = 'mes') -> Dict:
    """
    Gera um relatório detalhado sobre um estado.
    
    Args:
        nome_estado: Nome do estado
        dados: Dados básicos já coletados sobre o estado
        
    Returns:
        Relatório completo sobre o estado
    """
    estado = dados["dados_basicos"]
    
    relatorio = {
        "nome": estado["nome"],
        "sigla": estado["sigla"],
        "codigo_ibge": estado["codigo"],
        "regiao": estado["regiao"]["nome"],
        "sigla_regiao": estado["regiao"]["sigla"],
        "data_geracao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dados_demograficos": {},
        "dados_socioeconomicos": {},
        "municipios": dados.get("municipios_relacionados", []),
        "total_municipios": dados.get("total_municipios", 0),
        "estatisticas": {}
    }
    
    # Processa dados demográficos
    dados_demograficos = dados.get("dados_demograficos", {})
    if dados_demograficos:
        relatorio["dados_demograficos"] = dados_demograficos
    
    # Processa dados socioeconômicos
    dados_socioeconomicos = dados.get("dados_socioeconomicos", {})
    if dados_socioeconomicos:
        relatorio["dados_socioeconomicos"] = dados_socioeconomicos
    
    # Amostra de municípios para análise mais detalhada (limita a 3 para não sobrecarregar)
    municipios_amostra = dados.get("municipios_relacionados", [])[:3]
    
    # Coleta dados detalhados para a amostra de municípios
    municipios_detalhados = []
    for municipio in municipios_amostra:
        try:
            info_municipio = await buscar_info_localidade(municipio["nome"])
            if info_municipio["tipo"] == "municipio":
                relatorio_municipio = await gerar_relatorio_municipio(municipio["nome"], info_municipio, periodo)
                municipios_detalhados.append(relatorio_municipio)
        except Exception as e:
            logger.error(f"Erro ao processar município {municipio['nome']}: {e}")
    
    relatorio["amostra_municipios"] = municipios_detalhados
    
    # Calcula estatísticas agregadas da amostra
    if municipios_detalhados:
        total_auxilios = sum(m.get("auxilios_emergenciais", {}).get("resumo", {}).get("total_valor", 0) for m in municipios_detalhados)
        total_bolsa = sum(m.get("bolsa_familia", {}).get("resumo", {}).get("total_valor", 0) for m in municipios_detalhados)
        total_convenios = sum(m.get("convenios", {}).get("resumo", {}).get("total_valor", 0) for m in municipios_detalhados)
        total_transferencias = sum(m.get("transferencias", {}).get("resumo", {}).get("total_valor", 0) for m in municipios_detalhados)
        
        relatorio["estatisticas"] = {
            "amostra": {
                "total_municipios_analisados": len(municipios_detalhados),
                "total_auxilios_emergenciais": total_auxilios,
                "total_bolsa_familia": total_bolsa,
                "total_convenios": total_convenios,
                "total_transferencias": total_transferencias,
                "total_recursos": total_auxilios + total_bolsa + total_convenios + total_transferencias,
                "media_recursos_por_municipio": (total_auxilios + total_bolsa + total_convenios + total_transferencias) / len(municipios_detalhados) if municipios_detalhados else 0
            }
        }
    
    return relatorio

async def gerar_relatorio_regiao(nome_regiao: str, dados: Dict, periodo: str = 'mes') -> Dict:
    """
    Gera um relatório detalhado sobre uma região.
    
    Args:
        nome_regiao: Nome da região
        dados: Dados básicos já coletados sobre a região
        
    Returns:
        Relatório completo sobre a região
    """
    regiao = dados["dados_basicos"]
    
    relatorio = {
        "nome": regiao["nome"],
        "sigla": regiao["sigla"],
        "codigo_ibge": regiao["codigo"],
        "data_geracao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dados_demograficos": {},
        "dados_socioeconomicos": {},
        "estados": dados.get("estados_relacionados", []),
        "total_estados": len(dados.get("estados_relacionados", [])),
        "estatisticas": {}
    }
    
    # Processa dados demográficos
    dados_demograficos = dados.get("dados_demograficos", {})
    if dados_demograficos:
        relatorio["dados_demograficos"] = dados_demograficos
    
    # Processa dados socioeconômicos
    dados_socioeconomicos = dados.get("dados_socioeconomicos", {})
    if dados_socioeconomicos:
        relatorio["dados_socioeconomicos"] = dados_socioeconomicos
    
    # Amostra de estados para análise mais detalhada (limita a 2 para não sobrecarregar)
    estados_amostra = dados.get("estados_relacionados", [])[:2]
    
    # Coleta dados detalhados para a amostra de estados
    estados_detalhados = []
    for estado in estados_amostra:
        try:
            info_estado = await buscar_info_localidade(estado["sigla"])
            if info_estado["tipo"] == "estado":
                relatorio_estado = await gerar_relatorio_estado(estado["nome"], info_estado, periodo)
                estados_detalhados.append(relatorio_estado)
        except Exception as e:
            logger.error(f"Erro ao processar estado {estado['nome']}: {e}")
    
    relatorio["amostra_estados"] = estados_detalhados
    
    # Calcula estatísticas agregadas da amostra
    if estados_detalhados:
        total_municipios = sum(e.get("total_municipios", 0) for e in estados_detalhados)
        
        relatorio["estatisticas"] = {
            "amostra": {
                "total_estados_analisados": len(estados_detalhados),
                "total_municipios": total_municipios,
                "media_municipios_por_estado": total_municipios / len(estados_detalhados) if estados_detalhados else 0
            }
        }
        
        # Agrega estatísticas de recursos se disponíveis
        if all("estatisticas" in e and "amostra" in e["estatisticas"] for e in estados_detalhados):
            total_recursos = sum(e["estatisticas"]["amostra"].get("total_recursos", 0) for e in estados_detalhados)
            relatorio["estatisticas"]["amostra"]["total_recursos"] = total_recursos
            relatorio["estatisticas"]["amostra"]["media_recursos_por_estado"] = total_recursos / len(estados_detalhados) if estados_detalhados else 0
    
    return relatorio

async def gerar_relatorio_completo(nome_localidade: str, periodo: str = 'mes', data_referencia: Optional[str] = None, 
periodo_valor: Optional[str] = None) -> Dict:
    """
    Gera um relatório completo sobre uma localidade, identificando automaticamente
    se é um município, estado ou região.
    
    Args:
        nome_localidade: Nome da localidade (município, cidade, estado ou região)
        periodo: Tipo de período para análise ('dia', 'semana', 'mes', 'trimestre', 'semestre', 'ano')
        data_referencia: Data de referência no formato 'YYYY-MM-DD' (padrão: data atual)
        
    Returns:
        Relatório completo sobre a localidade
    """
    # Converte a data de referência se fornecida
    data_ref = None
    if data_referencia:
        try:
            data_ref = datetime.datetime.strptime(data_referencia, "%Y-%m-%d")
        except ValueError:
            logger.warning(f"Formato de data inválido: {data_referencia}. Usando data atual.")
    
    # Calcula o período
    data_inicial, data_final = calcular_periodo(periodo, data_ref, periodo_valor)
    """
    Gera um relatório completo sobre uma localidade, identificando automaticamente
    se é um município, estado ou região.
    
    Args:
        nome_localidade: Nome da localidade (município, cidade, estado ou região)
        
    Returns:
        Relatório completo sobre a localidade
    """
    # Busca informações básicas sobre a localidade
    info_localidade = await buscar_info_localidade(nome_localidade)
    
    # Adiciona informações sobre o período ao relatório
    periodo_info = {
        "periodo": periodo,
        "data_inicial": data_inicial.strftime("%Y-%m-%d"),
        "data_final": data_final.strftime("%Y-%m-%d"),
        "data_referencia": data_ref.strftime("%Y-%m-%d") if data_ref else datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    if info_localidade["tipo"] == "municipio":
        relatorio = await gerar_relatorio_municipio(nome_localidade, info_localidade, periodo)
        relatorio["periodo_info"] = periodo_info
        return relatorio
    elif info_localidade["tipo"] == "estado":
        relatorio = await gerar_relatorio_estado(nome_localidade, info_localidade, periodo)
        relatorio["periodo_info"] = periodo_info
        return relatorio
    elif info_localidade["tipo"] == "regiao":
        relatorio = await gerar_relatorio_regiao(nome_localidade, info_localidade, periodo)
        relatorio["periodo_info"] = periodo_info
        return relatorio
    else:
        return {
            "erro": f"Não foi possível identificar a localidade: {nome_localidade}",
            "data_geracao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def formatar_valor_monetario(valor: float) -> str:
    """Formata um valor monetário em reais"""
    if not isinstance(valor, (int, float)):
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def exibir_relatorio_texto(relatorio: Dict) -> None:
    """
    Exibe o relatório em formato de texto.
    
    Args:
        relatorio: Relatório gerado
    """
    """
    Exibe o relatório em formato de texto.
    
    Args:
        relatorio: Relatório gerado
    """
    if "erro" in relatorio:
        print(f"\nERRO: {relatorio['erro']}")
        return
    
    print("\n" + "=" * 80)
    print(f"RELATÓRIO: {relatorio.get('nome', '')}")
    print("=" * 80)
    print(f"Data de geração: {relatorio.get('data_geracao', '')}")
    
    # Exibe informações do período
    if "periodo_info" in relatorio:
        periodo_info = relatorio["periodo_info"]
        print(f"\nPERÍODO DE ANÁLISE: {periodo_info['periodo'].upper()}")
        print(f"Data inicial: {periodo_info['data_inicial']}")
        print(f"Data final: {periodo_info['data_final']}")
        print(f"Data de referência: {periodo_info['data_referencia']}")
    
    if "sigla_estado" in relatorio:  # É um município
        print(f"\nMUNICÍPIO: {relatorio['nome']} - {relatorio['sigla_estado']}")
        print(f"Código IBGE: {relatorio.get('codigo_ibge', 'N/A')}")
        
        # Dados Demográficos
        if "dados_demograficos" in relatorio and relatorio["dados_demograficos"]:
            dados_demo = relatorio["dados_demograficos"]
            print("\nDADOS DEMOGRÁFICOS:")
            print(f"População total: {dados_demo.get('populacao_total', 'N/A'):,}".replace(",", ".") if isinstance(dados_demo.get('populacao_total'), (int, float)) else f"População total: {dados_demo.get('populacao_total', 'N/A')}")
            print(f"População urbana: {dados_demo.get('populacao_urbana', 'N/A'):,}".replace(",", ".") if isinstance(dados_demo.get('populacao_urbana'), (int, float)) else f"População urbana: {dados_demo.get('populacao_urbana', 'N/A')}")
            print(f"População rural: {dados_demo.get('populacao_rural', 'N/A'):,}".replace(",", ".") if isinstance(dados_demo.get('populacao_rural'), (int, float)) else f"População rural: {dados_demo.get('populacao_rural', 'N/A')}")
            print(f"Densidade demográfica: {dados_demo.get('densidade_demografica', 'N/A')} hab/km²")
            print(f"Área territorial: {dados_demo.get('area_territorial', 'N/A')} km²")
        
        # Dados Socioeconômicos
        # Dados Socioeconômicos
        if "dados_socioeconomicos" in relatorio and relatorio["dados_socioeconomicos"]:
            dados_socio = relatorio["dados_socioeconomicos"]
            print("\nDADOS SOCIOECONÔMICOS:")
            
            # PIB
            if "pib" in dados_socio and isinstance(dados_socio["pib"], dict):
                pib_data = dados_socio["pib"]
                print(f"PIB: {formatar_valor_monetario(pib_data.get('total', 0))}")
                print(f"PIB per capita: {formatar_valor_monetario(pib_data.get('per_capita', 0))}")
                if "ano_referencia" in pib_data:
                    print(f"Ano de referência (PIB): {pib_data.get('ano_referencia')}")
            else:
                # Compatibilidade com formato antigo
                print(f"PIB: {formatar_valor_monetario(dados_socio.get('pib', 0))}")
                print(f"PIB per capita: {formatar_valor_monetario(dados_socio.get('pib_per_capita', 0))}")
            
            # IDH
            if "idh" in dados_socio and isinstance(dados_socio["idh"], dict):
                idh_data = dados_socio["idh"]
                print(f"IDH: {idh_data.get('valor', 'N/A')}")
                if "classificacao" in idh_data:
                    print(f"Classificação IDH: {idh_data.get('classificacao')}")
                if "ano_referencia" in idh_data:
                    print(f"Ano de referência (IDH): {idh_data.get('ano_referencia')}")
            else:
                # Compatibilidade com formato antigo
                print(f"IDH: {dados_socio.get('idh', 'N/A')}")
            
            # Educação
            if "educacao" in dados_socio and isinstance(dados_socio["educacao"], dict):
                print("\nEducação:")
                for chave, valor in dados_socio["educacao"].items():
                    nome_formatado = chave.replace('_', ' ').title()
                    if isinstance(valor, (int, float)):
                        if "taxa" in chave.lower() or "percentual" in chave.lower():
                            print(f"- {nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"- {nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"- {nome_formatado}: {valor}")
            
            # Saúde
            if "saude" in dados_socio and isinstance(dados_socio["saude"], dict):
                print("\nSaúde:")
                for chave, valor in dados_socio["saude"].items():
                    nome_formatado = chave.replace('_', ' ').title()
                    if isinstance(valor, (int, float)):
                        if "taxa" in chave.lower() or "percentual" in chave.lower():
                            print(f"- {nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"- {nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"- {nome_formatado}: {valor}")
            
            # Outras informações
            for chave, valor in dados_socio.items():
                if chave not in ['pib', 'idh', 'educacao', 'saude', 'pib_per_capita']:
                    if isinstance(valor, dict):
                        print(f"\n{chave.replace('_', ' ').title()}:")
                        for sub_chave, sub_valor in valor.items():
                            sub_nome = sub_chave.replace('_', ' ').title()
                            if isinstance(sub_valor, (int, float)):
                                if "valor" in sub_chave.lower() or "total" in sub_chave.lower() or "pib" in sub_chave.lower():
                                    print(f"- {sub_nome}: {formatar_valor_monetario(sub_valor)}")
                                elif "percentual" in sub_chave.lower() or "taxa" in sub_chave.lower():
                                    print(f"- {sub_nome}: {sub_valor:.1f}%")
                                else:
                                    print(f"- {sub_nome}: {sub_valor:,}".replace(",", "."))
                            else:
                                print(f"- {sub_nome}: {sub_valor}")
                    elif isinstance(valor, (int, float)):
                        nome_formatado = chave.replace('_', ' ').title()
                        if "valor" in chave.lower() or "total" in chave.lower() or "pib" in chave.lower():
                            print(f"{nome_formatado}: {formatar_valor_monetario(valor)}")
                        elif "percentual" in chave.lower() or "taxa" in chave.lower():
                            print(f"{nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"{nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"{chave.replace('_', ' ').title()}: {valor}")
        
        # Indicadores Municipais
        if "indicadores" in relatorio and relatorio["indicadores"]:
            indicadores = relatorio["indicadores"]
            print("\nINDICADORES MUNICIPAIS:")
            
            # Exibe os indicadores disponíveis
            for categoria, dados in indicadores.items():
                print(f"\n{categoria.replace('_', ' ').upper()}:")
                if isinstance(dados, dict):
                    for chave, valor in dados.items():
                        if isinstance(valor, (int, float)) and 'valor' in chave.lower():
                            print(f"  {chave.replace('_', ' ').title()}: {formatar_valor_monetario(valor)}")
                        elif isinstance(valor, (int, float)) and 'percentual' in chave.lower():
                            print(f"  {chave.replace('_', ' ').title()}: {valor:.2f}%")
                        elif isinstance(valor, (int, float)):
                            print(f"  {chave.replace('_', ' ').title()}: {valor:,}".replace(",", "."))
                        else:
                            print(f"  {chave.replace('_', ' ').title()}: {valor}")
                else:
                    print(f"  {dados}")
        
        # Auxílios Emergenciais
        if "auxilios_emergenciais" in relatorio and "resumo" in relatorio["auxilios_emergenciais"]:
            resumo = relatorio["auxilios_emergenciais"]["resumo"]
            print("\nAUXÍLIOS EMERGENCIAIS:")
            print(f"Total de beneficiários: {resumo.get('total_beneficiarios', 0):,}".replace(",", "."))
            print(f"Total de recursos: {formatar_valor_monetario(resumo.get('total_valor', 0))}")
            print(f"Média por beneficiário: {formatar_valor_monetario(resumo.get('media_valor_por_beneficiario', 0))}")

        
        # Bolsa Família
        if "bolsa_familia" in relatorio and "resumo" in relatorio["bolsa_familia"]:
            resumo = relatorio["bolsa_familia"]["resumo"]
            print("\nBOLSA FAMÍLIA:")
            print(f"Total de beneficiários: {resumo.get('total_beneficiarios', 0):,}".replace(",", "."))
            print(f"Total de recursos: {formatar_valor_monetario(resumo.get('total_valor', 0))}")
            print(f"Média por beneficiário: {formatar_valor_monetario(resumo.get('media_valor_por_beneficiario', 0))}")
        
        # Convênios
        if "convenios" in relatorio and "resumo" in relatorio["convenios"]:
            resumo = relatorio["convenios"]["resumo"]
            print("\nCONVÊNIOS:")
            print(f"Total de registros: {relatorio['convenios'].get('total_registros', 0):,}".replace(",", "."))
            print(f"Total de recursos: {formatar_valor_monetario(resumo.get('total_valor', 0))}")
            print(f"Média por convênio: {formatar_valor_monetario(resumo.get('media_valor', 0))}")
        
        # Transferências
        if "transferencias" in relatorio and "resumo" in relatorio["transferencias"]:
            resumo = relatorio["transferencias"]["resumo"]
            print("\nTRANSFERÊNCIAS:")
            print(f"Total de registros: {relatorio['transferencias'].get('total_registros', 0):,}".replace(",", "."))
            print(f"Total de recursos: {formatar_valor_monetario(resumo.get('total_valor', 0))}")
            print(f"Média por transferência: {formatar_valor_monetario(resumo.get('media_valor', 0))}")
        
        # Estatísticas gerais
        if "estatisticas" in relatorio:
            print("\nESTATÍSTICAS GERAIS:")
            print(f"Total de recursos recebidos: {formatar_valor_monetario(relatorio['estatisticas'].get('total_recursos_recebidos', 0))}")
            
            if "distribuicao_recursos" in relatorio["estatisticas"]:
                dist = relatorio["estatisticas"]["distribuicao_recursos"]
                print("\nDistribuição de recursos:")
                print(f"- Auxílios Emergenciais: {dist.get('auxilios_emergenciais', 0)*100:.1f}%")
                print(f"- Bolsa Família: {dist.get('bolsa_familia', 0)*100:.1f}%")
                print(f"- Convênios: {dist.get('convenios', 0)*100:.1f}%")
                print(f"- Transferências: {dist.get('transferencias', 0)*100:.1f}%")
    
    elif "sigla" in relatorio and "regiao" in relatorio:  # É um estado
        print(f"\nESTADO: {relatorio['nome']} ({relatorio['sigla']})")
        print(f"Região: {relatorio['regiao']} ({relatorio['sigla_regiao']})")
        print(f"Código IBGE: {relatorio.get('codigo_ibge', 'N/A')}")
        print(f"Total de municípios: {relatorio.get('total_municipios', 0):,}".replace(",", "."))
        
        # Dados Demográficos
        if "dados_demograficos" in relatorio and relatorio["dados_demograficos"]:
            dados_demo = relatorio["dados_demograficos"]
            print("\nDADOS DEMOGRÁFICOS:")
            print(f"População total: {dados_demo.get('populacao_total', 'N/A'):,}".replace(",", ".") if isinstance(dados_demo.get('populacao_total'), (int, float)) else f"População total: {dados_demo.get('populacao_total', 'N/A')}")
            print(f"Densidade demográfica: {dados_demo.get('densidade_demografica', 'N/A')} hab/km²")
            print(f"Área territorial: {dados_demo.get('area_territorial', 'N/A')} km²")
            
            # Exibe distribuição por sexo se disponível
            if 'distribuicao_sexo' in dados_demo and isinstance(dados_demo['distribuicao_sexo'], dict):
                print("\nDistribuição por sexo:")
                dist_sexo = dados_demo['distribuicao_sexo']
                for sexo, valor in dist_sexo.items():
                    if isinstance(valor, (int, float)):
                        percentual = valor / dados_demo.get('populacao_total', 1) * 100 if dados_demo.get('populacao_total') else 0
                        print(f"- {sexo.title()}: {valor:,} ({percentual:.1f}%)".replace(",", "."))
                    else:
                        print(f"- {sexo.title()}: {valor}")
        
        # Dados Socioeconômicos
        # Dados Socioeconômicos
        if "dados_socioeconomicos" in relatorio and relatorio["dados_socioeconomicos"]:
            dados_socio = relatorio["dados_socioeconomicos"]
            print("\nDADOS SOCIOECONÔMICOS:")
            
            # PIB
            if "pib" in dados_socio and isinstance(dados_socio["pib"], dict):
                pib_data = dados_socio["pib"]
                print(f"PIB: {formatar_valor_monetario(pib_data.get('total', 0))}")
                print(f"PIB per capita: {formatar_valor_monetario(pib_data.get('per_capita', 0))}")
                if "ano_referencia" in pib_data:
                    print(f"Ano de referência (PIB): {pib_data.get('ano_referencia')}")
            else:
                # Compatibilidade com formato antigo
                print(f"PIB: {formatar_valor_monetario(dados_socio.get('pib', 0))}")
                print(f"PIB per capita: {formatar_valor_monetario(dados_socio.get('pib_per_capita', 0))}")
            
            # IDH
            if "idh" in dados_socio and isinstance(dados_socio["idh"], dict):
                idh_data = dados_socio["idh"]
                print(f"IDH: {idh_data.get('valor', 'N/A')}")
                if "classificacao" in idh_data:
                    print(f"Classificação IDH: {idh_data.get('classificacao')}")
                if "ano_referencia" in idh_data:
                    print(f"Ano de referência (IDH): {idh_data.get('ano_referencia')}")
            else:
                # Compatibilidade com formato antigo
                print(f"IDH: {dados_socio.get('idh', 'N/A')}")
            
            # Educação
            if "educacao" in dados_socio and isinstance(dados_socio["educacao"], dict):
                print("\nEducação:")
                for chave, valor in dados_socio["educacao"].items():
                    nome_formatado = chave.replace('_', ' ').title()
                    if isinstance(valor, (int, float)):
                        if "taxa" in chave.lower() or "percentual" in chave.lower():
                            print(f"- {nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"- {nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"- {nome_formatado}: {valor}")
            
            # Saúde
            if "saude" in dados_socio and isinstance(dados_socio["saude"], dict):
                print("\nSaúde:")
                for chave, valor in dados_socio["saude"].items():
                    nome_formatado = chave.replace('_', ' ').title()
                    if isinstance(valor, (int, float)):
                        if "taxa" in chave.lower() or "percentual" in chave.lower():
                            print(f"- {nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"- {nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"- {nome_formatado}: {valor}")
            
            # Outras informações
            for chave, valor in dados_socio.items():
                if chave not in ['pib', 'idh', 'educacao', 'saude', 'pib_per_capita']:
                    if isinstance(valor, dict):
                        print(f"\n{chave.replace('_', ' ').title()}:")
                        for sub_chave, sub_valor in valor.items():
                            sub_nome = sub_chave.replace('_', ' ').title()
                            if isinstance(sub_valor, (int, float)):
                                if "valor" in sub_chave.lower() or "total" in sub_chave.lower() or "pib" in sub_chave.lower():
                                    print(f"- {sub_nome}: {formatar_valor_monetario(sub_valor)}")
                                elif "percentual" in sub_chave.lower() or "taxa" in sub_chave.lower():
                                    print(f"- {sub_nome}: {sub_valor:.1f}%")
                                else:
                                    print(f"- {sub_nome}: {sub_valor:,}".replace(",", "."))
                            else:
                                print(f"- {sub_nome}: {sub_valor}")
                    elif isinstance(valor, (int, float)):
                        nome_formatado = chave.replace('_', ' ').title()
                        if "valor" in chave.lower() or "total" in chave.lower() or "pib" in chave.lower():
                            print(f"{nome_formatado}: {formatar_valor_monetario(valor)}")
                        elif "percentual" in chave.lower() or "taxa" in chave.lower():
                            print(f"{nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"{nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"{chave.replace('_', ' ').title()}: {valor}")
        
        # Estatísticas da amostra
        if "estatisticas" in relatorio and "amostra" in relatorio["estatisticas"]:
            amostra = relatorio["estatisticas"]["amostra"]
            print(f"\nESTATÍSTICAS (baseadas em amostra de {amostra.get('total_municipios_analisados', 0)} municípios):")
            print(f"Total de recursos: {formatar_valor_monetario(amostra.get('total_recursos', 0))}")
            print(f"Média de recursos por município: {formatar_valor_monetario(amostra.get('media_recursos_por_municipio', 0))}")
            print("\nDistribuição por programa:")
            print(f"- Auxílios Emergenciais: {formatar_valor_monetario(amostra.get('total_auxilios_emergenciais', 0))}")
            print(f"- Bolsa Família: {formatar_valor_monetario(amostra.get('total_bolsa_familia', 0))}")
            print(f"- Convênios: {formatar_valor_monetario(amostra.get('total_convenios', 0))}")
            print(f"- Transferências: {formatar_valor_monetario(amostra.get('total_transferencias', 0))}")

    
    elif "sigla" in relatorio and "codigo_ibge" in relatorio:  # É uma região
        print(f"\nREGIÃO: {relatorio['nome']} ({relatorio['sigla']})")
        print(f"Código IBGE: {relatorio.get('codigo_ibge', 'N/A')}")
        print(f"Total de estados: {relatorio.get('total_estados', 0)}")
        
        # Dados Demográficos
        if "dados_demograficos" in relatorio and relatorio["dados_demograficos"]:
            dados_demo = relatorio["dados_demograficos"]
            print("\nDADOS DEMOGRÁFICOS:")
            print(f"População total: {dados_demo.get('populacao_total', 'N/A'):,}".replace(",", ".") if isinstance(dados_demo.get('populacao_total'), (int, float)) else f"População total: {dados_demo.get('populacao_total', 'N/A')}")
            print(f"Densidade demográfica: {dados_demo.get('densidade_demografica', 'N/A')} hab/km²")
            print(f"Área territorial: {dados_demo.get('area_territorial', 'N/A')} km²")
            
            # Exibe distribuição por sexo se disponível
            if 'distribuicao_sexo' in dados_demo and isinstance(dados_demo['distribuicao_sexo'], dict):
                print("\nDistribuição por sexo:")
                dist_sexo = dados_demo['distribuicao_sexo']
                for sexo, valor in dist_sexo.items():
                    if isinstance(valor, (int, float)):
                        percentual = valor / dados_demo.get('populacao_total', 1) * 100 if dados_demo.get('populacao_total') else 0
                        print(f"- {sexo.title()}: {valor:,} ({percentual:.1f}%)".replace(",", "."))
                    else:
                        print(f"- {sexo.title()}: {valor}")
        
        # Dados Socioeconômicos
        # Dados Socioeconômicos
        if "dados_socioeconomicos" in relatorio and relatorio["dados_socioeconomicos"]:
            dados_socio = relatorio["dados_socioeconomicos"]
            print("\nDADOS SOCIOECONÔMICOS:")
            
            # PIB
            if "pib" in dados_socio and isinstance(dados_socio["pib"], dict):
                pib_data = dados_socio["pib"]
                print(f"PIB: {formatar_valor_monetario(pib_data.get('total', 0))}")
                print(f"PIB per capita: {formatar_valor_monetario(pib_data.get('per_capita', 0))}")
                if "ano_referencia" in pib_data:
                    print(f"Ano de referência (PIB): {pib_data.get('ano_referencia')}")
            else:
                # Compatibilidade com formato antigo
                print(f"PIB: {formatar_valor_monetario(dados_socio.get('pib', 0))}")
                print(f"PIB per capita: {formatar_valor_monetario(dados_socio.get('pib_per_capita', 0))}")
            
            # IDH
            if "idh" in dados_socio and isinstance(dados_socio["idh"], dict):
                idh_data = dados_socio["idh"]
                print(f"IDH médio: {idh_data.get('valor', 'N/A')}")
                if "classificacao" in idh_data:
                    print(f"Classificação IDH: {idh_data.get('classificacao')}")
                if "ano_referencia" in idh_data:
                    print(f"Ano de referência (IDH): {idh_data.get('ano_referencia')}")
            else:
                # Compatibilidade com formato antigo
                print(f"IDH médio: {dados_socio.get('idh_medio', 'N/A')}")
            
            # Educação
            if "educacao" in dados_socio and isinstance(dados_socio["educacao"], dict):
                print("\nEducação:")
                for chave, valor in dados_socio["educacao"].items():
                    nome_formatado = chave.replace('_', ' ').title()
                    if isinstance(valor, (int, float)):
                        if "taxa" in chave.lower() or "percentual" in chave.lower():
                            print(f"- {nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"- {nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"- {nome_formatado}: {valor}")
            
            # Saúde
            if "saude" in dados_socio and isinstance(dados_socio["saude"], dict):
                print("\nSaúde:")
                for chave, valor in dados_socio["saude"].items():
                    nome_formatado = chave.replace('_', ' ').title()
                    if isinstance(valor, (int, float)):
                        if "taxa" in chave.lower() or "percentual" in chave.lower():
                            print(f"- {nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"- {nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"- {nome_formatado}: {valor}")
            
            # Outras informações
            for chave, valor in dados_socio.items():
                if chave not in ['pib', 'idh', 'educacao', 'saude', 'pib_per_capita', 'idh_medio']:
                    if isinstance(valor, dict):
                        print(f"\n{chave.replace('_', ' ').title()}:")
                        for sub_chave, sub_valor in valor.items():
                            sub_nome = sub_chave.replace('_', ' ').title()
                            if isinstance(sub_valor, (int, float)):
                                if "valor" in sub_chave.lower() or "total" in sub_chave.lower() or "pib" in sub_chave.lower():
                                    print(f"- {sub_nome}: {formatar_valor_monetario(sub_valor)}")
                                elif "percentual" in sub_chave.lower() or "taxa" in sub_chave.lower():
                                    print(f"- {sub_nome}: {sub_valor:.1f}%")
                                else:
                                    print(f"- {sub_nome}: {sub_valor:,}".replace(",", "."))
                            else:
                                print(f"- {sub_nome}: {sub_valor}")
                    elif isinstance(valor, (int, float)):
                        nome_formatado = chave.replace('_', ' ').title()
                        if "valor" in chave.lower() or "total" in chave.lower() or "pib" in chave.lower():
                            print(f"{nome_formatado}: {formatar_valor_monetario(valor)}")
                        elif "percentual" in chave.lower() or "taxa" in chave.lower():
                            print(f"{nome_formatado}: {valor:.1f}%")
                        else:
                            print(f"{nome_formatado}: {valor:,}".replace(",", "."))
                    else:
                        print(f"{chave.replace('_', ' ').title()}: {valor}")
        
        # Lista estados
        if "estados" in relatorio:
            print("\nEstados:")
            for estado in relatorio["estados"]:
                print(f"- {estado['nome']} ({estado['sigla']})")
        
        # Estatísticas da amostra
        if "estatisticas" in relatorio and "amostra" in relatorio["estatisticas"]:
            amostra = relatorio["estatisticas"]["amostra"]
            print(f"\nESTATÍSTICAS (baseadas em amostra de {amostra.get('total_estados_analisados', 0)} estados):")
            print(f"Total de municípios: {amostra.get('total_municipios', 0):,}".replace(",", "."))
            print(f"Média de municípios por estado: {amostra.get('media_municipios_por_estado', 0):.1f}")

            
            if "total_recursos" in amostra:
                print(f"Total de recursos: {formatar_valor_monetario(amostra.get('total_recursos', 0))}")
                print(f"Média de recursos por estado: {formatar_valor_monetario(amostra.get('media_recursos_por_estado', 0))}")
    
    print("\n" + "=" * 80)

async def main(nome_localidade: str, formato: str = "texto", salvar: bool = True, periodo: str = "mes", 
data_referencia: Optional[str] = None, periodo_valor: Optional[str] = None):
    """
    Função principal para uso direto do módulo.
    Gera e exibe um relatório completo sobre uma localidade.
    
    Args:
        nome_localidade: Nome da localidade (município, cidade, estado ou região)
        formato: Formato de saída ("texto" ou "json")
        salvar: Se True, salva o relatório em arquivo
        periodo: Tipo de período para análise ('dia', 'semana', 'mes', 'trimestre', 'semestre', 'ano')
        data_referencia: Data de referência no formato 'YYYY-MM-DD' (padrão: data atual)
    """
    """
    Função principal para uso direto do módulo.
    Gera e exibe um relatório completo sobre uma localidade.
    
    Args:
        nome_localidade: Nome da localidade (município, cidade, estado ou região)
        formato: Formato de saída ("texto" ou "json")
        salvar: Se True, salva o relatório em arquivo
    """
    print(f"\nGerando relatório para: {nome_localidade}")
    print(f"Período: {periodo.upper()}")
    if data_referencia:
        print(f"Data de referência: {data_referencia}")
    print("Isso pode levar alguns minutos, dependendo da localidade...")
    
    relatorio = await gerar_relatorio_completo(nome_localidade, periodo, data_referencia, periodo_valor)
    
    if formato == "texto":
        exibir_relatorio_texto(relatorio)
    else:
        print(json.dumps(relatorio, indent=2, ensure_ascii=False))
    
    if salvar:
        # Cria um nome de arquivo baseado na localidade e data
        # Remove caracteres especiais que podem causar problemas em nomes de arquivos
        nome_arquivo = re.sub(r'[\\/*?:"<>|]', '_', normalizar_texto(nome_localidade))
        nome_arquivo = f"{nome_arquivo.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if formato == "texto":
            # Salva em formato de texto
            arquivo_txt = os.path.join(REPORTS_DIR, f"{nome_arquivo}.txt")
            with open(arquivo_txt, 'w', encoding='utf-8') as f:
                # Redireciona a saída da função para o arquivo
                import sys
                original_stdout = sys.stdout
                sys.stdout = f
                exibir_relatorio_texto(relatorio)
                sys.stdout = original_stdout
            print(f"\nRelatório salvo em: {arquivo_txt}")
        else:
            # Salva em formato JSON
            arquivo_json = os.path.join(REPORTS_DIR, f"{nome_arquivo}.json")
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            print(f"\nRelatório salvo em: {arquivo_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera relatórios sobre localidades")
    parser.add_argument("localidade", help="Nome da localidade (município, cidade, estado ou região)")
    parser.add_argument("--formato", choices=["texto", "json"], default="texto", help="Formato de saída (texto ou json)")
    parser.add_argument("--no-save", action="store_true", help="Não salvar o relatório em arquivo")
    parser.add_argument("--periodo", choices=["dia", "mes", "ano"], default="mes", 
                        help="Tipo de período para análise (dia, mes, ano)")
    parser.add_argument("--data", help="Data de referência no formato YYYY-MM-DD (padrão: data atual)")
    parser.add_argument("--periodo-valor", help="Valor específico do período: YYYY-MM-DD para dia, YYYY-MM para mês, YYYY para ano")
    
    args = parser.parse_args()
    
    asyncio.run(main(args.localidade, args.formato, not args.no_save, args.periodo, args.data, args.periodo_valor))
