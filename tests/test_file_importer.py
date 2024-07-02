import unittest
from core.file_importer import arquivo_corresponde


class TestArquivoCorresponde(unittest.TestCase):
    def test_arquivo_corresponde(self):
        arquivo = "23701_2023-12-15-17-00.yng_gz"
        datas_aproximadas = ["2023-12-15-17-00", "2023-12-15-16-50"]
        formatos = ["yng_gz"]

        self.assertTrue(arquivo_corresponde(arquivo, datas_aproximadas, formatos))

    def test_formato_nao_corresponde_em_string(self):
        arquivo = "23701_2023-12-15-17-00.yng_gz"
        datas_aproximadas = ["2023-12-15-17-00", "2023-12-15-16-50"]
        formatos = "mir_gz"

        self.assertFalse(arquivo_corresponde(arquivo, datas_aproximadas, formatos))

    def test_arquivo_nao_corresponde_formato(self):
        arquivo = "23701_2023-12-15-17-00.yng_gz"
        datas_aproximadas = ["2023-12-15-17-00", "2023-12-15-16-50"]
        formatos = ["mir_gz", "mir2_gz"]

        self.assertFalse(arquivo_corresponde(arquivo, datas_aproximadas, formatos))

    def test_arquivo_corresponde_formato_multiplo(self):
        arquivo = "23701_2023-12-15-17-00.mir2_gz"
        datas_aproximadas = ["2023-12-15-17-00", "2023-12-15-16-50"]
        formatos = ["mir_gz", "mir2_gz"]

        self.assertTrue(arquivo_corresponde(arquivo, datas_aproximadas, formatos))


if __name__ == '__main__':
    unittest.main()
