"""
Script para corrigir problemas de formatação de strings na função exibir_relatorio_texto
"""
import re

def corrigir_strings():
    # Caminho para o arquivo
    arquivo = "tools/relatorio_localidade.py"
    
    # Ler o conteúdo do arquivo
    with open(arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Corrigir as strings com quebras de linha
    conteudo_corrigido = conteudo.replace('print("\n', 'print("\\n')
    
    # Corrigir as strings com formatação f-string
    conteudo_corrigido = conteudo_corrigido.replace('print(f"\n', 'print(f"\\n')
    
    # Salvar o arquivo corrigido
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo_corrigido)
    
    print("Strings corrigidas com sucesso!")

if __name__ == "__main__":
    corrigir_strings()
