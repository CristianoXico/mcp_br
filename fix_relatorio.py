"""
Script para corrigir a função exibir_relatorio_texto no arquivo relatorio_localidade.py
para lidar corretamente com dados socioeconômicos em formato de dicionário aninhado.
"""

import re

# Caminho para os arquivos
arquivo_original = "tools/relatorio_localidade.py"
arquivo_temporario = "tools/relatorio_localidade.py.new"

# Função para corrigir a exibição de dados socioeconômicos para municípios
def corrigir_exibicao_municipios():
    with open(arquivo_original, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Localizar a seção de dados socioeconômicos para municípios
    padrao = re.compile(r'(        # Dados Socioeconômicos\n        if "dados_socioeconomicos" in relatorio and relatorio\["dados_socioeconomicos"\]:\n            dados_socio = relatorio\["dados_socioeconomicos"\]\n            print\("\\nDADOS SOCIOECONÔMICOS:"\)\n            print\(f"PIB: {formatar_valor_monetario\(dados_socio\.get\(\'pib\', 0\)\)}"\)\n            print\(f"PIB per capita: {formatar_valor_monetario\(dados_socio\.get\(\'pib_per_capita\', 0\)\)}"\)\n            print\(f"IDH: {dados_socio\.get\(\'idh\', \'N/A\'\)}"\)\s+\n            # Exibe outras informações socioeconômicas se disponíveis\n            for chave, valor in dados_socio\.items\(\):\n                if chave not in \[\'pib\', \'pib_per_capita\', \'idh\'\]:\n                    if isinstance\(valor, \(int, float\)\) and \'valor\' in chave\.lower\(\):\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {formatar_valor_monetario\(valor\)}"\)\n                    elif isinstance\(valor, \(int, float\)\):\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {valor:,}"\.replace\(",", "\."\)\)\n                    else:\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {valor}"\))')
    
    # Nova implementação para exibição de dados socioeconômicos para municípios
    nova_implementacao = """        # Dados Socioeconômicos
        if "dados_socioeconomicos" in relatorio and relatorio["dados_socioeconomicos"]:
            dados_socio = relatorio["dados_socioeconomicos"]
            print("\\nDADOS SOCIOECONÔMICOS:")
            
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
                print("\\nEducação:")
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
                print("\\nSaúde:")
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
                        print(f"\\n{chave.replace('_', ' ').title()}:")
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
                        print(f"{chave.replace('_', ' ').title()}: {valor}")"""
    
    # Substituir a implementação antiga pela nova
    conteudo_modificado = re.sub(padrao, nova_implementacao, conteudo)
    
    # Verificar se a substituição foi feita
    if conteudo == conteudo_modificado:
        print("Não foi possível encontrar o padrão para municípios. Tentando abordagem alternativa...")
        return False
    
    # Salvar o conteúdo modificado
    with open(arquivo_temporario, 'w', encoding='utf-8') as f:
        f.write(conteudo_modificado)
    
    return True

# Função para corrigir a exibição de dados socioeconômicos para estados
def corrigir_exibicao_estados():
    with open(arquivo_original if not corrigir_exibicao_municipios() else arquivo_temporario, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Localizar a seção de dados socioeconômicos para estados
    padrao = re.compile(r'(        # Dados Socioeconômicos\n        if "dados_socioeconomicos" in relatorio and relatorio\["dados_socioeconomicos"\]:\n            dados_socio = relatorio\["dados_socioeconomicos"\]\n            print\("\\nDADOS SOCIOECONÔMICOS:"\)\n            print\(f"PIB: {formatar_valor_monetario\(dados_socio\.get\(\'pib\', 0\)\)}"\)\n            print\(f"PIB per capita: {formatar_valor_monetario\(dados_socio\.get\(\'pib_per_capita\', 0\)\)}"\)\n            print\(f"IDH: {dados_socio\.get\(\'idh\', \'N/A\'\)}"\)\s+\n            # Exibe outras informações socioeconômicas se disponíveis\n            for chave, valor in dados_socio\.items\(\):\n                if chave not in \[\'pib\', \'pib_per_capita\', \'idh\'\]:\n                    if isinstance\(valor, \(int, float\)\) and \'valor\' in chave\.lower\(\):\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {formatar_valor_monetario\(valor\)}"\)\n                    elif isinstance\(valor, \(int, float\)\):\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {valor:,}"\.replace\(",", "\."\)\)\n                    else:\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {valor}"\))')
    
    # Nova implementação para exibição de dados socioeconômicos para estados
    nova_implementacao = """        # Dados Socioeconômicos
        if "dados_socioeconomicos" in relatorio and relatorio["dados_socioeconomicos"]:
            dados_socio = relatorio["dados_socioeconomicos"]
            print("\\nDADOS SOCIOECONÔMICOS:")
            
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
                print("\\nEducação:")
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
                print("\\nSaúde:")
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
                        print(f"\\n{chave.replace('_', ' ').title()}:")
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
                        print(f"{chave.replace('_', ' ').title()}: {valor}")"""
    
    # Substituir a implementação antiga pela nova
    conteudo_modificado = re.sub(padrao, nova_implementacao, conteudo)
    
    # Verificar se a substituição foi feita
    if conteudo == conteudo_modificado:
        print("Não foi possível encontrar o padrão para estados. Tentando abordagem alternativa...")
        return False
    
    # Salvar o conteúdo modificado
    with open(arquivo_temporario, 'w', encoding='utf-8') as f:
        f.write(conteudo_modificado)
    
    return True

# Função para corrigir a exibição de dados socioeconômicos para regiões
def corrigir_exibicao_regioes():
    with open(arquivo_original if not (corrigir_exibicao_municipios() or corrigir_exibicao_estados()) else arquivo_temporario, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Localizar a seção de dados socioeconômicos para regiões
    padrao = re.compile(r'(        # Dados Socioeconômicos\n        if "dados_socioeconomicos" in relatorio and relatorio\["dados_socioeconomicos"\]:\n            dados_socio = relatorio\["dados_socioeconomicos"\]\n            print\("\\nDADOS SOCIOECONÔMICOS:"\)\n            print\(f"PIB: {formatar_valor_monetario\(dados_socio\.get\(\'pib\', 0\)\)}"\)\n            print\(f"PIB per capita: {formatar_valor_monetario\(dados_socio\.get\(\'pib_per_capita\', 0\)\)}"\)\n            print\(f"IDH médio: {dados_socio\.get\(\'idh_medio\', \'N/A\'\)}"\)\s+\n            # Exibe outras informações socioeconômicas se disponíveis\n            for chave, valor in dados_socio\.items\(\):\n                if chave not in \[\'pib\', \'pib_per_capita\', \'idh_medio\'\]:\n                    if isinstance\(valor, \(int, float\)\) and \'valor\' in chave\.lower\(\):\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {formatar_valor_monetario\(valor\)}"\)\n                    elif isinstance\(valor, \(int, float\)\):\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {valor:,}"\.replace\(",", "\."\)\)\n                    else:\n                        print\(f"{chave\.replace\(\'_\', \' \'\)\.title\(\)}: {valor}"\))')
    
    # Nova implementação para exibição de dados socioeconômicos para regiões
    nova_implementacao = """        # Dados Socioeconômicos
        if "dados_socioeconomicos" in relatorio and relatorio["dados_socioeconomicos"]:
            dados_socio = relatorio["dados_socioeconomicos"]
            print("\\nDADOS SOCIOECONÔMICOS:")
            
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
                print("\\nEducação:")
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
                print("\\nSaúde:")
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
                        print(f"\\n{chave.replace('_', ' ').title()}:")
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
                        print(f"{chave.replace('_', ' ').title()}: {valor}")"""
    
    # Substituir a implementação antiga pela nova
    conteudo_modificado = re.sub(padrao, nova_implementacao, conteudo)
    
    # Verificar se a substituição foi feita
    if conteudo == conteudo_modificado:
        print("Não foi possível encontrar o padrão para regiões. Tentando abordagem alternativa...")
        return False
    
    # Salvar o conteúdo modificado
    with open(arquivo_temporario, 'w', encoding='utf-8') as f:
        f.write(conteudo_modificado)
    
    return True

# Função para aplicar todas as correções
def aplicar_correcoes():
    # Tentar corrigir as exibições para municípios, estados e regiões
    if corrigir_exibicao_municipios():
        print("Correção para municípios aplicada com sucesso!")
    
    if corrigir_exibicao_estados():
        print("Correção para estados aplicada com sucesso!")
    
    if corrigir_exibicao_regioes():
        print("Correção para regiões aplicada com sucesso!")
    
    print(f"\nArquivo temporário criado: {arquivo_temporario}")
    print("Para aplicar as alterações, execute:")
    print(f"copy {arquivo_temporario} {arquivo_original}")

if __name__ == "__main__":
    aplicar_correcoes()
