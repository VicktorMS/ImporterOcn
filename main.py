from setproctitle import setproctitle
from PyQt6.QtWidgets import QApplication
import sys
from ui.ui_main_window import MainWindow
from utils.set_config import ler_configuracao


def main():
    setproctitle("OCN Importer")
    configuracoes = ler_configuracao('config/caminhos_default.txt')
    app = QApplication(sys.argv)
    window = MainWindow(configuracoes)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

