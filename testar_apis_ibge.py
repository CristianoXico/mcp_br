"""
Script para testar todas as APIs do IBGE implementadas
"""

import json
import logging
import os
import sys
from time import sleep

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa todas as APIs
from tools.ibge_localidades import (
    listar_regioes, listar_estados, listar_mesorregioes, listar_microrregioes,
    listar_municipios, buscar_municipio_por_codigo, buscar_municipio_por_nome,
    listar_distritos, listar_subdistritos, buscar_area_territorial
)

from tools.ibge_agregados import (
    listar_agregados, obter_agregado_por_id, listar_periodos_agregado,
    listar_variaveis_agregado, listar_localidades_agregado,
    listar_niveis_territoriais_agregado, obter_metadados_agregado,
    consultar_agregado
)

from tools.ibge_malhas import (
    obter_malha, obter_malha_por_ano
)

from tools.ibge_metadados import (
    listar_fontes, listar_pesquisas, listar_periodos_pesquisa,
    obter_metadados_pesquisa_periodo, listar_agregados_pesquisa_periodo,
    obter_agregado, listar_variaveis_agregado as listar_variaveis_agregado_metadados, obter_variavel,
    listar_classificacoes_agregado, listar_niveis_classificacao,
    listar_categorias_nivel, obter_categoria, listar_dominios,
    listar_variaveis, listar_unidades_medida, listar_conceitos
)

from tools.ibge_cnae import (
    listar_secoes, obter_secao, listar_divisoes, obter_divisao,
    listar_grupos, obter_grupo, listar_classes, obter_classe,
    listar_subclasses, obter_subclasse, pesquisar_cnae
)

from tools.ibge_censos import (
    obter_area_territorial, obter_populacao,
    calcular_densidade_demografica, obter_indicadores_demograficos
)

from tools.ibge_nomes import (
    pesquisar_nomes, ranking_nomes, frequencia_nome
)

from tools.ibge_censos import (
    obter_area_territorial as censo_obter_area_territorial,
    obter_populacao, calcular_densidade_demografica,
    obter_indicadores_demograficos
)

# Importa as novas APIs implementadas
from tools.ibge_bdg import (
    listar_estacoes, obter_estacao, 
    listar_estacoes_por_uf as bdg_listar_estacoes_por_uf,
    listar_estacoes_por_municipio as bdg_listar_estacoes_por_municipio,
    listar_estacoes_por_tipo as bdg_listar_estacoes_por_tipo,
    listar_tipos_estacoes as bdg_listar_tipos_estacoes
)

from tools.ibge_bngb import (
    pesquisar_nomes_geograficos, obter_nome_geografico,
    listar_nomes_geograficos_por_uf as listar_nomes_por_uf, 
    listar_nomes_geograficos_por_municipio as listar_nomes_por_municipio,
    listar_nomes_geograficos_por_tipo as listar_nomes_por_tipo, 
    listar_tipos_nomes_geograficos as listar_tipos_nomes
)

from tools.ibge_calendario import (
    listar_eventos as listar_eventos_calendario, 
    obter_evento as obter_evento_calendario,
    listar_eventos_por_tipo as calendario_listar_eventos_por_tipo,
    listar_eventos_por_produto, 
    listar_tipos_eventos as listar_tipos_eventos_calendario
)

from tools.ibge_hgeohnor import (
    listar_estacoes as listar_estacoes_raap, 
    obter_estacao as obter_estacao_raap,
    listar_estacoes_por_uf as hgeohnor_listar_estacoes_por_uf,
    listar_estacoes_por_municipio as hgeohnor_listar_estacoes_por_municipio,
    listar_estacoes_por_tipo as hgeohnor_listar_estacoes_por_tipo,
    listar_tipos_estacoes as hgeohnor_listar_tipos_estacoes
)

from tools.ibge_noticias import (
    listar_noticias, obter_noticia,
    listar_noticias_por_tipo, listar_noticias_por_produto,
    pesquisar_noticias, listar_tipos_noticias
)

from tools.ibge_paises import (
    listar_paises, obter_pais, listar_paises_por_continente,
    listar_paises_por_bloco, listar_continentes, obter_continente,
    listar_blocos, obter_bloco
)

from tools.ibge_pesquisas import (
    listar_pesquisas, obter_pesquisa, listar_periodos_pesquisa,
    obter_periodo_pesquisa, listar_resultados_pesquisa, obter_resultado_pesquisa,
    listar_indicadores_pesquisa, obter_indicador_pesquisa
)

from tools.ibge_ppp import (
    listar_processamentos as listar_processamentos_ppp, 
    obter_processamento as obter_processamento_ppp,
    listar_processamentos_por_status, listar_processamentos_por_usuario,
    listar_status_processamentos, obter_resultado_processamento
)

from tools.ibge_produtos import (
    listar_produtos, obter_produto, listar_produtos_por_tipo,
    listar_produtos_por_tema, listar_tipos_produtos, obter_tipo_produto,
    listar_temas_produtos, obter_tema_produto
)

from tools.ibge_progrid import (
    listar_celulas, obter_celula, listar_celulas_por_nivel,
    listar_celulas_por_uf, listar_celulas_por_municipio,
    listar_niveis_progrid, obter_nivel_progrid
)

from tools.ibge_publicacoes import (
    listar_publicacoes, obter_publicacao, listar_publicacoes_por_tipo,
    listar_publicacoes_por_tema, pesquisar_publicacoes,
    listar_tipos_publicacoes, listar_temas_publicacoes
)

from tools.ibge_rbmc import (
    listar_estacoes, obter_estacao, listar_estacoes_por_uf,
    listar_estacoes_por_municipio, listar_estacoes_por_tipo,
    listar_tipos_estacoes, listar_arquivos_estacao, obter_arquivo_estacao
)

from tools.ibge_rmpg import (
    listar_estacoes as listar_estacoes_rmpg,
    obter_estacao as obter_estacao_rmpg,
    listar_estacoes_por_uf as listar_estacoes_por_uf_rmpg,
    listar_estacoes_por_municipio as listar_estacoes_por_municipio_rmpg,
    listar_estacoes_por_status, listar_status_estacoes,
    listar_dados_estacao, obter_dado_estacao
)

def salvar_resultado(nome_teste, resultado):
    """Salva o resultado do teste em um arquivo JSON"""
    diretorio = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados_testes')
    os.makedirs(diretorio, exist_ok=True)
    
    caminho_arquivo = os.path.join(diretorio, f"{nome_teste}.json")
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Resultado do teste '{nome_teste}' salvo em {caminho_arquivo}")

