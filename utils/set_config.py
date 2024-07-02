
def ler_configuracao(caminho_arquivo):
    configuracoes = {}
    with open(caminho_arquivo, 'r') as file:
        for linha in file:
            if '=' in linha:
                chave, valor = linha.strip().split('=', 1)
                configuracoes[chave] = valor
    return configuracoes