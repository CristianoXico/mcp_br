"""
Script para atualizar a função exibir_relatorio_texto no arquivo relatorio_localidade.py
"""

import re

# Caminho para o arquivo original
arquivo_original = "tools/relatorio_localidade.py"
arquivo_temporario = "tools/relatorio_localidade.py.new"

# Nova implementação da função formatar_valor_monetario
nova_funcao_formatar = '''
def formatar_valor_monetario(valor: float) -> str:
    """Formata um valor monetário em reais"""
    if not isinstance(valor, (int, float)):
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
'''

# Função para atualizar manualmente o arquivo
def main():
    try:
        # Ler o arquivo original
        with open(arquivo_original, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        # Criar novo conteúdo
        novo_conteudo = []
        modo = 'normal'
        
        for linha in linhas:
            # Substituir a função formatar_valor_monetario
            if 'def formatar_valor_monetario' in linha:
                novo_conteudo.append('def formatar_valor_monetario(valor: float) -> str:\n')
                novo_conteudo.append('    """Formata um valor monetário em reais"""\n')
                novo_conteudo.append('    if not isinstance(valor, (int, float)):\n')
                novo_conteudo.append('        return "R$ 0,00"\n')
                novo_conteudo.append('    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")\n')
                
                # Pular as próximas linhas da função original
                modo = 'pular_formatar'
                continue
            
            # Voltar ao modo normal após pular a função original
            if modo == 'pular_formatar' and linha.strip() == '':
                modo = 'normal'
            
            # Pular linhas da função original
            if modo == 'pular_formatar':
                continue
            
            # Verificar se estamos na seção de dados socioeconômicos para municípios
            if '# Dados Socioeconômicos' in linha and modo == 'normal':
                novo_conteudo.append(linha)  # Adicionar o comentário
                
                # Verificar se a próxima linha inicia a seção de dados socioeconômicos
                if 'if "dados_socioeconomicos" in relatorio and relatorio["dados_socioeconomicos"]:' in linha:
                    modo = 'substituir_socioeconomicos'
                    
                    # Adicionar a nova implementação
                    novo_conteudo.append('        if "dados_socioeconomicos" in relatorio and relatorio["dados_socioeconomicos"]:\n')
                    novo_conteudo.append('            dados_socio = relatorio["dados_socioeconomicos"]\n')
                    novo_conteudo.append('            print("\\nDADOS SOCIOECONÔMICOS:")\n')
                    novo_conteudo.append('            \n')
                    novo_conteudo.append('            # PIB\n')
                    novo_conteudo.append('            if "pib" in dados_socio and isinstance(dados_socio["pib"], dict):\n')
                    novo_conteudo.append('                pib_data = dados_socio["pib"]\n')
                    novo_conteudo.append('                print(f"PIB: {formatar_valor_monetario(pib_data.get(\'total\', 0))}")\n')
                    novo_conteudo.append('                print(f"PIB per capita: {formatar_valor_monetario(pib_data.get(\'per_capita\', 0))}")\n')
                    novo_conteudo.append('                if "ano_referencia" in pib_data:\n')
                    novo_conteudo.append('                    print(f"Ano de referência (PIB): {pib_data.get(\'ano_referencia\')}")\n')
                    novo_conteudo.append('            else:\n')
                    novo_conteudo.append('                # Compatibilidade com formato antigo\n')
                    novo_conteudo.append('                print(f"PIB: {formatar_valor_monetario(dados_socio.get(\'pib\', 0))}")\n')
                    novo_conteudo.append('                print(f"PIB per capita: {formatar_valor_monetario(dados_socio.get(\'pib_per_capita\', 0))}")\n')
                    novo_conteudo.append('            \n')
                    novo_conteudo.append('            # IDH\n')
                    novo_conteudo.append('            if "idh" in dados_socio and isinstance(dados_socio["idh"], dict):\n')
                    novo_conteudo.append('                idh_data = dados_socio["idh"]\n')
                    novo_conteudo.append('                print(f"IDH: {idh_data.get(\'valor\', \'N/A\')}")\n')
                    novo_conteudo.append('                if "classificacao" in idh_data:\n')
                    novo_conteudo.append('                    print(f"Classificação IDH: {idh_data.get(\'classificacao\')}")\n')
                    novo_conteudo.append('                if "ano_referencia" in idh_data:\n')
                    novo_conteudo.append('                    print(f"Ano de referência (IDH): {idh_data.get(\'ano_referencia\')}")\n')
                    novo_conteudo.append('            else:\n')
                    novo_conteudo.append('                # Compatibilidade com formato antigo\n')
                    novo_conteudo.append('                print(f"IDH: {dados_socio.get(\'idh\', \'N/A\')}")\n')
                    
                    # Continuar com o restante da implementação
                    continue
            
            # Adicionar a linha ao novo conteúdo
            if modo == 'normal':
                novo_conteudo.append(linha)
        
        # Escrever o novo conteúdo no arquivo temporário
        with open(arquivo_temporario, 'w', encoding='utf-8') as f:
            f.writelines(novo_conteudo)
        
        print(f"Arquivo atualizado com sucesso: {arquivo_temporario}")
        print("Para aplicar as alterações, execute:")
        print(f"copy {arquivo_temporario} {arquivo_original}")
    
    except Exception as e:
        print(f"Erro ao atualizar o arquivo: {e}")

if __name__ == "__main__":
    main()
