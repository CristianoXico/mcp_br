def formatar_valor_monetario(valor: float) -> str:
    """Formata um valor monetário em reais"""
    if not isinstance(valor, (int, float)):
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def exibir_relatorio_texto_corrigido(relatorio: dict) -> None:
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
