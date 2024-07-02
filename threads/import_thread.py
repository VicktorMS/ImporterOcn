from PyQt6.QtCore import QThread, pyqtSignal

from core.file_importer import importar_arquivos


class ImportThread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(int, int, list, list)

    def __init__(self, origem, destino, datas_sensores):
        super().__init__()
        self.origem = origem
        self.destino = destino
        self.datas_sensores = datas_sensores

    def run(self):
        importados, nao_importados = importar_arquivos(self.origem, self.destino, self.datas_sensores, self.progress)
        total_importados = len(importados)
        total_nao_importados = len(nao_importados)
        self.result.emit(total_importados, total_nao_importados, importados, nao_importados)