from PyQt6.QtGui import QIcon

from threads.import_thread import ImportThread
from utils.messages import show_success, exibir_erro
from utils.validators import validar_diretorio, extrair_datas_e_sensores

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit,
    QProgressBar, QStatusBar, QPushButton, QWidget, QGridLayout,
    QVBoxLayout, QHBoxLayout, QStyleFactory
)
import sys


class MainWindow(QMainWindow):
    def __init__(self, configuracoes):
        super().__init__()

        self.setWindowTitle("OCN Importer")
        self.setFixedSize(800, 600)

        # Aplicar estilo Fusion
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.setWindowIcon(QIcon('assets/import_icon.png'))

        # Configuração do widget central e layout principal
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Layout para os campos de entrada
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        main_layout.addLayout(grid_layout)

        # Diretório de origem
        self.origem_label = QLabel("Diretório de Origem:")
        grid_layout.addWidget(self.origem_label, 0, 0)
        self.origem_input = QLineEdit(self)
        self.origem_input.setText(configuracoes.get("origem", ""))  # Valor padrão do arquivo de configuração
        self.origem_input.setPlaceholderText("Digite o diretório de origem")
        self.origem_input.textChanged.connect(self.validar_campos)
        grid_layout.addWidget(self.origem_input, 0, 1)

        # Diretório de destino
        self.destino_label = QLabel("Diretório de Destino:")
        grid_layout.addWidget(self.destino_label, 1, 0)
        self.destino_input = QLineEdit(self)
        self.destino_input.setText(configuracoes.get("destino", ""))  # Valor padrão do arquivo de configuração
        self.destino_input.setPlaceholderText("Digite o diretório de destino")
        self.destino_input.textChanged.connect(self.validar_campos)
        grid_layout.addWidget(self.destino_input, 1, 1)

        # Lista de arquivos
        self.datas_horas_label = QLabel("Perdas do PyPerdas:")
        grid_layout.addWidget(self.datas_horas_label, 2, 0)
        self.datas_horas_input = QTextEdit(self)
        self.datas_horas_input.setPlaceholderText(
            '[\n\t"[BRM_1_ANNANERY][YOUNG]: 2023-12-15 17:00->2023-12-15 17:00",'
            '\n\t"[BRM_1_ANNANERY][YOUNG]: 2023-12-15 17:00->2023-12-15 17:00"\n]'
        )
        self.datas_horas_input.textChanged.connect(self.validar_campos)
        grid_layout.addWidget(self.datas_horas_input, 2, 1, 1, 2)

        # Barra de progresso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Botão para iniciar a importação de arquivos
        self.button = QPushButton("Importar Arquivos", self)
        self.button.setEnabled(False)
        self.button.clicked.connect(self.iniciar_importacao)
        self.button.setStyleSheet("font-size: 16px; padding: 10px;")

        # Centralizar o botão no layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Texto para exibir o relatório
        self.relatorio = QTextEdit(self)
        self.relatorio.setReadOnly(True)
        self.relatorio.setVisible(False)
        main_layout.addWidget(self.relatorio)

        # Barra de status
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

    def validar_campos(self):
        origem = self.origem_input.text().strip()
        destino = self.destino_input.text().strip()
        mensagem = self.datas_horas_input.toPlainText().strip()

        if origem and destino and mensagem:
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    def validar_campos(self):
        origem = self.origem_input.text()
        destino = self.destino_input.text()
        datas_horas = self.datas_horas_input.toPlainText()

        if origem and destino and datas_horas:
            self.button.setEnabled(True)
        else:
            self.button.setEnabled(False)

    def iniciar_importacao(self):
        origem = self.origem_input.text()
        destino = self.destino_input.text()
        datas_horas = self.datas_horas_input.toPlainText()

        if not validar_diretorio(origem):
            exibir_erro("O Diretório de origem é inválido ou não existe.")
            return

        if not validar_diretorio(destino):
            exibir_erro("O Diretório de destino é inválido ou não existe.")
            return

        lista_datas_horas = extrair_datas_e_sensores(datas_horas)
        if not lista_datas_horas:
            exibir_erro('A lista de datas é inválida. '
                        'Use o formato: '
                        '["[BRM_1_ANNANERY][YOUNG]: 2023-12-15 17:00->2023-12-15 17:00"]')
            return

        self.progress_bar.setVisible(True)
        self.status_bar.showMessage("Importando Arquivos...")

        self.thread = ImportThread(origem, destino, lista_datas_horas)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.result.connect(self.importacao_concluida)
        self.thread.start()

    def importacao_concluida(self, total_importados, total_nao_importados, importados, nao_importados):
        self.progress_bar.setVisible(False)
        self.relatorio.setVisible(True)
        self.status_bar.clearMessage()

        relatorio = f"Total de arquivos esperados: {total_importados + total_nao_importados}\n"
        relatorio += f"Arquivos importados: {total_importados}\n"
        relatorio += f"Arquivos não importados: {total_nao_importados}\n\n"

        if importados:
            relatorio += "Arquivos Importados:\n"
            for arquivo, sensor, data_hora in importados:
                relatorio += f"Sensor: {sensor}, \nData: {data_hora}, \nArquivo: {arquivo}\n\n"
            relatorio += "\n"

        if nao_importados:
            relatorio += "Arquivos Não Importados:\n"
            for arquivo, sensor, data_hora in nao_importados:
                relatorio += f"Sensor: {sensor}, \nData: {data_hora}, \nArquivo: {arquivo}\n\n"

        self.relatorio.setText(relatorio)

        show_success("Importação Concluída!")