def testar_api_localidades():
    """Testa a API de Localidades"""
    logger.info("Testando API de Localidades...")
    
    # Testa listar regiões
    logger.info("Testando listar_regioes()...")
    regioes = listar_regioes()
    salvar_resultado("localidades_regioes", regioes)
    
    # Testa listar estados
    logger.info("Testando listar_estados()...")
    estados = listar_estados()
    salvar_resultado("localidades_estados", estados)
    
    # Testa listar estados de uma região específica
    if regioes and len(regioes) > 0 and isinstance(regioes[0], dict) and "id" in regioes[0]:
        regiao_id = regioes[0]["id"]
        logger.info(f"Testando listar_estados(regiao={regiao_id})...")
        estados_regiao = listar_estados(regiao=regiao_id)
        salvar_resultado(f"localidades_estados_regiao_{regiao_id}", estados_regiao)
    
    # Testa listar mesorregiões
    logger.info("Testando listar_mesorregioes()...")
    mesorregioes = listar_mesorregioes()
    salvar_resultado("localidades_mesorregioes", mesorregioes)
    
    # Testa listar microrregiões
    logger.info("Testando listar_microrregioes()...")
    microrregioes = listar_microrregioes()
    salvar_resultado("localidades_microrregioes", microrregioes)
    
    # Testa listar municípios
    logger.info("Testando listar_municipios()...")
    municipios = listar_municipios()
    salvar_resultado("localidades_municipios", municipios)
    
    # Testa buscar município por código
    if municipios and len(municipios) > 0 and isinstance(municipios[0], dict) and "id" in municipios[0]:
        municipio_id = str(municipios[0]["id"])
        logger.info(f"Testando buscar_municipio_por_codigo(codigo_municipio={municipio_id})...")
        municipio = buscar_municipio_por_codigo(codigo_municipio=municipio_id)
        salvar_resultado(f"localidades_municipio_{municipio_id}", municipio)
    
    # Testa buscar município por nome
    if municipios and len(municipios) > 0 and isinstance(municipios[0], dict) and "nome" in municipios[0]:
        municipio_nome = municipios[0]["nome"]
        logger.info(f"Testando buscar_municipio_por_nome(nome_municipio='{municipio_nome}')...")
        municipio = buscar_municipio_por_nome(nome_municipio=municipio_nome)
        salvar_resultado(f"localidades_municipio_nome_{municipio_nome}", municipio)
    
    # Testa listar distritos
    logger.info("Testando listar_distritos()...")
    distritos = listar_distritos()
    salvar_resultado("localidades_distritos", distritos)
    
    # Testa listar subdistritos
    logger.info("Testando listar_subdistritos()...")
    subdistritos = listar_subdistritos()
    salvar_resultado("localidades_subdistritos", subdistritos)
    
    # Testa buscar área territorial
    if municipios and len(municipios) > 0 and isinstance(municipios[0], dict) and "id" in municipios[0]:
        municipio_id = str(municipios[0]["id"])
        logger.info(f"Testando buscar_area_territorial(codigo_municipio={municipio_id})...")
        area = buscar_area_territorial(codigo_municipio=municipio_id)
        salvar_resultado(f"localidades_area_territorial_{municipio_id}", area)

def testar_api_agregados():
    """Testa a API de Agregados"""
    logger.info("Testando API de Agregados...")
    
    # Testa listar agregados
    logger.info("Testando listar_agregados()...")
    agregados = listar_agregados()
    salvar_resultado("agregados_lista", agregados)
    
    # Testa obter agregado por ID
    if agregados and len(agregados) > 0 and isinstance(agregados[0], dict) and "id" in agregados[0]:
        agregado_id = agregados[0]["id"]
        logger.info(f"Testando obter_agregado_por_id(id_agregado='{agregado_id}')...")
        agregado = obter_agregado_por_id(id_agregado=agregado_id)
        salvar_resultado(f"agregados_detalhe_{agregado_id}", agregado)
        
        # Testa listar períodos do agregado
        logger.info(f"Testando listar_periodos_agregado(id_agregado='{agregado_id}')...")
        periodos = listar_periodos_agregado(id_agregado=agregado_id)
        salvar_resultado(f"agregados_periodos_{agregado_id}", periodos)
        
        # Testa listar variáveis do agregado
        logger.info(f"Testando listar_variaveis_agregado(id_agregado='{agregado_id}')...")
        variaveis = listar_variaveis_agregado(agregado_id)
        salvar_resultado(f"agregados_variaveis_{agregado_id}", variaveis)
        
        # Testa listar localidades do agregado
        logger.info(f"Testando listar_localidades_agregado(id_agregado='{agregado_id}')...")
        localidades = listar_localidades_agregado(agregado_id)
        salvar_resultado(f"agregados_localidades_{agregado_id}", localidades)
        
        # Testa listar níveis territoriais do agregado
        logger.info(f"Testando listar_niveis_territoriais_agregado(id_agregado='{agregado_id}')...")
        niveis = listar_niveis_territoriais_agregado(agregado_id)
        salvar_resultado(f"agregados_niveis_territoriais_{agregado_id}", niveis)
        
        # Testa obter metadados do agregado
        logger.info(f"Testando obter_metadados_agregado(id_agregado='{agregado_id}')...")
        metadados = obter_metadados_agregado(agregado_id)
        salvar_resultado(f"agregados_metadados_{agregado_id}", metadados)
        
        # Testa consultar agregado
        if variaveis and len(variaveis) > 0 and isinstance(variaveis[0], dict) and "id" in variaveis[0]:
            variavel_id = str(variaveis[0]["id"])
            logger.info(f"Testando consultar_agregado(id_agregado='{agregado_id}', variaveis=['{variavel_id}'])...")
            consulta = consultar_agregado(id_agregado=agregado_id, variaveis=[variavel_id])
            salvar_resultado(f"agregados_consulta_{agregado_id}_{variavel_id}", consulta)

def testar_api_malhas():
    """Testa a API de Malhas"""
    logger.info("Testando API de Malhas...")
    
    # Testa obter malha do Brasil
    logger.info("Testando obter_malha(localidade='BR')...")
    malha_br = obter_malha(localidade='BR')
    salvar_resultado("malhas_brasil", malha_br)
    
    # Testa obter malha por ano
    logger.info("Testando obter_malha_por_ano(ano='2020', localidade='BR')...")
    malha_br_2020 = obter_malha_por_ano(ano='2020', localidade='BR')
    salvar_resultado("malhas_brasil_2020", malha_br_2020)

