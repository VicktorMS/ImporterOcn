import json
import os
import re
from datetime import datetime, timedelta

# Carregar o dicionário do arquivo .txt
with open('config/formato_sensor.txt', 'r') as file:
    FORMATO_SENSOR = json.load(file)


def calcular_intervalo_entre_datas(data_hora_inicial, data_hora_final):
    formato = "%Y-%m-%d %H:%M"
    dt_inicial = datetime.strptime(data_hora_inicial, formato)
    dt_final = datetime.strptime(data_hora_final, formato)

    intervalos = []
    while dt_inicial <= dt_final:
        intervalos.append(dt_inicial.strftime(formato))
        dt_inicial += timedelta(hours=1)

    return intervalos


def extrair_datas_e_sensores(mensagem):
    padrao = re.compile(r'\[([^\]]+)\]\[([^\]]+)\]: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})->(\d{4}-\d{2}-\d{2} \d{2}:\d{2})')
    matches = padrao.findall(mensagem)

    resultados_unicos = set()
    for _, sensor, data_inicial, data_final in matches:
        intervalos = calcular_intervalo_entre_datas(data_inicial, data_final)
        formatos = FORMATO_SENSOR.get(sensor, [])
        for data in intervalos:
            data_formatada = data.replace(' ', '-').replace(':', '-')
            for formato in formatos:
                resultados_unicos.add((data_formatada, sensor, formato))
    return list(resultados_unicos)

def validar_diretorio(diretorio):
    return os.path.isdir(diretorio)
