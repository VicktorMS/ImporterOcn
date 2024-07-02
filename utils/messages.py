from PyQt6.QtWidgets import QMessageBox


def show_success(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText(message)
    msg.setWindowTitle("Sucesso")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def exibir_erro(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(message)
    msg.setWindowTitle("Erro")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()