def testar_api_metadados():
    """Testa a API de Metadados Estatísticos"""
    logger.info("Testando API de Metadados Estatísticos...")
    
    # Testa listar fontes
    logger.info("Testando listar_fontes()...")
    fontes = listar_fontes()
    salvar_resultado("metadados_fontes", fontes)
    
    # Testa listar pesquisas
    logger.info("Testando listar_pesquisas()...")
    pesquisas = listar_pesquisas()
    salvar_resultado("metadados_pesquisas", pesquisas)
    
    # Testa listar períodos de uma pesquisa
    if pesquisas and len(pesquisas) > 0 and isinstance(pesquisas[0], dict) and "id" in pesquisas[0]:
        pesquisa_id = pesquisas[0]["id"]
        logger.info(f"Testando listar_periodos_pesquisa(pesquisa='{pesquisa_id}')...")
        periodos = listar_periodos_pesquisa(pesquisa=pesquisa_id)
        salvar_resultado(f"metadados_periodos_pesquisa_{pesquisa_id}", periodos)
        
        # Testa obter metadados de uma pesquisa para um período
        if periodos and len(periodos) > 0 and isinstance(periodos[0], dict) and "id" in periodos[0]:
            periodo_id = periodos[0]["id"]
            logger.info(f"Testando obter_metadados_pesquisa_periodo(pesquisa='{pesquisa_id}', periodo='{periodo_id}')...")
            metadados = obter_metadados_pesquisa_periodo(pesquisa=pesquisa_id, periodo=periodo_id)
            salvar_resultado(f"metadados_pesquisa_{pesquisa_id}_periodo_{periodo_id}", metadados)
            
            # Testa listar agregados de uma pesquisa para um período
            logger.info(f"Testando listar_agregados_pesquisa_periodo(pesquisa='{pesquisa_id}', periodo='{periodo_id}')...")
            agregados = listar_agregados_pesquisa_periodo(pesquisa=pesquisa_id, periodo=periodo_id)
            salvar_resultado(f"metadados_agregados_pesquisa_{pesquisa_id}_periodo_{periodo_id}", agregados)
            
            # Testa obter agregado
            if agregados and len(agregados) > 0 and isinstance(agregados[0], dict) and "id" in agregados[0]:
                agregado_id = agregados[0]["id"]
                logger.info(f"Testando obter_agregado(pesquisa='{pesquisa_id}', periodo='{periodo_id}', agregado='{agregado_id}')...")
                agregado = obter_agregado(pesquisa=pesquisa_id, periodo=periodo_id, agregado=agregado_id)
                salvar_resultado(f"metadados_agregado_{pesquisa_id}_periodo_{periodo_id}_agregado_{agregado_id}", agregado)
                
                # Testa listar variáveis do agregado
                logger.info(f"Testando listar_variaveis_agregado(pesquisa='{pesquisa_id}', periodo='{periodo_id}', agregado='{agregado_id}')...")
                variaveis = listar_variaveis_agregado(pesquisa=pesquisa_id, periodo=periodo_id, agregado=agregado_id)
                salvar_resultado(f"metadados_variaveis_agregado_{pesquisa_id}_periodo_{periodo_id}_agregado_{agregado_id}", variaveis)
                
                # Testa obter variável
                if variaveis and len(variaveis) > 0 and isinstance(variaveis[0], dict) and "id" in variaveis[0]:
                    variavel_id = variaveis[0]["id"]
                    logger.info(f"Testando obter_variavel(pesquisa='{pesquisa_id}', periodo='{periodo_id}', agregado='{agregado_id}', variavel='{variavel_id}')...")
                    variavel = obter_variavel(pesquisa=pesquisa_id, periodo=periodo_id, agregado=agregado_id, variavel=variavel_id)
                    salvar_resultado(f"metadados_variavel_{pesquisa_id}_periodo_{periodo_id}_agregado_{agregado_id}_variavel_{variavel_id}", variavel)
                
                # Testa listar classificações do agregado
                logger.info(f"Testando listar_classificacoes_agregado(pesquisa='{pesquisa_id}', periodo='{periodo_id}', agregado='{agregado_id}')...")
                classificacoes = listar_classificacoes_agregado(pesquisa=pesquisa_id, periodo=periodo_id, agregado=agregado_id)
                salvar_resultado(f"metadados_classificacoes_agregado_{pesquisa_id}_periodo_{periodo_id}_agregado_{agregado_id}", classificacoes)
                
                # Testa listar níveis de uma classificação
                if classificacoes and len(classificacoes) > 0 and isinstance(classificacoes[0], dict) and "id" in classificacoes[0]:
                    classificacao_id = classificacoes[0]["id"]
                    logger.info(f"Testando listar_niveis_classificacao(pesquisa='{pesquisa_id}', periodo='{periodo_id}', agregado='{agregado_id}', classificacao='{classificacao_id}')...")
                    niveis = listar_niveis_classificacao(pesquisa=pesquisa_id, periodo=periodo_id, agregado=agregado_id, classificacao=classificacao_id)
                    salvar_resultado(f"metadados_niveis_classificacao_{pesquisa_id}_periodo_{periodo_id}_agregado_{agregado_id}_classificacao_{classificacao_id}", niveis)
                    
                    # Testa listar categorias de um nível
                    if niveis and len(niveis) > 0 and isinstance(niveis[0], dict) and "id" in niveis[0]:
                        nivel_id = niveis[0]["id"]
                        logger.info(f"Testando listar_categorias_nivel(pesquisa='{pesquisa_id}', periodo='{periodo_id}', agregado='{agregado_id}', classificacao='{classificacao_id}', nivel='{nivel_id}')...")
                        categorias = listar_categorias_nivel(pesquisa=pesquisa_id, periodo=periodo_id, agregado=agregado_id, classificacao=classificacao_id, nivel=nivel_id)
                        salvar_resultado(f"metadados_categorias_nivel_{pesquisa_id}_periodo_{periodo_id}_agregado_{agregado_id}_classificacao_{classificacao_id}_nivel_{nivel_id}", categorias)
                        
                        # Testa obter categoria
                        if categorias and len(categorias) > 0 and isinstance(categorias[0], dict) and "id" in categorias[0]:
                            categoria_id = categorias[0]["id"]
                            logger.info(f"Testando obter_categoria(pesquisa='{pesquisa_id}', periodo='{periodo_id}', agregado='{agregado_id}', classificacao='{classificacao_id}', nivel='{nivel_id}', categoria='{categoria_id}')...")
                            categoria = obter_categoria(pesquisa=pesquisa_id, periodo=periodo_id, agregado=agregado_id, classificacao=classificacao_id, nivel=nivel_id, categoria=categoria_id)
                            salvar_resultado(f"metadados_categoria_{pesquisa_id}_periodo_{periodo_id}_agregado_{agregado_id}_classificacao_{classificacao_id}_nivel_{nivel_id}_categoria_{categoria_id}", categoria)
    
    # Testa listar domínios
    logger.info("Testando listar_dominios()...")
    dominios = listar_dominios()
    salvar_resultado("metadados_dominios", dominios)
    
    # Testa listar variáveis
    logger.info("Testando listar_variaveis()...")
    variaveis = listar_variaveis()
    salvar_resultado("metadados_variaveis", variaveis)
    
    # Testa listar unidades de medida
    logger.info("Testando listar_unidades_medida()...")
    unidades = listar_unidades_medida()
    salvar_resultado("metadados_unidades_medida", unidades)
    
    # Testa listar conceitos
    logger.info("Testando listar_conceitos()...")
    conceitos = listar_conceitos()
    salvar_resultado("metadados_conceitos", conceitos)

