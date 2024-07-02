import unittest

from utils.date_utils import gerar_datas_aproximadas
from utils.validators import extrair_datas_e_sensores, calcular_intervalo_entre_datas


class TestValidators(unittest.TestCase):

    def test_extrair_datas_e_sensores(self):
        mensagem = """
        [ 
            "[BRM_1_ANNANERY][YOUNG]: 2023-12-15 18:00->2023-12-15 19:00",
            "[BRM_1_ANNANERY][YOUNG]: 2023-12-15 18:00->2023-12-15 20:00",
            "[BRM_1_ANNANERY][YOUNG]: 2023-12-15 18:00->2023-12-15 10:00",
            "[BRM_1_ANNANERY][MIROS]: 2023-12-15 18:00->2023-12-15 19:00",
        ]
        """

        resultado_esperado = [
            ('2023-12-15-20-00', 'YOUNG', 'yng_gz'),
            ('2023-12-15-18-00', 'MIROS', 'mir2_gz'),
            ('2023-12-15-19-00', 'YOUNG', 'yng_gz'),
            ('2023-12-15-19-00', 'MIROS', 'mir2_gz'),
            ('2023-12-15-19-00', 'MIROS', 'mir_gz'),
            ('2023-12-15-18-00', 'YOUNG', 'yng_gz'),
            ('2023-12-15-18-00', 'MIROS', 'mir_gz')
        ]

        resultado = extrair_datas_e_sensores(mensagem)
        print(resultado)
        # self.assertEqual(resultado_esperado, resultado)

    def test_intervalo_entre_datas(self):
        data_hora_inicial = "2023-12-15 17:00"
        data_hora_final = "2023-12-15 22:00"

        esperado = [
            '2023-12-15 17:00',
            '2023-12-15 18:00',
            '2023-12-15 19:00',
            '2023-12-15 20:00',
            '2023-12-15 21:00',
            '2023-12-15 22:00'
        ]

        resultado = calcular_intervalo_entre_datas(data_hora_inicial, data_hora_final)

        self.assertEqual(resultado, esperado)

    def test_gerar_datas_aproximadas(self):
        data_hora_str = "2023-12-15-17-00"
        intervalo_minutos = 10
        resultado = gerar_datas_aproximadas(data_hora_str, intervalo_minutos)

        esperado = [
            "2023-12-15-17-00",
            "2023-12-15-16-59",
            "2023-12-15-16-58",
            "2023-12-15-16-57",
            "2023-12-15-16-56",
            "2023-12-15-16-55",
            "2023-12-15-16-54",
            "2023-12-15-16-53",
            "2023-12-15-16-52",
            "2023-12-15-16-51",
            "2023-12-15-16-50"
        ]

        self.assertEqual(resultado, esperado)


if __name__ == '__main__':
    unittest.main()
