"""
Файл main, представляющий собой точку входа в приложение
весь функционал представлен в файле image_editor.py
"""
import sys
from PyQt5.QtWidgets import QApplication
from image_editor import ImageEditor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