def testar_api_cnae():
    """Testa a API de CNAE"""
    logger.info("Testando API de CNAE...")
    
    # Testa listar seções
    logger.info("Testando listar_secoes()...")
    secoes = listar_secoes()
    salvar_resultado("cnae_secoes", secoes)
    
    # Testa obter seção
    if secoes and len(secoes) > 0 and isinstance(secoes[0], dict) and "id" in secoes[0]:
        secao_id = secoes[0]["id"]
        logger.info(f"Testando obter_secao(id_secao='{secao_id}')...")
        secao = obter_secao(id_secao=secao_id)
        salvar_resultado(f"cnae_secao_{secao_id}", secao)
        
        # Testa listar divisões de uma seção
        logger.info(f"Testando listar_divisoes(id_secao='{secao_id}')...")
        divisoes = listar_divisoes(id_secao=secao_id)
        salvar_resultado(f"cnae_divisoes_secao_{secao_id}", divisoes)
    
    # Testa listar divisões
    logger.info("Testando listar_divisoes()...")
    divisoes = listar_divisoes()
    salvar_resultado("cnae_divisoes", divisoes)
    
    # Testa obter divisão
    if divisoes and len(divisoes) > 0 and isinstance(divisoes[0], dict) and "id" in divisoes[0]:
        divisao_id = divisoes[0]["id"]
        logger.info(f"Testando obter_divisao(id_divisao='{divisao_id}')...")
        divisao = obter_divisao(id_divisao=divisao_id)
        salvar_resultado(f"cnae_divisao_{divisao_id}", divisao)
        
        # Testa listar grupos de uma divisão
        logger.info(f"Testando listar_grupos(id_divisao='{divisao_id}')...")
        grupos = listar_grupos(id_divisao=divisao_id)
        salvar_resultado(f"cnae_grupos_divisao_{divisao_id}", grupos)
    
    # Testa listar grupos
    logger.info("Testando listar_grupos()...")
    grupos = listar_grupos()
    salvar_resultado("cnae_grupos", grupos)
    
    # Testa obter grupo
    if grupos and len(grupos) > 0 and isinstance(grupos[0], dict) and "id" in grupos[0]:
        grupo_id = grupos[0]["id"]
        logger.info(f"Testando obter_grupo(id_grupo='{grupo_id}')...")
        grupo = obter_grupo(id_grupo=grupo_id)
        salvar_resultado(f"cnae_grupo_{grupo_id}", grupo)
        
        # Testa listar classes de um grupo
        logger.info(f"Testando listar_classes(id_grupo='{grupo_id}')...")
        classes = listar_classes(id_grupo=grupo_id)
        salvar_resultado(f"cnae_classes_grupo_{grupo_id}", classes)
    
    # Testa listar classes
    logger.info("Testando listar_classes()...")
    classes = listar_classes()
    salvar_resultado("cnae_classes", classes)
    
    # Testa obter classe
    if classes and len(classes) > 0 and isinstance(classes[0], dict) and "id" in classes[0]:
        classe_id = classes[0]["id"]
        logger.info(f"Testando obter_classe(id_classe='{classe_id}')...")
        classe = obter_classe(id_classe=classe_id)
        salvar_resultado(f"cnae_classe_{classe_id}", classe)
        
        # Testa listar subclasses de uma classe
        logger.info(f"Testando listar_subclasses(id_classe='{classe_id}')...")
        subclasses = listar_subclasses(id_classe=classe_id)
        salvar_resultado(f"cnae_subclasses_classe_{classe_id}", subclasses)
    
    # Testa listar subclasses
    logger.info("Testando listar_subclasses()...")
    subclasses = listar_subclasses()
    salvar_resultado("cnae_subclasses", subclasses)
    
    # Testa obter subclasse
    if subclasses and len(subclasses) > 0 and isinstance(subclasses[0], dict) and "id" in subclasses[0]:
        subclasse_id = subclasses[0]["id"]
        logger.info(f"Testando obter_subclasse(id_subclasse='{subclasse_id}')...")
        subclasse = obter_subclasse(id_subclasse=subclasse_id)
        salvar_resultado(f"cnae_subclasse_{subclasse_id}", subclasse)
    
    # Testa pesquisar CNAE
    logger.info("Testando pesquisar_cnae(termo='agricultura')...")
    pesquisa = pesquisar_cnae(termo='agricultura')
    salvar_resultado("cnae_pesquisa_agricultura", pesquisa)

def testar_api_nomes():
    """Testa a API de Nomes"""
    logger.info("Testando API de Nomes...")
    
    # Testa pesquisar nomes
    logger.info("Testando pesquisar_nomes(nome='JOSE')...")
    nomes = pesquisar_nomes(nome='JOSE')
    salvar_resultado("nomes_pesquisa_jose", nomes)
    
    # Testa ranking de nomes
    logger.info("Testando ranking_nomes()...")
    ranking = ranking_nomes()
    salvar_resultado("nomes_ranking", ranking)
    
    # Testa ranking de nomes por sexo
    logger.info("Testando ranking_nomes(sexo='M')...")
    ranking_masculino = ranking_nomes(sexo='M')
    salvar_resultado("nomes_ranking_masculino", ranking_masculino)
    
    # Testa ranking de nomes por década
    logger.info("Testando ranking_nomes(decada='2010')...")
    ranking_2010 = ranking_nomes(decada='2010')
    salvar_resultado("nomes_ranking_2010", ranking_2010)
    
    # Testa frequência de nome
    logger.info("Testando frequencia_nome(nome='MARIA')...")
    frequencia = frequencia_nome(nome='MARIA')
    salvar_resultado("nomes_frequencia_maria", frequencia)
    
    # Testa frequência de nome por sexo
    logger.info("Testando frequencia_nome(nome='MARIA', sexo='F')...")
    frequencia_feminino = frequencia_nome(nome='MARIA', sexo='F')
    salvar_resultado("nomes_frequencia_maria_feminino", frequencia_feminino)

def testar_api_censos():
    """Testa a API de Censos"""
    logger.info("Testando API de Censos...")
    
    # Testa obter área territorial
    logger.info("Testando obter_area_territorial(localidade='3304557')...")
    area = obter_area_territorial(localidade='3304557')
    salvar_resultado("censos_area_territorial_3304557", area)
    
    # Testa obter população
    logger.info("Testando obter_populacao(localidade='3304557')...")
    populacao = obter_populacao(localidade='3304557')
    salvar_resultado("censos_populacao_3304557", populacao)
    
    # Testa calcular densidade demográfica
    logger.info("Testando calcular_densidade_demografica(localidade='3304557')...")
    densidade = calcular_densidade_demografica(localidade='3304557')
    salvar_resultado("censos_densidade_demografica_3304557", densidade)
    
    # Testa obter indicadores demográficos
    logger.info("Testando obter_indicadores_demograficos(localidade='3304557')...")
    indicadores = obter_indicadores_demograficos(localidade='3304557')
    salvar_resultado("censos_indicadores_demograficos_3304557", indicadores)

def testar_api_bdg():
    """Testa a API do Banco de Dados Geodésicos (BDG)"""
    logger.info("Testando API do Banco de Dados Geodésicos (BDG)...")
    
    # Testa listar estações geodésicas
    logger.info("Testando listar_estacoes()...")
    estacoes = listar_estacoes()
    salvar_resultado("bdg_estacoes", estacoes)
    
    # Testa obter estação geodésica por ID
    if estacoes and len(estacoes) > 0 and isinstance(estacoes[0], dict) and "id" in estacoes[0]:
        estacao_id = estacoes[0]["id"]
        logger.info(f"Testando obter_estacao(id_estacao='{estacao_id}')...")
        estacao = obter_estacao(id_estacao=estacao_id)
        salvar_resultado(f"bdg_estacao_{estacao_id}", estacao)
    
    # Testa listar estações por UF
    logger.info("Testando bdg_listar_estacoes_por_uf(uf='RJ')...")
    estacoes_uf = bdg_listar_estacoes_por_uf(uf='RJ')
    salvar_resultado("bdg_estacoes_uf_RJ", estacoes_uf)
    
    # Testa listar estações por município
    logger.info("Testando bdg_listar_estacoes_por_municipio(id_municipio='3304557')...")
    estacoes_municipio = bdg_listar_estacoes_por_municipio(id_municipio='3304557')
    salvar_resultado("bdg_estacoes_municipio_3304557", estacoes_municipio)
    
    # Testa listar tipos de estações
    logger.info("Testando bdg_listar_tipos_estacoes()...")
    tipos = bdg_listar_tipos_estacoes()
    salvar_resultado("bdg_tipos_estacoes", tipos)
    
    # Testa listar estações por tipo
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando bdg_listar_estacoes_por_tipo(tipo='{tipo_id}')...")
        estacoes_tipo = bdg_listar_estacoes_por_tipo(tipo=tipo_id)
        salvar_resultado(f"bdg_estacoes_tipo_{tipo_id}", estacoes_tipo)

