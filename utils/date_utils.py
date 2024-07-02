from datetime import datetime, timedelta


def gerar_datas_aproximadas(data_hora_str, intervalo_minutos=10):
    formato = "%Y-%m-%d-%H-%M"
    data_hora = datetime.strptime(data_hora_str, formato)
    datas_aproximadas = [data_hora - timedelta(minutes=minutos) for minutos in range(intervalo_minutos + 1)]
    return [data_hora.strftime(formato) for data_hora in datas_aproximadas]
