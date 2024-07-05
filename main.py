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