def testar_api_bngb():
    """Testa a API do Banco de Nomes Geográficos do Brasil (BNGB)"""
    logger.info("Testando API do Banco de Nomes Geográficos do Brasil (BNGB)...")
    
    # Testa pesquisar nomes geográficos
    logger.info("Testando pesquisar_nomes_geograficos(nome='rio')...")
    nomes = pesquisar_nomes_geograficos(nome='rio')
    salvar_resultado("bngb_pesquisa_rio", nomes)
    
    # Testa obter nome geográfico por ID
    if nomes and len(nomes) > 0 and isinstance(nomes[0], dict) and "id" in nomes[0]:
        nome_id = nomes[0]["id"]
        logger.info(f"Testando obter_nome_geografico(id_nome='{nome_id}')...")
        nome = obter_nome_geografico(id_nome=nome_id)
        salvar_resultado(f"bngb_nome_{nome_id}", nome)
    
    # Testa listar nomes por UF
    logger.info("Testando listar_nomes_por_uf(uf='RJ')...")
    nomes_uf = listar_nomes_por_uf(uf='RJ')
    salvar_resultado("bngb_nomes_uf_RJ", nomes_uf)
    
    # Testa listar nomes por município
    logger.info("Testando listar_nomes_por_municipio(id_municipio='3304557')...")
    nomes_municipio = listar_nomes_por_municipio(id_municipio='3304557')
    salvar_resultado("bngb_nomes_municipio_3304557", nomes_municipio)
    
    # Testa listar tipos de nomes
    logger.info("Testando listar_tipos_nomes()...")
    tipos = listar_tipos_nomes()
    salvar_resultado("bngb_tipos_nomes", tipos)
    
    # Testa listar nomes por tipo
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando listar_nomes_por_tipo(tipo='{tipo_id}')...")
        nomes_tipo = listar_nomes_por_tipo(tipo=tipo_id)
        salvar_resultado(f"bngb_nomes_tipo_{tipo_id}", nomes_tipo)

def testar_api_calendario():
    """Testa a API de Calendário do IBGE"""
    logger.info("Testando API de Calendário do IBGE...")
    
    # Testa listar eventos do calendário
    logger.info("Testando listar_eventos_calendario()...")
    eventos = listar_eventos_calendario()
    salvar_resultado("calendario_eventos", eventos)
    
    # Testa obter evento por ID
    if eventos and len(eventos) > 0 and isinstance(eventos[0], dict) and "id" in eventos[0]:
        evento_id = eventos[0]["id"]
        logger.info(f"Testando obter_evento_calendario(id_evento='{evento_id}')...")
        evento = obter_evento_calendario(id_evento=evento_id)
        salvar_resultado(f"calendario_evento_{evento_id}", evento)
    
    # Testa listar tipos de eventos
    logger.info("Testando listar_tipos_eventos_calendario()...")
    tipos = listar_tipos_eventos_calendario()
    salvar_resultado("calendario_tipos_eventos", tipos)
    
    # Testa listar eventos por tipo
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando listar_eventos_por_tipo(tipo='{tipo_id}')...")
        eventos_tipo = listar_eventos_por_tipo(tipo=tipo_id)
        salvar_resultado(f"calendario_eventos_tipo_{tipo_id}", eventos_tipo)
    
    # Testa listar eventos por produto
    logger.info("Testando listar_eventos_por_produto(id_produto='IPCA')...")
    eventos_produto = listar_eventos_por_produto(id_produto='IPCA')
    salvar_resultado("calendario_eventos_produto_IPCA", eventos_produto)
    
    # Testa listar eventos por data
    logger.info("Testando listar_eventos_calendario(data_inicio='2023-01-01', data_fim='2023-12-31')...")
    eventos_data = listar_eventos_calendario(data_inicio='2023-01-01', data_fim='2023-12-31')
    salvar_resultado("calendario_eventos_2023", eventos_data)

def testar_api_hgeohnor():
    """Testa a API hgeoHNOR"""
    logger.info("Testando API hgeoHNOR...")
    
    # Testa listar estações RAAP
    logger.info("Testando listar_estacoes_raap()...")
    estacoes = listar_estacoes_raap()
    salvar_resultado("hgeohnor_estacoes", estacoes)
    
    # Testa obter estação RAAP por ID
    if estacoes and len(estacoes) > 0 and isinstance(estacoes[0], dict) and "id" in estacoes[0]:
        estacao_id = estacoes[0]["id"]
        logger.info(f"Testando obter_estacao_raap(id_estacao='{estacao_id}')...")
        estacao = obter_estacao_raap(id_estacao=estacao_id)
        salvar_resultado(f"hgeohnor_estacao_{estacao_id}", estacao)
    
    # Testa listar estações por UF
    logger.info("Testando hgeohnor_listar_estacoes_por_uf(uf='RJ')...")
    estacoes_uf = hgeohnor_listar_estacoes_por_uf(uf='RJ')
    salvar_resultado("hgeohnor_estacoes_uf_RJ", estacoes_uf)
    
    # Testa listar estações por município
    logger.info("Testando hgeohnor_listar_estacoes_por_municipio(id_municipio='3304557')...")
    estacoes_municipio = hgeohnor_listar_estacoes_por_municipio(id_municipio='3304557')
    salvar_resultado("hgeohnor_estacoes_municipio_3304557", estacoes_municipio)
    
    # Testa listar tipos de estações
    logger.info("Testando hgeohnor_listar_tipos_estacoes()...")
    tipos = hgeohnor_listar_tipos_estacoes()
    salvar_resultado("hgeohnor_tipos_estacoes", tipos)
    
    # Testa listar estações por tipo
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando hgeohnor_listar_estacoes_por_tipo(tipo='{tipo_id}')...")
        estacoes_tipo = hgeohnor_listar_estacoes_por_tipo(tipo=tipo_id)
        salvar_resultado(f"hgeohnor_estacoes_tipo_{tipo_id}", estacoes_tipo)

def testar_api_noticias():
    """Testa a API de Notícias"""
    logger.info("Testando API de Notícias...")
    
    # Testa listar notícias
    logger.info("Testando listar_noticias()...")
    noticias = listar_noticias()
    salvar_resultado("noticias_lista", noticias)
    
    # Testa obter notícia por ID
    if noticias and "items" in noticias and len(noticias["items"]) > 0 and isinstance(noticias["items"][0], dict) and "id" in noticias["items"][0]:
        noticia_id = noticias["items"][0]["id"]
        logger.info(f"Testando obter_noticia(id_noticia='{noticia_id}')...")
        noticia = obter_noticia(id_noticia=noticia_id)
        salvar_resultado(f"noticias_noticia_{noticia_id}", noticia)
    
    # Testa listar tipos de notícias
    logger.info("Testando listar_tipos_noticias()...")
    tipos = listar_tipos_noticias()
    salvar_resultado("noticias_tipos", tipos)
    
    # Testa listar notícias por tipo
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando listar_noticias_por_tipo(tipo='{tipo_id}')...")
        noticias_tipo = listar_noticias_por_tipo(tipo=tipo_id)
        salvar_resultado(f"noticias_tipo_{tipo_id}", noticias_tipo)
    
    # Testa listar notícias por produto
    logger.info("Testando listar_noticias_por_produto(id_produto='IPCA')...")
    noticias_produto = listar_noticias_por_produto(id_produto='IPCA')
    salvar_resultado("noticias_produto_IPCA", noticias_produto)
    
    # Testa pesquisar notícias
    logger.info("Testando pesquisar_noticias(termo='economia')...")
    noticias_pesquisa = pesquisar_noticias(termo='economia')
    salvar_resultado("noticias_pesquisa_economia", noticias_pesquisa)

