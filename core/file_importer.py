import os
import shutil
from utils.date_utils import gerar_datas_aproximadas


def importar_arquivos(origem, destino, datas_sensores, progress_callback):
    arquivos_importados = []
    nao_importados = []

    arquivos_origem = os.listdir(origem)
    total_datas_sensores = len(datas_sensores)

    for i, (data_hora, sensor, formatos) in enumerate(datas_sensores, start=1):
        encontrado = importar_arquivo_para_sensor(origem, destino, data_hora, sensor, formatos, arquivos_origem, arquivos_importados, nao_importados)
        if not encontrado:
            nao_importados.append((f"{data_hora} - Arquivo não encontrado", sensor, data_hora))

        progress_callback.emit(int(i / total_datas_sensores * 100))

    return arquivos_importados, nao_importados


def importar_arquivo_para_sensor(origem, destino, data_hora, sensor, formatos, arquivos_origem, arquivos_importados, nao_importados):
    encontrado = False
    datas_aproximadas = gerar_datas_aproximadas(data_hora)

    for arquivo in arquivos_origem:
        if arquivo_corresponde(arquivo, datas_aproximadas, formatos):
            origem_arquivo = os.path.join(origem, arquivo)
            destino_arquivo = os.path.join(destino, arquivo)

            if os.path.isfile(origem_arquivo):
                sucesso, mensagem = copiar_arquivo(origem_arquivo, destino_arquivo)
                if sucesso:
                    arquivos_importados.append((arquivo, sensor, data_hora))
                else:
                    nao_importados.append((arquivo, sensor, data_hora, mensagem))
                encontrado = True
                break

    return encontrado


def arquivo_corresponde(arquivo, datas_aproximadas, formatos):
    if isinstance(formatos, str):
        formatos = [formatos]
    return any(data in arquivo for data in datas_aproximadas) and any(arquivo.endswith(formato) for formato in formatos)


def copiar_arquivo(origem_arquivo, destino_arquivo):
    try:
        print(f"Copiando {origem_arquivo} para {destino_arquivo}")
        shutil.copy2(origem_arquivo, destino_arquivo)
        return True, ""
    except Exception as e:
        print(f"Erro ao copiar {origem_arquivo}: {e}")
        return False, str(e)