def testar_api_paises():
    """Testa a API de Países"""
    logger.info("Testando API de Países...")
    
    # Testa listar países
    logger.info("Testando listar_paises()...")
    paises = listar_paises()
    salvar_resultado("paises_lista", paises)
    
    # Testa obter país por ID
    logger.info("Testando obter_pais(id_pais='BRA')...")
    pais = obter_pais(id_pais='BRA')
    salvar_resultado("paises_pais_BRA", pais)
    
    # Testa listar continentes
    logger.info("Testando listar_continentes()...")
    continentes = listar_continentes()
    salvar_resultado("paises_continentes", continentes)
    
    # Testa obter continente por ID
    if continentes and len(continentes) > 0 and isinstance(continentes[0], dict) and "id" in continentes[0]:
        continente_id = continentes[0]["id"]
        # Convertemos o ID para string e usamos apenas os primeiros caracteres para evitar problemas no nome do arquivo
        continente_id_safe = str(continente_id).replace("'", "").replace("{}", "").replace(":", "_").replace(",", "_").replace(" ", "")[:20]
        logger.info(f"Testando obter_continente(id_continente='{continente_id}')...")
        continente = obter_continente(id_continente=continente_id)
        salvar_resultado(f"paises_continente_id", continente)
    
    # Testa listar países por continente
    if continentes and len(continentes) > 0 and isinstance(continentes[0], dict) and "id" in continentes[0]:
        continente_id = continentes[0]["id"]
        logger.info(f"Testando listar_paises_por_continente(id_continente='{continente_id}')...")
        paises_continente = listar_paises_por_continente(id_continente=continente_id)
        salvar_resultado("paises_por_continente", paises_continente)
    
    # Testa listar blocos
    logger.info("Testando listar_blocos()...")
    blocos = listar_blocos()
    salvar_resultado("paises_blocos", blocos)
    
    # Testa obter bloco por ID
    if blocos and len(blocos) > 0 and isinstance(blocos[0], dict) and "id" in blocos[0]:
        bloco_id = blocos[0]["id"]
        logger.info(f"Testando obter_bloco(id_bloco='{bloco_id}')...")
        bloco = obter_bloco(id_bloco=bloco_id)
        salvar_resultado("paises_bloco_info", bloco)
    
    # Testa listar países por bloco
    if blocos and len(blocos) > 0 and isinstance(blocos[0], dict) and "id" in blocos[0]:
        bloco_id = blocos[0]["id"]
        logger.info(f"Testando listar_paises_por_bloco(id_bloco='{bloco_id}')...")
        paises_bloco = listar_paises_por_bloco(id_bloco=bloco_id)
        salvar_resultado("paises_por_bloco", paises_bloco)

def testar_api_pesquisas():
    """Testa a API de Pesquisas"""
    logger.info("Testando API de Pesquisas...")
    
    # Testa listar pesquisas
    logger.info("Testando listar_pesquisas()...")
    pesquisas = listar_pesquisas()
    salvar_resultado("pesquisas_lista", pesquisas)
    
    # Testa obter pesquisa por ID
    if pesquisas and len(pesquisas) > 0 and isinstance(pesquisas[0], dict) and "id" in pesquisas[0]:
        pesquisa_id = pesquisas[0]["id"]
        logger.info(f"Testando obter_pesquisa(id_pesquisa='{pesquisa_id}')...")
        pesquisa = obter_pesquisa(id_pesquisa=pesquisa_id)
        salvar_resultado(f"pesquisas_pesquisa_{pesquisa_id}", pesquisa)
    
    # Testa listar períodos de pesquisa
    if pesquisas and len(pesquisas) > 0 and isinstance(pesquisas[0], dict) and "id" in pesquisas[0]:
        pesquisa_id = pesquisas[0]["id"]
        logger.info(f"Testando listar_periodos_pesquisa(id_pesquisa='{pesquisa_id}')...")
        periodos = listar_periodos_pesquisa(id_pesquisa=pesquisa_id)
        salvar_resultado(f"pesquisas_pesquisa_{pesquisa_id}_periodos", periodos)
        
        # Testa obter período de pesquisa
        if periodos and len(periodos) > 0 and isinstance(periodos[0], dict) and "id" in periodos[0]:
            periodo_id = periodos[0]["id"]
            logger.info(f"Testando obter_periodo_pesquisa(id_pesquisa='{pesquisa_id}', id_periodo='{periodo_id}')...")
            periodo = obter_periodo_pesquisa(id_pesquisa=pesquisa_id, id_periodo=periodo_id)
            salvar_resultado(f"pesquisas_pesquisa_{pesquisa_id}_periodo_{periodo_id}", periodo)
            
            # Testa listar resultados de pesquisa
            logger.info(f"Testando listar_resultados_pesquisa(id_pesquisa='{pesquisa_id}', id_periodo='{periodo_id}')...")
            resultados = listar_resultados_pesquisa(id_pesquisa=pesquisa_id, id_periodo=periodo_id)
            salvar_resultado(f"pesquisas_pesquisa_{pesquisa_id}_periodo_{periodo_id}_resultados", resultados)
            
            # Testa obter resultado de pesquisa
            if resultados and len(resultados) > 0 and isinstance(resultados[0], dict) and "id" in resultados[0]:
                resultado_id = resultados[0]["id"]
                logger.info(f"Testando obter_resultado_pesquisa(id_pesquisa='{pesquisa_id}', id_periodo='{periodo_id}', id_resultado='{resultado_id}')...")
                resultado = obter_resultado_pesquisa(id_pesquisa=pesquisa_id, id_periodo=periodo_id, id_resultado=resultado_id)
                salvar_resultado(f"pesquisas_pesquisa_{pesquisa_id}_periodo_{periodo_id}_resultado_{resultado_id}", resultado)
    
    # Testa listar indicadores de pesquisa
    if pesquisas and len(pesquisas) > 0 and isinstance(pesquisas[0], dict) and "id" in pesquisas[0]:
        pesquisa_id = pesquisas[0]["id"]
        logger.info(f"Testando listar_indicadores_pesquisa(id_pesquisa='{pesquisa_id}')...")
        indicadores = listar_indicadores_pesquisa(id_pesquisa=pesquisa_id)
        salvar_resultado(f"pesquisas_pesquisa_{pesquisa_id}_indicadores", indicadores)
        
        # Testa obter indicador de pesquisa
        if indicadores and len(indicadores) > 0 and isinstance(indicadores[0], dict) and "id" in indicadores[0]:
            indicador_id = indicadores[0]["id"]
            logger.info(f"Testando obter_indicador_pesquisa(id_pesquisa='{pesquisa_id}', id_indicador='{indicador_id}')...")
            indicador = obter_indicador_pesquisa(id_pesquisa=pesquisa_id, id_indicador=indicador_id)
            salvar_resultado(f"pesquisas_pesquisa_{pesquisa_id}_indicador_{indicador_id}", indicador)

def testar_api_ppp():
    """Testa a API do Serviço de Posicionamento por Ponto Preciso (PPP)"""
    logger.info("Testando API do Serviço de Posicionamento por Ponto Preciso (PPP)...")
    
    # Testa listar processamentos
    logger.info("Testando listar_processamentos_ppp()...")
    processamentos = listar_processamentos_ppp()
    salvar_resultado("ppp_processamentos", processamentos)
    
    # Testa obter processamento por ID
    if processamentos and len(processamentos) > 0 and isinstance(processamentos[0], dict) and "id" in processamentos[0]:
        processamento_id = processamentos[0]["id"]
        logger.info(f"Testando obter_processamento(id_processamento='{processamento_id}')...")
        processamento = obter_processamento(id_processamento=processamento_id)
        salvar_resultado(f"ppp_processamento_{processamento_id}", processamento)
    
    # Testa listar status de processamentos
    logger.info("Testando listar_status_processamentos()...")
    status = listar_status_processamentos()
    salvar_resultado("ppp_status", status)
    
    # Testa listar processamentos por status
    if status and len(status) > 0 and isinstance(status[0], dict) and "id" in status[0]:
        status_id = status[0]["id"]
        logger.info(f"Testando listar_processamentos_por_status(status='{status_id}')...")
        processamentos_status = listar_processamentos_por_status(status=status_id)
        salvar_resultado(f"ppp_processamentos_status_{status_id}", processamentos_status)
    
    # Testa listar processamentos por usuário
    logger.info("Testando listar_processamentos_por_usuario(id_usuario='teste@ibge.gov.br')...")
    processamentos_usuario = listar_processamentos_por_usuario(id_usuario='teste@ibge.gov.br')
    salvar_resultado("ppp_processamentos_usuario_teste", processamentos_usuario)
    
    # Testa obter resultado de processamento
    if processamentos and len(processamentos) > 0 and isinstance(processamentos[0], dict) and "id" in processamentos[0]:
        processamento_id = processamentos[0]["id"]
        logger.info(f"Testando obter_resultado_processamento(id_processamento='{processamento_id}')...")
        resultado = obter_resultado_processamento(id_processamento=processamento_id)
        salvar_resultado(f"ppp_processamento_{processamento_id}_resultado", resultado)

def testar_api_produtos():
    """Testa a API de Produtos"""
    logger.info("Testando API de Produtos...")
    
    # Testa listar produtos
    logger.info("Testando listar_produtos()...")
    produtos = listar_produtos()
    salvar_resultado("produtos_lista", produtos)
    
    # Testa obter produto por ID
    if produtos and isinstance(produtos, dict) and "id" in produtos:
        produto_id = produtos["id"]
        logger.info(f"Testando obter_produto(id_produto='{produto_id}')...")
        produto = obter_produto(id_produto=produto_id)
        salvar_resultado("produtos_produto_info", produto)
    
    # Testa listar tipos de produtos
    logger.info("Testando listar_tipos_produtos()...")
    tipos = listar_tipos_produtos()
    salvar_resultado("produtos_tipos", tipos)
    
    # Testa obter tipo de produto
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando obter_tipo_produto(id_tipo='{tipo_id}')...")
        tipo = obter_tipo_produto(id_tipo=tipo_id)
        salvar_resultado(f"produtos_tipo_{tipo_id}", tipo)
    
    # Testa listar produtos por tipo
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando listar_produtos_por_tipo(id_tipo='{tipo_id}')...")
        produtos_tipo = listar_produtos_por_tipo(id_tipo=tipo_id)
        salvar_resultado(f"produtos_tipo_{tipo_id}_produtos", produtos_tipo)
    
    # Testa listar temas de produtos
    logger.info("Testando listar_temas_produtos()...")
    temas = listar_temas_produtos()
    salvar_resultado("produtos_temas", temas)
    
    # Testa obter tema de produto
    if temas and len(temas) > 0 and isinstance(temas[0], dict) and "id" in temas[0]:
        tema_id = temas[0]["id"]
        logger.info(f"Testando obter_tema_produto(id_tema='{tema_id}')...")
        tema = obter_tema_produto(id_tema=tema_id)
        salvar_resultado(f"produtos_tema_{tema_id}", tema)
    
    # Testa listar produtos por tema
    if temas and len(temas) > 0 and isinstance(temas[0], dict) and "id" in temas[0]:
        tema_id = temas[0]["id"]
        logger.info(f"Testando listar_produtos_por_tema(id_tema='{tema_id}')...")
        produtos_tema = listar_produtos_por_tema(id_tema=tema_id)
        salvar_resultado(f"produtos_tema_{tema_id}_produtos", produtos_tema)

def testar_api_progrid():
    """Testa a API ProGrid"""
    logger.info("Testando API ProGrid...")
    
    # Testa listar células
    logger.info("Testando listar_celulas()...")
    celulas = listar_celulas()
    salvar_resultado("progrid_celulas", celulas)
    
    # Testa obter célula por ID
    if celulas and len(celulas) > 0 and isinstance(celulas[0], dict) and "id" in celulas[0]:
        celula_id = celulas[0]["id"]
        logger.info(f"Testando obter_celula(id_celula='{celula_id}')...")
        celula = obter_celula(id_celula=celula_id)
        salvar_resultado(f"progrid_celula_{celula_id}", celula)
    
    # Testa listar níveis ProGrid
    logger.info("Testando listar_niveis_progrid()...")
    niveis = listar_niveis_progrid()
    salvar_resultado("progrid_niveis", niveis)
    
    # Testa obter nível ProGrid
    if niveis and len(niveis) > 0 and isinstance(niveis[0], dict) and "id" in niveis[0]:
        nivel_id = niveis[0]["id"]
        logger.info(f"Testando obter_nivel_progrid(id_nivel='{nivel_id}')...")
        nivel = obter_nivel_progrid(id_nivel=nivel_id)
        salvar_resultado(f"progrid_nivel_{nivel_id}", nivel)
    
    # Testa listar células por nível
    if niveis and len(niveis) > 0 and isinstance(niveis[0], dict) and "id" in niveis[0]:
        nivel_id = niveis[0]["id"]
        logger.info(f"Testando listar_celulas_por_nivel(id_nivel='{nivel_id}')...")
        celulas_nivel = listar_celulas_por_nivel(id_nivel=nivel_id)
        salvar_resultado(f"progrid_nivel_{nivel_id}_celulas", celulas_nivel)
    
    # Testa listar células por UF
    logger.info("Testando listar_celulas_por_uf(uf='RJ')...")
    celulas_uf = listar_celulas_por_uf(uf='RJ')
    salvar_resultado("progrid_celulas_uf_RJ", celulas_uf)
    
    # Testa listar células por município
    logger.info("Testando listar_celulas_por_municipio(id_municipio='3304557')...")
    celulas_municipio = listar_celulas_por_municipio(id_municipio='3304557')
    salvar_resultado("progrid_celulas_municipio_3304557", celulas_municipio)

def testar_api_publicacoes():
    """Testa a API de Publicações"""
    logger.info("Testando API de Publicações...")
    
    # Testa listar publicações
    logger.info("Testando listar_publicacoes()...")
    publicacoes = listar_publicacoes()
    salvar_resultado("publicacoes_lista", publicacoes)
    
    # Testa obter publicação por ID
    if publicacoes and "items" in publicacoes and len(publicacoes["items"]) > 0 and isinstance(publicacoes["items"][0], dict) and "id" in publicacoes["items"][0]:
        publicacao_id = publicacoes["items"][0]["id"]
        logger.info(f"Testando obter_publicacao(id_publicacao='{publicacao_id}')...")
        publicacao = obter_publicacao(id_publicacao=publicacao_id)
        salvar_resultado("publicacoes_publicacao_info", publicacao)
    
    # Testa listar tipos de publicações
    logger.info("Testando listar_tipos_publicacoes()...")
    tipos = listar_tipos_publicacoes()
    salvar_resultado("publicacoes_tipos", tipos)
    
    # Testa listar publicações por tipo
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando listar_publicacoes_por_tipo(tipo='{tipo_id}')...")
        publicacoes_tipo = listar_publicacoes_por_tipo(tipo=tipo_id)
        salvar_resultado(f"publicacoes_tipo_{tipo_id}", publicacoes_tipo)
    
    # Testa listar temas de publicações
    logger.info("Testando listar_temas_publicacoes()...")
    temas = listar_temas_publicacoes()
    salvar_resultado("publicacoes_temas", temas)
    
    # Testa listar publicações por tema
    if temas and len(temas) > 0 and isinstance(temas[0], dict) and "id" in temas[0]:
        tema_id = temas[0]["id"]
        logger.info(f"Testando listar_publicacoes_por_tema(tema='{tema_id}')...")
        publicacoes_tema = listar_publicacoes_por_tema(tema=tema_id)
        salvar_resultado(f"publicacoes_tema_{tema_id}", publicacoes_tema)
    
    # Testa pesquisar publicações
    logger.info("Testando pesquisar_publicacoes(termo='brasil')...")
    publicacoes_pesquisa = pesquisar_publicacoes(termo='brasil')
    salvar_resultado("publicacoes_pesquisa_brasil", publicacoes_pesquisa)

def testar_api_rbmc():
    """Testa a API da Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS (RBMC)"""
    logger.info("Testando API da Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS (RBMC)...")
    
    # Testa listar estações
    logger.info("Testando listar_estacoes()...")
    estacoes = listar_estacoes()
    salvar_resultado("rbmc_estacoes", estacoes)
    
    # Testa obter estação por ID
    if estacoes and len(estacoes) > 0 and isinstance(estacoes[0], dict) and "id" in estacoes[0]:
        estacao_id = estacoes[0]["id"]
        logger.info(f"Testando obter_estacao(id_estacao='{estacao_id}')...")
        estacao = obter_estacao(id_estacao=estacao_id)
        salvar_resultado("rbmc_estacao_info", estacao)
    
    # Testa listar estações por UF
    logger.info("Testando listar_estacoes_por_uf(uf='RJ')...")
    estacoes_uf = listar_estacoes_por_uf(uf='RJ')
    salvar_resultado("rbmc_estacoes_uf_RJ", estacoes_uf)
    
    # Testa listar estações por município
    logger.info("Testando listar_estacoes_por_municipio(id_municipio='3304557')...")
    estacoes_municipio = listar_estacoes_por_municipio(id_municipio='3304557')
    salvar_resultado("rbmc_estacoes_municipio_3304557", estacoes_municipio)
    
    # Testa listar tipos de estações
    logger.info("Testando listar_tipos_estacoes()...")
    tipos = listar_tipos_estacoes()
    salvar_resultado("rbmc_tipos_estacoes", tipos)
    
    # Testa listar estações por tipo
    if tipos and len(tipos) > 0 and isinstance(tipos[0], dict) and "id" in tipos[0]:
        tipo_id = tipos[0]["id"]
        logger.info(f"Testando listar_estacoes_por_tipo(tipo='{tipo_id}')...")
        estacoes_tipo = listar_estacoes_por_tipo(tipo=tipo_id)
        salvar_resultado("rbmc_estacoes_tipo_info", estacoes_tipo)
    
    # Testa listar arquivos de estação
    if estacoes and len(estacoes) > 0 and isinstance(estacoes[0], dict) and "id" in estacoes[0]:
        estacao_id = estacoes[0]["id"]
        logger.info(f"Testando listar_arquivos_estacao(id_estacao='{estacao_id}')...")
        arquivos = listar_arquivos_estacao(id_estacao=estacao_id)
        salvar_resultado("rbmc_estacao_arquivos", arquivos)
        
        # Testa obter arquivo de estação
        if arquivos and len(arquivos) > 0 and isinstance(arquivos[0], dict) and "id" in arquivos[0]:
            arquivo_id = arquivos[0]["id"]
            logger.info(f"Testando obter_arquivo_estacao(id_estacao='{estacao_id}', id_arquivo='{arquivo_id}')...")
            arquivo = obter_arquivo_estacao(id_estacao=estacao_id, id_arquivo=arquivo_id)
            salvar_resultado("rbmc_estacao_arquivo_info", arquivo)

def testar_api_rmpg():
    """Testa a API da Rede Maregráfica Permanente para Geodésia (RMPG)"""
    logger.info("Testando API da Rede Maregráfica Permanente para Geodésia (RMPG)...")
    
    # Testa listar estações
    logger.info("Testando listar_estacoes_rmpg()...")
    estacoes = listar_estacoes_rmpg()
    salvar_resultado("rmpg_estacoes", estacoes)
    
    # Testa obter estação por ID
    if estacoes and len(estacoes) > 0 and isinstance(estacoes[0], dict) and "id" in estacoes[0]:
        estacao_id = estacoes[0]["id"]
        logger.info(f"Testando obter_estacao_rmpg(id_estacao='{estacao_id}')...")
        estacao = obter_estacao_rmpg(id_estacao=estacao_id)
        salvar_resultado("rmpg_estacao_info", estacao)
    
    # Testa listar estações por UF
    logger.info("Testando listar_estacoes_por_uf_rmpg(uf='RJ')...")
    estacoes_uf = listar_estacoes_por_uf_rmpg(uf='RJ')
    salvar_resultado("rmpg_estacoes_uf_RJ", estacoes_uf)
    
    # Testa listar estações por município
    logger.info("Testando listar_estacoes_por_municipio_rmpg(id_municipio='3304557')...")
    estacoes_municipio = listar_estacoes_por_municipio_rmpg(id_municipio='3304557')
    salvar_resultado("rmpg_estacoes_municipio_3304557", estacoes_municipio)
    
    # Testa listar status de estações
    logger.info("Testando listar_status_estacoes()...")
    status = listar_status_estacoes()
    salvar_resultado("rmpg_status_estacoes", status)
    
    # Testa listar estações por status
    if status and len(status) > 0 and isinstance(status[0], dict) and "id" in status[0]:
        status_id = status[0]["id"]
        logger.info(f"Testando listar_estacoes_por_status(status='{status_id}')...")
        estacoes_status = listar_estacoes_por_status(status=status_id)
        salvar_resultado("rmpg_estacoes_status_info", estacoes_status)
    
    # Testa listar dados de estação
    if estacoes and len(estacoes) > 0 and isinstance(estacoes[0], dict) and "id" in estacoes[0]:
        estacao_id = estacoes[0]["id"]
        logger.info(f"Testando listar_dados_estacao(id_estacao='{estacao_id}')...")
        dados = listar_dados_estacao(id_estacao=estacao_id)
        salvar_resultado("rmpg_estacao_dados", dados)
        
        # Testa obter dado de estação
        if dados and len(dados) > 0 and isinstance(dados[0], dict) and "id" in dados[0]:
            dado_id = dados[0]["id"]
            logger.info(f"Testando obter_dado_estacao(id_estacao='{estacao_id}', id_dado='{dado_id}')...")
            dado = obter_dado_estacao(id_estacao=estacao_id, id_dado=dado_id)
            salvar_resultado("rmpg_estacao_dado_info", dado)

def main():
    """Função principal para testar todas as APIs"""
    logger.info("Iniciando testes das APIs do IBGE...")
    
    # Testa a API de Localidades
    testar_api_localidades()
    
    # Testa a API de Agregados
    testar_api_agregados()
    
    # Testa a API de Malhas
    testar_api_malhas()
    
    # Testa a API de Metadados
    testar_api_metadados()
    
    # Testa a API de CNAE
    testar_api_cnae()
    
    # Testa a API de Nomes
    testar_api_nomes()
    
    # Testa a API de Censos
    testar_api_censos()
    
    # Testa as novas APIs implementadas
    testar_api_bdg()
    testar_api_bngb()
    testar_api_calendario()
    testar_api_hgeohnor()
    testar_api_noticias()
    testar_api_paises()
    testar_api_pesquisas()
    testar_api_ppp()
    testar_api_produtos()
    testar_api_progrid()
    testar_api_publicacoes()
    testar_api_rbmc()
    testar_api_rmpg()
    
    logger.info("Testes concluídos com sucesso!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Erro durante os testes: {e}")
        raise

if __name__ == "__main__":
    main()
